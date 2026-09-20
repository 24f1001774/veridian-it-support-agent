import os

try:
    from dotenv import load_dotenv
    # Load .env from current directory or parent directory
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass

# API Configuration - Compatible with Groq / OpenAI API
API_KEY = os.environ.get("GROQ_API_KEY", "")
BASE_URL = os.environ.get("BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "openai/gpt-oss-120b")

# Company Metadata
COMPANY_NAME = "Veridian Corp"
EXERCISE_DATE_RANGE = "21 September 2026 – 25 September 2026"
