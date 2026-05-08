from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('api_key')