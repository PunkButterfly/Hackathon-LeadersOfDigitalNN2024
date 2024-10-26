import os

from catboost import CatBoostClassifier, Pool
import pandas as pd

    
class CatBoostPredictor:
    def __init__(self, path_to_weights, weights_name):
        current_weights_path = os.path.join(path_to_weights, weights_name)
        self.catboost_classifier = CatBoostClassifier().load_model(current_weights_path, format='cbm')

        self.accnt_ids = None
        self.predictions = None
        self.submission = None

    def predict(self, X: pd.DataFrame):
        pooled = Pool(data=X)

        predictions = self.catboost_classifier.predict(pooled)

        return predictions