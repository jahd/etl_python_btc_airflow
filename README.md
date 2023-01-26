# My project
This project is an ETL : scheduling a python scrypt with airflow 
We will be using a btc dataset that gives us informations about bitcoin price performance over months
This BTC csv is hosted on Kaggle : https://www.kaggle.com/datasets/pavelbiz/monthly-btc-rate-from-2014-to-present
You need to have api credentials to pull the data

# etl_python_btc_airflow

An ETL with a python script analyzing BTC performance over months, using Airflow for orchestration

# environment set-up
python3.7 -m virtualenv airflow-venv
source airflow-venv/bin/activate
export AIRFLOW_HOME=~/airflow     
python setup.py install 

# .env
Create a .env with :
    # create credentials for kaggle api and use them as variable
    -KAGGLE_USERNAME="kaggle name"
    -KAGGLE_KEY="kaggle key"

    # if SIGTERM signal on airflow :
    -no_proxy="*"

# airflow 
airflow webserver -p 8080
airflow scheduler


# dags
we created a DAG that run the python scrypt every month and load the result into an sqlite SQL database