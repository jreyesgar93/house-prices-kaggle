import pandas as pd
import luigi
from pipeline.task_3_split import Split
from sklearn.feature_selection import RFECV
from sklearn.linear_model import Ridge
import numpy as np
import pickle


class FeatureSelection(luigi.Task):
    def requires(self):
        return Split()

    def run(self):

        ##loading data
        X_train, X_test, y_train, y_test = pickle.load(
            open("tmp/split_sets/split_dataset.pkl", "rb")
        )["datasets"]

        idx_train, idx_test = pickle.load(
            open("tmp/split_sets/split_dataset.pkl", "rb")
        )["id"]

        ##selecting data
        X_names = list(X_train.columns)
        y_names = y_train.name

        X_train = np.array(X_train)
        y_train = np.array(y_train)
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        ## Feature Slection
        feat_selection = RFECV(Ridge(), cv=5)
        feat_selection.fit(X_train, y_train)

        selected_features = [
            i for indx, i in enumerate(X_names) if feat_selection.support_[indx] == True
        ]
        print(selected_features)

        X_train = feat_selection.transform(X_train)
        X_test = feat_selection.transform(X_test)

        output_file = open(self.output().path, "wb")
        ## Saving
        pickle.dump(
            {
                "names": [X_names, y_names],
                "selected_features": [selected_features],
                "data": [X_train, X_test, y_train, y_test],
                "id": [idx_train, idx_test],
            },
            output_file,
        )
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget(
            "tmp/selected_features/selected_features_data.pkl"
        )
