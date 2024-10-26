from io import StringIO
import os
import base64

import pandas as pd
import requests as rq
import streamlit as st
import shap

st.set_option('deprecation.showPyplotGlobalUse', False)

BACKEND_URL = f"http://backend:{os.getenv("BACKEND_PORT")}"
# BACKEND_URL = f"http://0.0.0.0:8128"

# st.set_page_config(page_title="DIGITAL HACK NN 2024", layout="wide")
st.header("Загрузите данные")

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

            # Создание CSV из DataFrame
            result_csv = response_df[["accnt_id", "erly_pnsn_flg"]].to_csv(
                sep=';',
                encoding = 'cp1251',
                index=False
            )

            result_b64 = base64.b64encode(result_csv.encode()).decode()  # Кодирование в строку base64

            # HTML и JavaScript для автоматической загрузки
            download_href = f'''
            <a href="data:file/csv;base64,{result_b64}" download="submission.csv">
                <script>
                    setTimeout(() => {{
                        var link = document.createElement('a');
                        link.href = 'data:file/csv;base64,{result_b64}';
                        link.download = 'submission.csv';
                        link.click();
                    }}, 100);
                </script>
                Скачать результат в формате для тестирования
            </a>
            '''

            st.markdown(download_href, unsafe_allow_html=True)

            cols = response_df.columns.to_list()
            features_cols = [col for col in cols if not col.startswith("shap") and col != "accnt_id"]
            shap_cols = [col for col in cols if col.startswith("shap") and col != "accnt_id" and col != "shap_base_value"]

            for i, (idx, row) in enumerate(response_df.iterrows()):
                # # Данные записи
                if row["erly_pnsn_flg"]:
                    header_text = f"""<h2>Клиент <span style='color:red;'> досрочно выйдет на пенсию</span></h2>"""
                else:
                    header_text = f"""<h2>Клиент не выйдет на пенсию досрочно</h2>"""
                
                # Использование HTML для стилизации текста
                st.markdown(header_text, unsafe_allow_html=True)
                # st.divider()
                # Создание колонок для отображения графика и данных
                col1, col2 = st.columns(2)

                with col1:
                    # Отображение таблицы в первой колонке
                    st.write("Данные клиента (сокращенные)")
                    selected_cols = ["accnt_id", "brth_yr", "erly_pnsn_flg"]
                    st.write(row[selected_cols].to_frame().T)  # Один ряд DataFrame


                with st.expander("Детальные данные клиента"):
                    # Табличные значения текущей записи
                    st.write(row.to_frame().T)

                with col2:
                    # Построение и отображение графика во второй колонке
                    shap.force_plot(
                        response_df["shap_base_value"].values[i],
                        response_df[shap_cols].values[i],
                        response_df[features_cols].values[i],
                        feature_names=features_cols,
                        matplotlib=True
                    )
                    st.pyplot()

        else:
            st.error("Failed to upload files")
