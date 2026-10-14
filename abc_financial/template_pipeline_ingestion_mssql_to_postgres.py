import logging
from prefect import flow, task

# note: incorporate audit trail
# note: incorporate dlq

"""
This a pileline intended as one off migration from mssql to postgres by batch
"""
# connect to mssql to get data
@task
def get_data_mssql() -> any: # raw
    data = {}
    try:
        print()
        return data
    except Exception as e:
        logging.error(e)
        raise e

@task
def dump_to_postgres() -> any: # bronze
    data = {}
    try:
        print()
        return data
    except Exception as e:
        logging(e)
        raise e

@flow
def main() -> any:
    data = {}
    try:
        print()
        return data
    except Exception as e:
        logging.error(e)
        raise e

# in case of manual run
created_by = __name__
if created_by == "__main__":
    main.serve(
        name=created_by
        # cron="0 8 * * *" # runs 8AM daily
    )