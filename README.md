# Agent Movies

## What the AI Agent Does
* Ask About a Movie: You send a message with a movie title, and the agent tells you its current score.
* Recommend Similar Movies: The agent suggests similar movies that have higher scores than the movie you asked about.
* Track Watched Movies: You can tell the agent when you've watched a movie, and it keeps a record so it doesn't recommend those movies again.
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
	* The agent understands your intent based on keywords in your message:
		* If you say "about [movie]" or "score of [movie]", it retrieves the movie's score and recommendations.
		* If you say "I watched [movie]" or "I've seen [movie]", it adds that movie to your watched list.
	* It extracts the movie title from your message and processes it accordingly.

⠀
## Example Interaction
Here’s how you might interact with the agent:
* You: "Tell me about Inception" Agent: "Inception has a score of 8.8. Here are similar movies with better scores:  
  1 The Dark Knight (score: 9.0)  
  2 Interstellar (score: 8.9) If you've watched any of these, let me know by saying 'I watched [movie title]'."
* You: "I watched The Dark Knight" Agent: "Noted, you've watched The Dark Knight."
* Later, if you ask about another movie, the agent will exclude "The Dark Knight" from its recommendations.

⠀
## Key Features
* Accurate Recommendations:
  * Only recommends similar movies with higher scores than the movie you asked about.
  * Excludes movies you've already watched to keep recommendations fresh.
  * Recommendations are sorted by popularity to ensure they're relevant and well-known.
* Error Handling:
  * If the movie title isn't found, the agent responds with "Movie not found, please check the title and try again."
  * If there are no similar movies with better scores, it informs you and may suggest popular similar movies instead.
* Simple Interaction:
  * Uses keyword matching to understand your intent, making it easy to use.
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
* Server:
  * A Flask server processes incoming messages, interacts with the TMDb API and database, and sends responses via Twilio.
  * The server handles multiple users concurrently, making it scalable.

⠀
## Limitations and Future Improvements
* Current Limitations:
  * Uses simple keyword matching, which may not handle complex queries well.
  * Assumes the most popular movie when there are multiple matches for a title (e.g., remakes).
  * Limited to text-based responses for now, though WhatsApp supports media like movie posters.
* Possible Improvements:
  * Add natural language processing for better intent recognition.
  * Include a confirmation step for ambiguous movie titles.
  * Send movie posters or trailers to enhance the experience.
  * Add commands like "help" or "list watched movies" for more functionality.

⠀
## How to Get Started
To use this agent, it needs to be set up with:
* A Twilio account with a WhatsApp-enabled number.
* A TMDb API key for movie data.
* A MongoDB database for storing user data.
* A server (e.g., Flask) deployed on a platform like Heroku or AWS.

⠀Once set up, you can start messaging the WhatsApp number to ask about movies and track your watched list. The agent will handle the rest, providing you with scores and personalized recommendations.