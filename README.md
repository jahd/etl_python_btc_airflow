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
Initial dataset


we created a DAG that runs the python scrypt every month and load the result into an sqlite SQL database
<img width="702" alt="Capture d’écran 2023-01-26 à 21 30 30" src="https://user-images.githubusercontent.com/45184003/214944095-6665de71-0f90-4c27-afda-d6d67e0dfaf0.png">

Result loaded into the SQL database

<img width="529" alt="Capture d’écran 2023-01-26 à 21 29 04" src="https://user-images.githubusercontent.com/45184003/214944106-008e96f9-e07c-4e84-b06e-777e7cd7530a.png">
