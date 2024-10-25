import pandas as pd

from models.classifier import CatBoostPredictor
from models.data_processor import DataProccesor

class Pipeline:
    def __init__(
            self,
            path_to_weights: str,
            classifier_weights_name: str = 'default_classifier.cbm'
        ):
        self.classifier_model = CatBoostPredictor(path_to_weights=path_to_weights, weights_name=classifier_weights_name)

    def forward(self, transactions: pd.DataFrame, clients: pd.DataFrame):

        data_processor = DataProccesor()
        processed_data = data_processor.process(transactions, clients)

        model_result = self.classifier_model.predict(processed_data)
        submission_csv = self.build_submission(clients, model_result)

        return model_result, submission_csv
        

    def build_submission(self, clients, model_result):
        submission = clients[['accnt_id']].copy()
        submission['erly_pnsn_flg'] = model_result

        return submission
