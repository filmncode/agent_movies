from typing import List
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseService:
    def __init__(self):
        self.mongo_uri = os.getenv('MONGODB_URI')
        if not self.mongo_uri:
            raise ValueError("MongoDB URI not found in environment variables")
            
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.movie_score
        self.watched_movies = self.db.watched_movies

    def add_watched_movie(self, user_id: str, movie_id: int) -> bool:
        """Add a movie to user's watched list"""
        try:
            result = self.watched_movies.update_one(
                {'user_id': user_id},
                {'$addToSet': {'movies': movie_id}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error adding watched movie: {str(e)}")
            return False

    def get_watched_movies(self, user_id: str) -> List[int]:
        """Get list of movies watched by user"""
        try:
            user_doc = self.watched_movies.find_one({'user_id': user_id})
            return user_doc.get('movies', []) if user_doc else []
        except Exception as e:
            print(f"Error getting watched movies: {str(e)}")
            return []

    def is_movie_watched(self, user_id: str, movie_id: int) -> bool:
        """Check if user has watched a specific movie"""
        try:
            return movie_id in self.get_watched_movies(user_id)
        except Exception as e:
            print(f"Error checking watched movie: {str(e)}")
            return False 