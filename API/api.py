from fastapi import FastAPI
import psycopg2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import random

# Conexión a la base de datos PostgreSQL
connection = psycopg2.connect(
   host="localhost",
   database="Spotify",
   user="postgres",
   password="GestionDatos")
cursor = connection.cursor()

# Cargar los datos de las tablas song, artist y genres desde PostgreSQL en un dataframe de pandas
cursor.execute("SELECT * FROM song")
song_results = cursor.fetchall()
song_columns = [desc[0] for desc in cursor.description]
songs_df = pd.DataFrame(song_results, columns=song_columns)

cursor.execute("SELECT * FROM artist")
artist_results = cursor.fetchall()
artist_columns = [desc[0] for desc in cursor.description]
artists_df = pd.DataFrame(artist_results, columns=artist_columns)

cursor.execute("SELECT * FROM genres")
genre_results = cursor.fetchall()
genre_columns = [desc[0] for desc in cursor.description]
genres_df = pd.DataFrame(genre_results, columns=genre_columns)

# Entrenar el modelo KNN con los datos de las características de las canciones
model = KMeans(n_clusters=10)
model.fit(songs_df[['energy', 'valence', 'danceability', 'instrumentalness', 'tempo', 'key']])

# Crear la aplicación FastAPI
app = FastAPI()

# Definir el endpoint que recibe los datos de una canción y devuelve 10 recomendaciones de canciones similares
@app.post("/recommendations")
async def get_recommendations(song_name: str, artist_name: str):
    
    # Obtener las características de la canción ingresada
    song = songs_df[(songs_df['name'] == song_name) & (songs_df['artists'] == artist_name)]
    print(song)
    # Obtener las canciones recomendadas
    song_cluster = model.predict(song[['energy', 'valence', 'danceability', 'instrumentalness', 'tempo', 'key']])[0]
    cluster_songs = songs_df.loc[(model.labels_== song_cluster) & (np.abs(songs_df['popularity'] - songs_df['popularity']) < 5)]
    recommendations = cluster_songs.sort_values('popularity', ascending=False).head(10)
    
    # Obtener la información de las canciones recomendadas de las tablas cargadas 
    # Obtener la información de las canciones recomendadas de las tablas cargadas 
    songs = []
    for index, row in recommendations.iterrows():
        artists_names = []
        artist_ids = row['id_artists'].replace('[','').replace(']','').replace('\'','').split(', ')
        for artist_id in artist_ids:
            if artists_df['id'].isin([artist_id]).any():
                artist_name = artists_df.loc[artists_df['id'] == artist_id]['name'].iloc[0]
                artists_names.append(artist_name)
        genres = []
        for artist_id in artist_ids:
            if artists_df['id'].isin([artist_id]).any():
                artist_genres = artists_df.loc[artists_df['id'] == artist_id]['genres'].iloc[0]
                for genre_name in artist_genres.split(','):
                    genre_name = genre_name.strip()
                    if genre_name not in genres:
                        genres.append(genre_name)
        song = {'name': row['name'], 'artists': artists_names, 'genres': genres}
        songs.append(song)


    
    # Devolver las canciones recomendadas como respuesta de la solicitud
    return {'recommendations': songs}
