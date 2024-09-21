import pandas as pd
import unittest
from unittest.mock import patch, Mock

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project_code.app.constants.constants import API_URL
from project_code.app.api_manager.api_manager import get_data_as_dataframe, retrieve_data


class TestRetrieveData(unittest.TestCase):
    @patch("project_code.app.api_manager.api_manager.get")
    def test_retrieves_data_successfully(self, mock_get):
        expected_response_text = '{"data": "success"}'

        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = expected_response_text

        response = retrieve_data()

        mock_get.assert_called_once_with(API_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, expected_response_text)

    @patch("project_code.app.api_manager.api_manager.get")
    def test_raises_exception_for_wrong_http_code(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 404

        with self.assertRaises(Exception):
            retrieve_data()


class TestGetDataAsDataframe(unittest.TestCase):

    @patch('project_code.app.api_manager.api_manager.retrieve_data')
    @patch('project_code.app.api_manager.api_manager.write_temp_csv')
    @patch('project_code.app.api_manager.api_manager.convert_csv_to_dataframe')
    @patch('project_code.app.api_manager.api_manager.delete_temp_csv')
    def test_get_data_as_dataframe_success(self, mock_delete, mock_convert, mock_write, mock_retrieve_data):
        mock_response = Mock()
        mock_response.text = 'Sample response text'
        mock_retrieve_data.return_value = mock_response

        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_convert.return_value = mock_df

        result = get_data_as_dataframe()

        mock_retrieve_data.assert_called_once()
        mock_write.assert_called_once_with(mock_response)
        mock_convert.assert_called_once()
        self.assertEqual(mock_delete.call_count, 2)
        pd.testing.assert_frame_equal(result, mock_df)

    @patch('project_code.app.api_manager.api_manager.retrieve_data')
    @patch('project_code.app.api_manager.api_manager.delete_temp_csv')
    def test_get_data_as_dataframe_exception(self, mock_delete, mock_retrieve_data):
        mock_retrieve_data.side_effect = ValueError

        result = get_data_as_dataframe()

        mock_retrieve_data.assert_called_once()
        mock_delete.assert_not_called()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
