import streamlit as st
import re
import random
import os
import time

# --- DATABASE RISPOSTE (Le tue 318 risposte) ---
RISPOSTE = {
    "1":"C","2":"A","3":"B","4":"C","5":"A","6":"B","7":"A","8":"B","9":"C","10":"B","11":"B","12":"A","13":"C","14":"A","15":"A","16":"B","17":"B","18":"C","19":"A","20":"C","21":"B","22":"A","23":"C","24":"A","25":"C","26":"B","27":"B","28":"B","29":"A","30":"B","31":"C","32":"A","33":"C","34":"B","35":"B","36":"A","37":"B","38":"C","39":"B","40":"A","41":"A","42":"B","43":"C","44":"C","45":"B","46":"A","47":"C","48":"A","49":"A","50":"B","51":"B","52":"C","53":"A","54":"C","55":"B","56":"A","57":"B","58":"C","59":"B","60":"A","61":"C","62":"C","63":"C","64":"B","65":"A","66":"B","67":"B","68":"C","69":"C","70":"A","71":"A","72":"B","73":"C","74":"A","75":"A","76":"B","77":"B","78":"C","79":"A","80":"A","81":"B","82":"A","83":"A","84":"C","85":"A","86":"A","87":"B","88":"C","89":"A","90":"B","91":"A","92":"B","93":"A","94":"C","95":"B","96":"A","97":"C","98":"C","99":"B","100":"B","101":"C","102":"B","103":"A","104":"C","105":"C","106":"A","107":"B","108":"A","109":"B","110":"C","111":"B","112":"B","113":"A","114":"C","115":"A","116":"C","117":"C","118":"B","119":"C","120":"C","121":"A","122":"C","123":"A","124":"B","125":"C","126":"B","127":"B","128":"A","129":"A","130":"C","131":"A","132":"C","133":"A","134":"A","135":"C","136":"B","137":"B","138":"A","139":"B","140":"A","141":"B","142":"B","143":"A","144":"B","145":"A","146":"C","147":"B","148":"C","149":"C","150":"C","151":"A","152":"C","153":"C","154":"A","155":"C","156":"A","157":"C","158":"B","159":"B","160":"C","161":"B","162":"C","163":"C","164":"A","165":"A","166":"B","167":"B","168":"A","169":"C","170":"C","171":"B","172":"A","173":"C","174":"C","175":"C","176":"B","177":"A","178":"C","179":"B","180":"C","181":"C","182":"A","183":"C","184":"C","185":"B","186":"A","187":"C","188":"B","189":"B","190":"A","191":"A","192":"B","193":"C","194":"A","195":"B","196":"C","197":"C","198":"B","199":"A","200":"C","201":"B","202":"A","203":"C","204":"A","205":"C","206":"A","207":"A","208":"B","209":"A","210":"C","211":"A","212":"B","213":"B","214":"A","215":"C","216":"A","217":"A","218":"B","219":"A","220":"B","221":"A","222":"A","223":"C","224":"A","225":"B","226":"A","227":"A","228":"C","229":"A","230":"A","231":"B","232":"A","233":"B","234":"A","235":"C","236":"A","237":"A","238":"B","239":"C","240":"B","241":"C","242":"B","243":"A","244":"B","245":"C","246":"B","247":"C","248":"A","249":"B","250":"B","251":"A","252":"B","253":"C","254":"C","255":"C","256":"B","257":"B","258":"C","259":"C","260":"B","261":"C","262":"C","263":"C","264":"A","265":"C","266":"B","267":"C","268":"C","269":"B","270":"B","271":"B","272":"A","273":"A","274":"C","275":"C","276":"B","277":"B","278":"C","279":"C","280":"B","281":"C","282":"B","283":"A","284":"B","285":"C","286":"B","287":"C","288":"A","289":"B","290":"B","291":"A","292":"B","293":"C","294":"C","295":"C","296":"B","297":"B","298":"C","299":"C","300":"B","301":"C","302":"C","303":"C","304":"A","305":"C","306":"B","307":"C","308":"C","309":"B","310":"B","311":"B","312":"A","313":"A","314":"C","315":"C","316":"B","317":"B","318":"C"
}

def pulisci_testo(t):
    # Rimuove virgolette e spazi multipli che rendono le domande brutte
    t = t.replace('"', '').replace('  ', ' ')
    return t.strip()

@st.cache_data
def prepara_dati():
    if not os.path.exists("quiz.csv"): return "File non trovato"
    try:
        with open("quiz.csv", "r", encoding="utf-8-sig") as f: testo = f.read()
    except:
        with open("quiz.csv", "r", encoding="latin-1") as f: testo = f.read()
    
    lista = []
    # Pattern migliorato per catturare meglio i testi sporchi di Excel
    pattern = r"(\d{1,3})\s+(.*?)\s+[Aa]\s*[\)\.]\s*(.*?)\s+[Bb]\s*[\)\.]\s*(.*?)\s+[Cc]\s*[\)\.]\s*(.*?)(?=\s+\d{1,3}\s+(?:.*?)[Aa]\s*[\)\.]|$)"
    trovate = re.finditer(pattern, testo, re.DOTALL | re.IGNORECASE)
    
    for m in trovate:
        id_q = m.group(1).strip()
        lista.append({
            "id": id_q,
            "q": pulisci_testo(m.group(2)),
            "a": pulisci_testo(m.group(3)),
            "b": pulisci_testo(m.group(4)),
            "c": pulisci_testo(m.group(5)),
            "corretta": RISPOSTE.get(id_q, "A")
        })
    return lista

st.set_page_config(page_title="Simulatore Esame Tartufo", layout="centered")

if 'esame_attivo' not in st.session_state:
    st.session_state.esame_attivo = False

def inizia_esame():
    db = prepara_dati()
    if isinstance(db, list):
        st.session_state.quiz_db = random.sample(db, min(30, len(db)))
        st.session_state.indice = 0
        st.session_state.errori = 0
        st.session_state.punti = 0
        st.session_state.inizio_tempo = time.time()
        st.session_state.esame_attivo = True
        st.session_state.finito = False
        st.session_state.risposta_data = False

# --- UI ---
if not st.session_state.esame_attivo:
    st.title("🍄 Simulatore Esame Tartufo")
    st.info("Configurazione: 30 domande | 30 minuti | Max 4 errori")
    if st.button("INIZIA SIMULAZIONE", use_container_width=True):
        inizia_esame()
        st.rerun()
else:
    # Timer
    trascorso = time.time() - st.session_state.inizio_tempo
    rimanente = max(0, 1800 - int(trascorso))
    mins, secs = divmod(rimanente, 60)
    
    # Header
    c1, c2, c3 = st.columns(3)
    c1.metric("Domanda", f"{st.session_state.indice + 1}/30")
    c2.metric("Tempo", f"{mins:02d}:{secs:02d}")
    c3.metric("Errori", f"{st.session_state.errori}/4")

    if rimanente <= 0 or st.session_state.errori >= 5:
        st.session_state.finito = True

    if not st.session_state.finito and st.session_state.indice < 30:
        item = st.session_state.quiz_db[st.session_state.indice]
        st.markdown(f"### {item['q']}")
        
        opzioni = [f"A) {item['a']}", f"B) {item['b']}", f"C) {item['c']}"]
        
        # Disabilita il radio dopo la conferma per evitare cambi
        scelta = st.radio("Scegli la risposta:", opzioni, index=None, key=f"r_{st.session_state.indice}", disabled=st.session_state.risposta_data)
        
        if not st.session_state.risposta_data:
            if st.button("Conferma Risposta", use_container_width=True):
                if scelta:
                    st.session_state.risposta_data = True
                    st.session_state.ultima_scelta = scelta[0]
                    if scelta[0] == item['corretta']:
                        st.session_state.punti += 1
                    else:
                        st.session_state.errori += 1
                    st.rerun()
                else:
                    st.warning("Seleziona un'opzione!")
        else:
            # Feedback visivo
            corretta = item['corretta']
            if st.session_state.ultima_scelta == corretta:
                st.success(f"✅ CORRETTO! La risposta è {corretta}")
            else:
                st.error(f"❌ SBAGLIATO! La tua risposta: {st.session_state.ultima_scelta}. La risposta corretta è: {corretta}")
            
            if st.button("Vai alla Prossima →", use_container_width=True):
                st.session_state.indice += 1
                st.session_state.risposta_data = False
                st.rerun()
    else:
        st.divider()
        if st.session_state.errori < 5 and rimanente > 0:
            st.balloons()
            st.header("🏆 ESAME SUPERATO!")
            st.write(f"Ottimo lavoro! Hai risposto correttamente a {st.session_state.punti} domande su 30.")
        else:
            st.header("❌ ESAME FALLITO")
            st.write(f"Hai commesso {st.session_state.errori} errori. Riprova per migliorare!")
        
        if st.button("Torna al Menu"):
            st.session_state.esame_attivo = False
            st.rerun()
