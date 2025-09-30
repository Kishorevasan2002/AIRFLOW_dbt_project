# docker/superset_config.py
import os

# Read database connection info from environment variables
DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

# Construct the SQLAlchemy URI for Superset's metadata database
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

# Read Redis connection info from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# Configure caching to use Redis
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': 1,
}

# Set a mandatory SECRET_KEY for Flask
SECRET_KEY = os.getenv("SECRET_KEY")

# Allow file uploads for CSV/Excel
CSV_EXTENSIONS = {"csv"}
EXCEL_EXTENSIONS = {"xls", "xlsx"}
ALLOWED_EXTENSIONS = CSV_EXTENSIONS.union(EXCEL_EXTENSIONS)