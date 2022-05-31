import argparse
import logging

from sqlalchemy.util import asyncio

from app.adapters.db.provision import delete_database

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db_name", help="database name")
    args = parser.parse_args()
    logger.info(f"dropping database: {args.db_name}")
    asyncio.get_event_loop().run_until_complete(delete_database(args.db_name))
