FROM quay.io/astronomer/astro-runtime:9.7.0

WORKDIR "/usr/local/airflow"
COPY dbt/dbt-requirements.txt ./
RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir -r dbt-requirements.txt && deactivate
