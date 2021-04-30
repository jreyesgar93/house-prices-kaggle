
import pandas as pd
import luigi
from src.pipeline.task_4_feature_selection import FeatureSelection
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPRegressor
import numpy as np 
import pickle

class TrainMLP(luigi.Task):
    def requires(self):
        return FeatureSelection()

    def run(self):
        
        X_train, X_test, y_train,y_test = pickle.load(open("tmp/selected_features_data.pkl","rb"))["data"]
        
        parameters = {"random_state":[42],'hidden_layer_sizes':[10,50,100,200], 'early_stopping':[True,False],'alpha':[.001,.1,.0001]}
        
        mlp = MLPRegressor()
        clf=GridSearchCV(mlp,parameters)
        clf.fit(X_train,y_train)
        
        
        output_file = open(self.output().path, "wb")
        pickle.dump({"mlp":[clf]}, output_file)
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget("tmp/model_mlp.pkl")