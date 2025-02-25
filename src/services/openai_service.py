import os
from openai import OpenAI
from typing import Tuple, Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    """Service for advanced natural language processing using OpenAI models"""
    
    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Default model to use
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        
        # Initialize conversation history
        self.conversation_histories = {}
    
    def process_message(self, message: str, user_id: str) -> Tuple[str, Optional[str], Dict[str, Any]]:
        """
        Process a message using OpenAI to determine intent and extract entities
        Returns: (intent, entity, context)
        """
        # Get or initialize conversation history for this user
        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = []
        
        # Add user message to history
        self.conversation_histories[user_id].append({
            "role": "user",
            "content": message
        })
        
        # Prepare the system message with instructions
        system_message = {
            "role": "system",
            "content": """
            You are a movie recommendation assistant. Your job is to:
            1. Understand what the user is asking about movies
            2. Extract the intent of their message (get_info, mark_watched, help, list_watched, or unknown)
            3. Extract any movie titles mentioned
            4. Provide additional context that might be helpful
            
            Respond in JSON format with the following structure:
            {
                "intent": "get_info|mark_watched|help|list_watched|unknown",
                "movie_title": "extracted movie title or null if none",
                "context": {
                    "additional_info": "any additional information extracted",
                    "sentiment": "positive|negative|neutral",
                    "confidence": 0.0-1.0
                }
            }
            """
        }
        
        # Create the messages array with system message and conversation history
        # Limit history to last 5 messages to keep context manageable
        messages = [system_message] + self.conversation_histories[user_id][-5:]
        
        try:
            # Call the OpenAI API using the new format
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent outputs
                max_tokens=150    # Limit token usage
            )
            
            # Extract the response content
            content = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_histories[user_id].append({
                "role": "assistant",
                "content": content
            })
            
            # Parse the JSON response
            import json
            try:
                parsed = json.loads(content)
                intent = parsed.get("intent", "unknown")
                movie_title = parsed.get("movie_title")
                context = parsed.get("context", {})
                
                return intent, movie_title, context
                
            except json.JSONDecodeError:
                # If JSON parsing fails, fall back to default values
                return "unknown", None, {"error": "Failed to parse response"}
                
        except Exception as e:
            # Handle API errors
            print(f"Error calling OpenAI API: {str(e)}")
            return "unknown", None, {"error": str(e)}
    
    def generate_response(self, prompt: str, user_id: str, context: Dict[str, Any] = None) -> str:
        """
        Generate a natural language response using OpenAI
        """
        # Prepare context information
        context_str = ""
        if context:
            context_str = f"Context: {context}\n\n"
        
        # Create the system message
        system_message = {
            "role": "system",
            "content": f"""
            You are a friendly movie recommendation assistant on WhatsApp. 
            {context_str}
            Keep your responses conversational, helpful, and concise (suitable for WhatsApp).
            Focus on providing accurate movie information and personalized recommendations.
            """
        }
        
        # Get conversation history for this user
        history = self.conversation_histories.get(user_id, [])
        
        # Create messages array
        messages = [system_message] + history[-5:] + [{
            "role": "user",
            "content": prompt
        }]
        
        try:
            # Call the OpenAI API using the new format
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Higher temperature for more creative responses
                max_tokens=300    # Allow longer responses
            )
            
            # Extract and return the response content
            return response.choices[0].message.content
            
        except Exception as e:
            # Handle API errors
            print(f"Error generating response: {str(e)}")
            return "I'm having trouble generating a response right now. Please try again later."
    
    def clear_history(self, user_id: str) -> None:
        """Clear conversation history for a user"""
        if user_id in self.conversation_histories:
            self.conversation_histories[user_id] = [] 