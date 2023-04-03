import psycopg2
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import joblib

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

# Train the KNN model with the song feature data
model = KMeans(n_clusters=10)
model.fit(songs_df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']])

# Save the trained model to a file
joblib.dump(model, 'saved_model.pkl')
