import streamlit as st
import pandas as pd
import re
import random

# --- 1. TUTTE LE 318 RISPOSTE (CARICATE) ---
RISPOSTE = {
    "1":"C","2":"A","3":"B","4":"C","5":"A","6":"B","7":"A","8":"B","9":"C","10":"B","11":"B","12":"A","13":"C","14":"A","15":"A","16":"B","17":"B","18":"C","19":"A","20":"C","21":"B","22":"A","23":"C","24":"A","25":"C","26":"B","27":"B","28":"B","29":"A","30":"B","31":"C","32":"A","33":"C",
    "34":"B","35":"B","36":"A","37":"B","38":"C","39":"B","40":"A","41":"A","42":"B","43":"C","44":"C","45":"B","46":"A","47":"C","48":"A","49":"A","50":"B","51":"B","52":"C","53":"A","54":"C","55":"B","56":"A","57":"B","58":"C","59":"B","60":"A","61":"C","62":"C","63":"C","64":"B","65":"A","66":"B","67":"B","68":"C","69":"C","70":"A","71":"A","72":"B","73":"C","74":"A","75":"A","76":"B","77":"B","78":"C","79":"A","80":"A","81":"B","82":"A","83":"A","84":"C","85":"A","86":"A","87":"B","88":"C","89":"A","90":"B","91":"A","92":"B",
    "93":"A","94":"C","95":"B","96":"A","97":"C","98":"C","99":"B","100":"B","101":"C","102":"B","103":"A","104":"C","105":"C","106":"A","107":"B","108":"A","109":"B","110":"C","111":"B","112":"B","113":"A","114":"C","115":"A","116":"C","117":"C","118":"B","119":"C","120":"C","121":"A","122":"C","123":"A","124":"B","125":"C","126":"B","127":"B","128":"A","129":"A","130":"C","131":"A","132":"C","133":"A","134":"A","135":"C","136":"B","137":"B","138":"A","139":"B","140":"A","141":"B","142":"B","143":"A","144":"B","145":"A","146":"C","147":"B","148":"C","149":"C","150":"C","151":"A","152":"C","153":"C","154":"A","155":"C","156":"A","157":"C","158":"B","159":"B","160":"C","161":"B","162":"C","163":"C","164":"A","165":"A","166":"B","167":"B","168":"A","169":"C","170":"C","171":"B","172":"A","173":"C","174":"C","175":"C","176":"B","177":"A","178":"C","179":"B","180":"C","181":"C","182":"A","183":"C","184":"C",
    "185":"B","186":"A","187":"C","188":"B","189":"B","190":"A","191":"A","192":"B","193":"C","194":"A","195":"B","196":"C","197":"C","198":"B","199":"A","200":"C","201":"B","202":"A","203":"C","204":"A","205":"C","206":"A","207":"A","208":"B","209":"A","210":"C","211":"A","212":"B","213":"B","214":"A","215":"C","216":"A","217":"A","218":"B","219":"A","220":"B","221":"A","222":"A","223":"C","224":"A","225":"B","226":"A","227":"A","228":"C","229":"A","230":"A","231":"B","232":"A","233":"B","234":"A","235":"C","236":"A","237":"A","238":"B","239":"C","240":"B","241":"C","242":"B","243":"A","244":"B","245":"C","246":"B","247":"C","248":"A","249":"B","250":"B","251":"A","252":"B","253":"C","254":"C","255":"C","256":"B","257":"B","258":"C","259":"C","260":"B","261":"C","262":"C","263":"C","264":"A","265":"C","266":"B","267":"C","268":"C","269":"B","270":"B","271":"B","272":"A","273":"A","274":"C","275":"C","276":"B","277":"B","278":"C","279":"C","280":"B","281":"C","282":"B","283":"A","284":"B","285":"C","286":"B","287":"C","288":"A","289":"B","290":"B","291":"A","292":"B","293":"C","294":"C","295":"C","296":"B","297":"B","298":"C","299":"C","300":"B","301":"C","302":"C","303":"C","304":"A","305":"C","306":"B","307":"C","308":"C","309":"B","310":"B","311":"B","312":"A","313":"A","314":"C","315":"C","316":"B","317":"B","318":"C"
}

@st.cache_data
def prepara_dati():
    # Leggiamo il file come testo puro per evitare errori con le virgole
    try:
        with open("quiz.csv", "r", encoding="utf-8") as f:
            linee = f.readlines()
    except:
        with open("quiz.csv", "r", encoding="latin-1") as f:
            linee = f.readlines()
            
    lista = []
    for riga in linee:
        riga = riga.strip().strip('"') # Pulisce la riga da spazi e virgolette di Excel
        # Cerca Numero, Domanda e le tre opzioni a) b) c)
        m = re.search(r"(\d+)\s+(.*?)\s+a\)\s+(.*?)\s+b\)\s+(.*?)\s+c\)\s+(.*)", riga, re.DOTALL)
        if m:
            id_q = m.group(1)
            lista.append({
                "id": id_q,
                "q": m.group(2).strip(),
                "a": m.group(3).strip(),
                "b": m.group(4).strip(),
                "c": m.group(5).strip(),
                "corretta": RISPOSTE.get(id_q, "A")
            })
    return lista

# --- INTERFACCIA ---
st.set_page_config(page_title="Quiz Tartufo", layout="centered")
st.title("🍄 Quiz Tesserino Tartufo")

if 'db' not in st.session_state:
    st.session_state.db = prepara_dati()
    if not st.session_state.db:
        st.error("Errore: Non sono riuscito a leggere le domande dal file quiz.csv. Controlla il formato!")
    else:
        random.shuffle(st.session_state.db)
    st.session_state.i = 0
    st.session_state.punti = 0

if st.session_state.i < len(st.session_state.db):
    item = st.session_state.db[st.session_state.i]
    st.write(f"### Domanda {item['id']}")
    st.info(item['q'])
    
    opzioni = [f"A) {item['a']}", f"B) {item['b']}", f"C) {item['c']}"]
    scelta = st.radio("Scegli la risposta corretta:", opzioni, index=None)
    
    if st.button("Conferma Risposta", use_container_width=True):
        if scelta:
            lettera = scelta[0]
            if lettera == item['corretta']:
                st.success("✅ ESATTO!")
                st.session_state.punti += 1
            else:
                st.error(f"❌ SBAGLIATO! La risposta corretta era la {item['corretta']}")
            
            st.session_state.i += 1
            st.button("Avanti")
        else:
            st.warning("Seleziona una risposta!")
else:
    st.balloons()
    st.header("🏆 Quiz Terminato!")
    st.write(f"Hai totalizzato {st.session_state.punti} punti su {len(st.session_state.db)}.")
    if st.button("Ricomincia"):
        st.session_state.i = 0
        st.session_state.punti = 0
        random.shuffle(st.session_state.db)
        st.rerun()
