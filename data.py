import streamlit as st
from request import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
st.title("Analyse des données")
logo_path = "gproconsulting.png" 
st.sidebar.image(logo_path, use_column_width=True)

data = collection.find({}, {"Nom": 1, "metrage": 1, "kilometrage": 1, "Date": 1})
df = pd.DataFrame(data) 
df = df.drop("_id", axis=1)
st.write(df)

col1, col2 = st.columns(2)

# Displaying the description of the data
with col1:
    st.write("Description des données :")
    st.write(df.describe())

# Checking for missing values
missing_values = df.isnull().sum()

# Displaying missing values count
with col2:
    st.write("Nombre de valeurs manquantes par colonne :")
    st.write(missing_values)

df['metrage'] = df['metrage'].fillna(0)
df['kilometrage'] = df['kilometrage'].fillna(0)


selected_column = st.selectbox("Sélectionner une colonne :", options=df.columns, key="select_column")

# Créer un diagramme en bâtons
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=df, x=selected_column, ax=ax)
ax.set_title(f'Diagramme en bâtons pour la colonne "{selected_column}"')
ax.set_xlabel(selected_column)
ax.set_ylabel('Count')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)