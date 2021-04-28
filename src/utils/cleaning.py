def clean_column(col):
    """
    Limpiamos las columnas, quitando símbolos y sustituyendo espacios por guión bajo
    """
    return col.lower() \
        .replace('/', '_') \
        .replace(' ', '_') \
        .replace('#', 'num') \
        .replace('(', '') \
        .replace(')', '')


