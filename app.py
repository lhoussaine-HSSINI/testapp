# streamlit_app.py
import pandas as pd
import streamlit as st
import mysql.connector


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets['mysql'])


conn = init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows_1 = run_query("SELECT * from parasconti;")
rows = run_query("SELECT * from cotepara;")
df=pd.DataFrame(rows)
df_1=pd.DataFrame(rows)
# rows = run_query("SELECT * from mytable;")
st.dataframe(df)
st.table(df)
st.dataframe(df_1)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .viewerBadge_link__1S137 {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
