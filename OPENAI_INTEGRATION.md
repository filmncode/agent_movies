# OpenAI Integration for Natural Conversation

This document explains how to set up and use the OpenAI integration for more natural conversations in the Movie Score application.

## Overview

The OpenAI integration enhances the Movie Score application with advanced natural language processing capabilities, allowing for:

1. **More Natural Conversations**: Users can interact with the bot in a more conversational way without needing to follow strict command formats.
2. **Better Understanding**: The system can understand complex queries and extract relevant information even when phrased in unusual ways.
3. **Context Awareness**: The system maintains conversation history to provide more contextually relevant responses.
4. **Personalized Responses**: Responses are generated dynamically based on the specific user query and context.

## Setup Instructions

### 1. Environment Variables

Add the following to your `.env` file:

```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
USE_OPENAI=true
```

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: The OpenAI model to use (default: gpt-3.5-turbo)
- `USE_OPENAI`: Set to "true" to enable OpenAI integration (default: false)

### 2. Install Dependencies

Make sure you have the OpenAI Python package installed (version 1.0.0 or higher):

```bash
pip install openai>=1.0.0
```

This should already be included in your requirements.txt file.

> **Note**: This integration uses the new OpenAI API format introduced in version 1.0.0. If you're experiencing issues, make sure you're using the latest version of the OpenAI package.

## How It Works

### 1. Message Processing

When a user sends a message, the system:

1. Passes the message to the OpenAI service
2. OpenAI analyzes the message to determine:
   - The user's intent (get_info, mark_watched, help, list_watched)
   - Any movie titles mentioned
   - Additional context (sentiment, confidence, etc.)
3. Based on the detected intent, the system retrieves relevant data (movie details, watched movies, etc.)
4. The system generates a natural language response using OpenAI

### 2. Conversation History

The system maintains conversation history for each user, allowing for:

- **Follow-up Questions**: Users can ask follow-up questions without repeating context
- **Personalized Interactions**: The system remembers previous interactions
- **Context-Aware Responses**: Responses take into account the conversation flow

The history is limited to the last 5 messages to keep context manageable and reduce token usage.

## Example Interactions

With OpenAI integration enabled, users can interact in more natural ways:

### Movie Information

**User**: "I was thinking about watching Inception. Is it any good?"

**System**: *[Processes with OpenAI to determine intent is 'get_info' and movie is 'Inception']*

**Response**: "Inception is definitely worth watching! It has a score of 8.8/10. Directed by Christopher Nolan, it's a mind-bending sci-fi thriller about entering people's dreams. If you enjoy it, you might also like The Dark Knight (9.0/10) or Interstellar (8.6/10)."

### Marking as Watched

**User**: "Just finished watching The Shawshank Redemption. It was amazing!"

**System**: *[Processes with OpenAI to determine intent is 'mark_watched' and movie is 'The Shawshank Redemption']*

**Response**: "I'm glad you enjoyed The Shawshank Redemption! I've marked it as watched for you. Based on this, you might enjoy The Green Mile (8.5/10) or The Godfather (9.2/10)."

### Complex Queries

**User**: "Can you recommend something like Pulp Fiction but with less violence?"

**System**: *[Processes with OpenAI to understand the complex query]*

**Response**: "If you like Pulp Fiction's style but want less violence, you might enjoy The Grand Budapest Hotel or The Big Lebowski. Both have Tarantino's quirky dialogue and interesting characters but with less graphic content."

## Limitations and Considerations

1. **API Costs**: Using OpenAI's API incurs costs based on token usage. Monitor your usage to manage expenses.

2. **Response Time**: API calls add some latency to responses. The system is designed to minimize this, but responses will be slightly slower than with the basic NLP.

3. **Fallback Mechanism**: If OpenAI processing fails for any reason, the system falls back to the basic NLP processing.

4. **Privacy Considerations**: Conversation history is stored in memory. Consider implementing proper data retention policies.

## Troubleshooting

### Common Issues

1. **"OpenAI service not initialized"**:
   - Check that your OPENAI_API_KEY is correctly set in the .env file
   - Verify that USE_OPENAI is set to "true"

2. **API Version Errors**:
   - Make sure you're using OpenAI Python package version 1.0.0 or higher
   - If you see errors about `openai.ChatCompletion`, you need to update your OpenAI package

3. **Slow Responses**:
   - Consider using a faster model like "gpt-3.5-turbo" instead of "gpt-4"
   - Reduce the conversation history length

4. **Unexpected Responses**:
   - Check the logs to see what intent and entities were detected
   - Adjust the system message in the OpenAI service if needed

### Logging

The system logs detailed information about OpenAI processing. Check the logs for:
- Detected intents and entities
- API errors
- Response generation issues 