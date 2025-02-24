from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from services.message_handler import MessageHandler
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/test", methods=['GET', 'POST'])
def test():
    logger.info("Test endpoint hit!")
    logger.info(f"Method: {request.method}")
    return "Test endpoint working!"

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    logger.info(f"Webhook hit with method: {request.method}")
    
    # Handle GET requests (for Twilio verification)
    if request.method == 'GET':
        logger.info("Webhook verification request")
        return "Webhook endpoint working!"
    
    # Handle POST requests (actual messages)
    try:
        # Log raw request data
        logger.info(f"Request headers: {dict(request.headers)}")
        logger.info(f"Request form data: {dict(request.form)}")
        
        # Get the incoming message details
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '').strip()
        
        logger.info(f"Processing message: '{incoming_msg}' from {sender}")
        
        # Process the message
        handler = MessageHandler()
        response_text, success = handler.handle_message(incoming_msg, sender)
        
        logger.info(f"Handler response: {response_text} (success: {success})")
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_text)
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        resp.message("Sorry, I encountered an error. Please try again.")
        return str(resp)

@app.route("/", methods=['GET'])
def home():
    logger.info("Home endpoint hit!")
    return "WhatsApp webhook server is running!"

if __name__ == "__main__":
    # Make sure we're logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)
    
    logger.info("Server starting up...")
    # Allow external access
    app.run(debug=True, host='0.0.0.0', port=5000) 