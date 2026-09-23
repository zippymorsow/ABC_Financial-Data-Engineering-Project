# This is for ingestion of data from MSSQL to PostgreSQL for the ABC Financial project. It is a one-time migration script that extracts data from the legacy MSSQL database and loads it into the new PostgreSQL database.
import pandas as pd

# def calculate_efficiency(score: float, time_spent: int) -> float:
#     """Calculate the task efficiency rating.

#     Takes a performance score and divides it by the total minutes taken.
    
#     :param score: The baseline accuracy or performance score.
#     :param time_spent: Total duration in minutes.
#     :return: Calculated efficiency percentage.
#     """
#     return (score / time_spent) * 100