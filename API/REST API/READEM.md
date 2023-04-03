# API REST
This folder contains the code for the REST API that recommends similar songs based on the characteristics of an entered song. The API uses a machine learning model trained on song data stored in a PostgreSQL database.

## Requirements

To run the API, the following Python packages are required:

- fastapi
- uvicorn
-psycopg2
- panda
-numpy
-scikit-learn

These packages can be installed by running the following command in the terminal: `pip install -r requirements.txt`

## Execution

To run the API, open a terminal in the `rest_api` folder and run the following command: `uvicorn app:app --reload`


This will start the API server at `http://localhost:8000/`.

## Endpoints

The API has a single endpoint that receives the data for a song and returns 10 recommendations for similar songs. The endpoint is located at the following URL:

http://localhost:8000/recommendations


The endpoint must be accessed via a POST request. The request must contain the following parameters in JSON format:

- song_name: The name of the song entered.
- artist_name: The name of the artist of the entered song.

The endpoint will return a response in JSON format with the recommended songs. Each recommended song will have the following fields:

- name: The name of the song.
- artists: A list of the names of the artists of the song.
- genres: A list of the genres of the artists in the song.

