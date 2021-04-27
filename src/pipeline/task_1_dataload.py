import luigi
import pickle


import os 
import yaml


class DataLoad(luigi.Task):
    
    
    def run(self):
        
        ## Loading YAML file with config
        with open('credentials/credentials.yaml', 'r') as f:
            config = yaml.safe_load(f)
            
        ## Seting environ vars
        user =  config['kaggle']['username']
        key =  config['kaggle']['key']
        os.environ['KAGGLE_USERNAME'] = user
        os.environ['KAGGLE_KEY'] = key
        
        os.system("kaggle competitions download house-prices-advanced-regression-techniques -f train.csv --path ../data/")
        f = self.output().open("data/train.csv","r")
        f.close()
        
        
    def output(self):
        return luigi.local_target.LocalTarget("data/train.csv")

        
        
            
        
    
