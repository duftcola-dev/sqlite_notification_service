-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

++ ESPAÑOL ++

APP :

    sqlite3 + flask app + redis

DESCRIPCIÓN:

    Esta es una aplicación para la gestion de ficheros csv. 
    Los ficheros se cargan en local en el directorio bucked.
    Desde el direcorio bucked se mueven al directorio workspace; 
    al mismo tiempo se envía una notificacion de manera asíncrona 
    a un servicion de backend por cada archivo que se ha traladado.

    A continuacion lo archivos son analizados.Los campos na o null son 
    eliminados y las cabeceras on formateadas a mayúsculas. De forma asyncrona
    se envian notificaciones cunado se encuentran campos na y cuando se lleva a cabo el 
    proceso de formatea. Los arhivos originales no se modifican , solo las copias que son trasladadas
    al directorio processed data.

REQUERIMIENTOS:

    Esta aplicación con tal de funcionar require :
        Python 3>=3.8,3.9,3.10
        Flask 
        aioFlask
        Sqlite3
        Redis 
        Makefile
        Docker
        Docker-Compose

        **Esta app en concreto fue desarrollada con Python3.9 y Ubuntu 20.04 Focal

        ** La mayoria de dependencias son instaladas en la carpeta local 
        mediante el comando make install, sin embargo otras es necessario instalarlas 
        a parte en el sistem como :

            Python 3>=3.8,3.9,3.10
            Makefile
            Docker
            Docker-Compose
            Sqlite3

MANUAL DE USUARIO

    ** Ejecuta los siguientes comandos en consola : 

    make install **crea un venv e instala todas las dependencias necessarias

    make up_d ** ejecuta el servicio de backen en mode asincrono

    make test ** ejecuta test unitario

    make run ** ejecuta la aplicación main.py

    [ATENCIÓN] !! no es necessario activar un entrono virtual para ejecutar estos comandos !!


-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------

++ ENGLISH ++
APP:

    sqlite3 + flask app + redis

DESCRIPTION:

    This is an application for managing csv files.
    The files are uploaded locally to the bucked directory.
    From the bucked directory they are moved to the workspace directory;
    at the same time a notification is sent asynchronously
    to a backend service for each file that has been moved.

    Next the files are parsed. The na or null fields are
    removed and on headers formatted to uppercase. asynchronously
    notifications are sent when na fields are found and when the
    formatting process. The original files are not modified, only the copies that are transferred
    to the processed data directory.

REQUIREMENTS:

    This application in order to work requires:
        Python 3>=3.8,3.9,3.10
        Flask
        aioFlask
        sqlite3
        Redis
        makefile
        Docker
        docker-compose

        **This specific app was developed with Python3.9 and Ubuntu 20.04 Focal

        ** Most dependencies are installed in the local folder
        using the make install command, however others need to be installed
        separately in the system as:

            Python 3>=3.8,3.9,3.10
            makefile
            Docker
            docker-compose
            sqlite3

USER MANUAL

    ** Execute the following commands in console:

    make install **create a venv and install all necessary dependencies

    make up_d ** runs the backend service in asynchronous mode

    make test ** runs unit test

    make run ** runs the application main.py

    [ATTENTION] !! it is not necessary to activate a virtual environment to execute these commands !!