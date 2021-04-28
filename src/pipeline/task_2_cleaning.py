import configparser
import pandas as pd
import luigi
from src.pipeline.task_1_dataload import DataLoad
from src.utils.cleaning import *
from sklearn.preprocessing import OneHotEncoder



class Cleaning(luigi.Task):
    
    def requires(self):
        return DataLoad(self)
        
    def run(self):
        config = configparser.ConfigParser()
        config.read("config/public/variables.ini")
        
        var = config["KAGGLE"]["variables"]
        
        df = pd.read_csv('data/train.csv')
        df.rename(columns={col: clean_column(col) for col in df.columns.values}, inplace=True)
        
        string_dtypes = df.convert_dtypes().select_dtypes("string")
        string_dtypes = string_dtypes.fillna("na")
        string_dtypes = string_dtypes.applymap(clean_column)
        encoder = OneHotEncoder(drop = "if_binary",sparse = False)
        encoder.fit(string_dtypes)
        string_dtypes = encoder.transform(string_dtypes)
        string_dtypes =pd.DataFrame(string_dtypes,columns = encoder.get_feature_names())
        
        numericg_dtypes = df.convert_dtypes().select_dtypes(["float","integer"])
   
        df = pd.concat([numericg_dtypes,string_dtypes],axis=1)   
        
        
        df.to_csv('tmp/clean_data.csv',index = False)
        
        f = self.output().open("tmp/clean_data.csv","r")
        f.close()
        
    def output(self):
        return  luigi.local_target.LocalTarget("tmp/clean_data.csv")
        
        
        
        