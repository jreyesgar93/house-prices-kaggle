import configparser
import pandas as pd
import luigi
from pipeline.task_2_cleaning import Cleaning

from sklearn.model_selection import train_test_split
import pickle


class Split(luigi.Task):
    def requires(self):
        return Cleaning()

    def run(self):
        ### Importing data
        df = pd.read_csv("tmp/clean_data/clean_data.csv", index_col=None)

        ### Selecting X Y
        y = df["saleprice"]
        X = df[df.columns[df.columns != "saleprice"]]

        ### Spliting data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42
        )
        idx_train = X_train["id"]
        X_train = X_train[X_train.columns[X_train.columns != "id"]]

        idx_test = X_test["id"]
        X_test = X_test[X_test.columns[X_test.columns != "id"]]

        ### Saving file
        output_file = open(self.output().path, "wb")
        pickle.dump(
            {
                "datasets": [X_train, X_test, y_train, y_test],
                "id": [idx_train, idx_test],
            },
            output_file,
        )
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget("tmp/split_sets/split_dataset.pkl")
