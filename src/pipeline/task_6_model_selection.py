import pandas as pd
import luigi
import numpy as np
import pickle
from pipeline.task_5_training import TrainRandomForest, TrainMLP, TrainElasticNet, TrainLasso
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from utils.model_selection import *


class ModelSelection(luigi.Task):
    def requires(self):
        yield TrainRandomForest()
        yield TrainMLP()
        yield TrainElasticNet()
        yield TrainLasso()

    def run(self):
        ### Loading data
        X_train, X_test, y_train, y_test = pickle.load(
            open("tmp/selected_features/selected_features_data.pkl", "rb")
        )["data"]
        random_forest = pickle.load(open("tmp/models/model_randomforest.pkl", "rb"))[
            "random_forest"
        ][0]
        mlp = pickle.load(open("tmp/models/model_mlp.pkl", "rb"))["mlp"][0]
        elastic_net = pickle.load(open("tmp/models/model_elasticnet.pkl", "rb"))[
            "elastic_net"
        ][0]
        
        lasso = pickle.load(open("tmp/models/model_lasso.pkl", "rb"))[
            "lasso"
        ][0]
        
        
        ## Calculating scores
        estimators = [random_forest, mlp, elastic_net,lasso]
        scores = model_selection_scores(X_train, y_train, X_test, y_test, estimators)
        ### Selecting Best
        best = model_selection(scores)

        best_model = scores[best]["model"]

        output_file = open(self.output().path, "wb")
        pickle.dump(best_model, output_file)
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget("model/selected_model.pkl")
