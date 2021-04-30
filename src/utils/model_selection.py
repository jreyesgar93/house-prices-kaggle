import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def eval_scores(x,y_true,models,scores):
    results = list()
    for i in range(len(scores)):
        for j in range(len(models)):
            pred = models[j].predict(x)
            score = scores[i](y_true,pred)
            
            results.append([str(models[j].estimator),str(scores[i]),score])
    
    df_scores = pd.DataFrame(results,columns = ["models","score_type","score"])
    return df_scores
        
def score_model_mae(X_train, y_train,X_test,y_test, estimator, **kwargs):
    """
    Test various estimators.
    """
 
    model = estimator


    

    expected_train  = y_train
    predicted_train = model.predict(X_train)
    
    expected_test  = y_test
    predicted_test = model.predict(X_test)
    mae_train = mean_absolute_error(expected_train, predicted_train)
    mae_test = mean_absolute_error(expected_test, predicted_test)

    # Compute and return F1 (harmonic mean of precision and recall)
    return {estimator.estimator.__class__.__name__:{"model":estimator, "mae_train":mae_train, "mae_test":mae_test, "relative_error":abs((mae_train-mae_test)/mae_train)}}

def model_selection_scores(X_train, y_train,X_test,y_test, estimators, **kwargs):
    
    score = dict()
    for estimator in estimators:
        score.update(score_model_mae(X_train, y_train,X_test,y_test, estimator))
        print(score)

        
    return score

def model_selection(scores,threshold=.1):
    mae_old = 10000000000
    best = None
    for model in scores:
        mae = scores[model]["mae_train"]
        rel = scores[model]["relative_error"]
        
        if rel <= threshold:
            if mae<=mae_old:
                mae_old = mae
                best = model
            else:
                pass
        else: 
            pass
    return best
        
    
    
    