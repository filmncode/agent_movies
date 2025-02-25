from twilio.rest import Client
from typing import Optional, Tuple
import os
from dotenv import load_dotenv
from services.nlp_service import NLPService

load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise ValueError("Twilio credentials not found in environment variables")
            
        self.client = Client(self.account_sid, self.auth_token)
        self.nlp_service = NLPService()

    def send_message(self, to_number: str, message: str) -> bool:
        """Send WhatsApp message using Twilio"""
        try:
            self.client.messages.create(
                body=message,
                from_=f"whatsapp:{self.from_number}",
                to=f"whatsapp:{to_number}"
            )
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False

    def process_message(self, message: str) -> Tuple[str, Optional[str]]:
        """
        Process incoming message to determine intent and extract movie title
        Returns: (intent, movie_title)
        """
        # Use the NLP service to process the message
        return self.nlp_service.process_message(message) 