import unittest
from unittest.mock import patch, MagicMock
import os
import json
import base64
import sys
import pandas as pd

from google.oauth2 import service_account
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from project_code.app.db_manager.DBManager import DBManager


class TestDBManager(unittest.TestCase):

    def setUp(self):
        self.db_manager = DBManager()

    @patch('google.cloud.bigquery.Client')
    @patch('google.oauth2.service_account.Credentials.from_service_account_info')
    @patch('os.path.exists')
    def test_init(self, mock_exists, mock_credentials, mock_client):
        # Scenario 1: GOOGLE_APPLICATION_CREDENTIALS_JSON is defined
        with patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS_JSON': base64.b64encode(json.dumps({"project_id": "test-project"}).encode()).decode()}):
            mock_exists.return_value = False
            mock_credentials.return_value = MagicMock()
            
            DBManager()
            
            mock_credentials.assert_called_once()
            mock_client.assert_called_once()
            mock_client.reset_mock()
            mock_credentials.reset_mock()

        # Scenario 2: SERVICE_KEY_PATH exists
        with patch.dict(os.environ, {}, clear=True):
            mock_exists.return_value = True
            with patch('google.cloud.bigquery.Client.from_service_account_json') as mock_from_json:
                DBManager()
                mock_from_json.assert_called_once()
            mock_client.assert_not_called()

        # Scenario 3: None of the previous conditions are met
        mock_exists.return_value = False
        DBManager()
        mock_client.assert_called_once()
        
    @patch('google.cloud.bigquery.Client.query')
    def test_get_max_id_date(self, mock_query):
        mock_job = MagicMock()
        mock_job.result.return_value.to_dataframe.return_value = pd.DataFrame({'idDate': [100]})
        mock_query.return_value = mock_job

        result = self.db_manager.get_max_id_date()
        self.assertEqual(result, 100)

        # Test when table is empty
        mock_job.result.return_value.to_dataframe.return_value = pd.DataFrame({'idDate': [pd.NA]})
        result = self.db_manager.get_max_id_date()
        self.assertEqual(result, 0)

    @patch('google.cloud.bigquery.Client.query')
    def test_get_max_id_price(self, mock_query):
        mock_job = MagicMock()
        mock_job.result.return_value.to_dataframe.return_value = pd.DataFrame({'idPrix': [200]})
        mock_query.return_value = mock_job

        result = self.db_manager.get_max_id_price()
        self.assertEqual(result, 200)

        # Test when table is empty
        mock_job.result.return_value.to_dataframe.return_value = pd.DataFrame({'idPrix': [pd.NA]})
        result = self.db_manager.get_max_id_price()
        self.assertEqual(result, 0)

    @patch('google.cloud.bigquery.Client.query')
    def test_get_id_fuel(self, mock_query):
        mock_job = MagicMock()
        mock_job.result.return_value.to_dataframe.return_value = pd.DataFrame({'idCarburant': [5]})
        mock_query.return_value = mock_job

        result = self.db_manager.get_id_fuel("Diesel")
        self.assertEqual(result, 5)

        # Test when fuel is not found
        mock_job.result.return_value.to_dataframe.return_value = pd.DataFrame()
        result = self.db_manager.get_id_fuel("Unknown Fuel")
        self.assertEqual(result, 0)

    @patch('google.cloud.bigquery.Client.query')
    def test_get_all_stations(self, mock_query):
        mock_job = MagicMock()
        mock_df = pd.DataFrame({'station_id': [1, 2], 'name': ['Station A', 'Station B']})
        mock_job.result.return_value.to_dataframe.return_value = mock_df
        mock_query.return_value = mock_job

        result = self.db_manager.get_all_stations()
        pd.testing.assert_frame_equal(result, mock_df)

    @patch('google.cloud.bigquery.Client.get_table')
    @patch('google.cloud.bigquery.Client.insert_rows')
    def test_insert_list(self, mock_insert_rows, mock_get_table):
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table
        mock_insert_rows.return_value = []

        list_to_insert = [{'col1': 'val1'}, {'col1': 'val2'}]
        self.db_manager.insert_list(list_to_insert, 'project.dataset.table')

        mock_get_table.assert_called_once_with('project.dataset.table')
        mock_insert_rows.assert_called_once_with(table=mock_table, rows=list_to_insert)

        # Test error case
        mock_insert_rows.return_value = ['Error']
        with patch('builtins.print') as mock_print:
            self.db_manager.insert_list(list_to_insert, 'project.dataset.table')
            mock_print.assert_called_once_with("Encountered errors while inserting row: ['Error']")


if __name__ == '__main__':
    unittest.main()
