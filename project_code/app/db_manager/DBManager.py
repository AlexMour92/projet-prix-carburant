import pandas as pd
import os
import json
import base64

from google.cloud import bigquery
from google.oauth2 import service_account
from constants.constants import (SERVICE_KEY_PATH,
                                 STATION_TABLE_ID,
                                 DATE_TABLE_ID,
                                 FUEL_TABLE_ID,
                                 PRICE_TEMP_TABLE_ID,
                                 PRICE_PROD_TABLE_ID)


class DBManager:
    """
    This class manages interactions with a BigQuery database.

    It uses a service account JSON key file for authentication and provides methods to:

    - Retrieve information from BigQuery tables (e.g., maximum IDs, fuel IDs)
    - Retrieve all data from a table
    - Insert a list of rows into a table
    """

    def __init__(self):
        """
        Initializes the DBManager object.

        Establishes a BigQuery client using the provided service account JSON key file path.
        """
        if 'GOOGLE_APPLICATION_CREDENTIALS_JSON' in os.environ:
            # Décodage du JSON encodé en base64
            json_content = base64.b64decode(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON']).decode('utf-8')
            json_acct_info = json.loads(json_content)
            credentials = service_account.Credentials.from_service_account_info(json_acct_info)
            self.client = bigquery.Client(credentials=credentials, project=json_acct_info['project_id'])
        elif os.path.exists(SERVICE_KEY_PATH):
            self.client = bigquery.Client.from_service_account_json(SERVICE_KEY_PATH)
        else:
            self.client = bigquery.Client()

    def get_max_id_date(self) -> int:
        """
        Retrieves the highest idDate value from the dim_date table.

        Executes a BigQuery query to select the maximum idDate from the `DATE_TABLE_ID` table and returns
        the value as an integer. Handles cases where no data exists in the table.

        :return: int: The highest idDate value in the dim_date table, or 0 if the table is empty.
        """
        sql = (f"SELECT MAX(idDate) as idDate "
               f"FROM `{DATE_TABLE_ID}`")
        query_job = self.client.query(sql)
        df_result = query_job.result().to_dataframe()
        if df_result['idDate'].iloc[0] is not pd.NA:
            return int(df_result['idDate'].iloc[0])
        return 0

    def get_max_id_price(self) -> int:
        """
        Retrieves the highest idPrix value from the fact_price table.

        Similar to get_max_id_date, this method retrieves the maximum idPrix value from the `PRICE_TABLE_ID` table.

        :return: int: The highest idPrix value in the fact_price table, or 0 if the table is empty.
                """
        sql = (f"SELECT MAX(idPrix) as idPrix "
               f"FROM `{PRICE_PROD_TABLE_ID}`")
        query_job = self.client.query(sql)
        df_result = query_job.result().to_dataframe()

        if df_result['idPrix'].iloc[0] is not pd.NA:
            return int(df_result['idPrix'].iloc[0])
        return 0

    def get_id_fuel(self, fuel_name: str) -> int:
        """
        Retrieves the idCarburant for a given fuel name from the dim_carburant table.

        Executes a BigQuery query to select the idCarburant where nom (fuel name) matches the provided
        `fuel_name` in the `FUEL_TABLE_ID` table. Returns the idCarburant value as an integer.
        Handles cases where the fuel name is not found in the table.

        :param fuel_name: str: The name of the fuel to search for.
        :return: int: The idCarburant value for the specified fuel name, or 0 if the fuel name is not found.
        """
        sql = (f"SELECT idCarburant "
               f"FROM `{FUEL_TABLE_ID}` "
               f"WHERE nom = '{fuel_name}'")
        query_job = self.client.query(sql)
        df_result = query_job.result().to_dataframe()
        if df_result.size != 0:
            return int(df_result['idCarburant'].iloc[0])
        return 0

    def get_all_stations(self) -> pd.DataFrame:
        """
        Retrieves all data from the stations table.

        Executes a BigQuery query to select all columns (`*`) from the `STATION_TABLE_ID`
        table and returns it as a pandas DataFrame.

        :return: pandas.DataFrame: A DataFrame containing all data from the stations table.
                """
        sql = (f"SELECT * "
               f"FROM {STATION_TABLE_ID}")
        query_job = self.client.query(sql)
        df_result = query_job.result().to_dataframe()
        return df_result

    def insert_list(self, list_to_insert: list, table_id: str) -> None:
        """
        Inserts a list of rows into a specified BigQuery table.

        Creates a BigQuery table object using the provided `table_id`, then inserts the
        rows from `list_to_insert` into the table. Handles and prints any errors that
        occur during the insertion process.

        :param list_to_insert: list: A list of dictionaries, where each dictionary represents
        a row to be inserted.
        :param table_id: str: The ID of the BigQuery table to insert the rows into.
        """
        table = self.client.get_table(table_id)
        errors = self.client.insert_rows(table=table, rows=list_to_insert)
        if not errors == []:
            print(f"Encountered errors while inserting row: {errors}")
