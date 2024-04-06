from scripts.streamlit_map import CreateMap
import streamlit as st

st.title("Maps")

st.header("Birth Places")
with CreateMap(database='family_trees.db',
               column='BIRTH_PLACE') as birth_map:
    birth_map.__run__()

st.header("Current Home Towns")
with CreateMap(database='family_trees.db',
               column='ADDRESS') as address_map:
    address_map.__run__()
