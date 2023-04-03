# Rest API

Esta carpeta contiene el código para la REST API que recomienda canciones similares basadas en las características de una canción ingresada. La API utiliza un modelo de aprendizaje automático entrenado en los datos de canciones almacenados en una base de datos PostgreSQL.

## Requerimientos

Para ejecutar la API, se necesitan los siguientes paquetes de Python:

- fastapi
- uvicorn
- psycopg2
- pandas
- numpy
- scikit-learn

Estos paquetes se pueden instalar ejecutando el siguiente comando en la terminal: `pip install -r requirements.txt`

## Ejecución

Para ejecutar la API, abra una terminal en la carpeta `rest_api` y ejecute el siguiente comando: `uvicorn app:app --reload`


Esto iniciará el servidor de la API en `http://localhost:8000/`.

## Endpoints

La API tiene un único endpoint que recibe los datos de una canción y devuelve 10 recomendaciones de canciones similares. El endpoint se encuentra en la siguiente URL:

http://localhost:8000/recommendations


El endpoint debe ser accedido mediante una solicitud POST. La solicitud debe contener los siguientes parámetros en formato JSON:

- song_name: El nombre de la canción ingresada.
- artist_name: El nombre del artista de la canción ingresada.

El endpoint devolverá una respuesta en formato JSON con las canciones recomendadas. Cada canción recomendada tendrá los siguientes campos:

- name: El nombre de la canción.
- artists: Una lista de los nombres de los artistas de la canción.
- genres: Una lista de los géneros de los artistas de la canción.


