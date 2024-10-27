from io import StringIO
import json
import base64

import os
import pandas as pd
import numpy as np
import requests as rq
import streamlit as st
import matplotlib.pyplot as plt

from map import draw_map


# def correct_names(names_list):
#     with open(f'.{WORKDIR}/data/feature_naming.json', 'r', encoding='utf-8') as file:
#         feature_naming_json = json.load(file)
#
#     corrected_names = []
#
#     for name in names_list:
#         if name in feature_naming_json:
#             corrected_names.append(feature_naming_json[name])
#         else:
#             corrected_names.append(name)
#
#     return corrected_names


def plot_shap_barchart(shap_values_raw, feature_values_raw, feature_names_raw):
    shap_values = []
    feature_values = []
    feature_names = []

    for i in range(len(shap_values_raw)):
        if abs(shap_values_raw[i]) > 0.005:
            shap_values.append(shap_values_raw[i])
            feature_values.append(feature_values_raw[i])
            feature_names.append(feature_names_raw[i])

    shap_values = np.array(shap_values)
    feature_values = np.array(feature_values)
    feature_names = np.array(feature_names)

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

if 'upload' not in st.session_state:
    st.session_state['upload'] = False

BACKEND_URL = f"http://backend:{os.getenv('BACKEND_PORT')}"
WORKDIR = ""
# BACKEND_URL = f"http://158.160.17.229:8228"
# WORKDIR = "/frontend/"

with open(f'.{WORKDIR}/data/feature_naming.json', 'r', encoding='utf-8') as file:
    feature_naming_json = dict(json.load(file))

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
        st.session_state.upload = True

    if st.session_state.upload:

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

            # HTML и JavaScript для формирования ссылки
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
                <h3> <span style='color:blue;'>Скачать результат в формате для тестирования </span></h3>
            </a>
            '''

            st.markdown(download_href, unsafe_allow_html=True)

            st.write('---')
            st.header('Детализация по клиентам')

            st.subheader(
                '''
                :blue[СИНИЕ] показатели вносят вклад в то, что клиент НЕ выйдет на пенсию досрочно.
                '''
            )
            st.subheader(
                '''
                :red[КРАСНЫЕ] показатели вносят вклад в то, что клиент выйдет на пенсию досрочно.
                '''
            )
            # st.subheader(
            #     '''
            #     Чем больше абсолютное значение показателя, тем больше вклад показателя в итоговое решение.
            #     '''
            # )

            cols = response_df.columns.to_list()
            features_cols = [col for col in cols if not col.startswith("shap") and col != "accnt_id"]
            shap_cols = [col for col in cols if col.startswith("shap") and col != "accnt_id" and col != "shap_base_value"]

            for i, (idx, row) in enumerate(response_df.iterrows()):
                # # Данные записи
                if row["erly_pnsn_flg"]:
                    header_text = f"""<h3>Клиент {row['accnt_id']} <span style='color:red;'> досрочно выйдет на пенсию</span></h3>"""
                else:
                    header_text = f"""<h3>Клиент {row['accnt_id']} не выйдет на пенсию досрочно</h3>"""

                # Использование HTML для стилизации текста
                st.markdown(header_text, unsafe_allow_html=True)

                # Построение и отображение графика во второй колонке
                plot_shap_barchart(
                    row[shap_cols].values,
                    row[features_cols].values,
                    list(map(lambda x: feature_naming_json.get(x, x), features_cols))
                ).show()

                st.pyplot()

                with st.expander("Детальные данные клиента"):
                    # Табличные значения текущей записи
                    st.write(row.to_frame().T)

                # Ограничение количества записей, чтобы не перегружать процессор, так как отрисовка графиков долгая
                if i > 6:
                    break

            st.write('---')
            st.header('Средний вклад показателя по регионам')

            map_cols = shap_cols.copy()
            map_cols.append('okato')

            snap_cols = response_df.columns.values[list(map(lambda x: x.startswith('shap'), response_df.columns.values))]
            agg_df = response_df.groupby('okato', as_index=False).agg({k: 'mean' for k in snap_cols})

            selected_map_col = st.selectbox(
                "Выберите показатель",
                list(map(lambda x: feature_naming_json.get(x, x), features_cols))
            )

            selected_map_col = "shap_" + str({v: k for k, v in feature_naming_json.items()}.get(selected_map_col, selected_map_col))

            draw_map(agg_df, selected_map_col)

        else:
            st.error("Failed to upload files")