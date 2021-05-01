import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def score_model_mae(X_train, y_train, X_test, y_test, estimator, **kwargs):
    """
    Test various estimators.
    """

    model = estimator

    expected_train = y_train
    predicted_train = model.predict(X_train)

    expected_test = y_test
    predicted_test = model.predict(X_test)
    mae_train = mean_absolute_error(expected_train, predicted_train)
    mae_test = mean_absolute_error(expected_test, predicted_test)

    # Compute and return F1 (harmonic mean of precision and recall)
    return {
        estimator.estimator.__class__.__name__: {
            "model": estimator,
            "mae_train": mae_train,
            "mae_test": mae_test,
            "relative_error": abs((mae_train - mae_test) / mae_train),
        }
    }


def model_selection_scores(X_train, y_train, X_test, y_test, estimators, **kwargs):
    """
    Computes the MAE score for each estimntor
    """

    score = dict()
    for estimator in estimators:
        score.update(score_model_mae(X_train, y_train, X_test, y_test, estimator))
        print(score)
    s = pd.DataFrame(score)
    s.to_csv("tmp/metrics/scores.csv")
    return score


def model_selection(scores, threshold=0.1):
    """
    Selects the best model from all the scores
    """
    mae_old = 10000000000
    best = None
    for model in scores:
        mae = scores[model]["mae_train"]
        rel = scores[model]["relative_error"]

        if rel <= threshold:
            if mae <= mae_old:
                mae_old = mae
                best = model
                s = pd.DataFrame({"model": [best.__class__.__name__], "score": [mae]})
            else:
                pass
        else:
            pass

    s.to_csv("tmp/metrics/score_selected.csv")
    return best
