from pathlib import Path
from enum import Enum

# URL to the API of the government.
API_URL = ('https://data.economie.gouv.fr/api/explore/v2.1/catalog/' +
           'datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/csv')

# Path to the project_code directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Path to a temporary CSV file.
CSV_FILE_PATH = PROJECT_ROOT / "app/temp_csv/carburants.csv"

# Path to the JSON of the service account key for Google BigQuery.
SERVICE_KEY_PATH = PROJECT_ROOT / "app/prix-carburants-idf-c312398d0721.json"

# These variables store the fully qualified table IDs for the station,
# date, fuel, and price dimensions, respectively, within the 'carbu_db'
# dataset in the 'prix-carburants-idf' project. These IDs will be used
# to construct SQL queries to retrieve data from the corresponding tables in BigQuery.
PROJECT_ID = "prix-carburants-idf"
DATASET_ID = "carbu_db"
STATION_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.dim_station"
DATE_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.dim_date"
FUEL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.dim_carburant"
# PRICE_TEMP_TABLE_ID is the ID of the table used to store temporary data.
PRICE_TEMP_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.fact_prix"
# PRICE_TEMP_TABLE_ID is the ID of the table where prices are stored permanently.
PRICE_PROD_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.fact_prix_prod"

HEADERS = [
    'id', 'latitude', 'longitude', 'cp', 'pop', 'adresse', 'ville',
    'services', 'prix', 'rupture', 'horaires', 'geom', 'gazole_maj',
    'gazole_prix', 'sp95_maj', 'sp95_prix', 'e85_maj', 'e85_prix',
    'gplc_maj', 'gplc_prix', 'e10_maj', 'e10_prix', 'sp98_maj', 'sp98_prix',
    'e10_rupture_debut', 'e10_rupture_type', 'sp98_rupture_debut',
    'sp98_rupture_type', 'sp95_rupture_debut', 'sp95_rupture_type',
    'e85_rupture_debut', 'e85_rupture_type', 'gplc_rupture_debut',
    'gplc_rupture_type', 'gazole_rupture_debut', 'gazole_rupture_type',
    'carburants_disponibles', 'carburants_indisponibles',
    'carburants_rupture_temporaire', 'carburants_rupture_definitive',
    'horaires_automate_24_24', 'services_service', 'departement',
    'code_departement', 'region', 'code_region', 'horaires_jour'
]

DTYPES = {
    'id': 'int',
    'latitude': 'float64',
    'longitude': 'float64',
    'cp': 'int',
    'pop': 'str',
    'adresse': 'str',
    'ville': 'str',
    'services': 'str',
    'prix': 'str',
    'rupture': 'str',
    'horaires': 'str',
    'geom': 'str',
    'gazole_maj': 'str',
    'gazole_prix': 'float64',
    'sp95_maj': 'str',
    'sp95_prix': 'float64',
    'e85_maj': 'str',
    'e85_prix': 'float64',
    'gplc_maj': 'str',
    'gplc_prix': 'float64',
    'e10_maj': 'str',
    'e10_prix': 'float64',
    'sp98_maj': 'str',
    'sp98_prix': 'float64',
    'e10_rupture_debut': 'str',
    'e10_rupture_type': 'str',
    'sp98_rupture_debut': 'str',
    'sp98_rupture_type': 'str',
    'sp95_rupture_debut': 'str',
    'sp95_rupture_type': 'str',
    'e85_rupture_debut': 'str',
    'e85_rupture_type': 'str',
    'gplc_rupture_debut': 'str',
    'gplc_rupture_type': 'str',
    'gazole_rupture_debut': 'str',
    'gazole_rupture_type': 'str',
    'carburants_disponibles': 'str',
    'carburants_indisponibles': 'str',
    'carburants_rupture_temporaire': 'str',
    'carburants_rupture_definitive': 'str',
    'horaires_automate_24_24': 'str',
    'services_service': 'str',
    'departement': 'str',
    'code_departement': 'str',
    'region': 'str',
    'code_region': 'str',
    'horaires_jour': 'str'
}

# Columns used in the database
COLUMNS_TO_USE = [
    'id', 'latitude', 'longitude', 'cp',
    'ville', 'adresse', 'code_departement', 'gazole_prix', 'sp95_prix', 'e85_prix',
    'gplc_prix', 'e10_prix', 'sp98_prix'
]

# Region code for Île-de-France
IDF_REGION_CODE = '11'
