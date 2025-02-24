from crew import MoviescoreCrew
from crewai import Task
from services.db_service import DatabaseService
from services.whatsapp_service import WhatsAppService

def test_database():
    print("\nTesting Database Connection...")
    db = DatabaseService()
    
    # Test adding and retrieving watched movies
    user_id = "test_user_123"
    movie_id = 27205  # Inception's TMDB ID
    
    # Add movie to watched list
    success = db.add_watched_movie(user_id, movie_id)
    print(f"Added movie {movie_id} to watched list: {success}")
    
    # Get watched movies
    watched_movies = db.get_watched_movies(user_id)
    print(f"Watched movies for user: {watched_movies}")
    
    # Check if movie is watched
    is_watched = db.is_movie_watched(user_id, movie_id)
    print(f"Is movie {movie_id} watched? {is_watched}")

def test_whatsapp():
    print("\nTesting WhatsApp Integration...")
    whatsapp = WhatsAppService()
    
    # Replace with your WhatsApp number (format: +1234567890)
    test_number = "+YOUR_PHONE_NUMBER"
    
    # Test sending a message
    message = "Hello! This is a test message from Movie Score Bot."
    success = whatsapp.send_message(test_number, message)
    print(f"Sent WhatsApp message: {success}")
    
    # Test message processing
    test_messages = [
        "Tell me about Inception",
        "I watched Inception",
        "What's the score of The Dark Knight",
        "random message"
    ]
    
    for msg in test_messages:
        intent, title = whatsapp.process_message(msg)
        print(f"\nMessage: {msg}")
        print(f"Intent: {intent}")
        print(f"Movie Title: {title}")

def main():
    try:
        test_database()
    except Exception as e:
        print(f"Database test failed: {str(e)}")
    
    try:
        test_whatsapp()
    except Exception as e:
        print(f"WhatsApp test failed: {str(e)}")

if __name__ == "__main__":
    main() 