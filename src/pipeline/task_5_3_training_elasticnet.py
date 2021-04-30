
import pandas as pd
import luigi
from src.pipeline.task_4_feature_selection import FeatureSelection
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import ElasticNetCV
import numpy as np 
import pickle

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
