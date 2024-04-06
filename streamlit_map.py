import sqlite3
import streamlit as st
import pandas as pd
import numpy as np

conn = sqlite3.connect('family_trees.db')
query = '''
    SELECT
        FULL_NAME,
        BIRTH_PLACE_LATITUDE,
        BIRTH_PLACE_LONGITUDE
    FROM NUSHI
    WHERE BIRTH_PLACE_LATITUDE IS NOT NULL
    AND BIRTH_PLACE_LONGITUDE IS NOT NULL;
'''
birthplace_df = pd.read_sql_query(sql=query, con=conn)
print(birthplace_df)

# Add random noise to latitude and longitude
noise_scale = 0.001  # Adjust this value as needed
birthplace_df['BIRTH_PLACE_LATITUDE'] += np.random.normal(0, noise_scale, size=len(birthplace_df))
birthplace_df['BIRTH_PLACE_LONGITUDE'] += np.random.normal(0, noise_scale, size=len(birthplace_df))

st.map(data=birthplace_df,
       latitude='BIRTH_PLACE_LATITUDE',
       longitude='BIRTH_PLACE_LONGITUDE',
       size=10)
