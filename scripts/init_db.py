import argparse
import logging

from sqlalchemy.util import asyncio

from app.adapters.db.provision import create_database

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="database name")
    args = parser.parse_args()

    db_name = args.name or "app"
    logger.info(f"Creating database: {db_name}")
    asyncio.get_event_loop().run_until_complete(create_database(db_name))
