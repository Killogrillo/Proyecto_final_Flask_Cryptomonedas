# MyCryptos App

Aplicación de control de valores en criptomonedas, programa realizado con el framework Flask, con motor de base de datos SQLite.

## En su entorno de python ejecutar comando
```
pip install -r requirements.txt
```
Las librerias de flask utilizadas están en https://flask.palletsprojects.com/en/2.2.x/

## Creación BBDD

El fichero `Base_datos.txt` contiene el modelo a seguir para crear la base de datos.
Con SQLite crea una base de datos con el fichero indicado.

## Fichero .env

Debes hacer lo siguiente:

1. Copiar el fichero `.env_template` a.env y agregar las siguientes lineas

    ```
    FLASK_APP=main.py
    FLASK_DEBUG=true

    ```
## Ejecucion con el .env

Debes ejecutar este comando:
```
flask run
```
## SECRET_KEY
Debes pedir una SECRET KEY.

## API_KEY
Debes pedir una API KEY a la página coinAPI.io

## Fichero .config
Copiar el fichero `config_template`:

    ```
    cp config_template.py config.py
    ```

Después debes hacer lo siguiente:

1. Introducir la ruta a tu BBDD en el nuevo fichero
    ```
    ORIGIN_DATA = <tu ruta aquí>
    ```
2. Introducir tu SECRET KEY en el nuevo fichero
    ```
    SECRET_KEY = <tu clave aquí>
    ```
3. Introducir tu API KEY en el nuevo fichero
    ```
    API_KEY = <tu clave aquí>
    ```

