import os

def load_env_file():
    """Load .env key-values natively into os.environ without requiring python-dotenv."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(current_dir, ".env"),
        os.path.join(os.path.dirname(current_dir), ".env")
    ]
    for c in candidates:
        if os.path.isfile(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            if k not in os.environ:
                                os.environ[k] = v
                break
            except Exception:
                pass

load_env_file()

# API Configuration - Compatible with Groq / OpenAI API
API_KEY = os.environ.get("GROQ_API_KEY", "")
BASE_URL = os.environ.get("BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "openai/gpt-oss-120b")

# Company Metadata
COMPANY_NAME = "Veridian Corp"
EXERCISE_DATE_RANGE = "21 September 2026 – 25 September 2026"
