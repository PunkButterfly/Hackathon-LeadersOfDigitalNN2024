import numpy as np
import pandas as pd
import yaml


class DataProcessorV0:
    """
    Базовая заглушка
    """
    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
        clients['gndr'] = clients['gndr'].replace({'ж': 0, 'м': 1})
        self.processed_data = clients[['accnt_id', 'brth_yr', 'prsnt_age', 'gndr', 'erly_pnsn_flg']].astype(
            {
                'brth_yr': 'int64',
                'prsnt_age': 'int64',
                'gndr': 'int64',
                'erly_pnsn_flg': 'int64',
            }
        )
        return self.processed_data


class DataProcessorV1:
    """
    Исходный датасет, только клиенты
    """
    def __init__(self):
        with open('./backend/models/configs/processor_v1.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
        clients_columns_typing = self.config['data']['columns']['clients']
        clients_columns = list(self.config['data']['columns']['clients'].keys())

        clients = clients[clients_columns]

        clients['gndr'] = clients['gndr'].map({'ж': 0, 'м': 1})
        clients['accnt_bgn_date'] = clients['accnt_bgn_date'].astype(np.int64) // 1e9
        clients['accnt_status'] = clients['accnt_status'].map({'Накопительный период': 0, 'Выплатной период': 1})
        # le = LabelEncoder()
        # clients['prvs_npf'] = le.fit_transform(clients['prvs_npf'])
        # le = LabelEncoder()
        # clients['brth_plc'] = le.fit_transform(clients['brth_plc'])
        # clients['addrss_type'] = clients['addrss_type'].map({'Адрес места жительства': 0, 'Адрес по прописке': 1, 'Адрес для информирования': 2, 'Адрес за пределами РФ': 3})
        clients['okato'] = clients['okato'].fillna('0').apply(lambda x: str(x)[:2])
        clients['phn'] = clients['phn'].map({'нет': 0, 'да': 1})
        clients['email'] = clients['email'].map({'нет': 0, 'да': 1})
        clients['lk'] = clients['lk'].map({'нет': 0, 'да': 1})
        clients['assgn_npo'] = clients['assgn_npo'].map({'нет': 0, 'да': 1})
        clients['assgn_ops'] = clients['assgn_ops'].map({'нет': 0, 'да': 1})

        self.processed_data = clients.astype(
            clients_columns_typing
        )

        return self.processed_data
