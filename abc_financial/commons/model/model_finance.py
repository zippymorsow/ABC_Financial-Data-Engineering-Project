import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator, ValidationInfo, computed_field, model_validator
import logging
from ..shared.helper import standardizeToUpper, standardizeToLower, standardizelimitacccode
from commons.config import *
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import urllib.parse as passparser

# creation of tables will be documented here, and basic data validations as well.
class bronze_LegacyLedgerRecord(BaseModel):
    """
    This class represents a legacy ledger entry in the ABC Financial project. It is used to model the data structure of the legacy MSSQL database for the purpose of data ingestion and migration to PostgreSQL.
    """
    entry_id : str
    account_code : str
    account_name : str
    amount : str
    entry_type : str
    currency : str
    posted_at : str
    reconciliation_status : str
    ingested_at : datetime.datetime
    ingested_by : str

class silver_LegacyLedgerRecord(BaseModel):
    """
    This class is based from bronze_LegacyLedgerRecord, and has applied manipulations and data standardization.
    """
    entry_id : int
    account_code : standardizelimitacccode                  # limit len == 4
    account_name : standardizeToLower                       # lowercase
    amount : Decimal
    entry_type : standardizeToUpper                         # uppercase
    currency : standardizeToUpper                           # uppercase
    amountusd : Decimal                                     # computed base currency
    posted_at : datetime.datetime
    reconciliation_status : standardizeToUpper              # uppercase
    created_at : datetime.datetime
    created_by : str
    modified_at : datetime.datetime = None                  # update date timestamp
    deleted_at : datetime.datetime = None                   # soft delete date timestamp
    flagdelete : bool = False                               # soft delete flag
    
    @model_validator(mode="before")
    @classmethod
    def base_currency(cls, data : any, info : any) -> any:
        context = info.context or {}
        usdbaserate = round(Decimal(str(context.get("usdrate", "62.35"))), 4)
        amount = round(Decimal(data.get("amount",0)), 4)
        if data.get("USD") != "USD":
            baseamount = amount * usdbaserate
            data["amountusd"] = baseamount
        else:
            data["amountusd"] = amount
        return data

class silver_currencyrates(BaseModel):
    """
    This class represents the currency exchange rates in the ABC Financial project. It is used to model the data structure of the currency rates for the purpose of data ingestion and migration to PostgreSQL."""
    date : datetime.date
    base : standardizeToUpper
    quote : standardizeToUpper
    rate : Decimal
    ingested_at : datetime.datetime = None
    ingested_by : str
    modified_at : datetime.datetime = None  # update date timestamp
    deleted_at : datetime.datetime = None   # soft delete date timestamp
    flagdelete : bool = False               # soft delete flag
    # sample data {"date":"2026-09-27","base":"USD","quote":"AED","rate":3.6725}

class sys_audittrail(BaseModel):
    """
    Schema of audit trail.
    """
    # sys_audittrail_id : int
    sync_batch_id : str
    pipeline_name : str
    execution_status : str
    records_extracted : int
    records_loaded : int
    records_rejected_dlq : int
    execution_metadata : dict
    execution_summary : str
    triggered_at : datetime.datetime
    triggered_by : str

class sys_migration_dlq(BaseModel):
    """
    Schema of Dead-Letter-Queue (DLQ)
    """
    # dlq_id : int
    failed_at : datetime.datetime
    source_entry_id : int
    raw_payload : str
    error_message : str
    pipeline_stage : str

# database connection
class DatabaseFactory:
    """
    Factory class to create and cache SQLAlchemy engines for different database types.
    """
    def __init__(self):
        # This dictionary acts as our memory cache for live SQLAlchemy engines
        self._engines = {}

    def get_engine(self, db_type: str, database_name: str):
        """Dynamically generates, caches, and returns a SQLAlchemy Engine."""
        db_type = db_type.upper()
        
        # Create a unique key for this specific database combination
        cache_key = f"{db_type}_{database_name}"
        
        # Performance Win: If the engine exists in cache, return it immediately
        if cache_key in self._engines:
            return self._engines[cache_key]
            
        # Otherwise, construct the appropriate connection URL string
        if db_type == "MSSQL":
            url = (
                f"mssql+pyodbc://{MSSQL_DEFAULT_USER}:{passparser.quote_plus(MSSQL_SA_PASSWORD)}@{MSSQL_ENVIRONMENT}:{MSSQL_DB_PORT}/{database_name}"
                f"?driver={passparser.quote_plus("ODBC Driver 18 for SQL Server")}&encrypt=yes&trustServerCertificate=yes"
            )
        elif db_type == "POSTGRES":
            url = f"postgresql+psycopg2://{POSTGRES_DEFAULT_USER}:{passparser.quote_plus(POSTGRES_PASSWORD)}@{POSTGRES_ENVIRONMENT}:{POSTGRES_DB_PORT}/{database_name}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
            
        try:
            # INTEGRATION: Initialize the real SQLAlchemy engine here
            # pool_pre_ping=True acts as an automatic health-check for Docker connections
            new_engine = create_engine(url, pool_pre_ping=True)
            
            # Save the newly built engine into our cache
            self._engines[cache_key] = new_engine
            logging.info(f"Created and cached a brand NEW engine for: {cache_key}")
            
            return new_engine
            
        except SQLAlchemyError as e:
            logging.error(f"Failed to initialize SQLAlchemy engine for {cache_key}: {e}")
            raise e



# # for testing purpose
# def main():
#     ledger = None
#     logging.info(ledger)
#     if __name__ == "__main__":
#         ledger = silver_LegacyLedgerRecord(
#             entry_id = "203"
#             ,account_code = "X78x"
#             ,account_name = "Sample_account_name"
#             ,amount = "15.23"
#             ,entry_type = "cccc"
#             ,currency = "php"
#             ,posted_at = datetime.datetime.now()
#             ,reconciliation_status = "some status"
#               # # SUPPLY THE FIELDS AS YOU NEED
#         )
#     logging.info(ledger)
#     return ledger
# main()