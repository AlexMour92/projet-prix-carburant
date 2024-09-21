from os import remove
from requests import Response

from constants.constants import CSV_FILE_PATH


def write_temp_csv(response: Response) -> None:
    """
    Writes the content of a requests Response object to a temporary CSV file.

    :param response: requests.Response: The HTTP response object containing the CSV data.
    """
    try:
        with open(CSV_FILE_PATH, 'w', encoding='utf-8') as writer:
            writer.write(response.text)
    except OSError as e:
        print(f'Message: {str(e)}')


def delete_temp_csv() -> None:
    """
    Deletes the temporary CSV file.

    Attempts to delete the CSV file specified by CSV_FILE_PATH.
    If the file does not exist or there is an error during deletion,
    an error message is printed.
    """
    try:
        remove(CSV_FILE_PATH)
    except OSError as e:
        print(f"Message: {str(e)}")
