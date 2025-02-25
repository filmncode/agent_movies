#!/usr/bin/env python
"""
Test script for OpenAI integration in Movie Score application.
This script tests the OpenAI service's ability to process messages and generate responses.
"""

import os
import sys
from dotenv import load_dotenv
from services.openai_service import OpenAIService

# Load environment variables
load_dotenv()

def test_openai_processing():
    """Test OpenAI message processing"""
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file")
        sys.exit(1)
    
    try:
        # Initialize OpenAI service
        openai_service = OpenAIService()
        print("OpenAI service initialized successfully")
        print(f"Using model: {openai_service.model}")
        
        # Test user ID
        test_user = "test_user_123"
        
        # Test messages
        test_messages = [
            "Tell me about Inception",
            "I watched The Dark Knight yesterday",
            "What movies have I watched?",
            "Can you recommend something like Pulp Fiction but less violent?",
            "help"
        ]
        
        # Process each message
        for message in test_messages:
            print("\n" + "="*50)
            print(f"Testing message: '{message}'")
            
            # Process message
            intent, movie_title, context = openai_service.process_message(message, test_user)
            print(f"Detected intent: {intent}")
            print(f"Extracted movie title: {movie_title}")
            print(f"Context: {context}")
            
            # Generate response
            prompt = f"The user said: '{message}'. Please respond as a movie recommendation bot."
            response = openai_service.generate_response(prompt, test_user)
            print("\nGenerated response:")
            print(response)
        
        print("\n" + "="*50)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_openai_processing() 