# house-prices-kaggle



### Execution 

#### Versión de Python

Este repositorio corre con Python 3.7.4

 
####  Clonar el repositorio, actualización del pip y generar un pyenv. 

- Dentro de la instancia o directorio desado, clonarás el repositorio:

`git clone https://github.com/jreyesgar93/house-prices-kaggle.git`

- Actualizas el pip install:

`pip install --upgrade pip`

- Creas ([aquí una guía de instalación para pyenv](https://github.com/pyenv/pyenv)), y activas tu pyenv:

```
pyenv virtualenv 3.7.4 house-prices
pyenv activate house-prices
```

#### Instalar paquete 
Una vez descargado el repositorio, realiza la instalación

```
pip install house-prices-kaggle/
```

#### Credentials

Para poder descargar la base de datos, es necesario tener una cuenta con llave privada de kaggle y haber aceptaro los términos del concurso. 

- Debes tener las credenciales para poder acceder. Primero colócate dentro del directorio del repositorio con 
```
cd house-price-kaggle
```
- Después coloca tus credenciales con las siguientes líneas de código en la terminal:
```
mkdir config/local
touch config/local/credentials.yaml
nano config/local/credentials.yaml
```
Dentro del archivo debes colocar esta estructura:

```
---
kaggle:
  username: "usuario"
  key: "llave"
  
```

#### Ejecución del Programa
El programa se ejecuta desde la linea de comandos.

```
Usage: houseprices [OPTIONS]

  CLI for House pricing model

Options:
  --houseid INTEGER   Input the House Id to get prediction
  --restart [yes|no]  Restart and retrain model.
  --help              Show this message and exit.


```

Debes colocar un comando similar al siguiente:


```
houseprices --houseid 12 --restart no

```

Si es la primera vez que ejecutas el programa la opcion `--restart` es redundante, ya que de todas formas se ejecutará el pipeline por completo. Si ya lo ejecutaste alguna vez, recomendamos seleccionar `--restart no` para obtener una prediccón mas rápida.

