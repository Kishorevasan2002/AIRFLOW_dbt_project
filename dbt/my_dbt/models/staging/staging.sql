{{ config(
materialized='table',
unique_key='id'
)}}
with source as (
select *
from {{ source('dev', 'raw_weather_data')}}
)
select
id,
city,
temperature,
weather_descriptions,
wind_speed,
time as weather_time_local,
(inserted_at + (utc_offset || 'hours')::interval) as inserted_at_local
from source
