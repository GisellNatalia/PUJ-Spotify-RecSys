# Spotify Recommender System
This project aims to build a song recommendation system from Spotify data. We used two datasets, one for songs and the other for artists, which were cleaned and stored in PostgreSQL and BigQuery.

## Team Members
Manuel Andres Paz Castillo & Gisell Natalia Cristiano Muñoz 

## Data
The datasets used in this project were obtained from the Spotify API and can be found [here](https://drive.google.com/drive/folders/1toW8fa6ag4oNU00RuJHVUwhwEqmMsJaZ). 

## Implemented Components
The project consists of three installments, each with a specific objective:

### 1. Exploratory Data Analysis and Data Cleaning.
Folder: `/EDA`

This component involves the analysis and cleaning of the Spotify data to prepare it for the subsequent components.

### 2. ETL Process.
Folder: `/ETL`

This component includes the construction of an ETL process to automate the transformation and loading of data to PostgreSQL and BigQuery.

### 3.  Dashboard, Machine Learning Model, and API REST.
Folders: `/Dashboard` and `/API`

This component involves the construction of a dashboard with two indicators and three graphs to provide insights into the Spotify data. Additionally, a machine learning model was created using the K-Means algorithm to recommend songs based on an entered song. Finally, a API REST was constructed to enable the recommendation of songs through the created model.

## How to use the repository
Each component is located in a separate folder at the root of the repository. Inside each folder is a README file that details the steps for its execution and deployment.
