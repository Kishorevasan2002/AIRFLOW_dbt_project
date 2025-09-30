-- Create the database for Airflow and set its owner
CREATE DATABASE airflow_db OWNER airflow_user;

-- Create the user for Superset
CREATE USER superset WITH PASSWORD 'superset';

-- Create the database for Superset's metadata and set its owner
CREATE DATABASE superset OWNER superset;