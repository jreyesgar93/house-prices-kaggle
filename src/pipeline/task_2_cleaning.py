import configparser
import pandas as pd
import luigi
from src.pipeline.task_1_dataload import DataLoad
from src.utils.cleaning import *
from sklearn.preprocessing import OneHotEncoder
from scipy import stats

class Cleaning(luigi.Task):
    def requires(self):
        return DataLoad()

    def run(self):
        ##Load Config File
        config = configparser.ConfigParser()
        config.read("config/public/variables.ini")

        var = config["KAGGLE"]["variables"]
        
        ##Load Dataset
        df = pd.read_csv("data/train.csv")
        
        ## Clean Column Names
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
        numericg_dtypes['lotfrontage'] =  numericg_dtypes['lotfrontage'].fillna(value = numericg_dtypes['lotfrontage'].mode()[0])
        numericg_dtypes['masvnrarea'] =  numericg_dtypes['masvnrarea'].fillna(value = numericg_dtypes['masvnrarea'].mode()[0])
        numericg_dtypes['garageyrblt'] =  numericg_dtypes['garageyrblt'].fillna(numericg_dtypes['yearbuilt'])

        ## Merging to final dataset
        df = pd.concat([numericg_dtypes, string_dtypes], axis=1)

        ## Saving File
        df.to_csv("tmp/clean_data.csv", index=False)
        
        ## Defining luigi output
        f = self.output().open("tmp/clean_data.csv", "r")
        f.close()

    def output(self):
        return luigi.local_target.LocalTarget("tmp/clean_data.csv")
