import sqlalchemy
import pandas as pd 
import sqlite3
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
from dotenv import main

main.load_dotenv()
os.makedirs("working_dir", exist_ok = True)

def getwhatweneed(df_month):    
    len_positif = len(df_month.query('perf > 0'))
    len_dataframe = len(df_month)
    len_negatif = len_dataframe - len_positif
    percentage_positif = (round(len_positif/len_dataframe,4) * 100)
    perf_average = round(df_month['perf'].mean(),2)
    result_list = []
    result_list.extend([len_positif, len_negatif, percentage_positif, perf_average])
    return result_list


def run_btc_etl():
    os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
    os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')
    os.environ["no_proxy"] = os.getenv('no_proxy_KEY')

    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('pavelbiz/monthly-btc-rate-from-2014-to-present', path="working_dir")

    with zipfile.ZipFile('./working_dir/monthly-btc-rate-from-2014-to-present.zip', 'r') as zip_ref:
        zip_ref.extractall("./working_dir/")
    df = pd.read_csv("./working_dir/BTC-USD.csv")
    df["perf"] = round(((df["Close"] - df["Open"]) / df["Open"]) * 100, 2)
    df['Date'] = pd.to_datetime(df['Date'])
    month_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
                  "november", "december"]
    df_by_month = pd.DataFrame(month_list, columns=["month"])

    columns_add = ["positif", "negatif", "percentage_positif", "perf_average"]

    for newcol in columns_add:
        df_by_month[newcol] = None

    month_list_enrich = []
    for i in month_list:
        i = df['Date'].map(lambda x: x.month) == month_list.index(i) + 1
        month_list_enrich.append(i)

    for count, i in enumerate(month_list_enrich):
        df_month = df[month_list_enrich[count]]
        result_list = getwhatweneed(df_month)
        for count_columns, i in enumerate(columns_add):
            df_by_month.at[count, i] = result_list[count_columns]

    final_df = df_by_month.sort_values('percentage_positif', ascending=False)
    final_df

    print(
        f'The most profitable month of the year is {final_df.iloc[0][0]} by being {final_df.iloc[0][1]} times profitable and {final_df.iloc[0][2]} times loss-making')
    print("here is the final table :")
    print(final_df.to_string(index=False))

    DATABASE_LOCATION="sqlite:///working_dir/btc_db.sqlite"
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('working_dir/btc_db.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS init_table(
        month VARCHAR(200),
        positif INT,
        negatif INT,
        percentage_positif FLOAT,
        perf_average FLOAT
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        final_df.to_sql("final_df_table", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")