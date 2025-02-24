from crewai import Agent, Crew, Process, Task
from langchain.tools import Tool
from typing import List
from services.tmdb_service import TMDbService
from services.whatsapp_service import WhatsAppService
from services.db_service import DatabaseService
import os
from dotenv import load_dotenv
from services.message_handler import MessageHandler

# Load environment variables
load_dotenv()

# Verify OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

class MoviescoreCrew():
    """movie_score crew"""

    def __init__(self):
        self.tmdb_service = TMDbService()
        self.whatsapp_service = WhatsAppService()
        self.db_service = DatabaseService()
        # Initialize agents
        self.whatsapp_agent = self._create_whatsapp_agent()
        self.movie_query_agent = self._create_movie_query_agent()
        self.recommendation_agent = self._create_recommendation_agent()
        self.tracker_agent = self._create_tracker_agent()

    def _create_whatsapp_agent(self) -> Agent:
        """WhatsApp communication agent"""
        tools = [
            Tool(
                name="send_whatsapp_message",
                description="Send a message to a user via WhatsApp using Twilio API",
                func=self._send_whatsapp_message
            ),
            Tool(
                name="process_incoming_message",
                description="Process incoming WhatsApp messages and extract intent and movie titles",
                func=self._process_incoming_message
            )
        ]
        
        return Agent(
            name="WhatsApp Agent",
            role="Communication Manager",
            goal="Handle WhatsApp messaging and user interactions",
            backstory="I am a specialized agent that manages WhatsApp communications, "
                     "ensuring smooth interaction with users through the WhatsApp platform.",
            tools=tools,
            verbose=True
        )

    def _create_movie_query_agent(self) -> Agent:
        """Movie information query agent"""
        tools = [
            Tool(
                name="search_movie",
                description="Search for a movie in TMDb database",
                func=self._search_movie
            ),
            Tool(
                name="get_movie_score",
                description="Get the score of a specific movie from TMDb",
                func=self._get_movie_score
            ),
            Tool(
                name="get_movie_details",
                description="Get detailed information about a movie",
                func=self._get_movie_details
            )
        ]
        
        return Agent(
            name="Movie Query Agent",
            role="Movie Information Specialist",
            goal="Search and retrieve accurate movie information",
            backstory="I am an expert at finding and validating movie information "
                     "from various reliable sources to provide accurate data.",
            tools=tools,
            verbose=True
        )

    def _create_recommendation_agent(self) -> Agent:
        """Movie recommendation agent"""
        tools = [
            Tool(
                name="get_similar_movies",
                description="Find similar movies with higher scores than the reference movie",
                func=self._get_similar_movies
            ),
            Tool(
                name="filter_unwatched_movies",
                description="Filter out movies that the user has already watched",
                func=self._filter_unwatched_movies
            ),
            Tool(
                name="sort_by_popularity",
                description="Sort movies by their popularity",
                func=self._sort_by_popularity
            )
        ]
        
        return Agent(
            name="Recommendation Agent",
            role="Movie Recommendation Specialist",
            goal="Generate personalized movie recommendations",
            backstory="I analyze user preferences and movie patterns to provide "
                     "tailored movie recommendations that match user interests.",
            tools=tools,
            verbose=True
        )

    def _create_tracker_agent(self) -> Agent:
        """Movie tracking agent"""
        tools = [
            Tool(
                name="add_watched_movie",
                description="Add a movie to user's watched list",
                func=self._add_watched_movie
            ),
            Tool(
                name="get_watched_movies",
                description="Get the list of movies watched by a user",
                func=self._get_watched_movies
            ),
            Tool(
                name="check_if_watched",
                description="Check if a user has watched a specific movie",
                func=self._check_if_watched
            )
        ]
        
        return Agent(
            name="Tracker Agent",
            role="Movie Progress Tracker",
            goal="Track and manage user movie watching progress",
            backstory="I maintain detailed records of users' movie watching history "
                     "and help manage their watchlist and progress.",
            tools=tools,
            verbose=True
        )

    def create_crew(self, tasks: List[Task]) -> Crew:
        """Creates the crew with specified tasks"""
        return Crew(
            agents=[
                self.movie_query_agent,
                self.recommendation_agent,
                self.tracker_agent,
                self.whatsapp_agent
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

    # Tool implementation methods
    def _send_whatsapp_message(self, message: str, phone_number: str) -> bool:
        """Send WhatsApp message"""
        return self.whatsapp_service.send_message(phone_number, message)

    def _process_incoming_message(self, description: str) -> dict:
        """Process incoming WhatsApp messages"""
        # Extract movie title and phone number from description
        parts = description.split(" and send it to ")
        if len(parts) != 2:
            return {'error': 'Invalid message format'}
            
        message = parts[0]
        phone_number = parts[1].strip()
        
        # Use message handler to process
        handler = MessageHandler()
        response, success = handler.handle_message(message, phone_number)
        
        if success:
            self.whatsapp_service.send_message(phone_number, response)
            
        return {
            'success': success,
            'response': response,
            'phone_number': phone_number
        }

    def _search_movie(self, title: str) -> str:
        """Search for a movie in TMDb"""
        movie, message = self.tmdb_service.search_movie(title)
        if not movie:
            return message
        return self.tmdb_service.format_movie_info(movie)

    def _get_movie_score(self, movie_id: int) -> str:
        """Get movie score from TMDb"""
        movie, message = self.tmdb_service.get_movie_details(movie_id)
        if not movie:
            return message
        return f"Score: {movie.get('vote_average', 0.0)}/10"

    def _get_movie_details(self, movie_id: int) -> str:
        """Get detailed movie information"""
        movie, message = self.tmdb_service.get_movie_details(movie_id)
        if not movie:
            return message
        return self.tmdb_service.format_movie_info(movie)

    def _get_similar_movies(self, movie_id: int, min_score: float) -> str:
        """Get similar movies with higher scores"""
        movies, message = self.tmdb_service.get_similar_movies(movie_id, min_score)
        if not movies:
            return message
            
        result = "Similar movies:\n"
        for i, movie in enumerate(movies[:5], 1):  # Show top 5 similar movies
            result += f"\n{i}. {self.tmdb_service.format_movie_info(movie)}"
        return result

    def _filter_unwatched_movies(self, movies: List[dict], user_id: str) -> List[dict]:
        """Filter out watched movies"""
        watched_ids = self.db_service.get_watched_movies(user_id)
        return [movie for movie in movies if movie.get('id') not in watched_ids]

    def _sort_by_popularity(self, movies: List[dict]) -> List[dict]:
        """Sort movies by popularity"""
        return sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)

    def _add_watched_movie(self, user_id: str, movie_id: int) -> bool:
        """Add movie to watched list"""
        return self.db_service.add_watched_movie(user_id, movie_id)

    def _get_watched_movies(self, user_id: str) -> List[int]:
        """Get user's watched movies"""
        return self.db_service.get_watched_movies(user_id)

    def _check_if_watched(self, user_id: str, movie_id: int) -> bool:
        """Check if user watched a movie"""
        return self.db_service.is_movie_watched(user_id, movie_id)