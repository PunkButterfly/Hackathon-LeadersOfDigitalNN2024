from io import StringIO
import os

import pandas as pd
import requests as rq
import streamlit as st
import shap

st.set_option('deprecation.showPyplotGlobalUse', False)

BACKEND_URL = f"http://backend:{os.getenv("BACKEND_PORT")}"
# BACKEND_URL = f"http://0.0.0.0:8128"

st.header("Загрузите данные")
st.subheader("")

transactions = st.file_uploader("Загрузка файла с транзакциями")
clients = st.file_uploader("Загрузка файла с клиентами")

backend_model_list = rq.get(f"{BACKEND_URL}/get_model_names/").json()

model_weights = st.selectbox(
    "Выберите модель",
    backend_model_list,
)

if transactions is not None and clients is not None:

    if st.button("Upload"):
        st.write("Данные загружены")
        post_data = {"transactions": transactions, "clients": clients}

        request_files = {
            "transactions": (transactions.name, transactions, "text/csv"),
            "clients": (clients.name, clients, "text/csv"),
        }

        data = {
            "model_weights": model_weights
        }

    
        csv_response = rq.post(f"{BACKEND_URL}/upload_csv/", files=request_files, data=data)

        if csv_response.status_code == 200:
            csv_content = csv_response.content.decode("utf-8")
            response_df = pd.read_csv(StringIO(csv_content))
            st.write("Результирующий датафрейм")
            st.dataframe(response_df)

            cols = response_df.columns.to_list()
            features_cols = [col for col in cols if not col.startswith("shap") and col != "accnt_id"]
            shap_cols = [col for col in cols if col.startswith("shap") and col != "accnt_id" and col != "shap_base_value"]
            response_df[features_cols].values.tolist()
            response_df[shap_cols].values.tolist()

            for i in range(len(response_df)):
                shap.force_plot(
                    response_df["shap_base_value"].values[i],
                    response_df[shap_cols].values[i],
                    response_df[features_cols].values[i],
                    feature_names=features_cols,
                    matplotlib=True
                )
                st.pyplot()
                # break

        else:
            st.error("Failed to upload files")
