import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "config" / ".env"

load_dotenv(ENV_PATH)

MSSQL_SA_PASSWORD =  os.getenv("MSSQL_SA_PASSWORD")
MSSQL_DEFAULT_USER = os.getenv("MSSQL_DEFAULT_USER")
MSSQL_PID = os.getenv("MSSQL_PID")
MSSQL_ENVIRONMENT = os.getenv("MSSQL_ENVIRONMENT")
MSSQL_DB_PORT = os.getenv("MSSQL_DB_PORT")
MSSQL_DB_DOCKER_PORT = os.getenv("MSSQL_DB_DOCKER_PORT")

POSTGRES_ENVIRONMENT = os.getenv("POSTGRES_ENVIRONMENT")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT")
POSTGRES_DB_DOCKER_PORT = os.getenv("POSTGRES_DB_DOCKER_PORT")
POSTGRES_DEFAULT_USER = os.getenv("")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")