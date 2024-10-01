import logging


def setup_logging():
    # base config
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.getLogger('api_manager').setLevel(logging.INFO)
    logging.getLogger('db_manager').setLevel(logging.INFO)
