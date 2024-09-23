import unittest
from unittest.mock import Mock, patch
import pandas as pd
from datetime import datetime

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from project_code.app.db_manager.Updater import Updater


class TestUpdater(unittest.TestCase):

    def setUp(self):
        # Create a test DataFrame
        self.test_df = pd.DataFrame({
            'id': ['1', '2'],
            'latitude': ['48.8566', '45.7640'],
            'longitude': ['2.3522', '4.8357'],
            'cp': ['75001', '69001'],
            'ville': ['Paris', 'Lyon'],
            'gazole_prix': ['1.5', '1.6'],
            'gplc_prix': ['0.8', '0.9'],
            'sp95_prix': ['1.7', '1.8'],
            'sp98_prix': ['1.8', '1.9'],
            'e10_prix': ['1.6', '1.7'],
            'e85_prix': ['0.7', '0.8']
        })

        # Create a mock for DBManager
        self.mock_db = Mock()
        self.mock_db.get_id_fuel.side_effect = [1, 2, 3, 4, 5, 6]

        # Create the Updater object
        self.updater = Updater(self.test_df)
        self.updater.mydb = self.mock_db

    def test_init(self):
        self.assertIsInstance(self.updater.df, pd.DataFrame)
        self.assertEqual(self.updater.gazole_id, 1)
        self.assertEqual(self.updater.gplc_id, 2)
        self.assertEqual(self.updater.sp95_id, 3)
        self.assertEqual(self.updater.sp98_id, 4)
        self.assertEqual(self.updater.e10_id, 5)
        self.assertEqual(self.updater.e85_id, 6)

    def test_get_new_price(self):
        result = self.updater.get_new_price(1, 1, 1.5, 1, 1)
        expected = {'idPrix': 1, 'idStation': 1, 'idDate': 1, 'idCarburant': 1, 'prix': 1.5}
        self.assertEqual(result, expected)

        result = self.updater.get_new_price(1, 1, float('nan'), 1, 1)
        expected = {'idPrix': 1, 'idStation': 1, 'idDate': 1, 'idCarburant': 1, 'prix': None}
        self.assertEqual(result, expected)

    def test_get_datetime_to_insert(self):
        self.mock_db.get_max_id_date.return_value = 0
        result, id_date = self.updater.get_datetime_to_insert()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['idDate'], 1)
        self.assertIsInstance(result[0]['heureDate'], str)
        self.assertEqual(id_date, 1)

    def test_get_prices_to_insert(self):
        self.mock_db.get_max_id_price.return_value = 0
        result = self.updater.get_prices_to_insert(1)

        self.assertEqual(len(result), 12)  # 2 stations * 6 fuel types
        self.assertEqual(result[0]['idPrix'], 1)
        self.assertEqual(result[0]['idStation'], 1)
        self.assertEqual(result[0]['idDate'], 1)
        self.assertEqual(result[0]['idCarburant'], 1)
        self.assertEqual(result[0]['prix'], 1.5)

    def test_get_stations_to_insert(self):
        # Update this test to reflect the expected behavior
        stations_in_db = pd.DataFrame({'idStation': [1]})
        self.mock_db.get_all_stations.return_value = stations_in_db

        result = self.updater.get_stations_to_insert()

        expected_result = [{'idStation': 2, 'latitude': 45.7640, 'longitude': 4.8357, 'cp': 69001, 'ville': 'Lyon'}]
        self.assertEqual(result, expected_result)

    def test_get_list_fuels(self):
        row = self.test_df.iloc[0]
        result = self.updater.get_list_fuels(row)

        expected = [
            (1.5, 1), (0.8, 2), (1.7, 3),
            (1.8, 4), (1.6, 5), (0.7, 6)
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
