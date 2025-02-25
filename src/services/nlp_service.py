import spacy
import re
from typing import Tuple, Optional

class NLPService:
    """Service for natural language processing of user messages"""
    
    def __init__(self):
        # Load English language model - using the small model for efficiency
        # You can use 'en_core_web_md' or 'en_core_web_lg' for better accuracy
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            # If the model isn't installed, provide instructions
            raise ImportError(
                "Spacy model 'en_core_web_sm' not found. "
                "Please install it with: python -m spacy download en_core_web_sm"
            )
        
        # Define intent patterns - these could be moved to a configuration file
        self.intent_patterns = {
            'get_info': [
                r'(?:about|info|information|tell me about|what do you know about|details on|score of|rating of|how good is)\s+(.+)',
                r'(?:how is|how was|is|was)\s+(.+)(?:\s+any good|\s+worth watching|\s+good)?',
                r'(?:what is|what\'s)\s+(.+)(?:\s+about|\s+like)?',
                r'(.+)(?:\s+worth watching|\s+any good|\s+recommended)?'
            ],
            'mark_watched': [
                r'(?:i (?:have )?(?:just |recently )?(?:watched|seen)|i\'ve (?:just |recently )?(?:watched|seen)|seen|watched|completed|finished)\s+(.+)',
                r'(?:i (?:have )?finished|i\'ve finished|done with|completed)\s+(.+)',
                r'(?:add|mark|put)\s+(.+)(?:\s+as watched|\s+to my watched list|\s+to watched list)'
            ],
            'help': [
                r'(?:help|assist|support|how to use|instructions|commands|what can you do|how does this work)'
            ],
            'list_watched': [
                r'(?:list|show|what are|what have i|which) (?:movies have i watched|movies i\'ve watched|my watched movies|my watched list|watched movies)'
            ]
        }
    
    def process_message(self, message: str) -> Tuple[str, Optional[str]]:
        """
        Process a message to determine intent and extract entities
        Returns: (intent, entity)
        """
        # Clean the message
        clean_message = message.lower().strip()
        
        # Process with spaCy
        doc = self.nlp(clean_message)
        
        # Try to match intents using regex patterns first
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, clean_message)
                if match:
                    # If the pattern has a capture group, it's the entity (movie title)
                    if len(match.groups()) > 0:
                        return intent, match.group(1).strip()
                    else:
                        return intent, None
        
        # If no regex match, try to extract movie titles using NER
        # This is a fallback and might be less accurate
        movie_title = self._extract_potential_movie_title(doc)
        
        if movie_title:
            # If we found what looks like a movie title, assume get_info intent
            return 'get_info', movie_title
        
        # Default case - couldn't determine intent
        return 'unknown', None
    
    def _extract_potential_movie_title(self, doc) -> Optional[str]:
        """
        Extract what might be a movie title from the document
        Uses named entity recognition and other heuristics
        """
        # Check for named entities that might be movie titles
        # Movies are often recognized as WORK_OF_ART, ORG, or PERSON
        entities = [ent.text for ent in doc.ents if ent.label_ in ['WORK_OF_ART', 'ORG', 'PERSON']]
        
        if entities:
            # Return the longest entity as it's more likely to be a movie title
            return max(entities, key=len)
        
        # If no entities found, look for noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
        if noun_phrases:
            # Return the longest noun phrase
            return max(noun_phrases, key=len)
        
        return None
    
    def extract_sentiment(self, message: str) -> float:
        """
        Extract sentiment from a message
        Returns a score from -1 (negative) to 1 (positive)
        """
        doc = self.nlp(message.lower())
        
        # Simple sentiment analysis based on polarity of tokens
        # This is very basic - a proper sentiment analyzer would be better
        positive_words = {'good', 'great', 'excellent', 'amazing', 'love', 'enjoy', 'like', 'best', 'favorite', 'recommend'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'worst', 'boring', 'waste'}
        
        # Count positive and negative words
        positive_count = sum(1 for token in doc if token.text in positive_words)
        negative_count = sum(1 for token in doc if token.text in negative_words)
        
        # Calculate simple sentiment score
        total = positive_count + negative_count
        if total == 0:
            return 0  # Neutral
        
        return (positive_count - negative_count) / total 