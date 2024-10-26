from io import StringIO
import json
import os
import base64

import pandas as pd
import numpy as np
import requests as rq
import streamlit as st
import shap
import matplotlib.pyplot as plt


def correct_names(names_list):
    with open(f'.{WORKDIR}/data/feature_naming.json', 'r', encoding='utf-8') as file:
        feature_naming_json = json.load(file)

    corrected_names = []

    for name in names_list:
        if name in feature_naming_json:
            corrected_names.append(feature_naming_json[name])
        else:
            correct_names.append(name)

    return corrected_names


def plot_shap_barchart(shap_values, feature_values, feature_names):
    # Создадим барчарт, показывающий вклад каждого признака
    fig, ax = plt.subplots(figsize=(10, 6))

    # Порядок и направление графика будут зависеть от значения shap_values
    indices = np.argsort(shap_values)
    
    # Определяем цвета: красный для положительных, синий для отрицательных
    colors = ['red' if shap > 0 else 'blue' for shap in shap_values[indices]]

    ax.barh(range(len(shap_values)), shap_values[indices], align='center', color=colors)
    ax.set_yticks(range(len(shap_values)))
    ax.set_yticklabels([f'{feature_names[i]}: {feature_values[i]}' for i in indices])

    ax.set_xlabel("Значимость признаков")

    plt.gca().invert_yaxis()  # Обратный порядок, чтобы самый положительный был сверху
    plt.tight_layout()
    
    return fig


BACKEND_URL = f"http://backend:{os.getenv('BACKEND_PORT')}"
WORKDIR = ""
# BACKEND_URL = f"http://0.0.0.0:8128"
# WORKDIR = "/frontend/"

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(page_title="DIGITAL HACK NN 2024", layout="wide")
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

                st.text(f"Данные клиента {row['accnt_id']} (сокращенные)")

                # Построение и отображение графика во второй колонке
                print(correct_names(features_cols))

                plot_shap_barchart(
                    row[shap_cols].values,
                    row[features_cols].values,
                    correct_names(features_cols)
                ).show()

                st.pyplot()

                with st.expander("Детальные данные клиента"):
                    # Табличные значения текущей записи
                    st.write(row.to_frame().T)

        else:
            st.error("Failed to upload files")