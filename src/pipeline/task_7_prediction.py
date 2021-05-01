import pandas as pd
import luigi
import numpy as np
import pickle
from pipeline.task_2_cleaning import Cleaning
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from pipeline.task_6_model_selection import ModelSelection
from utils.model_selection import *


class Prediction(luigi.Task):
    idx = luigi.Parameter()

    def requires(self):
        return ModelSelection()

    def run(self):
        ## Loading models and data
        model = pickle.load(open("model/selected_model.pkl", "rb"))
        selected_features = pickle.load(
            open("tmp/selected_features/selected_features_data.pkl", "rb")
        )["selected_features"]

        X_train, X_test, _, _ = pickle.load(
            open("tmp/selected_features/selected_features_data.pkl", "rb")
        )["data"]

        idx_train, idx_test = pickle.load(
            open("tmp/selected_features/selected_features_data.pkl", "rb")
        )["id"]
        ## Merging datasets
        X = np.concatenate([X_train, X_test], axis=0)
        idx_all = pd.concat([idx_train, idx_test], axis=0)
        ##Prediction
        prediction = model.predict(X[idx_all == int(self.idx)])[0]

        g = self.output().open("w")
        g.write("ID: " + str(self.idx) + " Prediction: " + str(prediction))
        g.close()  # needed because files are atomic

    def output(self):
        # return luigi.local_target.LocalTarget("predictions/prediction.txt")
        return luigi.local_target.LocalTarget(
            "predictions/prediction-id-" + self.idx + ".txt"
        )
