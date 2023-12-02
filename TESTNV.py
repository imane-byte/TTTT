# Écrire le code Streamlit dans un fichier appelé app.py
streamlit_code = """

import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
from streamlit_folium import folium_static

# Charger les données à partir du fichier geoparquet
file_path = "C:\CODENADII\DATANEW.geoparquet"
gdf = gpd.read_parquet(file_path)

# Liste des attributs et jours disponibles
attributs = [att for att in gdf.columns[1:-1] if att != 'Date']  # Exclure l'attribut 'Date'
jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

# Sélection du jour
jour = st.selectbox('Sélectionner un jour :', jours)

# Sélection de l'attribut
attribut = st.selectbox('Sélectionner un attribut :', attributs)

# Construire le nom de la colonne en fonction de la sélection
colonne_selectionnee = f"{attribut}"  # Convertir le jour en majuscules pour correspondre aux données


# Créer la carte avec Folium
m = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], zoom_start=10)

# Vérifier si la colonne sélectionnée existe dans le GeoDataFrame
if colonne_selectionnee not in gdf.columns:
    st.error(f"La colonne {colonne_selectionnee} n'existe pas dans le GeoDataFrame.")
else:
    # Convertir les valeurs de la colonne en nombres flottants
    gdf[colonne_selectionnee] = gdf[colonne_selectionnee].astype(float)

    # Diviser les données en 5 classes
    nb_classes = 5
    class_bins = [gdf[colonne_selectionnee].quantile(i / nb_classes) for i in range(nb_classes + 1)]
    colors = ['#253494', '#2c7fb8', '#41b6c4', '#7fcdbb', '#c7e9b4' , '#ffffcc']  # Autre jeu de couleurs

    
    # Définir la colormap
    colormap = folium.LinearColormap(colors=colors, vmin=gdf[colonne_selectionnee].min(), vmax=gdf[colonne_selectionnee].max())
    
    # Ajouter manuellement les classes à la carte Folium
    colormap.add_to(m)

    # Ajouter la classification de couleur à la carte Folium
    for index, row in gdf.iterrows():
        value = row[colonne_selectionnee]
        color = colormap(value)

        # Utiliser folium.Polygon pour simuler un rectangle
        rectangle = folium.Polygon(
            locations=[(row.geometry.y - 0.001, row.geometry.x - 0.001),
                       (row.geometry.y - 0.001, row.geometry.x + 0.001),
                       (row.geometry.y + 0.001, row.geometry.x + 0.001),
                       (row.geometry.y + 0.001, row.geometry.x - 0.001)],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            tooltip=f"Value: {value}"
        )
        rectangle.add_to(m)


    # Barre latérale Streamlit
    st.sidebar.title("Légende")
    st.sidebar.header(f"{attribut} - {jour}")

    # Ajouter d'autres informations si nécessaire
    # st.sidebar.subheader("Informations supplémentaires")
    # st.sidebar.text("Ajoutez ici d'autres détails")

    # Afficher la carte Folium dans Streamlit
    st.sidebar.markdown("**Carte interactive**")
    st.sidebar.write("Cliquez sur les marqueurs pour plus d'informations.")
    
# Afficher la carte Folium dans Streamlit
folium_static(m)


"""

# Écrire le code Streamlit dans un fichier appelé app.py
with open('C:\CODENADII/appLI1NW.py', 'w', encoding='utf-8') as f:
    f.write(streamlit_code)

# Lancer Streamlit en mode de commande
!streamlit run C:\CODENADII/appLI1NW.py