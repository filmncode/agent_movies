from typing import Tuple, Optional
from services.tmdb_service import TMDbService
from services.db_service import DatabaseService
from services.whatsapp_service import WhatsAppService
import logging

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        self.tmdb_service = TMDbService()
        self.db_service = DatabaseService()
        self.whatsapp_service = WhatsAppService()

    def handle_message(self, message: str, user_id: str) -> Tuple[str, bool]:
        """
        Handle incoming message and return (response_message, success)
        """
        logger.debug(f"Processing message: '{message}' from {user_id}")
        
        # Clean up the WhatsApp number format if needed
        if user_id.startswith('whatsapp:'):
            user_id = user_id.replace('whatsapp:', '')
            
        intent, movie_title = self.whatsapp_service.process_message(message)
        logger.debug(f"Detected intent: {intent}, movie: {movie_title}")
        
        if not movie_title:
            return "Sorry, I couldn't understand which movie you're talking about. Try saying 'Tell me about [movie name]' or 'I watched [movie name]'", False
            
        if intent == 'get_info':
            return self._handle_movie_info(movie_title)
        elif intent == 'mark_watched':
            return self._handle_mark_watched(movie_title, user_id)
        else:
            return "Sorry, I don't understand that command. Try asking about a movie or marking one as watched!", False

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