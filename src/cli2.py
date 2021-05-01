import click
import os
import pandas as pd
import warnings
import sys
import glob


@click.command()
@click.option(
    "--houseid",
    type=int,
    help="Input the House Id to get prediction",
)
@click.option(
    "--restart", type=click.Choice(["yes", "no"]), help="Restart and retrain model."
)
def main(houseid, restart):
    """CLI for House pricing model"""
    if str(restart) == "yes":
        os.system('echo ">>>>>>>RESTARTING MODEL<<<<<<<<<<<<<<<"')
        try:
            os.remove("data/train.csv")
        except:
            pass

        try:
            os.remove("tmp/clean_data/clean_data.csv")
        except:
            pass

        try:
            os.remove("tmp/selected_features/selected_features_data.pkl")
        except:
            pass

        try:
            os.remove("tmp/split_sets/split_dataset.pkl")
        except:
            pass

        try:
            os.remove("tmp/models/model_elasticnet.pkl")
        except:
            pass

        try:
            os.remove("tmp/models/model_mlp.pkl")
        except:
            pass

        try:
            os.remove("tmp/models/model_lasso.pkl")
        except:
            pass

        try:
            os.remove("tmp/models/model_randomforest.pkl")
        except:
            pass

        try:
            os.remove("model/selected_model.pkl")
        except:
            pass

        try:
            for f in glob.glob("predictions/*"):
                os.remove(f)
        except:
            pass

        #       os.system("rm tmp/clean_data/* tmp/selected_features/* tmp/models/* tmp/split_sets/* ../predictions/* data/* ../model/*")
        os.system(
            "PYTHONPATH=. luigi --module pipeline.task_7_prediction Prediction --idx "
            + str(houseid)
            + " --local-scheduler"
        )
        print(
            os.system(
                "echo 'Your prediction is:' & cat predictions/prediction-id-"
                + str(houseid)
                + ".txt"
            ),
            file=sys.stdout,
        )
    else:
        os.system(
            "PYTHONPATH=. luigi --module pipeline.task_7_prediction Prediction --idx "
            + str(houseid)
            + " --local-scheduler > /dev/null"
        )
        print(
            os.system(
                "echo 'Your prediction is:' & cat predictions/prediction-id-"
                + str(houseid)
                + ".txt"
            ),
            file=sys.stdout,
        )


# if __name__ == "__main__":
#    main()
