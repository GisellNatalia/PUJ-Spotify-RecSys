# This is the Python file to extract, transform the data and then load it into PostgreSQL.

import psycopg2
from sqlalchemy import create_engine

import pandas as pd 
import numpy as np
from sklearn.impute import KNNImputer
from scipy.stats import mstats
import ast
import uuid

#############################################################################################################################################
# EXTRACT DATA

songs_df = pd.read_csv('data/tracks_mod.csv')
artists_df = pd.read_csv('data/artists_mod.csv')

artists_df.shape
artists_df.dtypes
artists_df.head()

songs_df.shape
songs_df.dtypes
songs_df.head()

########################################################################################################################################

# TRANSFORM DATA

#----------------------------
# Artists

# Column values are converted to agree with the Data dictionary
artists_df = artists_df.astype({"id":str, "followers":int, "genres":str, "name":str, "popularity":int}, errors='ignore')

# Removing artists without a defined genre
len(artists_df.loc[artists_df['genres']=='[]'])
artists_df = artists_df.drop(index=artists_df[artists_df['genres']=='[]'].index)

# Identify or create primary key
artists_df.columns

print("Is there a unique id per row?")
artists_df.shape[0] == len(artists_df["id"].unique())

print("Are there NA values?")
print(artists_df["id"].isnull().any())

# Each cell contains a single value
artists_df.duplicated().sum()

artists_df["name"].duplicated().sum()

artists_df[['name', 'genres']].duplicated().sum()

artists_df = artists_df.drop_duplicates(subset = ['name', 'genres'], keep = 'first').reset_index(drop = True)

# Checking NaN values
artists_df.isna().sum()

cols_to_impute = ['followers', 'popularity']

X = artists_df[cols_to_impute]

X_known = X[X.notnull().all(axis=1)]
X_unknown = X[X.isnull().any(axis=1)]

imputer = KNNImputer(n_neighbors=5)
imputer.fit(X_known)

X_imputed = pd.DataFrame(imputer.transform(X_unknown), columns=cols_to_impute, index=X_unknown.index)

artists_df.loc[X_imputed.index, cols_to_impute] = X_imputed

# Extract only the first genre from the list
artists_df['genres'] = artists_df['genres'].apply(lambda x: eval(x)[0])

# Extract unique values in gender
genres = artists_df['genres'].drop_duplicates()

# Outliers

winsorized_followers = mstats.winsorize(artists_df['followers'], limits=[0.05, 0.05])
artists_df['followers'] = winsorized_followers

winsorized_popularity = mstats.winsorize(artists_df['popularity'], limits=[0.05, 0.05])
artists_df['popularity'] = winsorized_popularity

#-------------------------
# Songs

# Column values are converted to agree with the Data dictionary
songs_df = songs_df.astype({"id":str, "name":str, "popularity":int, "duration_ms":int, "explicit":bool, "artists":str, "id_artists":str,
                            "release_date":str, "danceability":float, "energy":float, "key":int, "loudness":float, "mode":int,
                            "speechiness":float, "acousticness":float, "instrumentalness": float, "liveness":float,
                            "valence":float, "tempo":float, "time_signature":int}, errors='ignore')

# Identify or create primary key
songs_df.columns

print("Is there a unique id per row?")
songs_df.shape[0] == len(songs_df["id"].unique())

print("Are there NA values?")
print(songs_df["id"].isnull().any())

# Each cell contains a single value
songs_df.duplicated().sum()

songs_df['name'].duplicated().sum()

songs_df[['name', 'artists']].duplicated().sum()

songs_df = songs_df.drop_duplicates(subset = ['name', 'artists'], keep = 'first').reset_index(drop = True)

# Checking NaN values
songs_df.isna().sum()

cols_to_impute = ['popularity', 'duration_ms', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

X = songs_df[cols_to_impute]

X_known = X[X.notnull().all(axis=1)]
X_unknown = X[X.isnull().any(axis=1)]

imputer = KNNImputer(n_neighbors=5)
imputer.fit(X_known)

X_imputed = pd.DataFrame(imputer.transform(X_unknown), columns=cols_to_impute, index=X_unknown.index)

songs_df.loc[X_imputed.index, cols_to_impute] = X_imputed

# Outliers
quantitative_columns = ["popularity", "duration_ms", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence",
                         "tempo", "time_signature"]

for col in quantitative_columns:
    winsorized = mstats.winsorize(songs_df[col], limits=[0.05, 0.05])
    songs_df[col] = winsorized

# Create an intermediate table that maps song IDs to artist IDs
songs_artists = [(id_song, id_artist) for id_song, id_artist in zip(songs_df['id'], songs_df['id_artists'])]

songs_artist_tuples = [(id_song, id_artist) for id_song, id_artist in songs_artists for artist_id in id_artist]

songs_artist_df = pd.DataFrame(songs_artist_tuples, columns=['id_song', 'id_artist'])

songs_artist_df['id_artist'] = songs_artist_df['id_artist'].apply(lambda x: ast.literal_eval(x)[0])

songs_artist_df.drop_duplicates()

###############################################################################

# LOAD

# Database connection
conn = psycopg2.connect(
   host="localhost",
   database="Spotify",
   user="postgres",
   password="GestionDatos")

cursor = conn.cursor()

# Creating genre table
cursor.execute("CREATE TABLE IF NOT EXISTS genres (id UUID PRIMARY KEY, name TEXT)") 
conn.commit()

# Insert data in table
for genre in genres:
    cursor.execute("INSERT INTO genres (id, name) VALUES (%s, %s)", (str(uuid.uuid4()), genre))   
conn.commit()

# Create artist table
cursor.execute('''CREATE TABLE IF NOT EXISTS artist (id TEXT PRIMARY KEY,
               genres TEXT[],name TEXT,followers INTEGER, popularity INTEGER)''')    
conn.commit()

# Insert data from python to postgresql
engine = create_engine('postgresql+psycopg2://postgres:GestionDatos@localhost:5432/Spotify')
artists_df.to_sql('artist', engine,if_exists='replace', index=False)
conn.commit()

# Create songs table
cursor.execute(''' CREATE TABLE IF NOT EXISTS song (id TEXT PRIMARY KEY,
               name TEXT, popularity INTEGER, duration_ms INTEGER, explicit BOOLEAN, artists TEXT[], id_artists TEXT[], release_date TEXT,
               danceability FLOAT, energy FLOAT, key INTEGER, loudness FLOAT, mode INTEGER, speechiness FLOAT, acousticness FLOAT,
               instrumentalness FLOAT, liveness FLOAT, valence FLOAT, tempo FLOAT, time_signature INTEGER)''')    
conn.commit()

# Insert data from python to postgresql
engine = create_engine('postgresql+psycopg2://postgres:GestionDatos@localhost:5432/Spotify')
songs_df.to_sql('song', engine,if_exists='replace', index=False)
conn.commit()

# Create songs_artist table
cursor.execute("CREATE TABLE IF NOT EXISTS songs_artists (id_song TEXT, id_artist TEXT, PRIMARY KEY (id_song, id_artist))")
conn.commit()

# Insert data from python to postgresql
engine = create_engine('postgresql+psycopg2://postgres:GestionDatos@localhost:5432/Spotify')
songs_artist_df.to_sql('songs_artists', engine,if_exists='replace', index=False)
conn.commit()


# Close the connection to the database
conn.close()


