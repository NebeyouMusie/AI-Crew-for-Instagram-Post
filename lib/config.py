import os
from dotenv import load_dotenv


# Function to load configuration for the environment varialbles
def load_config():
    return load_dotenv()

# Function to retrieve GROQ API KEY
def get_groq_api_key():
    return os.getenv('GROQ_API_KEY')

def get_browserless_api_key():
    return os.getenv('BROWSERLESS_API_KEY')