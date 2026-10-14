import logging
from prefect import flow, task, get_run_logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from commons.model.model_finance import DatabaseFactory, 
from commons.shared.helper import execute_query, setup_pipeline_logging
from pathlib import Path

# # # create a one off migration for legacyledger
# # #     from mssql to postgres

# # # create a historical/reprocessing for silver_legacyledger

# # # create a change data capture
# # #     can be from silver_ledger to silver_accounts (add/soft delete)

# # # DO NOT CAN YOUR SELF INTO JUST PYTHON, IF REPROCESSING IS EASIER IN SQL QUERIES THEN LET'S DO IT!
# # # LET'S USE PY FOR FLOW, THEN CALL STORED PROCEDURES
# # # DO NOT OVERTHINKG

# note: incorporate audit trail
# note: incorporate dlq

"""
This a pileline intended as one off migration from mssql to postgres by batch
"""


@task
def get_data_mssql() -> any: # raw
    # 🎯 Grab Prefect's active worker logger context
    logging = get_run_logger() 
    data = {}
    query_string = "SELECT * FROM LEGACY_LEDGER"
    try:
        # create cache, and connect to mssql
        engine_mssql = DatabaseFactory().get_engine("mssql","ecom_db")
        data = execute_query(engine_mssql, query_string) # simple fetch, no complicados...
        # logging.info("temporary...")
        # logging.info(data)
        return data

    except Exception as e:
        logging.error(e)
        raise e


@task
def dump_to_postgres(data_in : list) -> any: # bronze
    # 🎯 Grab Prefect's active worker logger context
    logging = get_run_logger() 
    data = {}
    try:
        logging.info("dump_to_postgres")
        # how many are fetched?, sync batch id from prefect...etc (sys_audittrail)
        return data
    except Exception as e:
        logging.error(e)
        raise e

@flow
def main() -> any:
    # 🎯 Grab Prefect's active worker logger context
    logging = get_run_logger() 
    data = {}
    try:
        data = get_data_mssql()
        dump_to_postgres(data)
        return data
    except Exception as e:
        logging.error(e)
        raise e

# in case of manual run
created_by = Path(__file__).stem
print(f"Running {created_by} as a standalone script.")
if __name__ == "__main__":
    # Initialize the log file with this script's specific name first
    setup_pipeline_logging("ingestion_mssql_to_postgres")

    main.serve(
        name=created_by
        # cron="0 8 * * *" # runs 8AM daily
    )