import configparser
import pandas as pd
import luigi
from src.pipeline.task_1_dataload import DataLoad
from sklearn.preprocessing import OneHotEncoder



class Cleaning(luigi.Task):
    
    def requires(self):
        return DataLoad(self)
        
    def run(self):
        config = configparser.ConfigParser()
        


        
        f = self.output().open("tmp/clean_data.csv","r")
        f.close()
        
    def output(self):
        return  luigi.local_target.LocalTarget("tmp/clean_data.csv")
        
        
        
        