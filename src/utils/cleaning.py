from sklearn.preprocessing import OneHotEncoder
import pandas as pd


def clean_column(col):
    """
    Limpiamos las columnas, quitando símbolos y sustituyendo espacios por guión bajo
    """
    return (
        col.lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace("#", "num")
        .replace("(", "")
        .replace(")", "")
    )


def clean_df(df):
    df.rename(
        columns={col: clean_column(col) for col in df.columns.values}, inplace=True
    )
    ## Clean categorical data
    string_dtypes = df.convert_dtypes().select_dtypes("string")
    string_dtypes = string_dtypes.fillna("na")
    string_dtypes = string_dtypes.applymap(clean_column)

    ## Encoding
    encoder = OneHotEncoder(drop="if_binary", sparse=False)
    encoder.fit(string_dtypes)
    string_dtypes = encoder.transform(string_dtypes)
    string_dtypes = pd.DataFrame(string_dtypes, columns=encoder.get_feature_names())

    ## Impute numeric
    numericg_dtypes = df.convert_dtypes().select_dtypes(["float", "integer"])
    numericg_dtypes["lotfrontage"] = numericg_dtypes["lotfrontage"].fillna(
        value=numericg_dtypes["lotfrontage"].mode()[0]
    )
    numericg_dtypes["masvnrarea"] = numericg_dtypes["masvnrarea"].fillna(
        value=numericg_dtypes["masvnrarea"].mode()[0]
    )
    numericg_dtypes["garageyrblt"] = numericg_dtypes["garageyrblt"].fillna(
        numericg_dtypes["yearbuilt"]
    )

    ## Merging to final dataset
    df = pd.concat([numericg_dtypes, string_dtypes], axis=1)

    return df
