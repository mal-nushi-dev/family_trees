from scripts.streamlit_map import CreateMap
import streamlit as st

st.title("Maps")

st.header("Birth Places")
birth_search = st.text_input("Search for a person", key='birth_search')
with CreateMap(database='family_trees.db',
               column='BIRTH_PLACE',
               name=birth_search) as birth_map:
    birth_map.__run__()

st.header("Current Home Towns")
address_search = st.text_input("Search for a person", key='address_search')
with CreateMap(database='family_trees.db',
               column='ADDRESS',
               name=address_search) as address_map:
    address_map.__run__()
