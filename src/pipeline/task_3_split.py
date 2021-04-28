import configparser
import pandas as pd
import luigi
from src.pipeline.task_2_cleaning import Cleaning

from sklearn.model_selection import train_test_split



class Cleaning(luigi.Task):
    
    def requires(self):
        return Cleaning(self)
        
    def run(self):
        df = pd.read_csv("tmp/clean_data.csv",index_col= None)
        y = df['saleprice']
        X = df[df.columns[df.columns!='saleprice']]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        
        f = self.output().open("tmp/clean_data.csv","r")
        f.close()
        
    def output(self):
        return  luigi.local_target.LocalTarget("tmp/split_dataset.pkl")
        
        
        
        
