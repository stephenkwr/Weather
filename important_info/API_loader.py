from pathlib import Path
import os
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

def env(key : str) -> str:
    value = os.getenv(key)
    if value is None:
        raise KeyError(f"Environment variable '{key}' not found.")
    return value