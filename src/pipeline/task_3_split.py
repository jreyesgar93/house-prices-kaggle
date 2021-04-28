import configparser
import pandas as pd
import luigi
from src.pipeline.task_2_cleaning import Cleaning

from sklearn.model_selection import train_test_split
import pickle


class Split(luigi.Task):
    def requires(self):
        return Cleaning()

    def run(self):
        ### Importing data
        df = pd.read_csv("tmp/clean_data.csv", index_col=None)
        
        ### Selecting X Y
        y = df["saleprice"]
        X = df[df.columns[df.columns != "saleprice"]]

        ### Spliting data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42
        )
        
        ### Saving file
        output_file = open(self.output().path, "wb")
        pickle.dump([X_train, X_test, y_train, y_test], output_file)
        output_file.close()

    def output(self):
        return luigi.local_target.LocalTarget("tmp/split_dataset.pkl")
