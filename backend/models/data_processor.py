import numpy as np
import pandas as pd


class DataProccesorV0:
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
    def process(self, transactions: pd.DataFrame, clients: pd.DataFrame):
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

        clients_columns = [
            'slctn_nmbr',
            # 'clnt_id',
            'accnt_id',
            'gndr',
            'brth_yr',
            'prsnt_age',
            'accnt_bgn_date',
            # 'cprtn_prd_d',
            'accnt_status',
            'pnsn_age',
            # 'prvs_npf',
            # 'brth_plc',
            # 'addrss_type',
            # 'rgn',
            # 'dstrct',
            # 'city',
            # 'sttlmnt',
            # 'pstl_code',
            'okato',
            'phn',
            'email',
            'lk',
            'assgn_npo',
            'assgn_ops',

            'erly_pnsn_flg'
        ]

        preprocessed_data = clients[clients_columns]

        self.processed_data = preprocessed_data.astype(
            {
                'slctn_nmbr': np.int64,
                # 'clnt_id': 'str',
                'accnt_id': 'str',
                'gndr': np.int64,
                'brth_yr': np.int64,
                'prsnt_age': np.int64,
                'accnt_bgn_date': np.int64,
                # 'cprtn_prd_d': np.int64,
                'accnt_status': np.int64,
                'pnsn_age': np.int64,
                'okato': np.int64,
                'phn': np.int64,
                'email': np.int64,
                'lk': np.int64,
                'assgn_npo': np.int64,
                'assgn_ops': np.int64,

                'erly_pnsn_flg': np.int64,
            }
        )

        return self.processed_data