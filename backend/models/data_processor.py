import pandas as pd


class DataProccesor:
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
