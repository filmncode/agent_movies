# Movie Score - Technical Documentation

## Overview

Movie Score is an AI-powered WhatsApp bot that helps users discover, track, and get recommendations for movies. The application integrates with external services like TMDb (The Movie Database) for movie information and Twilio for WhatsApp messaging, providing a seamless user experience through a familiar messaging interface.

## System Architecture

The application follows a modular architecture with the following key components:

1. **Crew AI Framework**: The core of the application uses the CrewAI framework to orchestrate multiple AI agents that work together to process user requests.
2. **External Services**: Integration with TMDb API for movie data and Twilio for WhatsApp messaging.
3. **Database**: MongoDB for storing user data, particularly watched movies.
4. **Web Server**: Flask-based webhook server to handle incoming WhatsApp messages.

## Core Components

### 1. Agent System (CrewAI)

The application uses a multi-agent system implemented with CrewAI, where specialized agents handle different aspects of the application:

- **WhatsApp Agent**: Manages communication with users through WhatsApp.
- **Movie Query Agent**: Searches for and retrieves movie information from TMDb.
- **Recommendation Agent**: Generates personalized movie recommendations based on user preferences.
- **Tracker Agent**: Tracks and manages the user's movie watching history.

Each agent has specific tools and capabilities that allow it to perform its designated tasks.

### 2. Services

#### TMDb Service (`tmdb_service.py`)

Handles all interactions with The Movie Database API:
- Searching for movies by title
- Retrieving detailed movie information
- Finding similar movies with optional score filtering
- Formatting movie information for display

```python
# Key methods:
search_movie(title)         # Search for a movie by title
get_movie_details(movie_id) # Get detailed information about a movie
get_similar_movies(movie_id, min_score) # Get similar movies with minimum score
format_movie_info(movie)    # Format movie information for display
```

#### WhatsApp Service (`whatsapp_service.py`)

Manages WhatsApp communication using Twilio:
- Sending messages to users
- Processing incoming messages to determine intent and extract movie titles

```python
# Key methods:
send_message(to_number, message) # Send WhatsApp message using Twilio
process_message(message)         # Process incoming message to determine intent
```

#### Database Service (`db_service.py`)

Handles all database operations using MongoDB:
- Adding movies to a user's watched list
- Retrieving a user's watched movies
- Checking if a user has watched a specific movie

```python
# Key methods:
add_watched_movie(user_id, movie_id) # Add a movie to user's watched list
get_watched_movies(user_id)          # Get list of movies watched by user
is_movie_watched(user_id, movie_id)  # Check if user has watched a specific movie
```

#### Message Handler (`message_handler.py`)

Processes incoming messages and coordinates the appropriate response:
- Determining user intent from message content
- Handling movie information requests
- Managing "mark as watched" requests
- Generating appropriate responses

```python
# Key methods:
handle_message(message, user_id)      # Main method to process incoming messages
_handle_movie_info(movie_title)       # Handle movie information request
_handle_mark_watched(movie_title, user_id) # Handle marking a movie as watched
```

### 3. Webhook Server (`webhook_server.py`)

A Flask-based server that handles incoming webhook requests from Twilio:
- Receives incoming WhatsApp messages
- Processes messages using the Message Handler
- Returns formatted responses to Twilio for delivery to users

```python
# Key routes:
@app.route("/webhook", methods=['GET', 'POST']) # Main webhook endpoint
@app.route("/test", methods=['GET', 'POST'])    # Test endpoint
@app.route("/", methods=['GET'])                # Home endpoint
```

## User Interaction Flow

1. **User sends a message via WhatsApp** to the Twilio-provided phone number.
2. **Twilio forwards the message** to the webhook server.
3. **The webhook server processes the message**:
   - Extracts the message content and sender information
   - Passes the information to the Message Handler
4. **The Message Handler determines the intent**:
   - If asking about a movie: Retrieves movie information and similar movies
   - If marking a movie as watched: Updates the user's watched list and provides recommendations
5. **The response is sent back to Twilio**, which delivers it to the user via WhatsApp.

## Message Processing Logic

The system recognizes two primary intents:

1. **Movie Information Request**:
   - Triggered by phrases like "about [movie]", "score of [movie]", "tell me about [movie]"
   - Returns movie details (title, year, score, overview)
   - Includes recommendations for similar movies with good scores

2. **Mark Movie as Watched**:
   - Triggered by phrases like "I watched [movie]", "I've seen [movie]", "seen [movie]"
   - Adds the movie to the user's watched list
   - Provides recommendations based on the watched movie, excluding already watched movies

## Configuration and Environment Variables

The application requires several environment variables for proper operation:

- **OPENAI_API_KEY**: For the AI agents
- **TMDB_API_KEY**: For accessing The Movie Database API
- **TWILIO_ACCOUNT_SID**: For Twilio integration
- **TWILIO_AUTH_TOKEN**: For Twilio authentication
- **TWILIO_WHATSAPP_NUMBER**: The WhatsApp number used by the application
- **MONGODB_URI**: Connection string for the MongoDB database

## Running the Application

The application can be run in several modes:

1. **Normal Mode**: `python src/main.py`
2. **Training Mode**: `python src/main.py train [iterations] [filename]`
3. **Replay Mode**: `python src/main.py replay [task_id]`
4. **Test Mode**: `python src/main.py test [iterations] [model_name]`

The webhook server can be started separately with:
```
python src/webhook_server.py
```

## Dependencies

The application relies on several key libraries:
- `crewai`: For the multi-agent system
- `langchain`: For AI agent tools and capabilities
- `openai`: For AI model access
- `twilio`: For WhatsApp integration
- `pymongo`: For MongoDB database access
- `flask`: For the webhook server
- `requests`: For API calls
- `python-dotenv`: For environment variable management

## Limitations and Future Improvements

- **Natural Language Processing**: Currently uses simple keyword matching, could be enhanced with more sophisticated NLP.
- **Movie Disambiguation**: When multiple movies match a title, the system currently selects the most popular one without confirmation.
- **Media Support**: Could be enhanced to include movie posters or trailers in responses.
- **Additional Commands**: Could add functionality like "help" or "list watched movies".
- **User Preferences**: Could incorporate more sophisticated preference tracking beyond just watched movies. 