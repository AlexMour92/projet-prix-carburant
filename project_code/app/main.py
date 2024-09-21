import sys
sys.path.append("..")

from api_manager.api_manager import get_data_as_dataframe
from db_manager.Updater import Updater
from constants.constants import COLUMNS_TO_USE, IDF_REGION_CODE


def main() -> int:
    df = get_data_as_dataframe()  # Retrieve data from the government's API

    # We only keep data that will be inserted in database.
    df = df[df['code_region'] == IDF_REGION_CODE]  # For this project, we keep only the stations that are located in IDF
    df = df[COLUMNS_TO_USE]

    # Update database with new data.
    updater = Updater(df)
    updater.update_database()

    return 0


if __name__ == '__main__':
    main()
