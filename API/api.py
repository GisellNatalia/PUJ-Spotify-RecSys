from fastapi import FastAPI
import psycopg2
import pandas as pd
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
songs_df['cluster']=model.labels_

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
    cluster_songs = songs_df.loc[(songs_df['cluster'] == song_cluster) & ((songs_df['popularity'] == song['popularity'] - 5) | (songs_df['popularity'] == song['popularity'] + 5))]
    recommendations = cluster_songs.sort_values('popularity', ascending=False).head(10)
    
    # Obtener la información de las canciones recomendadas de las tablas cargadas en el paso 1
    songs = []
    for index, row in recommendations.iterrows():
        artists_names = []
        for artist_id in row['id_artists']:
            artist_name = artists_df.loc[artists_df['id'] == artist_id]['name'].iloc[0]
            artists_names.append(artist_name)
        song_genre = genres_df.loc[genres_df['id'] == row['genre']]['name'].iloc[0]
        song = {'name': row['name'], 'artists': artists_names, 'genre': song_genre}
        songs.append(song)
    
    # Devolver las canciones recomendadas como respuesta de la solicitud
    return {'recommendations': songs}
