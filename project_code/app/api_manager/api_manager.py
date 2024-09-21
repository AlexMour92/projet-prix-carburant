import pandas as pd

from requests import get, Response
from constants.constants import API_URL, CSV_FILE_PATH, HEADERS, DTYPES
from csv_tools.csv_tools import write_temp_csv, delete_temp_csv


def get_data_as_dataframe() -> pd.DataFrame:
    """
    Retrieves data from a specified API and returns it as a Pandas DataFrame.

    This function first fetches data from the API using the `retrieve_datas` function.
    If the API response is successful, it writes the data to a temporary CSV file,
    converts the CSV to a DataFrame, and then deletes the temporary file.
    :return: pd.DataFrame: A Pandas DataFrame containing the extracted data.
    """
    response = 0

    try:
        response = retrieve_data()
        delete_temp_csv()  # # Ensure temporary CSV file is deleted before writing
        write_temp_csv(response)
        df = convert_csv_to_dataframe()
        delete_temp_csv()  # Always delete the temporary file after use
        return df
    except ValueError as e:
        print(f'Message: {str(e)}')


def retrieve_data() -> Response:
    """
    Retrieves data from the specified API URL.

    Sends a GET request to the API URL and handles potential exceptions.

    :return: requests.Response: The HTTP response object containing the retrieved data.
    """
    response = get(API_URL)
    if response.status_code != 200:
        raise ValueError("Received code isn't 200.")
    return response


def convert_csv_to_dataframe() -> pd.DataFrame:
    """
    Converts a temporary CSV file to a Pandas DataFrame.

    Reads the CSV file specified by CSV_FILE_PATH and converts it to a DataFrame.

    :return: pd.DataFrame: A Pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(
        CSV_FILE_PATH,
        delimiter=';',
        names=HEADERS,
        dtype=DTYPES,
        skiprows=1,
        encoding='utf-8'
    )
