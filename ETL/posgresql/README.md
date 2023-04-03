#  PostgreSQL ETL
In this folder data is extracted from two CSV files, transformed and loaded into a PostgreSQL database. In the file "tracks_mod.csv" there are data about songs, while in "artists_mod.csv" there are data about artists. The objective is to load this data into a database for further analysis. The data is obtained directly from a Google Drive file and the script provides the necessary functionality to access it.

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
  |- ETL_data.py

```
## How to Run
1. Clone this repository to your local machine.
1. Make sure you have installed all the necessary packages and have a PostgreSQL database installed and configured.
4. Run the command python `ETL_data.py`.
5. The data will be extracted, transformed, and loaded into the PostgreSQL database.
