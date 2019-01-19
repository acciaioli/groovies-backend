import os
import logging
import time
import psycopg2


TIME_OUT = 30  # seconds
SLEEP_INTERVAL = 2  # seconds

PG_READY = "Postgres is ready!"
PG_NOT_READY = "Postgres isn't ready. Trying again in {} seconds...".format(SLEEP_INTERVAL)
PG_NEVER_READY = "Failed to connect to Postgres within {} seconds.".format(TIME_OUT)

DB_CONFIG = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB'),
}

start_time = time.time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def pg_is_ready(user, password, host, port, dbname):
    while time.time() - start_time < TIME_OUT:
        try:
            conn = psycopg2.connect(**vars())
            logger.info(PG_READY)
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(PG_NOT_READY)
            time.sleep(SLEEP_INTERVAL)

    logger.error(PG_NEVER_READY)
    return False


pg_is_ready(**DB_CONFIG)
