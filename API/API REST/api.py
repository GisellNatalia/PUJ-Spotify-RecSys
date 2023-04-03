import os
import psycopg2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import joblib
from fastapi import FastAPI

# Connection to the PostgreSQL database
connection = psycopg2.connect(
   host="localhost",
   database="Spotify",
   user="postgres",
   password="GestionDatos")
cursor = connection.cursor()

# Load the data from the song, artist and genres tables from PostgreSQL into a pandas dataframe
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

# Load pretrained KNN model from a file
model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'K-Means', 'saved_model.pkl'))

# Create the FastAPI application
app = FastAPI()

# Define the endpoint that receives song data and returns 10 similar song recommendations
@app.post("/recommendations")
async def get_recommendations(song_name: str, artist_name: str):
    
    # Get the characteristics of the entered song
    song = songs_df[(songs_df['name'] == song_name) & (songs_df['artists'] == artist_name)]
    print(song)

    # Get recommended songs
    song_cluster = model.predict(song[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']])[0]
    cluster_songs = songs_df.loc[(model.labels_== song_cluster) & (np.abs(songs_df['popularity'] - songs_df['popularity']) < 5)]
    recommendations = cluster_songs.sort_values('popularity', ascending=False).head(10)
    
    # Get the information of the recommended songs from the loaded tables
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


    
    # Return the recommended songs as response to the request
    return {'recommendations': songs}
