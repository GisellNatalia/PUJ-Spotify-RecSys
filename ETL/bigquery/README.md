#  BigQuery ETL
In this folder data is extracted from two CSV files, transformed and loaded into a BigQuery database. In the file "tracks_mod.csv" there are data about songs, while in "artists_mod.csv" there are data about artists. The objective is to load this data into a database for further analysis.

## Prerequisites
In order to run this project you need to have the following Python packages installed:
- pandas
- numpy
- scikit-learn
- scipy
- google.cloud
- google.oauth2
- uuid

In addition, you must have a BigQuery database installed and configured with the corresponding credentials.

## Folder structure
```
bigquery/
  |- ETL_data.py

```

## Description of Folders
- `src/`: This folder contains the Python script `ETL_data.py`, which is responsible for extracting, transforming, and loading the data into the BigQuery database.

## How to Run
1. Make sure you have installed all the necessary packages and have a Google Cloud Platform account with a BigQuery project created and configured.
2. Clone this repository to your local machine.
3. Navigate to the `src/` folder in the terminal.
4. Run the command python `ETL_data.py`.
5. The data will be extracted, transformed, and loaded into the BigQuery database.
