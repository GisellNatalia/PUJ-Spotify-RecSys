#  PostgreSQL ETL
In this folder data is extracted from two CSV files, transformed and loaded into a PostgreSQL database. In the file "tracks_mod.csv" there are data about songs, while in "artists_mod.csv" there are data about artists. The objective is to load this data into a database for further analysis.

## Prerequisites
In order to run this project you need to have the following Python packages installed:
- pandas
- numpy
- scikit-learn
- psycopg2
- sqlalchemy

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

## Description of Folders
- `data/`: This folder contains the CSV files that will be used for the data extraction.
- `src/`: This folder contains the Python script `ETL_data.py`, which is responsible for extracting, transforming, and loading the data into the PostgreSQL database.

## How to Run
1. Make sure you have installed all the necessary packages and have a PostgreSQL database installed and configured.
2. Clone this repository to your local machine.
3. Navigate to the `src/` folder in the terminal.
4. Run the command python `ETL_data.py`.
5. The data will be extracted, transformed, and loaded into the PostgreSQL database.