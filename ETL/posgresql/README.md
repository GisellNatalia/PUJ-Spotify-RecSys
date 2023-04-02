#  PostgreSQL
In this folder data is extracted from two CSV files, transformed and loaded into a PostgreSQL database. In the file "tracks_mod.csv" there are data about songs, while in "artists_mod.csv" there are data about artists. The objective is to load this data into a database for further analysis.

## Prerequisites
In order to run this project you need to have the following Python packages installed:

pandas
numpy
scikit-learn
psycopg2
sqlalchemy

In addition, you must have a PostgreSQL database installed and configured with the corresponding credentials.

## Folder structure
```
posgresql/
  |- data/
  |  |- tracks_mod.csv
  |  |- artists_mod.csv
  |- src/
  |  |- ETL_data.py

```

