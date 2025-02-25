# Agent Movies

## What the AI Agent Does
* Ask About a Movie: You send a message with a movie title, and the agent tells you its current score.
* Recommend Similar Movies: The agent suggests similar movies that have higher scores than the movie you asked about.
* Track Watched Movies: You can tell the agent when you've watched a movie, and it keeps a record so it doesn't recommend those movies again.
* View Your Watched Movies: You can ask to see a list of movies you've marked as watched.
* Natural Language Understanding: The agent understands various ways of asking about movies or marking them as watched.
* Conversational AI: With OpenAI integration, the agent can engage in natural conversations and understand complex queries.
* Via WhatsApp: All interactions happen through WhatsApp, making it easy and convenient.

⠀
## How It Works
The AI agent uses several tools to provide this functionality:
1 WhatsApp Integration:
	* The agent uses Twilio's WhatsApp API to receive and send messages.
	* When you send a message, Twilio forwards it to a server, which processes your request and sends a response back through WhatsApp.
2 Movie Data:
	* The agent uses the TMDb (The Movie Database) API to get movie information.
	* It searches for the movie you mention, retrieves its score (on a 0-10 scale), and finds similar movies.
	* It then filters the similar movies to include only those with higher scores and excludes any you've already watched.
3 Tracking Watched Movies:
	* The agent stores your watched movies in a database, using your WhatsApp number as a unique identifier.
	* When recommending movies, it checks this database to ensure it doesn't suggest movies you've already watched.
4 Message Processing:
	* The agent can use two different NLP approaches:
		* Basic NLP: Uses spaCy for intent recognition and entity extraction
		* Advanced NLP: Uses OpenAI's models for more natural conversation and complex query understanding
	* It maintains conversation history to provide context-aware responses when using OpenAI
	* It can understand complex queries like "recommend something like Pulp Fiction but less violent"

⠀
## Example Interaction
Here's how you might interact with the agent:

### Basic Interaction
* You: "Tell me about Inception" 
  Agent: "Inception has a score of 8.8. Here are similar movies with better scores:  
  1 The Dark Knight (score: 9.0)  
  2 Interstellar (score: 8.9) If you've watched any of these, let me know by saying 'I watched [movie title]'."
* You: "I watched The Dark Knight" 
  Agent: "Noted, you've watched The Dark Knight."
* You: "What movies have I watched?" 
  Agent: "You've watched 1 movie. Here are the most recent ones:
  1. The Dark Knight (9.0/10)"
* You: "help" 
  Agent: "Here's how you can use Movie Score:
  1. Get movie information: 'Tell me about [movie title]' or 'How good is [movie title]'
  2. Mark a movie as watched: 'I watched [movie title]' or 'Mark [movie title] as watched'
  3. See your watched movies: 'Show my watched movies' or 'What have I watched'
  4. Get help: 'help' or 'how does this work'
  
  I'll provide movie scores, recommendations, and keep track of what you've watched!"

### Advanced Interaction (with OpenAI)
* You: "I'm in the mood for a sci-fi movie, something mind-bending like Inception"
  Agent: "If you enjoyed Inception's mind-bending narrative, I'd recommend checking out 'Interstellar' (8.6/10), another Christopher Nolan masterpiece with complex scientific concepts and emotional depth. 'Arrival' (7.9/10) is also excellent with its non-linear storytelling and thought-provoking take on language and time. Both offer the intellectual stimulation and visual spectacle you'd appreciate if you liked Inception."
* You: "That sounds great, but I've already seen Interstellar"
  Agent: "I understand you've seen Interstellar already. In that case, besides Arrival, you might enjoy 'The Prestige' (8.5/10), another Nolan film with clever twists, or 'Blade Runner 2049' (8.0/10) which offers stunning visuals and philosophical themes. 'Annihilation' (6.9/10) is also worth considering for its surreal and thought-provoking approach to sci-fi. Would you like more details about any of these?"

⠀
## Key Features
* Natural Language Understanding:
  * Basic NLP: Uses spaCy for intent recognition and entity extraction
  * Advanced NLP (with OpenAI): Enables natural conversations and complex query understanding
  * Maintains conversation context for follow-up questions
* Accurate Recommendations:
  * Only recommends similar movies with higher scores than the movie you asked about.
  * Excludes movies you've already watched to keep recommendations fresh.
  * Recommendations are sorted by popularity to ensure they're relevant and well-known.
* Error Handling:
  * If the movie title isn't found, the agent responds with "Movie not found, please check the title and try again."
  * If there are no similar movies with better scores, it informs you and may suggest popular similar movies instead.
* Simple Interaction:
  * Uses natural language processing to understand your intent, making it easy to use.
  * Responses are formatted clearly for readability on WhatsApp.

⠀
## Technical Details
* WhatsApp Integration:
  * Twilio handles the messaging, with a webhook set up to receive your messages and send responses.
  * Your phone number is used to identify you and track your watched movies.
* Movie Data:
  * The TMDb API provides movie scores (vote_average) and similar movies.
  * The agent filters similar movies based on scores and your watched list, then sorts them by popularity.
* Database:
  * MongoDB stores your watched movies, with your WhatsApp number as the key.
  * Each entry includes a list of movie IDs you've watched, ensuring efficient lookups.
* Natural Language Processing:
  * Basic NLP: Uses spaCy for intent recognition and entity extraction
  * Advanced NLP: Optional OpenAI integration for more natural conversations
  * Conversation history is maintained for context-aware responses
* Server:
  * A Flask server processes incoming messages, interacts with the TMDb API and database, and sends responses via Twilio.
  * The server handles multiple users concurrently, making it scalable.

⠀
## Limitations and Future Improvements
* Current Limitations:
  * Basic NLP uses simple pattern matching, which may not handle complex queries well.
  * OpenAI integration adds cost and latency to responses.
  * Assumes the most popular movie when there are multiple matches for a title (e.g., remakes).
  * Limited to text-based responses for now, though WhatsApp supports media like movie posters.
* Possible Improvements:
  * Implement a hybrid approach that uses basic NLP for simple queries and OpenAI for complex ones.
  * Include a confirmation step for ambiguous movie titles.
  * Send movie posters or trailers to enhance the experience.
  * Add more sophisticated recommendation algorithms based on user preferences.

⠀
## How to Get Started
To use this agent, it needs to be set up with:
* A Twilio account with a WhatsApp-enabled number.
* A TMDb API key for movie data.
* A MongoDB database for storing user data.
* (Optional) An OpenAI API key for advanced natural language processing.
* A server (e.g., Flask) deployed on a platform like Heroku or AWS.

For detailed setup instructions, see:
* INSTALL_NLP.md - For setting up the basic NLP components
* OPENAI_INTEGRATION.md - For setting up the OpenAI integration

⠀Once set up, you can start messaging the WhatsApp number to ask about movies and track your watched list. The agent will handle the rest, providing you with scores and personalized recommendations.