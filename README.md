python -m venv mon_ia_env

# Install dependencies

source mon_ia_env/Scripts/activate
pip install requirements.txt

# Run the api

uvicorn api:app --reload

#
