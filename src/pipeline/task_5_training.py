
import pandas as pd
import luigi
from src.pipeline.task_4_feature_selection import FeatureSelection
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import ElasticNetCV
import numpy as np 
import pickle

class TrainRandomForest(luigi.Task):
    def requires(self):
        return FeatureSelection()

    def run(self):
        
        X_train, X_test, y_train,y_test = pickle.load(open("tmp/selected_features_data.pkl","rb"))["data"]
        
        parameters = {'random_state':([42]), 'n_estimators':[100, 160,50],'max_depth':[None,3,10]}
        
        rf = RandomForestRegressor()
        clf=GridSearchCV(rf,parameters)
        clf.fit(X_train,y_train)
        
        
        output_file = open(self.output().path, "wb")
        pickle.dump({"random_forest":[clf]}, output_file)
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget("tmp/model_randomforest.pkl")


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




class TrainElasticNet(luigi.Task):
    def requires(self):
        return FeatureSelection()

    def run(self):
        
        X_train, X_test, y_train,y_test = pickle.load(open("tmp/selected_features_data.pkl","rb"))["data"]
        
        parameters = {'l1_ratio':[.5,.25,.75],'random_state':[42]}
        
        en = ElasticNetCV()
        clf=GridSearchCV(en,parameters)
        clf.fit(X_train,y_train)
        
        
        output_file = open(self.output().path, "wb")
        pickle.dump({"elastic_net":[clf]}, output_file)
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget("tmp/model_elasticnet.pkl")