import pandas as pd
import luigi
import numpy as np 
import pickle
from src.pipeline.task_5_training import TrainRandomForest, TrainMLP, TrainElasticNet
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from src.utils.model_selection import *

class ModelSelection(luigi.Task):
    def requires(self):
        yield TrainRandomForest()
        yield TrainMLP()
        yield TrainElasticNet()

    def run(self):
        
        X_train, X_test, y_train,y_test = pickle.load(open("tmp/selected_features_data.pkl","rb"))["data"]
        random_forest = pickle.load(open("tmp/model_randomforest.pkl","rb"))["random_forest"][0]
        mlp = pickle.load(open("tmp/model_mlp.pkl","rb"))["mlp"][0]
        elastic_net = pickle.load(open("tmp/model_elasticnet.pkl","rb"))["elastic_net"][0]
                
        
        
        estimators= [random_forest,mlp,elastic_net]
        scores = model_selection_scores(X_train, y_train,X_test,y_test, estimators)
        
        best = model_selection(scores)
        
        best_model = scores[best]["model"]
        
        output_file = open(self.output().path, "wb")
        pickle.dump(best_model, output_file)
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget("tmp/selected_model.pkl")
