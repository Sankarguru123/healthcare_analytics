from sqlalchemy import create_engine
from config import *


def hc_get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_size=5,          # number of open connections
        max_overflow=10,      # extra connections allowed
        pool_timeout=30,      # seconds to wait
        pool_recycle=1800,    # recycle connections (30 min)
        echo=False            # True for SQL debug
    )
