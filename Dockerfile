FROM quay.io/astronomer/astro-runtime:11.9.0

# Defina o diretório de trabalho
WORKDIR /app

# Crie e defina permissões para diretórios necessários
RUN mkdir -p /app/.dbt /app/dbt/logs /app/logs && \
    chmod -R 777 /app/.dbt /app/dbt /app/logs

# Copie o projeto dbt e as dependências
COPY dbt /app/dbt    
COPY dbt/requirements.txt /app/dbt-requirements.txt
COPY dbt/profiles.yml /app/.dbt/profiles.yml
COPY dbt/dbt_project.yml /app/dbt_project.yml

# Instale dependências do DBT
RUN python -m virtualenv /app/dbt_venv && \
    /app/dbt_venv/bin/pip install --no-cache-dir -r /app/dbt-requirements.txt

# Instale dependências restantes
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Defina as variáveis de ambiente para DBT
ENV DBT_PROJECT_DIR=/app
ENV DBT_PROFILES_DIR=/app/.dbt

# Atualize e instale o Git
USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# Clone o repositório GitHub
RUN git clone https://github.com/janpaulosalvador00/poc250824.git /app/poc250824

# Geração da documentação DBT
RUN dbt docs generate --project-dir /app/dbt

# Mova os arquivos gerados para o diretório de docs
RUN mkdir -p /app/dbt_docs_dir && \
    cp /app/dbt/target/manifest.json /app/dbt_docs_dir/manifest.json && \
    cp /app/dbt/target/catalog.json /app/dbt_docs_dir/catalog.json && \
    cp /app/dbt/target/index.html /app/dbt_docs_dir/index.html

# Comando padrão para o container
CMD ["dbt", "debug"]
