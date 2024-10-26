from datetime import datetime as dt
import streamlit as st
import streamlit.components.v1 as components

print(dt.now(), "Analytics Visited")

st.set_page_config(layout="wide")

feature = st.selectbox(
    "Выберите макроэкономический показатель",
    ["МРОТ в регионе", "Средняя ЗП", "Население"],
)

if feature == "МРОТ в регионе":
    components.html(open("frontend/data/mrot.html", 'r', encoding='utf-8').read(), height=500)
elif feature == "Средняя ЗП":
    components.html(open("frontend/data/zp.html", 'r', encoding='utf-8').read(), height=500)
elif feature == "Население":
    components.html(open("frontend/data/people.html", 'r', encoding='utf-8').read(), height=500)