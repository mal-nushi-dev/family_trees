import streamlit as st
from scripts.streamlit_filter_dataframe import filtered_df
import sqlite3
import pandas as pd


# Set page configurations
st.set_page_config(
    layout="centered"
)


# Load data from the database
def create_dataframe(database_path, table_name):
    conn = sqlite3.connect(database_path)
    query = f"SELECT * FROM {table_name};"
    database_df = pd.read_sql_query(sql=query, con=conn)
    df_filter = filtered_df(database_df)
    database = df_filter.filter_dataframe()
    return database


# Print page title
st.title("DATABASE")
st.write("""Welcome to the database page! Here, you can view the database and
         use our filtering options to explore the data.
         Take a look at the table below to get started.""")

# Create a DatabasePage object and run it
database_page = create_dataframe(database_path='family_trees.db',
                                 table_name="NUSHI")
st.dataframe(database_page)
