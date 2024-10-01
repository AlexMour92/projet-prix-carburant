import pandas as pd
import logging
from datetime import datetime

from db_manager.DBManager import DBManager
from constants.constants import PRICE_TEMP_TABLE_ID, STATION_TABLE_ID, DATE_TABLE_ID

logger = logging.getLogger(__name__)


class Updater:
    """
    This class is responsible for updating a database with new fuel price data.

    It takes a pandas DataFrame containing fuel price information and interacts with
    a database manager (DBManager) to insert new entries.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initializes the Updater object.

        :param df: pd.DataFrame: A pandas DataFrame containing fuel price data.
        This DataFrame is expected to have columns for station ID, latitude, longitude,
        postal code, city, and fuel prices for different types (e.g., gazole, gplc, sp95, etc.).
        """
        logger.info("Initializing Updater")
        self.df = df.copy()  # Create a copy of the DataFrame to avoid modifying the original
        self.mydb = DBManager()  # Initialize the database manager object

        logger.debug("Retrieving fuel IDs from database")
        # Get fuel IDs from database
        self.gazole_id = int(self.mydb.get_id_fuel('gazole'))
        self.gplc_id = int(self.mydb.get_id_fuel('gplc'))
        self.sp95_id = int(self.mydb.get_id_fuel('sp95'))
        self.sp98_id = int(self.mydb.get_id_fuel('sp98'))
        self.e10_id = int(self.mydb.get_id_fuel('e10'))
        self.e85_id = int(self.mydb.get_id_fuel('e85'))

        logger.info("Updater initialized successfully")

    def update_database(self):
        """
        Updates the database with the new data found in the DataFrame provided to the Updater.

        This method performs the following steps:
            1. Extracts data for Date, Stations (if not already present), and Prices.
            2. Inserts the extracted data into their respective tables in the database.
        """
        logger.info("Starting database update process")
        # Extract data for insertion
        datetime_to_insert, id_date = self.get_datetime_to_insert()
        stations_to_insert = self.get_stations_to_insert()
        prices_to_insert = self.get_prices_to_insert(id_date)

        # Insert data into database tables
        if stations_to_insert.__len__() != 0:
            logger.info(f"Inserting {len(stations_to_insert)} new stations")
            self.mydb.insert_list(stations_to_insert, STATION_TABLE_ID)
        else:
            logger.info("No new stations to insert")

        logger.info(f"Inserting new date entry: {datetime_to_insert[0]['heureDate']}")
        self.mydb.insert_list(datetime_to_insert, DATE_TABLE_ID)

        logger.info(f"Inserting {len(prices_to_insert)} new price entries")
        self.mydb.insert_list(prices_to_insert, PRICE_TEMP_TABLE_ID)

        logger.info("Database update completed successfully")

    @staticmethod
    def get_new_price(id_station: int, fuel_id: int,
                      fuel_price: float, next_id_price: int,
                      id_date: int) -> dict:
        """
        Creates a dictionary representing a new price entry in the database.

        This method handles potential missing fuel price values by setting them to None.
        :param id_station: int: ID of the station.
        :param fuel_id: int: ID of the fuel type.
        :param fuel_price: float: Price of the fuel.
        :param next_id_price: int: The next available ID for a price entry (obtained from the database).
        :param id_date: int: ID of the date associated with the price.
        :return: dict: A dictionary representing a new price entry.
        """
        id_price = next_id_price

        if pd.isna(fuel_price):
            fuel_price = None

        return {
            'idPrix': id_price,
            'idStation': id_station,
            'idDate': id_date,
            'idCarburant': fuel_id,
            'prix': fuel_price
        }

    def get_datetime_to_insert(self):
        """
        Extracts data for a new date entry based on the current datetime.

        Retrieves the current datetime, formats it, and retrieves the next available ID for the date entry.
        :return: tuple: A tuple containing the datetime data as a dictionary and the next available ID for
        the date entry.
        """
        logger.debug("Generating new datetime entry")
        next_id_date = self.mydb.get_max_id_date() + 1
        now_datetime = datetime.now().isoformat(' ', timespec='seconds')[:19]

        datetime_to_insert = [{'idDate': next_id_date,
                               'heureDate': now_datetime}]
        logger.debug(f"New datetime entry created: ID {next_id_date}, DateTime {now_datetime}")
        return datetime_to_insert, next_id_date

    def get_prices_to_insert(self, id_date: int) -> list:
        """
        Generates a list of price entries to be inserted into the database.

        Iterates through the DataFrame, extracts fuel prices for each station, and creates new price entries.

        :param id_date: int: ID of the date associated with the price entries.
        :return: list: A list of dictionaries representing new price entries.
        """
        logger.debug("Generating price entries for insertion")
        prices_to_insert = []
        next_id_price = self.mydb.get_max_id_price() + 1

        for index, row in self.df.iterrows():
            list_fuel = self.get_list_fuels(row)
            for fuel_price, fuel_id in list_fuel:
                new_price = self.get_new_price(int(row['id']), fuel_id, fuel_price, next_id_price, id_date)
                next_id_price += 1
                prices_to_insert.append(new_price)

        logger.debug(f"Generated {len(prices_to_insert)} price entries")
        return prices_to_insert

    def get_stations_to_insert(self) -> list:
        """
        Identifies stations that are not already present in the database and prepares data for insertion.

        Compares the stations in the DataFrame with those in the database and extracts stations that need to be
        inserted.
        :return: list: A list of dictionaries representing new station entries.
        """
        logger.debug("Identifying new stations for insertion")
        stations_to_insert = []
        stations_in_database = self.mydb.get_all_stations()

        for index, row in self.df.iterrows():
            if int(row['id']) not in stations_in_database.idStation.values:
                new_station = {
                    'idStation': int(row['id']),
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'cp': int(row['cp']),
                    'ville': str(row['ville']),
                    'adresse': str(row['adresse']),
                    'codeDepartement': int(row['code_departement'])
                    }
                stations_to_insert.append(new_station)

        logger.debug(f"Identified {len(stations_to_insert)} new stations for insertion")
        return stations_to_insert

    def get_list_fuels(self, row: pd.Series):
        """
        Extracts fuel prices and their corresponding IDs from a DataFrame row.

        :param: row: pd.Series: A row from the DataFrame containing fuel price data.
        :return: list: A list of tuples, where each tuple contains a fuel price and its corresponding ID.
        """
        return [(float(row['gazole_prix']), self.gazole_id),
                (float(row['gplc_prix']), self.gplc_id),
                (float(row['sp95_prix']), self.sp95_id),
                (float(row['sp98_prix']), self.sp98_id),
                (float(row['e10_prix']), self.e10_id),
                (float(row['e85_prix']), self.e85_id)]
