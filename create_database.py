import sqlite3
import pandas as pd


def create_db(db_file, csv_file):
    conn = sqlite3.connect(db_file)
    df = pd.read_csv(csv_file)
    df.to_sql('table_name', conn, if_exists='replace', index=False)
    conn.close()


if __name__ == '__main__':
    create_db(db_file='data/sqlite3/database.db',
              csv_file='data/csv/Nushi-Genealogy-25-Mar-2024-140326324.csv'
              )
