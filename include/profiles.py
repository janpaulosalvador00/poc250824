from cosmos import ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

DBT_CONN_PROPERTIES = {
    "name": "dbt_dev",
    "target": "dev",
    "conn_id": "dbt-astro-postgres",
    "schema": "dbt",
}

dbt_dev_config = ProfileConfig(
    profile_name=DBT_CONN_PROPERTIES["name"],
    target_name=DBT_CONN_PROPERTIES["target"],
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=DBT_CONN_PROPERTIES["conn_id"],
        profile_args={"schema": DBT_CONN_PROPERTIES["schema"]},
    ),
)
