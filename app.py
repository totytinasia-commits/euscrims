import streamlit as st

# Configurazione della pagina (opzionale)
st.set_page_config(page_title="Statistiche Dashboard", layout="wide")

# CSS personalizzato per le card con dimensioni fisse e uguali
st.markdown("""
    <style>
    .stApp { 
        background-color: #121212; 
        color: #FFFFFF; 
    }
    
    /* Stile unificato per tutte le card metriche */
    .metric-card {
        background-color: #1e2229;
        border: 1px solid #2d333b;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        
        /* Forzatura dimensioni fisse e uguali per tutte le card */
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #93c5fd;
        font-weight: bold;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.1;
    }
    
    .metric-value {
        font-size: 1.5rem;
        color: #FFFFFF;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.subheader("📊 Pannello Statistiche")

# Dati di esempio (puoi sostituirli con i tuoi valori reali o calcolati)
val_one = 71
val_shit_one = 19
acc_one = "26.76%"

val_two = 230
val_shit_two = 15
acc_two = "6.52%"

# Prima riga di metriche
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Onehand</div>
            <div class="metric-value">{val_one}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Shit<br>Onehand</div>
            <div class="metric-value">{val_shit_one}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Acc% One</div>
            <div class="metric-value">{acc_one}</div>
        </div>
    """, unsafe_allow_html=True)

# Seconda riga di metriche
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Twohand</div>
            <div class="metric-value">{val_two}</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Shit<br>Twohand</div>
            <div class="metric-value">{val_shit_two}</div>
        </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Acc% Two</div>
            <div class="metric-value">{acc_two}</div>
        </div>
    """, unsafe_allow_html=True)
