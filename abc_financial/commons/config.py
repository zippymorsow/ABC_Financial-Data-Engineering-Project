import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "config" / ".env"

load_dotenv(ENV_PATH)

MSSQL_SA_PASSWORD =  os.getenv("MSSQL_SA_PASSWORD")
MSSQL_DEFAULT_USER = os.getenv("MSSQL_DEFAULT_USER")
MSSQL_SA_PASSWORD = os.getenv("MSSQL_SA_PASSWORD")
MSSQL_PID = os.getenv("MSSQL_PID")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")