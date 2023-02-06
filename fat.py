import mysql.connector
import streamlit as st
import pandas as pd
from mysql.connector import errorcode

# get db connection
try:
    cnx = mysql.connector.connect(**st.secrets['mysql'])
except mysql.connector.Error as err:
    print(" error occurred!")

datdata=pd.read_csv(r"C:\Users\faho_\PycharmProjects\web-scrapping\parasconti_final.csv", delimiter='\t', index_col = [0])
datdata=datdata.fillna(0)

for i,row in datdata.iterrows():

    # # insert operation
    try:
        # cursor
        cnxCursor = cnx.cursor()
        # sql query
        query="INSERT INTO parasconti (product_Id,product_Nom, product_Marque, product_Categorie,product_Prix,product_Description,product_Barcode,product_Image,product_Link) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)"
        # values
        values = (i+1,row.product_Nom, row.product_Marque, row.product_Categorie,row.product_Prix,row.product_Description,row.product_Barcode,row.product_Image,row.product_Link)
        # insert data into the table
        cnxCursor.execute(query, values)
        # commit
        cnx.commit()
        # total number of rows inserted
        print("Total rows inserted: %d" % (i+1))

    except mysql.connector.Error as err:
        print("Error: %s" % err.message)
    finally:
        # close cursor
        cnxCursor.close()
        # close connection
print("final")