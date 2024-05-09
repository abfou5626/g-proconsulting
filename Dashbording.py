import streamlit as st
from request import *
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
st.set_page_config(page_title="Dashbord",page_icon="🌍", layout="wide" )
st.subheader("🌍 Analyse de Donnnées  Business")
logo_path = "gproconsulting.png" 
st.sidebar.image(logo_path, use_column_width=True)

data = collection.find({}, {"Nom": 1, "metrage": 1, "kilometrage": 1, "Date": 1,"type_p":1})
df = pd.DataFrame(data) 

df['metrage'] = df['metrage'].fillna(0)
df['kilometrage'] = df['kilometrage'].fillna(0)
import pandas as pd

# Remplacer les valeurs None dans la colonne spécifique par "BLACK N07A"
df['type_p'] = df['type_p'].fillna("BLACK N07A")

df = df.drop("_id", axis=1)
st.sidebar.header("Filtrer") 
Nom=st.sidebar.multiselect(
    "select Nom",
    options=df["Nom"].unique(),
    default=df["Nom"].unique(),
)
type_p=st.sidebar.multiselect(
    "select Type produit",
    options=df["type_p"].unique(),
    default=df["type_p"].unique(),
)
Date=st.sidebar.multiselect(
    "select Date",
    options=df["Date"].unique(),
    default=df["Date"].unique(),
)

df_selection=df.query(
    "Nom==@Nom & Date==@Date & type_p==@type_p"
)
# Conversion des valeurs de la colonne "metrage" en numérique avec spécification du séparateur décimal ","
df_selection["metrage"] = pd.to_numeric(df_selection["metrage"].str.replace(',', '.'), errors="coerce")
df_selection["kilometrage"] = pd.to_numeric(df_selection["kilometrage"].str.replace(',', '.'), errors="coerce")

df_selection['metrage'].fillna(0, inplace=True)
df_selection['kilometrage'].fillna(0, inplace=True)

def home():
 with st.expander("Tabular"):
        showData = st.multiselect('Filtrer', df_selection.columns.tolist(), default=[])
        st.write(df_selection[showData])
 
 total_salaire=(df_selection["metrage"]).sum()
 salaire_mode=(df_selection["metrage"]).max()
 salaire_moyen=(df_selection["metrage"]).mean()
 
 total_kg=(df_selection["kilometrage"]).sum()
 kg_moyen=(df_selection["kilometrage"]).mean()

 total1,total2,total4,total5,total6=st.columns(5,gap='large')
 with total1:
     st.info("sum Metre",icon="➕")
     st.metric(label="Somme ", value=f"{total_salaire:,.0f}")
 with total2:
     st.info(" moyen Metre",)
     st.metric(label="moyen  ", value=f"{salaire_moyen:,.0f}")

 with total4:
     st.info(" mode Metre")
     st.metric(label="maximum ", value=f"{salaire_mode:,.0f}")
 with total5:
     st.info("total kg",icon="➕")
     st.metric(label="somme ", value=f"{total_kg:,.0f}")
 with total6:
     st.info("mean kg")
     st.metric(label="moyen", value=f"{kg_moyen:,.0f}")
 
 

home()
div1, div2=st.columns(2)
div3, div4=st.columns(2)

def pie():
    with div1:
        theme_plotly = None # None or streamlit
        fig = px.pie(df_selection, values='metrage', names='Nom', title='quantitée de tissu par entreprie ')
        fig.update_layout(legend_title="Country", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

def barchart():
    with div2:
        fig = px.bar(df_selection, y='metrage', x='Nom', text_auto='.2s',title="Controlled text sizes, positions and angles")
        fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

def chart_courbe():
    with div3:
        fig = px.line(df_selection, x='Date', y='metrage', color='Nom', title='Evolution des ventes au fil du temps')
        st.plotly_chart(fig, use_container_width=True)
def boite_moustache():
    with div4:
        # Créer la boîte à moustaches pour les données de 'metrage'
        fig_boxplot = px.box(df_selection, x='Nom', y='metrage', title='Boîte à moustaches de metrage par catégorie')

            # Afficher le graphique dans Streamlit
        st.plotly_chart(fig_boxplot, use_container_width=True)




chart_courbe()
boite_moustache()


pie()
barchart()

    