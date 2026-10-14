import sys, os
import requests
from urllib.parse import urlencode
from typing import Annotated
from pydantic import BeforeValidator, ValidationInfo
import pyodbc as odbc
import psycopg2
from commons.config import *
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_pipeline_logging(pipeline_name: str):
    """
    Configures standard Python logging to write to daily-rotating local files
    while ensuring compatibility with Prefect orchestration environments.
    """
    
    log_dir = os.path.abspath("logs")
    os.makedirs(log_dir, exist_ok=True)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # 1. Wipe out any pre-existing loose configurations to avoid loop bugs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    log_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 2. THE DUPLICATION FIX LAYER
    # If the script is running under a Prefect execution task, Prefect ALREADY handles the terminal output.
    # We only attach the native console handler if we are running standard local scripts without Prefect!
    is_prefect_running = os.getenv("PREFECT_API_URL") is not None or "prefect" in sys.modules
    
    if not is_prefect_running:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

    #  3. KEEP THE FILE HANDLER ACTIVE (Always runs smoothly in the background)
    file_path = os.path.join(log_dir, f"{pipeline_name}.log")
    file_handler = TimedRotatingFileHandler(
        filename=file_path, when="midnight", interval=1, backupCount=30, encoding="utf-8"
    )
    file_handler.suffix = "-%Y-%m-%d.log"
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    logging.info(f"Logging subsystem initialized. Target: {file_path}")


### Formatting
def standardize_toUpper(txt : str) -> str:
    return txt.upper()
standardizeToUpper = Annotated[str, BeforeValidator(standardize_toUpper)]

def standardize_toLower(txt : str) -> str:
    return txt.lower()
standardizeToLower = Annotated[str, BeforeValidator(standardize_toLower)]

def standardize_limitacccode(txt: str, info: ValidationInfo):
    if len(txt) != 4:
        logging.error(f"{__name__.__class__} || Field: {info.field_name} || Value: {txt}\nAccount code must be exactly 4 characters.")
        raise ValueError(f"Account code must be exactly 4 characters.")
standardizelimitacccode = Annotated[str, BeforeValidator(standardize_limitacccode)]

### API functions
def getAPIrequest(url : str, param : dict = {}) -> any:
    """
    This function sends an HTTP GET request to the specified URL with optional query parameters and returns the JSON response data.
    Args:
        url (str): The URL to send the GET request to.
        param (dict, optional): A dictionary of query parameters to include in the request. Defaults to an empty dictionary.
        Returns:
        any: The JSON response data from the API request, or None if an error occurred.
    """
    try:
        if url == "":
            logging.info("URL cannot be blank.")
            return

        # send http request & get data response
        if param == {}:
            resp = requests.get(url)
        else:
            resp = requests.get(f"{url}?{ urlencode(param) }")

        # raise a response for error status
        resp.raise_for_status()

        data = resp.json()
        return data

    except Exception as e:
        logging.error(e)
        raise e

### Database functions
def execute_query(engine, querystring : str) -> any:
    data = {}
    try:
        # Open an explicit connection from the engine pool
        with engine.connect() as connection:
            # SQLAlchemy requires raw SQL strings to be explicitly wrapped in text()
            result = connection.execute(text(querystring))
            
            # Fetch all rows from the execution result
            data = result.fetchall()
            return data
    except Exception as e:
        logging.error(e)
        raise e

# # for testing purpose
# if __name__ == "__main__":
    # data = getAPIrequest("https://api.frankfurter.dev/v2/rates",{"base":"USD"})