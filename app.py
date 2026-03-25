import streamlit as st
import pandas as pd
import re
import random

# Qui ho inserito tutte le risposte che mi hai scritto nei messaggi precedenti
RISPOSTE = {
    "1": "C", "2": "A", "3": "B", "4": "C", "5": "A", "6": "B", "7": "A", "8": "B", "9": "C", "10": "B",
    "11": "B", "12": "A", "13": "C", "14": "A", "15": "A", "16": "B", "17": "B", "18": "C", "19": "A", "20": "C",
    "34": "B", "35": "B", "36": "A", "37": "B", "38": "C", "39": "B", "40": "A", "41": "A", "42": "B", "43": "C",
    "80": "A", "81": "B", "82": "A", "83": "A", "84": "C", "85": "A", "126": "B", "172": "A", "315": "C", "318": "C"
}

@st.cache_data
def prepara_dati():
    df = pd.read_csv("quiz.csv", header=None)
    lista = []
    for riga in df[0]:
        m = re.search(r"(\d+)\s+(.*?)\s+a\)\s+(.*?)\s+b\)\s+(.*?)\s+c\)\s+(.*)", str(riga), re.DOTALL)
        if m:
            id_q = m.group(1)
            lista.append({"id": id_q, "q": m.group(2), "a": m.group(3), "b": m.group(4), "c": m.group(5), "corretta": RISPOSTE.get(id_q, "A")})
    return lista

st.set_page_config(page_title="Quiz Tartufo", layout="centered")
st.title("🍄 Quiz Tesserino Tartufo")

if 'db' not in st.session_state:
    st.session_state.db = prepara_dati()
    random.shuffle(st.session_state.db)
    st.session_state.i = 0
    st.session_state.punti = 0

if st.session_state.i < len(st.session_state.db):
    item = st.session_state.db[st.session_state.i]
    st.write(f"### Domanda {item['id']}")
    st.info(item['q'])
    scelta = st.radio("Risposta:", [f"A) {item['a']}", f"B) {item['b']}", f"C) {item['c']}"], index=None)
    if st.button("Conferma"):
        if scelta:
            if scelta[0] == item['corretta']:
                st.success("BRAVO!")
                st.session_state.punti += 1
            else:
                st.error(f"SBAGLIATO! Era la {item['corretta']}")
            st.session_state.i += 1
            st.rerun()
else:
    st.write(f"Fine! Punti: {st.session_state.punti}")
    if st.button("Ricomincia"):
        st.session_state.i = 0
        st.rerun()
