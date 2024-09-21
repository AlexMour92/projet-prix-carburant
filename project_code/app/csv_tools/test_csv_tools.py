import unittest
from unittest.mock import patch, mock_open, Mock

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project_code.app.constants.constants import CSV_FILE_PATH
from project_code.app.csv_tools.csv_tools import write_temp_csv, delete_temp_csv

SAMPLE_CSV = 'header1,header2\nvalue1,value2'

class TestWriteTempCSV(unittest.TestCase):
    def test_writes_response_content_to_csv(self):
        response = Mock()
        response.text = 'header1,header2\nvalue1,value2'

        with patch('builtins.open', new_callable=mock_open) as mock_file:
            write_temp_csv(response)

            mock_file.assert_called_once_with(CSV_FILE_PATH, 'w', encoding='utf-8')
            mock_file.return_value.__enter__.return_value.write.assert_called_once_with(response.text)

    def test_handles_print_error(self):
        response = Mock()
        response.text = 'header1,header2\nvalue1,value2'
        error_message = 'Message: File not found'

        with patch('builtins.open', side_effect=OSError('File not found')) as mock_file:
            with patch('builtins.print') as mock_print:
                write_temp_csv(response)

                mock_print.assert_called_once_with(error_message)


if __name__ == "__main__":
    unittest.main()
