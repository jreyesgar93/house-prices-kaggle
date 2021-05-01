# house-prices-kaggle



### Instrucciones para ejecución

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
pip install -r requirements.txt
```

#### Credentials

Para poder descargar la base de datos, es necesario tener una cuenta con llave privada de kaggle y haber aceptaro los términos del concurso. 

- Debes tener las credenciales para poder acceder. Esto se puede hacer colocando las siguientes líneas de código en la terminal:
```
mkdir config/local
touch config/local/credentials.yaml
nano config/local/credentials.yaml
```
Dentro del archivo deves colocar esta estructura:

```
---
kaggle:
  username: "usuario"
  key: "llave"
  
```


