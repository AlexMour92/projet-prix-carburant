import logging
from os import remove
from requests import Response

from constants.constants import CSV_FILE_PATH

logger = logging.getLogger(__name__)


def write_temp_csv(response: Response) -> None:
    """
    Writes the content of a requests Response object to a temporary CSV file.

    :param response: requests.Response: The HTTP response object containing the CSV data.
    """
    logger.info(f"Writing temporary CSV file to {CSV_FILE_PATH}")
    try:
        with open(CSV_FILE_PATH, 'w', encoding='utf-8') as writer:
            writer.write(response.text)
        logger.debug(f"Successfully wrote {len(response.text)} characters to temporary CSV file")
    except OSError as e:
        logger.error(f"Failed to write temporary CSV file: {str(e)}")
        print(f'Message: {str(e)}')


def delete_temp_csv() -> None:
    """
    Deletes the temporary CSV file.

    Attempts to delete the CSV file specified by CSV_FILE_PATH.
    If the file does not exist or there is an error during deletion,
    an error message is printed.
    """
    logger.info(f"Attempting to delete temporary CSV file: {CSV_FILE_PATH}")
    try:
        remove(CSV_FILE_PATH)
        logger.debug("Temporary CSV file successfully deleted")
    except OSError as e:
        logger.error(f"Failed to delete temporary CSV file: {str(e)}")
        print(f"Message: {str(e)}")
