FROM quay.io/astronomer/astro-runtime:9.7.0

WORKDIR "/usr/local/airflow"

RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY providers.txt ./
RUN pip install --no-cache-dir -r providers.txt

COPY dbt/requirements.txt ./dbt-requirements.txt
RUN pip install --no-cache-dir -r dbt-requirements.txt
