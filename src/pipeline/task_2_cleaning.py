import configparser
import pandas as pd
import luigi
from pipeline.task_1_dataload import DataLoad
from utils.cleaning import *
from sklearn.preprocessing import OneHotEncoder
from scipy import stats
import ast


class Cleaning(luigi.Task):
    def requires(self):
        return DataLoad()

    def run(self):
        ##Load Config File
        config = configparser.ConfigParser()
        config.read("config/public/variables.ini")

        var = ast.literal_eval(config["KAGGLE"]["variables"])

        ##Load Dataset
        df = pd.read_csv("data/train.csv")

        ## Clean Column Names
        df.rename(
            columns={col: clean_column(col) for col in df.columns.values}, inplace=True
        )

        ## Clean categorical data
        df = clean_df(df)

        ## Saving File
        df.to_csv("tmp/clean_data/clean_data.csv", index=False)

    def output(self):
        return luigi.local_target.LocalTarget("tmp/clean_data/clean_data.csv")
