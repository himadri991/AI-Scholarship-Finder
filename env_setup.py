from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access your API keys securely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

# Optional: Validate keys are loaded
if not all([GROQ_API_KEY, TAVILY_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID, PINECONE_API_KEY, PINECONE_ENVIRONMENT]):
    raise EnvironmentError("Some environment variables are missing. Check your .env file.")