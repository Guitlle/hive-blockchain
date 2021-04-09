Automatización en Hive con Beem
===============================

Votos
-----

Este script vota en el post más reciente de una lista de cuentas si no se ha votado en ese post y si no se ha votado en la última media hora.

Agregar cuentas a seguir en el archivo `cuentas` con los nombres de cada cuenta en líneas separadas, por ejemplo:

```
cuenta1
cuenta2
cuenta3
```

Agregar un archivo `.env` con la clave de publicación y la cuenta:

```
export hiveaccount=username
export postingkey=xxxxxxxxxxx
```

Preparar entorno de python:

```
cd /repositorio/
python3 -m venv devenv
source devenv/bin/activate
pip install -r requirements
```

Usando `crontab -e` agregar el script para que se ejecute cada hora o menos:

```
  1 *  *   *   *    /usr/bin/env bash -c 'cd /repositorio/automatizacion/; source ../devenv/bin/activate; source .env; python autovoto.py >> log' 2>&1
```
