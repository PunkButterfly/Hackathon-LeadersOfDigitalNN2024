import numpy as np
import pandas as pd
import yaml
import os
import random


class DataProcessorV0:
    """
    Базовая заглушка
    """
    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
        clients['gndr'] = clients['gndr'].replace({'ж': 0, 'м': 1})
        self.processed_data = clients[['accnt_id', 'brth_yr', 'prsnt_age', 'gndr']].astype(
            {
                'brth_yr': 'int64',
                'prsnt_age': 'int64',
                'gndr': 'int64',
            }
        )
        return self.processed_data


class DataProcessorV1:
    """
    Исходный датасет, только клиенты
    """
    def __init__(self, path_to_configs, config_name):
        current_weights_path = os.path.join(path_to_configs, config_name)
        with open(current_weights_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
        clients_columns_typing = self.config['data']['columns']['clients']
        clients_columns = list(self.config['data']['columns']['clients'].keys())

        clients = clients[clients_columns]

        clients['gndr'] = clients['gndr'].map({'ж': 0, 'м': 1})
        clients['accnt_bgn_date'] = clients['accnt_bgn_date'].astype(np.int64) // 1e9
        clients['accnt_status'] = clients['accnt_status'].map({'Накопительный период': 0, 'Выплатной период': 1})
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

# class DataProcessorV11:
#     """
#     Исходный датасет, клиенты и транзакции
#     """
#     def __init__(self, path_to_configs, config_name):
#         current_weights_path = os.path.join(path_to_configs, config_name)
#         with open(current_weights_path, 'r') as file:
#             self.config = yaml.safe_load(file)
#
#     def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
#         clients_columns_typing = self.config['data']['columns']['clients']
#         clients_columns = list(self.config['data']['columns']['clients'].keys())
#
#         clients = clients[clients_columns]
#
#         clients['gndr'] = clients['gndr'].map({'ж': 0, 'м': 1})
#         clients['accnt_bgn_date'] = clients['accnt_bgn_date'].astype(np.int64) // 1e9
#         clients['accnt_status'] = clients['accnt_status'].map({'Накопительный период': 0, 'Выплатной период': 1})
#         # le = LabelEncoder()
#         # clients['prvs_npf'] = le.fit_transform(clients['prvs_npf'])
#         # le = LabelEncoder()
#         # clients['brth_plc'] = le.fit_transform(clients['brth_plc'])
#         # clients['addrss_type'] = clients['addrss_type'].map({'Адрес места жительства': 0, 'Адрес по прописке': 1, 'Адрес для информирования': 2, 'Адрес за пределами РФ': 3})
#         clients['okato'] = clients['okato'].fillna('0').apply(lambda x: str(x)[:2])
#         clients['phn'] = clients['phn'].map({'нет': 0, 'да': 1})
#         clients['email'] = clients['email'].map({'нет': 0, 'да': 1})
#         clients['lk'] = clients['lk'].map({'нет': 0, 'да': 1})
#         clients['assgn_npo'] = clients['assgn_npo'].map({'нет': 0, 'да': 1})
#         clients['assgn_ops'] = clients['assgn_ops'].map({'нет': 0, 'да': 1})
#
#         processed_clients = clients.astype(
#             clients_columns_typing
#         )
#
#         # Агрегирование транзакционных данных
#         transactions = transactions.groupby('accnt_id').agg({
#             'oprtn_date': ['sum', 'mean', 'max', 'min'],
#             'sum': ['count']
#         }).reset_index()
#         transactions.columns = ['accnt_id', 'amount_sum', 'amount_mean', 'amount_max', 'amount_min',
#                                     'transaction_count']
#
#         # Соединение таблиц
#         self.processed_data = processed_clients.merge(transactions, on='accnt_id', how='left')
#
#         return self.processed_data

class DataProcessorV12:
    """
    Исходный датасет, клиенты + макроэкономические факторы
    """
    def __init__(self, path_to_configs, config_name):
        current_weights_path = os.path.join(path_to_configs, config_name)
        with open(current_weights_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
        clients_columns_typing = self.config['data']['columns']['clients']
        clients_columns = list(self.config['data']['columns']['clients'].keys())

        economics_columns_typing = self.config['data']['columns']['economics']
        economics_columns = list(self.config['data']['columns']['economics'].keys())

        clients = clients[clients_columns]

        clients['gndr'] = clients['gndr'].map({'ж': 0, 'м': 1})
        clients['accnt_bgn_date'] = clients['accnt_bgn_date'].astype(np.int64) // 1e9
        clients['okato'] = clients['okato'].fillna('0').apply(lambda x: str(x)[:2])
        clients['phn'] = clients['phn'].map({'нет': 0, 'да': 1})
        clients['email'] = clients['email'].map({'нет': 0, 'да': 1})
        clients['lk'] = clients['lk'].map({'нет': 0, 'да': 1})
        clients['assgn_npo'] = clients['assgn_npo'].map({'нет': 0, 'да': 1})
        clients['assgn_ops'] = clients['assgn_ops'].map({'нет': 0, 'да': 1})

        processed_clients = clients.astype(
            clients_columns_typing
        )

        economics = pd.read_csv("models/data/economics.csv")

        economics = economics[economics_columns]

        processed_economics = economics.astype(
            economics_columns_typing
        )

        self.processed_data = processed_clients.merge(processed_economics, on=["gndr", "okato"], how='left')

        return self.processed_data


class DataProcessorV13:
    """
    Исходный датасет, клиенты без дат + макроэкономические факторы
    """
    def __init__(self, path_to_configs, config_name):
        current_weights_path = os.path.join(path_to_configs, config_name)
        with open(current_weights_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
        clients_columns_typing = self.config['data']['columns']['clients']
        clients_columns = list(self.config['data']['columns']['clients'].keys())

        economics_columns_typing = self.config['data']['columns']['economics']
        economics_columns = list(self.config['data']['columns']['economics'].keys())

        clients = clients[clients_columns]

        clients['gndr'] = clients['gndr'].map({'ж': 0, 'м': 1})
        clients['okato'] = clients['okato'].fillna('0').apply(lambda x: str(x)[:2])
        clients['phn'] = clients['phn'].map({'нет': 0, 'да': 1})
        clients['email'] = clients['email'].map({'нет': 0, 'да': 1})
        clients['lk'] = clients['lk'].map({'нет': 0, 'да': 1})
        clients['assgn_npo'] = clients['assgn_npo'].map({'нет': 0, 'да': 1})
        clients['assgn_ops'] = clients['assgn_ops'].map({'нет': 0, 'да': 1})

        processed_clients = clients.astype(
            clients_columns_typing
        )

        economics = pd.read_csv("models/data/economics.csv")

        economics = economics[economics_columns]

        processed_economics = economics.astype(
            economics_columns_typing
        )

        self.processed_data = processed_clients.merge(processed_economics, on=["gndr", "okato"], how='left')

        return self.processed_data


class DataProcessorV2:
    """
    Обработанный датасет, только клиенты
    """

    def __init__(self, path_to_configs, config_name):
        current_weights_path = os.path.join(path_to_configs, config_name)
        with open(current_weights_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame, mode: str = 'inference'):

        clients['okato'] = clients['okato'].fillna('0').apply(lambda x: str(x)[:2])
        clients['gndr'] = clients['gndr'].map({'ж': 0, 'м': 1})
        clients['phn'] = clients['phn'].map({'нет': 0, 'да': 1})
        clients['email'] = clients['email'].map({'нет': 0, 'да': 1})
        clients['lk'] = clients['lk'].map({'нет': 0, 'да': 1})
        clients['assgn_npo'] = clients['assgn_npo'].map({'нет': 0, 'да': 1})
        clients['assgn_ops'] = clients['assgn_ops'].map({'нет': 0, 'да': 1})
        # Флаг наличия пред организации
        clients['prvs_npf_flg'] = clients['prvs_npf'].case_when(([(~clients['prvs_npf'].isnull(), 1),
                                                                  (clients['prvs_npf'].isnull(), 0),
                                                                  ]))

        clients['accnt_bgn_date'] = pd.to_datetime(clients['accnt_bgn_date'])
        # Возраст на момент подписания договора
        clients['age_agreement_start'] = clients['accnt_bgn_date'].dt.year - clients['brth_yr']

        # Для трейна переносим клиента в прошлое: спустя год после подписания договора
        # Преобразуем данные для обучения
        if mode == 'train':
            clients['age'] = (clients['accnt_bgn_date'] + pd.to_timedelta(365 * 5, 'days')).dt.year - clients['brth_yr']
            # Дата начала выплат = дата окончания договора = дата выхода на пенсию
            clients_on_pension_df = clients[clients['accnt_status'] == 'Выплатной период'].copy()
            clients_on_pension_df['accnt_end_date'] = clients_on_pension_df['accnt_bgn_date'] + pd.to_timedelta(
                clients_on_pension_df['cprtn_prd_d'], unit='days')

            clients_not_on_pension_df = clients[clients['accnt_status'] == 'Накопительный период'].copy()
            clients_not_on_pension_df['accnt_end_date'] = clients_not_on_pension_df['accnt_bgn_date'] + (
                        clients_not_on_pension_df['pnsn_age'] - clients_not_on_pension_df['age_agreement_start']).apply(
                lambda x: pd.to_timedelta(int(x) * 365, unit='days'))

            # pd.to_datetime('2030-01-01') #заглушка
            clients = clients.merge(
                pd.concat([clients_on_pension_df, clients_not_on_pension_df]).loc[:, ['clnt_id', 'accnt_end_date']],
                on='clnt_id', how='left')

            clients['accnt_end_age'] = clients['accnt_end_date'].dt.year - clients['brth_yr']
            # Если клиента перекинули через дату окончания договора
            # то убираем его из выборки для обучения
            clients['age_over_accnt_end_flg'] = clients['accnt_end_age'].case_when(([
                (clients['accnt_end_age'] <= clients['age'], 1),
                (clients['accnt_end_age'] > clients['age'], 0)
            ]))
            clients = clients[clients['age_over_accnt_end_flg'] == 0]

            # Исключаем клиентов, которые подписали договор после законного возраста выхода на пенсию
            clients.drop(index=clients[clients['age_agreement_start'] > clients['pnsn_age']].index, inplace=True)

        # Для инференса на тестовых данных Верим что вы придержитесь логики своего бизнес процесса и подадите возраст < pnsn_age
        # и можем без утечки данных использовать колонку
        elif mode == 'inference':
            clients['age'] = clients['prsnt_age']

        clients_columns_typing = self.config['data']['columns']['clients']
        clients_columns = list(self.config['data']['columns']['clients'].keys())

        clients = clients[clients_columns]
        self.processed_data = clients.astype(
            clients_columns_typing
        )

        return self.processed_data
