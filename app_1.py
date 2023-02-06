import pandas as pd
import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
from PIL import Image
import requests
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt



st.set_page_config(page_title="compare")

@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets['mysql'])

conn = init_connection()
c = conn.cursor()
@st.experimental_singleton
@st.cache
def update_cotepara(id, nom, marque, cat, prix, desc, lien_img, link_pro):
    try:
        values = (id,nom, marque, cat,   prix,   desc,   lien_img, link_pro,id)
        c.execute("UPDATE cotepara SET product_Id =%s, product_Nom=%s, product_Marque=%s, product_Categorie=%s,"
                  "product_Prix=%s,product_Description=%s,product_Image=%s , product_Link=%s WHERE   product_Id =%s", values)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)

@st.experimental_singleton
@st.cache
def update_paraconti(id_pro_1, nom_1, marqe_1, Categorie_1, prix_1, discr_1, barcode_1, image_1, link_pro_1):
    try:
        values = (id_pro_1,nom_1, marqe_1, Categorie_1,   prix_1,   discr_1, barcode_1, image_1, link_pro_1,id_pro_1)
        c.execute("UPDATE parasconti SET product_Id =%s, product_Nom=%s, product_Marque=%s, product_Categorie=%s,"
                  "product_Prix=%s,product_Description=%s,product_Barcode=%s,product_Image=%s , product_Link=%s WHERE   product_Id =%s", values)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
@st.experimental_singleton
@st.cache
def add_cotepara(id,Nom_add ,Marque_add  ,list_Categorie_add ,Prix_add  ,Description_add ,Image_add ,Link_add):
    try:
        # cursor
        # values
        values = (id ,Nom_add ,Marque_add  ,list_Categorie_add ,Prix_add ,Description_add, Image_add, Link_add)
        # insert data into the table
        c.execute("INSERT INTO cotepara (product_Id,product_Nom, product_Marque, product_Categorie,product_Prix,product_Description,product_Image,product_Link) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)", values)
        # commit
        conn.commit()
        # data = c.fetchall()
        # return data
    except mysql.connector.Error as err:
        print(err)

@st.experimental_singleton
@st.cache
def add_parasconti(id,Nom_add ,Marque_add  ,list_Categorie_add ,Prix_add  ,Description_add ,Barcode_add ,Image_add ,Link_add):
    try:
        # cursor
        # values
        values = (id ,Nom_add ,Marque_add  ,list_Categorie_add ,Prix_add ,Description_add ,Barcode_add ,Image_add ,Link_add)
        # insert data into the table
        c.execute("INSERT INTO parasconti (product_Id,product_Nom, product_Marque, product_Categorie,product_Prix,product_Description,product_Barcode,product_Image,product_Link) VALUES (%s,%s, %s, %s, %s, %s,%s, %s, %s)", values)
        # commit
        conn.commit()
        # data = c.fetchall()
        # return data
    except mysql.connector.Error as err:
        print(err)
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

@st.experimental_singleton
@st.experimental_memo(ttl=600)
def run_query():
    # rows = run_query("SELECT * from cotepara;")
    c.execute("SELECT * from cotepara;")
    rows=c.fetchall()
    coll = ["product_Id", "product_Nom", "product_Marque", "product_Categorie", "product_Prix", "product_Description",
            "product_Image", "product_Link"]
    Cotepara = pd.DataFrame(rows, columns=coll, index=None)
    # rows_1 = run_query("SELECT * from parasconti;")
    c.execute("SELECT * from parasconti;")
    rows_1 = c.fetchall()
    coll_1 = ["product_Id", "product_Nom", "product_Marque", "product_Categorie", "product_Prix", "product_Description",
              "product_Barcode", "product_Image", "product_Link"]
    Parasconti = pd.DataFrame(rows_1, columns=coll_1)
    return Cotepara, Parasconti
@st.experimental_memo(ttl=600)
@st.cache
def view_all_cotepara():
	c.execute("SELECT * from cotepara")
	data = c.fetchall()
	return data


def change(aa):
    global Cotepara
    Cotepara = aa

def change_parasconti(aa):
    global Parasconti
    Parasconti = aa
def main():
    global Cotepara, Parasconti
    Cotepara, Parasconti = run_query()
    with st.sidebar:
        selected = option_menu(None, ["Home", 'Cotepara', 'Parasconti'], default_index=0)

    if selected=="Home":
        list_ta3_produit_li_mxtarkin_fihom=[]
        list_ta3_produit_li_mxtarkin_fihom_marque = []
        list_product_parasconti_marque = []
        list_product_cotepara_marque = []
        data_Cotepara_compare = Cotepara.reset_index()
        data_Parasconti_compare = Parasconti.reset_index()



        for index, row in data_Cotepara_compare.iterrows():
            if row['product_Marque'] not in list_ta3_produit_li_mxtarkin_fihom_marque:
                if ((Parasconti['product_Marque'].eq(row['product_Marque'].upper())).any()):
                    list_ta3_produit_li_mxtarkin_fihom_marque.append(row['product_Marque'])
                else:
                    if row['product_Marque'] not in list_product_cotepara_marque:
                        list_product_cotepara_marque.append(row['product_Marque'])

        for index, row_1 in data_Parasconti_compare.iterrows():
            if (Cotepara['product_Nom'].eq(row_1['product_Nom'].lower())).any():
                list_ta3_produit_li_mxtarkin_fihom.append(row['product_Nom'])
            if (row_1['product_Marque'] not in list_ta3_produit_li_mxtarkin_fihom_marque and row_1['product_Marque'] not in list_product_parasconti_marque):
                list_product_parasconti_marque.append(row_1['product_Marque'])


        col1, col2 , col3= st.tabs(["Cotepara  ", "   Cotepara == Parasconti   ", "  Parasconti"])
        with col1:
            st.subheader("Cotepara")
            st.bar_chart(Cotepara["product_Marque"].value_counts())
            # st.write(Cotepara["product_Marque"].value_counts().plot(kind='bar', xlabel='Team', ylabel='Count', rot=0))
        with col2:
            st.subheader("Cotepara == Parasconti   ===> Marque : "+str(len(list_ta3_produit_li_mxtarkin_fihom_marque)))
            first_list, second_list, third_list , foor_list= [list_ta3_produit_li_mxtarkin_fihom_marque[i::4] for i in range(4)]
            s1, s2 , s3, s4= st.columns(4)
            for i in first_list:
                    s1.markdown("- " + i)
            for i in second_list:
                    s2.markdown("- " + i)
            for i in third_list:
                    s3.markdown("- " + i)
            for i in foor_list:
                    s4.markdown("- " + i)
        with col3:
            st.subheader("Parasconti")
            st.dataframe(Parasconti["product_Marque"].value_counts())
        # d=Parasconti["product_Marque"] == Cotepara["product_Marque"]
        # st.table(Cotepara["product_Marque"]==Parasconti["product_Marque"])

    if selected == 'Parasconti':
        selected3 = option_menu(None, ["Read", "Add", "Update", 'Search', 'Download'],
                                default_index=0, orientation="horizontal",
                                # , "z-index": 999992,"position": "fixed!important","top": "36px"
                                styles={
                                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                                    "nav-link": {"font-size": "12px!important", "text-align": "center", "margin": "0px",
                                                 "--hover-color": "#eee"},
                                    "nav-link-selected": {"background-color": "green", "font-size": "14px!important"},
                                }
                                )
        # header
        if selected3=="Read" :
            st.dataframe(Parasconti)
            if st.checkbox("show data"):
                number = st.number_input("Number of rows to view", 1)
                st.dataframe(Parasconti.head(int(number)))

            #   show  columns
            if st.button("column Names"):
                st.write(Parasconti.columns)

            #   show  shep
            if st.checkbox("Shape of Data"):

                data_dim = st.radio("show Dimension By ", ("Rows", "Columns"))
                if data_dim == "Rows":
                    st.text("Number of Rows : {}".format(Parasconti.shape[0]))
                    # st.write(df.shape[0])
                elif data_dim == "Columns":
                    st.text("Number of Columns : {}".format(Parasconti.shape[1]))
                    # st.write(df.shape[1])
                else:
                    st.write(Parasconti.shape)

            #   select columns
            if st.checkbox("select columns to show"):
                all_columns = Parasconti.columns.tolist()
                selected_columns = st.multiselect("select", all_columns)
                if selected_columns:
                    new_df = Parasconti[selected_columns]
                    st.dataframe(new_df)

            #   show data type
            if st.button("Data Types"):
                st.write(Parasconti.dtypes)

            #   show summary
            if st.button("Summary"):
                st.write(Parasconti.describe().T)
        if selected3 == "Search":
            key_searche = st.radio("search By ", ("nom", "marque", "id", "id interval", "prix", "prix interval"),
                                   horizontal=True)
            if key_searche == "id" or key_searche == "prix":
                if key_searche == "id":
                    key_input = st.number_input(label='Enter search by id', min_value=1, step=1, max_value=Parasconti.shape[0])
                else:
                    key_input = st.number_input(label='Enter search by price')
            elif key_searche == "prix interval":
                key_input = st.slider(
                    'prix values', 0.0, 10000.0, (90.0, 200.0))
            elif key_searche == "id interval":
                key_input = st.slider(
                    'id interval', 1, Parasconti.shape[0], (496, 700))
            else:
                key_input = st.text_input(label='Enter search term')
            if st.button("Search"):
                if key_searche == "prix":
                    data_ser = Parasconti[Parasconti["product_Prix"] == key_input]
                elif key_searche == "prix interval":
                    data_ser = Parasconti[
                        (Parasconti["product_Prix"] >= key_input[0]) & (Parasconti["product_Prix"] <= key_input[1])]
                elif key_searche == "id":
                    data_ser = Parasconti[Parasconti["product_Id"] == key_input]
                    data_ser_discription = data_ser[["product_Description"]].iloc[0]["product_Description"]
                    data_ser_barcode = data_ser[["product_Barcode"]].iloc[0]["product_Barcode"]
                    data_ser_image = data_ser[["product_Image"]].iloc[0]["product_Image"]
                    data_ser_nom = data_ser[["product_Nom"]].iloc[0]["product_Nom"]
                    data_ser_link = data_ser[["product_Link"]].iloc[0]["product_Link"]
                    data_ser = data_ser[
                        ["product_Id", "product_Nom", "product_Marque", "product_Categorie", "product_Prix"]]
                elif key_searche == "id interval":
                    data_ser = Parasconti[
                        (Parasconti["product_Id"] >= key_input[0]) & (Parasconti["product_Id"] <= key_input[1])]
                elif key_searche == "nom":
                    data_ser = Parasconti[
                        (Parasconti["product_Nom"] == key_input) | (Parasconti["product_Nom"] == key_input.lower()) | (Parasconti["product_Nom"] == key_input.upper())]
                elif key_searche == "marque":
                    data_ser = Parasconti[(Parasconti["product_Marque"] == key_input) | (
                                Parasconti["product_Marque"] == key_input.upper())]
                st.dataframe(data_ser)
                if key_searche == "id":
                    st.subheader("Description :")
                    st.markdown(data_ser_discription)
                    st.markdown(data_ser_barcode)
                    st.markdown(data_ser_link)
                    image = Image.open(requests.get(data_ser_image, stream=True).raw)
                    st.image(image, caption=data_ser_nom )
        if selected3 == "Update":
            serch_input_id_update_1 = st.number_input('Enter search id', min_value=1)
            data_ser_update_1 = Parasconti[Parasconti["product_Id"] == serch_input_id_update_1]
            data_ser_nom_update_1 = data_ser_update_1[["product_Nom"]].iloc[0]["product_Nom"]
            data_ser_marqe_update_1 = data_ser_update_1[["product_Marque"]].iloc[0]["product_Marque"]
            data_ser_barcode_update_1 = data_ser_update_1[["product_Barcode"]].iloc[0]["product_Barcode"]
            data_ser_Categorie_update_1 = data_ser_update_1[["product_Categorie"]].iloc[0]["product_Categorie"]
            data_ser_prix_update_1 = data_ser_update_1[["product_Prix"]].iloc[0]["product_Prix"]
            data_ser_discription_update_1 = data_ser_update_1[["product_Description"]].iloc[0]["product_Description"]
            data_ser_image_update_1 = data_ser_update_1[["product_Image"]].iloc[0]["product_Image"]
            data_ser_link_pro_update_1 = data_ser_update_1[["product_Link"]].iloc[0]["product_Link"]
            st.write('product Information')
            with  st.form(key='product_info'):
                id_pro_1=serch_input_id_update_1
                nom_1=st.text_input("enter nom", value=data_ser_nom_update_1)
                marqe_1=st.text_input("enter marqe", value=data_ser_marqe_update_1)
                barcode_1=st.text_input("enter barcode", value=data_ser_barcode_update_1)
                Categorie_1=st.text_input("enter Categorie", value=data_ser_Categorie_update_1)
                prix_1 = st.number_input('enter prix', value=data_ser_prix_update_1)
                discr_1=st.text_area("enter discription", value=data_ser_discription_update_1)
                image_1=st.text_input("enter image" , value=data_ser_image_update_1)
                link_pro_1 = st.text_input("enter link product", value=data_ser_link_pro_update_1)
                submit_form_1 = st.form_submit_button("Submit")
            if submit_form_1:
                update_paraconti(id_pro_1, nom_1, marqe_1, Categorie_1, prix_1, discr_1, barcode_1, image_1, link_pro_1)
                Parasconti.at[id_pro_1 - 1, 'product_Nom'] = nom
                Parasconti.at[id_pro_1 - 1, 'product_Marque'] = marqe
                Parasconti.at[id_pro_1 - 1, 'product_Categorie'] = Categorie
                Parasconti.at[id_pro_1 - 1, 'product_Prix'] = prix
                Parasconti.at[id_pro_1 - 1, 'product_Description'] = discr
                Parasconti.at[id_pro_1 - 1, 'product_Barcode'] = barcode_1
                Parasconti.at[id_pro_1 - 1, 'product_Image'] = image
                Parasconti.at[id_pro_1 - 1, 'product_Link'] = link_pro
                change_parasconti(Parasconti)
                # Cotepara.loc[id_pro-1, ["product_Nom", "product_Marque", "product_Categorie", "product_Prix","product_Description","product_Image", "product_Link"]] = [nom, marqe, Categorie, prix, discr, image, link_pro]
                st.success('This is a success message!', icon="✅")
                st.balloons()
        if selected3 == "Add":
            check_form_add_is_valid_1=True
            with  st.form(key='product_info'):
                st.write('product Information')
                Nom_add_1 = st.text_input("Nom")
                Prix_add_1 = st.number_input('Prix', min_value=1.00)
                Categorie_add_1 = st.multiselect('Categorie',['Minceur', 'Immunité', 'Stress & Sommeil', 'Compléments Alimentaires', 'Santé et Beauté','Circulation',
                                                            'Articulations ',' Rumatismes', 'Minceur & Fermeté','Forme & Energie', 'Spécial Femme'])
                Marque_add_1 = st.text_input("Marque")
                Description_add_1 = st.text_area("Description")
                Barcode_add_1 = st.text_area("Barcode")
                Image_add_1 = st.text_input("Link Image")
                Link_add_1 = st.text_input("Link Product")
                Submit_add_1 = st.form_submit_button("Submit")
                list_Categorie_add_1=""
                if Submit_add_1 :
                    if Nom_add_1 == "":
                        st.error("Nom empty")
                        check_form_add_is_valid_1=False
                    if Barcode_add_1 == "":
                        st.error("Barcode empty")
                        check_form_add_is_valid_1=False
                    if Categorie_add_1 == "":
                        st.error("Categorie empty")
                        check_form_add_is_valid_1=False
                    if Marque_add_1 == "":
                        st.error("Marque empty")
                        check_form_add_is_valid_1=False
                    if Description_add_1 == "":
                        st.error("Description empty")
                        check_form_add_is_valid_1=False
                    if Image_add_1 == "":
                        st.error("Link Image empty")
                        check_form_add_is_valid_1=False
                    if Link_add_1 == "":
                        st.error("Link Product empty")
                        check_form_add_is_valid_1=False

                    if check_form_add_is_valid_1:
                        for i in range(len(Categorie_add_1)):
                            list_Categorie_add_1+=Categorie_add_1[i]
                            if len(Categorie_add_1)-1 != i :
                                list_Categorie_add_1 +="   ,  "
                        add_parasconti(len(Cotepara)+1,Nom_add_1 ,Marque_add_1 ,list_Categorie_add_1 ,Prix_add_1 ,Description_add_1 ,Barcode_add_1 ,Image_add_1 ,Link_add_1)
                        list_row_product_1 = [len(Cotepara)+1 ,Nom_add_1 ,Marque_add_1 ,list_Categorie_add_1  ,Prix_add_1 ,Description_add_1 ,Barcode_add_1 ,Image_add_1 ,Link_add_1]
                        Parasconti.loc[len(Parasconti)] = list_row_product_1
                        change_parasconti(Parasconti)
                        st.success("success add")
                        st.balloons()

    if selected == 'Cotepara':
        selected3 = option_menu(None, ["Read", "Add", "Update", 'Search', 'Download'],
                                default_index=0, orientation="horizontal",
                                # , "z-index": 999992,"position": "fixed!important","top": "36px"
                                styles={
                                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                                    "nav-link": {"font-size": "12px!important", "text-align": "center", "margin": "0px",
                                                 "--hover-color": "#eee"},
                                    "nav-link-selected": {"background-color": "green", "font-size": "14px!important"},
                                }
                                )

        if selected3 == "Read":
            st.dataframe(Cotepara)
            if st.checkbox("show data"):
                number = st.number_input("Number of rows to view", 1)
                st.dataframe(Cotepara.head(int(number)))

            #   show  columns
            if st.button("column Names"):
                st.write(Cotepara.columns)

            #   show  shep
            if st.checkbox("Shape of Data"):

                data_dim = st.radio("show Dimension By ", ("Rows", "Columns"))
                if data_dim == "Rows":
                    st.text("Number of Rows : {}".format(Cotepara.shape[0]))
                    # st.write(df.shape[0])
                elif data_dim == "Columns":
                    st.text("Number of Columns : {}".format(Cotepara.shape[1]))
                    # st.write(df.shape[1])
                else:
                    st.write(Cotepara.shape)

            #   select columns
            if st.checkbox("select columns to show"):
                all_columns = Cotepara.columns.tolist()
                selected_columns = st.multiselect("select", all_columns)
                if selected_columns:
                    new_df = Cotepara[selected_columns]
                    st.dataframe(new_df)

            #   show data type
            if st.button("Data Types"):
                st.write(Cotepara.dtypes)

            #   show summary
            if st.button("Summary"):
                st.write(Cotepara.describe().T)
        if selected3 == "Search":
            key_searche = st.radio("search By ", ("nom", "marque", "id","id interval", "prix", "prix interval"), horizontal=True)
            if key_searche=="id" or key_searche=="prix":
                if key_searche == "id":
                    key_input = st.number_input(label='Enter search by id', min_value=1, step=1, max_value=Cotepara.shape[0])
                else:
                    key_input = st.number_input(label='Enter search by price')

            elif key_searche=="prix interval":
                key_input = st.slider(
                    'prix values',0.0, 2000.0, (100.0, 500.0))
            elif key_searche=="id interval":
                key_input = st.slider(
                    'id interval',1, Cotepara.shape[0] , (2000, 6500))
            else:
                key_input = st.text_input(label='Enter search term')
            if st.button("Search"):
                if key_searche == "prix":
                    data_ser=Cotepara[Cotepara["product_Prix"] == key_input]
                elif key_searche == "prix interval":
                    data_ser = Cotepara[(Cotepara["product_Prix"] >= key_input[0]) & (Cotepara["product_Prix"] <= key_input[1])]
                elif key_searche == "id":
                    data_ser=Cotepara[Cotepara["product_Id"] == key_input]
                    data_ser_discription = data_ser[["product_Description"]].iloc[0]["product_Description"]
                    data_ser_image = data_ser[["product_Image"]].iloc[0]["product_Image"]
                    data_ser_nom= data_ser[["product_Nom"]].iloc[0]["product_Nom"]
                    data_ser_link = data_ser[["product_Link"]].iloc[0]["product_Link"]
                    data_ser=data_ser[["product_Id", "product_Nom","product_Marque", "product_Categorie","product_Prix"]]
                elif key_searche == "id interval":
                    data_ser = Cotepara[(Cotepara["product_Id"] >= key_input[0]) & (Cotepara["product_Id"] <= key_input[1])]
                elif key_searche == "nom":
                    data_ser=Cotepara[(Cotepara["product_Nom"] == key_input) | (Cotepara["product_Nom"]==key_input.lower())]
                elif key_searche == "marque":
                    data_ser=Cotepara[
                        (Cotepara["product_Marque"] == key_input) | (Cotepara["product_Marque"]==key_input.upper()) | (Cotepara["product_Nom"] == key_input.lower())]
                st.dataframe(data_ser)
                if key_searche == "id":
                    st.subheader("Description :")
                    st.markdown(data_ser_discription)
                    st.markdown(data_ser_link)
                    image = Image.open(requests.get(data_ser_image, stream=True).raw)
                    st.image(image, caption=data_ser_nom )
        if selected3 == "Download":
            csv = convert_df(Cotepara)
            st.download_button(
                "Press to Download",
                csv,
                "Cotepara.csv",
                "text/csv",
                key='browser-data'
            )
        if selected3 == "Update":

            serch_input_id_update = st.number_input('Enter search id', min_value=1)

            data_ser_update = Cotepara[Cotepara["product_Id"] == serch_input_id_update]
            data_ser_discription_update = data_ser_update[["product_Description"]].iloc[0]["product_Description"]
            data_ser_prix_update = data_ser_update[["product_Prix"]].iloc[0]["product_Prix"]
            data_ser_Categorie_update = data_ser_update[["product_Categorie"]].iloc[0]["product_Categorie"]
            data_ser_nom_update = data_ser_update[["product_Nom"]].iloc[0]["product_Nom"]
            data_ser_marqe_update = data_ser_update[["product_Marque"]].iloc[0]["product_Marque"]
            data_ser_image_update = data_ser_update[["product_Image"]].iloc[0]["product_Image"]
            data_ser_link_pro_update = data_ser_update[["product_Link"]].iloc[0]["product_Link"]

            st.write('product Information')
            with  st.form(key='product_info'):
                id_pro=serch_input_id_update
                discr=st.text_area("enter discription", value=data_ser_discription_update)
                prix = st.number_input('enter prix', value=data_ser_prix_update)
                Categorie=st.text_input("enter Categorie", value=data_ser_Categorie_update)
                nom=st.text_input("enter nom", value=data_ser_nom_update)
                marqe=st.text_input("enter marqe", value=data_ser_marqe_update)
                image=st.text_input("enter image" , value=data_ser_image_update)
                link_pro = st.text_input("enter link product", value=data_ser_link_pro_update)
                submit_form = st.form_submit_button("Submit")
            if submit_form:
                update_cotepara(id_pro, nom, marqe, Categorie, prix, discr, image, link_pro)
                Cotepara.at[id_pro - 1, 'product_Nom'] = nom
                Cotepara.at[id_pro - 1, 'product_Marque'] = marqe
                Cotepara.at[id_pro - 1, 'product_Categorie'] = Categorie
                Cotepara.at[id_pro - 1, 'product_Prix'] = prix
                Cotepara.at[id_pro - 1, 'product_Description'] = discr
                Cotepara.at[id_pro - 1, 'product_Image'] = image
                Cotepara.at[id_pro - 1, 'product_Link'] = link_pro
                change(Cotepara)
                # Cotepara.loc[id_pro-1, ["product_Nom", "product_Marque", "product_Categorie", "product_Prix","product_Description","product_Image", "product_Link"]] = [nom, marqe, Categorie, prix, discr, image, link_pro]
                st.success('This is a success message!', icon="✅")
                st.balloons()
        if selected3 == "Add":
            check_form_add_is_valid=True
            with  st.form(key='product_info'):
                st.write('product Information')
                Nom_add = st.text_input("Nom")
                Prix_add = st.number_input('Prix', min_value=1.00)
                Categorie_add = st.multiselect('Categorie',['Minceur', 'Immunité', 'Stress & Sommeil', 'Compléments Alimentaires', 'Santé et Beauté','Circulation',
                                                            'Articulations ',' Rumatismes', 'Minceur & Fermeté','Forme & Energie', 'Spécial Femme'])
                Marque_add = st.text_input("Marque")
                Description_add = st.text_area("Description")
                Image_add = st.text_input("Link Image")
                Link_add = st.text_input("Link Product")
                Submit_add = st.form_submit_button("Submit")
                list_Categorie_add=""
                if Submit_add :
                    if Nom_add == "":
                        st.error("Nom empty")
                        check_form_add_is_valid=False
                    if Categorie_add == "":
                        st.error("Categorie empty")
                        check_form_add_is_valid=False
                    if Marque_add == "":
                        st.error("Marque empty")
                        check_form_add_is_valid=False
                    if Description_add == "":
                        st.error("Description empty")
                        check_form_add_is_valid=False
                    if Image_add == "":
                        st.error("Link Image empty")
                        check_form_add_is_valid=False
                    if Link_add == "":
                        st.error("Link Product empty")
                        check_form_add_is_valid=False

                    if check_form_add_is_valid:
                        for i in range(len(Categorie_add)):
                            list_Categorie_add+=Categorie_add[i]
                            if len(Categorie_add)-1 != i :
                                list_Categorie_add +="   ,  "
                        add_cotepara(len(Cotepara)+1,Nom_add ,Marque_add ,list_Categorie_add ,Prix_add ,Description_add ,Image_add ,Link_add)
                        list_row_product = [len(Cotepara)+1 ,Nom_add ,Marque_add ,list_Categorie_add  ,Prix_add ,Description_add ,Image_add ,Link_add]
                        Cotepara.loc[len(Cotepara)] = list_row_product
                        st.success("success add")
                        st.balloons()













    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .viewerBadge_link__1S137 {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == "__main__":
    main()