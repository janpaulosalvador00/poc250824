from cosmos import ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

CONNECTION_ID = {"name": "postgres_db", "conn_id": "dev-postgres"}

postgres_config = ProfileConfig(
    profile_name=CONNECTION_ID["name"],
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=CONNECTION_ID["conn_id"],
        profile_args={"schema": "dbt"},
    ),
)
