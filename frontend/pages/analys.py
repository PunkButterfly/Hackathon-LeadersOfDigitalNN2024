from datetime import datetime as dt
import streamlit as st
import streamlit.components.v1 as components

# WORKDIR = "./frontend/"
WORKDIR = ""

print(dt.now(), "Analytics Visited")

st.set_page_config(layout="wide")

feature = st.selectbox(
    "Выберите макроэкономический показатель",
    ["МРОТ в регионе", "Средняя ЗП", "Население"],
)

if feature == "МРОТ в регионе":
    components.html(open(f".{WORKDIR}/data/mrot.html", 'r', encoding='utf-8').read(), height=500)
elif feature == "Средняя ЗП":
    components.html(open(f".{WORKDIR}/data/zp.html", 'r', encoding='utf-8').read(), height=500)
elif feature == "Население":
    components.html(open(".{WORKDIR}/data/people.html", 'r', encoding='utf-8').read(), height=500)