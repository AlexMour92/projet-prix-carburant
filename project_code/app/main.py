import logging
import sys

sys.path.append("..")

from api_manager.api_manager import get_data_as_dataframe
from db_manager.Updater import Updater
from constants.constants import COLUMNS_TO_USE, IDF_REGION_CODE
from logging_config import setup_logging

logger = logging.getLogger(__name__)


def main() -> int:
    logger.info("Starting ETL process")

    logger.debug("Retrieving data from government API")
    df = get_data_as_dataframe()  # Retrieve data from the government's API

    logger.debug(f"Filtering data")
    # We only keep data that will be inserted in database.
    df = df[df['code_region'] == IDF_REGION_CODE]  # For this project, we keep only the stations that are located in IDF
    df = df[COLUMNS_TO_USE]
    logger.info(f"Processed DataFrame shape: {df.shape}")

    logger.info("Initializing database update")
    # Update database with new data.
    updater = Updater(df)
    updater.update_database()

    logger.info("ETL process completed successfully")
    return 0


if __name__ == '__main__':
    setup_logging()
    try:
        main()
    except Exception as e:
        logger.exception(f"An error occurred during the ETL process: {str(e)}")
        sys.exit(1)

