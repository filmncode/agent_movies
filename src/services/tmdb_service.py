import os
from typing import List, Optional, Dict, Tuple
import requests
from dotenv import load_dotenv

load_dotenv()

class TMDbService:
    """Service to interact with TMDb API"""
    
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = "https://api.themoviedb.org/3"
        
        if not self.api_key:
            raise ValueError("TMDB_API_KEY not found in environment variables")
    
    def search_movie(self, title: str) -> Tuple[Optional[Dict], str]:
        """
        Search for a movie by title
        Returns: (movie_data, message)
        """
        try:
            endpoint = f"{self.base_url}/search/movie"
            params = {
                'api_key': self.api_key,
                'query': title,
                'language': 'en-US',
                'page': 1
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            results = response.json().get('results', [])
            if not results:
                return None, f"No movies found matching '{title}'"
                
            # Return the most popular result
            movie = results[0]
            return movie, "Movie found successfully"
            
        except requests.exceptions.RequestException as e:
            return None, f"Error searching for movie: {str(e)}"
    
    def get_movie_details(self, movie_id: int) -> Tuple[Optional[Dict], str]:
        """
        Get detailed information about a movie
        Returns: (movie_details, message)
        """
        try:
            endpoint = f"{self.base_url}/movie/{movie_id}"
            params = {
                'api_key': self.api_key,
                'language': 'en-US',
                'append_to_response': 'credits,reviews'
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            movie = response.json()
            return movie, "Movie details retrieved successfully"
            
        except requests.exceptions.RequestException as e:
            return None, f"Error getting movie details: {str(e)}"
    
    def get_similar_movies(self, movie_id: int, min_score: float = 0.0) -> Tuple[List[Dict], str]:
        """
        Get similar movies with optional minimum score filter
        Returns: (similar_movies, message)
        """
        try:
            endpoint = f"{self.base_url}/movie/{movie_id}/similar"
            params = {
                'api_key': self.api_key,
                'language': 'en-US',
                'page': 1
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            movies = response.json().get('results', [])
            
            # Filter by minimum score and sort by popularity
            filtered_movies = [
                movie for movie in movies 
                if movie.get('vote_average', 0) >= min_score
            ]
            
            # Sort by popularity (descending)
            sorted_movies = sorted(
                filtered_movies,
                key=lambda x: x.get('popularity', 0),
                reverse=True
            )
            
            if not sorted_movies:
                return [], f"No similar movies found with minimum score of {min_score}"
                
            return sorted_movies, "Similar movies found successfully"
            
        except requests.exceptions.RequestException as e:
            return [], f"Error getting similar movies: {str(e)}"

    def format_movie_info(self, movie: Dict) -> str:
        """Format movie information for display"""
        title = movie.get('title', 'Unknown Title')
        score = movie.get('vote_average', 0.0)
        year = movie.get('release_date', '')[:4]
        overview = movie.get('overview', 'No overview available')
        
        return (
            f"Title: {title} ({year})\n"
            f"Score: {score}/10\n"
            f"Overview: {overview}\n"
        ) 