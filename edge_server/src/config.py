from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parent
load_dotenv(override=False)

HOST            : str = os.getenv("HOST", "0.0.0.0")
API_PORT        : int = int(os.getenv("API_PORT", "8000"))
STREAMLIT_PORT  : int = int(os.getenv("STREAMLIT_PORT", "8501"))
MAX_HISTORY     : int = int(os.getenv("MAX_HISTORY", "200"))   # items per edge

def as_dict() -> dict:
    return dict(
        HOST=HOST,
        API_PORT=API_PORT,
        STREAMLIT_PORT=STREAMLIT_PORT,
        MAX_HISTORY=MAX_HISTORY,
    )
