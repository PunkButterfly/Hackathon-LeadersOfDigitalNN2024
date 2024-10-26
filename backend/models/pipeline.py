import pandas as pd
import shap

from models.classifier import CatBoostPredictor
from models.data_processor import DataProcessorV0, DataProcessorV1, DataProcessorV12, DataProcessorV13, DataProcessorV2

class Pipeline:
    def __init__(
            self,
            path_to_weights: str,
            classifier_weights_name: str,
            path_to_configs: str
        ):
        self.classifier_model = CatBoostPredictor(path_to_weights=path_to_weights, weights_name=classifier_weights_name)
        
        if classifier_weights_name == 'default_classifier.cbm':
            self.data_processor = DataProcessorV0()
        elif classifier_weights_name == 'classifier_v1_sourceclients.cbm':
            self.data_processor = DataProcessorV1(path_to_configs=path_to_configs, config_name='processor_v1.yaml')
        elif classifier_weights_name == 'classifier_v12_sourceclients_macro.cbm':
            self.data_processor = DataProcessorV12(path_to_configs=path_to_configs, config_name='processor_v12.yaml')
        elif classifier_weights_name == 'classifier_v13_sourceclients_macro_nodates.cbm':
            self.data_processor = DataProcessorV13(path_to_configs=path_to_configs, config_name='processor_v13.yaml')
        elif classifier_weights_name == 'classifier_v2_historyclients.cbm':
            self.data_processor = DataProcessorV2(path_to_configs=path_to_configs, config_name='processor_v2.yaml')


    def forward(self, transactions: pd.DataFrame, clients: pd.DataFrame):
        
        # Процессинг данных
        processed_data = self.data_processor.process(transactions, clients)
        data_for_model = processed_data.drop(['accnt_id'], axis=1)

        # Предсказание модели
        model_result = self.classifier_model.predict(data_for_model)

        # Расчет SHAP-значений
        explainer = shap.TreeExplainer(self.classifier_model.catboost_classifier)
        shap_values = explainer(data_for_model)
        shap_values_df = pd.DataFrame(shap_values.values, columns=[f"shap_{col}" for col in data_for_model.columns])
        shap_base_value_df = pd.DataFrame(shap_values.base_values, columns=["shap_base_value"])

        # Формирование выходного датафрейма
        result_df = pd.concat([processed_data, shap_values_df, shap_base_value_df], axis=1)
        result_df['erly_pnsn_flg'] = model_result

        return result_df
