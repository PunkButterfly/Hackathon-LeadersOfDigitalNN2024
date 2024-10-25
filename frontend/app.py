from io import StringIO
import os

import pandas as pd
import requests as rq
import streamlit as st


BACKEND_URL = f"http://backend:{os.getenv('BACKEND_PORT')}"
# BACKEND_URL = f"http://0.0.0.0:8128"

st.header('Загрузите данные')
st.subheader('')

transactions = st.file_uploader('Загрузка файла с транзакциями')
clients = st.file_uploader('Загрузка файла с клиентами')

if transactions is not None and clients is not None:

    if st.button("Upload"):
        st.write('Данные загружены')
        post_data = {'transactions': transactions, 'clients': clients}

        request_files = {
            "transactions": (transactions.name, transactions, "text/csv"),
            "clients": (clients.name, clients, "text/csv"),
        }
        
        response = rq.post(f"{BACKEND_URL}/upload_csv/", files=request_files)

        if response.status_code == 200:
            csv_content = response.content.decode("utf-8")
            df = pd.read_csv(StringIO(csv_content))
            st.write("Generated CSV file:")
            st.dataframe(df)
        else:
            st.error("Failed to upload files")
