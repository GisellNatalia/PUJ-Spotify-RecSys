# This is the Python file to extract, transform the data and then load it into BigQuery.

import pandas as pd 
import numpy as np
from sklearn.impute import KNNImputer
from scipy.stats import mstats
from google.cloud import bigquery
from google.oauth2 import service_account
import uuid


#############################################################################################################################################
# EXTRACT DATA

songs_df = pd.read_csv('data/tracks_mod.csv')
artists_df = pd.read_csv('data/artists_mod.csv')


#############################################################################################################################################

# TRANSFORM DATA

#----------------------------
# Artists

# Column values are converted to agree with the Data dictionary
artists_df = artists_df.astype({"id":str, "followers":int, "genres":str, "name":str, "popularity":int}, errors='ignore')

# Removing artists without a defined genre
len(artists_df.loc[artists_df['genres']=='[]'])
artists_df = artists_df.drop(index=artists_df[artists_df['genres']=='[]'].index)

# Each cell contains a single value
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

# Each cell contains a single value
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


#############################################################################################################################################
# LOAD
credentials = service_account.Credentials.from_service_account_file("C:/Users/manue/OneDrive/Documentos/Gestion de Datos/GD_key.json", scopes=["https://www.googleapis.com/auth/cloud-platform"])
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

#------genres-----
# Creating the job config genres
job_config_genre = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.STRING,mode='REQUIRED'),
        bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING)
    ],
    # Drod and re-create table, if exist
    write_disposition="WRITE_TRUNCATE"
)

# Sending the job to BigQuery
genre_dicts = [{'id': str(uuid.uuid4()), 'name': genre} for genre in genres]
genres_df = pd.DataFrame(genre_dicts)

job = client.load_table_from_dataframe(genres_df, 'gestiondatos2023.ProyPazCristiano.genres', job_config=job_config_genre)
job.result()

# Verifying if table was successfully created or updated
table = client.get_table('gestiondatos2023.ProyPazCristiano.genres')
print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), 'gestiondatos2023.ProyPazCristiano.genres'))


#------artists-----
# Creating the job config artists
job_config_artists = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.STRING,mode='REQUIRED'),
        bigquery.SchemaField("genres", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("followers", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("popularity", bigquery.enums.SqlTypeNames.INTEGER)
    ],
    # Drod and re-create table, if exist
    write_disposition="WRITE_TRUNCATE"
)

# Sending the job to BigQuery
job = client.load_table_from_dataframe(artists_df, 'gestiondatos2023.ProyPazCristiano.artistas', job_config=job_config_artists)
job.result()

# Verifying if table was successfully created or updated
table = client.get_table('gestiondatos2023.ProyPazCristiano.artistas')
print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), 'gestiondatos2023.ProyPazCristiano.artistas'))


#------songs-----
job_config_canciones = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.STRING,mode='REQUIRED'),
        bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("popularity", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("duration_ms", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("explicit", bigquery.enums.SqlTypeNames.BOOLEAN),
        bigquery.SchemaField("artists", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("id_artists", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("release_date", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("danceability", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("energy", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("key", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("loudness", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("mode", bigquery.enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("speechiness", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("acousticness", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("instrumentalness", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("liveness", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("valence", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("tempo", bigquery.enums.SqlTypeNames.FLOAT),
        bigquery.SchemaField("time_signature", bigquery.enums.SqlTypeNames.INTEGER)
    ],
    # Drod and re-create table, if exist
    write_disposition="WRITE_TRUNCATE"
)

# Sending the job to BigQuery
job = client.load_table_from_dataframe(songs_df, 'gestiondatos2023.ProyPazCristiano.canciones', job_config=job_config_artists)
job.result()

# Verifying if table was successfully created or updated
table = client.get_table('gestiondatos2023.ProyPazCristiano.canciones')
print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), 'gestiondatos2023.ProyPazCristiano.canciones'))