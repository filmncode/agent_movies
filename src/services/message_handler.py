from typing import Tuple, Optional, List, Dict, Any
from services.tmdb_service import TMDbService
from services.db_service import DatabaseService
from services.whatsapp_service import WhatsAppService
from services.openai_service import OpenAIService
import logging
import os

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.tmdb_service = TMDbService()
        self.db_service = DatabaseService()
        self.whatsapp_service = WhatsAppService()
        
        # Initialize OpenAI service if API key is available
        self.use_openai = os.getenv('USE_OPENAI', 'false').lower() == 'true'
        if self.use_openai:
            try:
                self.openai_service = OpenAIService()
                logger.info("OpenAI service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI service: {str(e)}")
                self.use_openai = False

    def handle_message(self, message: str, user_id: str) -> Tuple[str, bool]:
        """
        Handle incoming message and return (response_message, success)
        """
        logger.debug(f"Processing message: '{message}' from {user_id}")
        
        # Clean up the WhatsApp number format if needed
        if user_id.startswith('whatsapp:'):
            user_id = user_id.replace('whatsapp:', '')
        
        # Process the message using OpenAI if enabled
        if self.use_openai:
            return self._handle_with_openai(message, user_id)
        else:
            # Fall back to the basic NLP processing
            intent, movie_title = self.whatsapp_service.process_message(message)
            logger.debug(f"Detected intent: {intent}, movie: {movie_title}")
            
            # Handle different intents
            if intent == 'get_info' and movie_title:
                return self._handle_movie_info(movie_title)
            elif intent == 'mark_watched' and movie_title:
                return self._handle_mark_watched(movie_title, user_id)
            elif intent == 'help':
                return self._handle_help_request(), True
            elif intent == 'list_watched':
                return self._handle_list_watched(user_id)
            else:
                return "Sorry, I couldn't understand your request. Try saying 'Tell me about [movie name]', 'I watched [movie name]', or 'help' for more options.", False

    def _handle_with_openai(self, message: str, user_id: str) -> Tuple[str, bool]:
        """Handle message processing with OpenAI"""
        try:
            # Process the message to get intent and entities
            intent, movie_title, context = self.openai_service.process_message(message, user_id)
            logger.debug(f"OpenAI detected intent: {intent}, movie: {movie_title}, context: {context}")
            
            # Prepare response data based on intent
            response_data = {}
            
            if intent == 'get_info' and movie_title:
                # Get movie information
                movie, msg = self.tmdb_service.search_movie(movie_title)
                if movie:
                    response_data['movie'] = movie
                    # Get similar movies
                    similar_movies, _ = self.tmdb_service.get_similar_movies(movie['id'], min_score=7.0)
                    if similar_movies:
                        response_data['similar_movies'] = similar_movies[:3]
                else:
                    response_data['error'] = f"Couldn't find information about '{movie_title}'"
                    
            elif intent == 'mark_watched' and movie_title:
                # Mark movie as watched
                movie, msg = self.tmdb_service.search_movie(movie_title)
                if movie:
                    response_data['movie'] = movie
                    # Check if already watched
                    if self.db_service.is_movie_watched(user_id, movie['id']):
                        response_data['already_watched'] = True
                    else:
                        # Mark as watched
                        success = self.db_service.add_watched_movie(user_id, movie['id'])
                        response_data['marked_watched'] = success
                        
                        # Get recommendations
                        if success:
                            similar_movies, _ = self.tmdb_service.get_similar_movies(movie['id'], min_score=7.5)
                            unwatched_similar = [m for m in similar_movies 
                                              if not self.db_service.is_movie_watched(user_id, m['id'])]
                            if unwatched_similar:
                                response_data['recommendations'] = unwatched_similar[:3]
                else:
                    response_data['error'] = f"Couldn't find the movie '{movie_title}'"
                    
            elif intent == 'list_watched':
                # Get watched movies
                watched_ids = self.db_service.get_watched_movies(user_id)
                response_data['watched_count'] = len(watched_ids)
                
                if watched_ids:
                    # Get details for each movie (up to 10)
                    watched_movies = []
                    for movie_id in watched_ids[:10]:
                        movie, _ = self.tmdb_service.get_movie_details(movie_id)
                        if movie:
                            watched_movies.append(movie)
                    response_data['watched_movies'] = watched_movies
                    
            elif intent == 'help':
                response_data['help_requested'] = True
            
            # Generate natural language response
            prompt = self._create_response_prompt(intent, response_data)
            response = self.openai_service.generate_response(prompt, user_id, context)
            
            return response, True
            
        except Exception as e:
            logger.error(f"Error processing with OpenAI: {str(e)}", exc_info=True)
            # Fall back to basic response
            return "I'm having trouble understanding your request right now. Could you try again with a simpler question about movies?", False
    
    def _create_response_prompt(self, intent: str, data: Dict[str, Any]) -> str:
        """Create a prompt for the OpenAI response generation based on the intent and data"""
        if intent == 'get_info':
            if 'error' in data:
                return f"The user asked about a movie, but I couldn't find information about it. Error: {data['error']}"
                
            movie = data.get('movie', {})
            similar = data.get('similar_movies', [])
            
            prompt = f"The user asked about the movie '{movie.get('title')}'. "
            prompt += f"Here's the information: Title: {movie.get('title')}, "
            prompt += f"Release date: {movie.get('release_date', 'unknown')}, "
            prompt += f"Score: {movie.get('vote_average', 'unknown')}/10, "
            prompt += f"Overview: {movie.get('overview', 'No overview available')}. "
            
            if similar:
                prompt += "Here are some similar movies they might like: "
                for i, s in enumerate(similar, 1):
                    prompt += f"{i}. {s.get('title')} ({s.get('vote_average')}/10) "
            
            return prompt
            
        elif intent == 'mark_watched':
            if 'error' in data:
                return f"The user tried to mark a movie as watched, but I couldn't find the movie. Error: {data['error']}"
                
            movie = data.get('movie', {})
            
            if data.get('already_watched'):
                return f"The user said they watched '{movie.get('title')}', but they've already marked it as watched before."
                
            if not data.get('marked_watched', False):
                return f"The user said they watched '{movie.get('title')}', but there was an error marking it as watched."
                
            prompt = f"The user said they watched '{movie.get('title')}'. I've marked it as watched for them. "
            
            if 'recommendations' in data:
                prompt += "Here are some recommendations based on this movie: "
                for i, r in enumerate(data['recommendations'], 1):
                    prompt += f"{i}. {r.get('title')} ({r.get('vote_average')}/10) "
            
            return prompt
            
        elif intent == 'list_watched':
            count = data.get('watched_count', 0)
            
            if count == 0:
                return "The user asked for their watched movies, but they haven't marked any movies as watched yet."
                
            prompt = f"The user asked for their watched movies. They've watched {count} movies. "
            
            if 'watched_movies' in data:
                prompt += "Here are their most recently watched movies: "
                for i, m in enumerate(data['watched_movies'], 1):
                    prompt += f"{i}. {m.get('title')} ({m.get('vote_average')}/10) "
                    
                if count > 10:
                    prompt += f"And {count - 10} more. "
            
            return prompt
            
        elif intent == 'help':
            return "The user asked for help. Explain how to use the movie recommendation service, including how to ask about movies, mark movies as watched, and view their watched list."
            
        else:
            return "The user sent a message that I couldn't understand. Please provide a helpful response explaining how they can interact with the movie recommendation service."

    def _handle_movie_info(self, movie_title: str) -> Tuple[str, bool]:
        """Handle movie information request"""
        movie, message = self.tmdb_service.search_movie(movie_title)
        if not movie:
            return f"Sorry, I couldn't find information about '{movie_title}'", False
            
        # Get similar movies with good scores
        similar_movies, _ = self.tmdb_service.get_similar_movies(movie['id'], min_score=7.0)
        
        response = self.tmdb_service.format_movie_info(movie)
        if similar_movies:
            response += "\n\nYou might also like:\n"
            for i, similar in enumerate(similar_movies[:3], 1):
                response += f"{i}. {similar['title']} ({similar['vote_average']}/10)\n"
                
        return response, True

    def _handle_mark_watched(self, movie_title: str, user_id: str) -> Tuple[str, bool]:
        """Handle marking a movie as watched"""
        movie, message = self.tmdb_service.search_movie(movie_title)
        if not movie:
            return f"Sorry, I couldn't find the movie '{movie_title}'", False
            
        # Check if already watched
        if self.db_service.is_movie_watched(user_id, movie['id']):
            return f"You've already marked {movie['title']} as watched!", True
            
        # Mark as watched
        success = self.db_service.add_watched_movie(user_id, movie['id'])
        if not success:
            return "Sorry, there was an error marking the movie as watched", False
            
        # Get recommendations based on this movie
        similar_movies, _ = self.tmdb_service.get_similar_movies(movie['id'], min_score=7.5)
        unwatched_similar = [m for m in similar_movies 
                           if not self.db_service.is_movie_watched(user_id, m['id'])]
        
        response = f"Great! I've marked {movie['title']} as watched."
        if unwatched_similar:
            response += "\n\nBased on this, you might enjoy:\n"
            for i, rec in enumerate(unwatched_similar[:3], 1):
                response += f"{i}. {rec['title']} ({rec['vote_average']}/10)\n"
                
        return response, True
        
    def _handle_help_request(self) -> str:
        """Handle help request"""
        return (
            "Here's how you can use Movie Score:\n\n"
            "1. Get movie information: 'Tell me about [movie title]' or 'How good is [movie title]'\n"
            "2. Mark a movie as watched: 'I watched [movie title]' or 'Mark [movie title] as watched'\n"
            "3. See your watched movies: 'Show my watched movies' or 'What have I watched'\n"
            "4. Get help: 'help' or 'how does this work'\n\n"
            "I'll provide movie scores, recommendations, and keep track of what you've watched!"
        )
        
    def _handle_list_watched(self, user_id: str) -> Tuple[str, bool]:
        """Handle request to list watched movies"""
        # Get list of watched movie IDs
        watched_ids = self.db_service.get_watched_movies(user_id)
        
        if not watched_ids:
            return "You haven't marked any movies as watched yet.", True
            
        # Get details for each movie (up to 10 to avoid too long messages)
        watched_movies = []
        for movie_id in watched_ids[:10]:
            movie, _ = self.tmdb_service.get_movie_details(movie_id)
            if movie:
                watched_movies.append(movie)
        
        # Format response
        if not watched_movies:
            return "You've marked some movies as watched, but I couldn't retrieve their details.", False
            
        response = f"You've watched {len(watched_ids)} movies. Here are the most recent ones:\n\n"
        for i, movie in enumerate(watched_movies, 1):
            response += f"{i}. {movie.get('title', 'Unknown')} ({movie.get('vote_average', 0)}/10)\n"
            
        if len(watched_ids) > 10:
            response += f"\nAnd {len(watched_ids) - 10} more..."
            
        return response, True 