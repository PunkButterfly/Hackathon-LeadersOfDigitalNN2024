import numpy as np


class Classifier:
    def __init__(self):
        pass

    def predict(self, transactions, clients):
        # Data processing...
        # Model processing...
        result_csv = clients[["accnt_id"]]
        result_csv["erly_pnsn_flg"] = np.zeros(len(clients))

        return result_csv