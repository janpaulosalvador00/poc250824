python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install black==23.12.1
pip install ruff==0.1.9
pip install -r providers.txt
pip install -r requirements.txt
pip install -r dbt/requirements.txt