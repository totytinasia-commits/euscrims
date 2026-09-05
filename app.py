import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import time

# 1. Page Configuration
st.set_page_config(page_title="Eu Scrims Club", layout="centered")

# 2. CSS for Dark Mode, buttons, clean tables, and fixed-height metric cards
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    
    div[data-testid="stDataFrame"] { background-color: #000000; width: 100% !important; }
    div[data-testid="stDataFrame"] div[data-baseweb="block"] { background-color: #000000 !important; }
    div[data-testid="stDataFrame"] table, tr, th, td {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-color: #FFFFFF !important;
        font-size: 11px !important;
    }

    .stButton button {
        background-color: #FFD700 !important;
        color: #00008B !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        border: none !important;
        width: 100% !important;
        height: 40px !important;
        white-space: nowrap !important;
    }
    .stButton button:hover { background-color: #FFC000 !important; color: #0000FF !important; }
    
    .stat-card {
        background-color: #1e2229;
        border: 1px solid #2d333b;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
        height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #93c5fd;
        font-weight: bold;
        margin-bottom: 4px;
        text-transform: uppercase;
        line-height: 1.1;
    }
    .stat-value {
        font-size: 1.1rem;
        color: #FFFFFF;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Page state management
if 'page' not in st.session_state:
    st.session_state.page = 'Player'

# Init Connection General
@st.cache_resource
def init_connection():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def ottieni_credenziali():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds_dict = dict(st.secrets["gcp_service_account"])
        return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    except Exception:
        return None

SHEET_ID_STATS = '1VrMCI4AA5zpflxulMVRpjRkVlhpzPHHYj24lSI1LfTw'
GID_PERSONAL_STATS = '869033822'

def scrivi_cella_per_gid(gid, cell_address, value):
    try:
        creds = ottieni_credenziali()
        if creds:
            client = gspread.authorize(creds)
            sheet = client.open_by_key(SHEET_ID_STATS)
            target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(gid).strip()), None)
            if target_ws:
                target_ws.update_acell(cell_address, value)
    except Exception:
        pass

# 3. Aligned Main Layout
col1, col2, col3 = st.columns([1, 2, 1]) 

with col2:
    if os.path.exists("logop.png"): st.image("logop.png", use_container_width=True)
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("REGISTERED PLAYERS", use_container_width=True): st.session_state.page = 'Player'
    if st.button("REGISTERED TEAMS", use_container_width=True): st.session_state.page = 'Teams'
    if st.button("RULES \ SETTING", use_container_width=True): st.session_state.page = 'Rules'
    if st.button("SCRIMS RESULT", use_container_width=True): st.session_state.page = 'Scrims'
    if st.button("PERSONAL STATS", use_container_width=True): st.session_state.page = 'Stats'
    if st.button("STAT COMP", use_container_width=True): st.session_state.page = 'STAT COMP'
    
    page = st.session_state.page

    if page == 'Rules':
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>SCORE</h2>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Details": ["1 KILL = 1 POINT", "250 DMG = 1 POINTS", "", "", ""],
            "Placement": ["1st SCORE X", "2nd SCORE X", "3rd SCORE X", "4th SCORE X", "5th or low SCORE X"],
            "Multiplier": ["1,2", "1,1", "1,05", "1", "1"]
        }), use_container_width=True, hide_index=True)
        
        st.markdown("<br><h2 style='text-align: center; color: #FFD700;'>EU SCRIMS MAPS</h2>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Setting": ["SPEED", "HOLD TIME", "ZONE DEMAGE"], "Value": ["120%", "70%", "120%"]}), use_container_width=True, hide_index=True)
        st.markdown("<h3 style='text-align: center; color: #FFD700;'>GENERAL RULES</h3>", unsafe_allow_html=True)
        st.markdown("- **THE SCRIMS IS 5 MATCHES**\n- **FIRST GAME STARTS 5 MIN AFTER SCHEDULED TIME**\n- **LAST MINUTE SUBS GOES THROUGH ADMINS**\n- **USE THE SAME IGN**")

    elif page == 'Teams':
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>TEAMS</h2>", unsafe_allow_html=True)
        try:
            ws = init_connection().open_by_key('1qfq7X9IuAcWEhFUuUbNkFfY2ssrmt04r1MFiaCC6ql0').worksheet("LOBBY / RULES")
            rows = ws.get('F7:K13')
            for i, row in enumerate(rows):
                while len(row) < 6: row.append("")
                st.markdown(f"<p style='color: #FFD700; font-weight: bold;'>Team {i+1}</p>", unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(row, columns=["TEAMS"]), use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error: {e}")

    elif page == 'Scrims':
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>SCRIMS</h2>", unsafe_allow_html=True)
        try:
            ws = init_connection().open_by_key('1qfq7X9IuAcWEhFUuUbNkFfY2ssrmt04r1MFiaCC6ql0').get_worksheet_by_id(823408140)
            
            col_raw = ws.get('E8:E15')
            col_e = [r[0] if (r and len(r) > 0 and r[0] is not None) else "" for r in col_raw]
            while len(col_e) < 8: col_e.append("")
            
            for g, rng in [("Game 1", "F8:H15"), ("Game 2", "J8:L15"), ("Game 3", "N8:P15"), ("Game 4", "R8:T15"), ("Game 5", "V8:X15")]:
                st.markdown(f"<h3 style='text-align: center; color: #FFD700;'>{g}</h3>", unsafe_allow_html=True)
                data = ws.get(rng)
                rows = []
                for idx in range(8):
                    r = data[idx] if idx < len(data) else []
                    rows.append({
                        "team": col_e[idx], 
                        "pos": r[0] if len(r)>0 else "", 
                        "kill": r[1] if len(r)>1 else "", 
                        "dmg": r[2] if len(r)>2 else ""
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            
            st.markdown("<h3 style='text-align: center; color: #FFD700;'>Total Score</h3>", unsafe_allow_html=True)
            
            data_score = ws.get('AE8:AF15')
            teams = []
            points = []
            
            for i in range(8):
                if i < len(data_score):
                    row = data_score[i]
                    teams.append(row[0] if (len(row) > 0 and row[0] is not None) else "")
                    points.append(row[1] if (len(row) > 1 and row[1] is not None) else "")
                else:
                    teams.append("")
                    points.append("")
            
            df_score = pd.DataFrame({
                "Position": range(1, 9), 
                "Team": teams, 
                "Points": points
            })
            
            st.dataframe(df_score, use_container_width=True, hide_index=True)
            
        except Exception as e: 
            st.error(f"Error: {e}")

    elif page == 'Stats':
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>STATS</h2>", unsafe_allow_html=True)
        try:
            ws = init_connection().open_by_key(SHEET_ID_STATS).get_worksheet_by_id(1732621049)
            raw_data = ws.get('D11:K35')
            
            player_data_dict = {}
            for r in raw_data:
                while len(r) < 8: r.append("")
                
                p_kill, val_kill = str(r[0]).strip(), str(r[1]).strip()
                if p_kill and p_kill.upper() not in ["NAN", "NONE", ""]:
                    if p_kill not in player_data_dict: player_data_dict[p_kill] = {"K": 0, "D": 0, "MVP": 0, "DEA": 0}
                    player_data_dict[p_kill]["K"] = val_kill if val_kill else 0
                
                p_dmg, val_dmg = str(r[2]).strip(), str(r[3]).strip()
                if p_dmg and p_dmg.upper() not in ["NAN", "NONE", ""]:
                    if p_dmg not in player_data_dict: player_data_dict[p_dmg] = {"K": 0, "D": 0, "MVP": 0, "DEA": 0}
                    player_data_dict[p_dmg]["D"] = val_dmg if val_dmg else 0

                p_mvp, val_mvp = str(r[4]).strip(), str(r[5]).strip()
                if p_mvp and p_mvp.upper() not in ["NAN", "NONE", ""]:
                    if p_mvp not in player_data_dict: player_data_dict[p_mvp] = {"K": 0, "D": 0, "MVP": 0, "DEA": 0}
                    player_data_dict[p_mvp]["MVP"] = val_mvp if val_mvp else 0

                p_dea, val_dea = str(r[6]).strip(), str(r[7]).strip()
                if p_dea and p_dea.upper() not in ["NAN", "NONE", ""]:
                    if p_dea not in player_data_dict: player_data_dict[p_dea] = {"K": 0, "D": 0, "MVP": 0, "DEA": 0}
                    player_data_dict[p_dea]["DEA"] = val_dea if val_dea else 0

            rows = [{"Player": k, **v} for k, v in player_data_dict.items()]
            df = pd.DataFrame(rows)
            
            if not df.empty:
                df['K'] = pd.to_numeric(df['K'], errors='coerce').fillna(0)
                df = df.sort_values(by="K", ascending=False).reset_index(drop=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e: 
            st.error(f"Error: {e}")

    elif page == 'STAT COMP':
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>STAT COMP</h2>", unsafe_allow_html=True)
        
        target_ws = None
        current_d13_val = ""
        extracted_players = []

        try:
            creds = ottieni_credenziali()
            if creds:
                client = gspread.authorize(creds)
                sheet = client.open_by_key(SHEET_ID_STATS)
                target_ws = next((ws for ws in sheet.worksheets() if str(ws.id).strip() == str(GID_PERSONAL_STATS).strip()), None)
                
                if target_ws:
                    d13_raw = target_ws.acell("D13").value
                    if d13_raw is not None and str(d13_raw).strip() != "":
                        current_d13_val = str(d13_raw).strip()
                    
                    col_c_values = target_ws.get("C12:C60")
                    for row in col_c_values:
                        if row and len(row) > 0:
                            p = str(row[0]).strip()
                            if p and p.lower() not in ["nan", "none", ""]:
                                extracted_players.append(p)
                    extracted_players = list(dict.fromkeys(extracted_players))
        except Exception as e:
            st.warning(f"Error reading initial Personal Stats sheet: {e}")

        if not extracted_players:
            extracted_players = ["No players available"]

        player_index = 0
        if current_d13_val in extracted_players:
            player_index = extracted_players.index(current_d13_val)

        selected_d13_val = st.selectbox("Select Player", extracted_players, index=player_index, key="sb_player_d13")
        
        if str(selected_d13_val).strip().lower() != str(current_d13_val).strip().lower():
            scrivi_cella_per_gid(GID_PERSONAL_STATS, "D13", selected_d13_val)
            st.rerun()

        with st.spinner("Updating data..."):
            time.sleep(0.2)

        st.markdown("---")

        def format_val(val, is_percentage=False, decimals=2):
            try:
                if val is None or str(val).strip() == "" or str(val).strip().lower() in ["nan", "none", "#n/a", "#valore!"]:
                    return "0.00%" if is_percentage else "0"
                clean_val = str(val).replace("%", "").strip().replace(",", ".")
                num = float(clean_val)
                factor = 10 ** decimals
                truncated = int(num * factor) / factor
                if is_percentage:
                    return f"{truncated:.{decimals}f}%"
                elif truncated.is_integer():
                    return str(int(truncated))
                else:
                    return f"{truncated:.{decimals}f}"
            except Exception:
                return str(val) if val is not None and str(val).strip() != "" else ("0.00%" if is_percentage else "0")

        summary_fired, summary_hit, summary_acc, summary_kill, summary_dmg, summary_mvp, summary_death, summary_assist = "0", "0", "0.00%", "0", "0", "0", "0", "0"
        summary_revive, summary_oh_shots, summary_oh_hit, summary_oh_acc = "0", "0", "0", "0.00%"
        summary_th_shots, summary_th_hit, summary_th_acc = "0", "0", "0.00%"
        
        faster_banana_val = "-"
        
        deadliest_weapons = []
        weapon_rows_data = []

        try:
            if target_ws:
                f16_s16 = target_ws.get("F16:T16")
                if f16_s16 and len(f16_s16) > 0:
                    rv = f16_s16[0]
                    summary_fired    = format_val(rv[0] if len(rv) > 0 else 0)
                    summary_hit      = format_val(rv[1] if len(rv) > 1 else 0)
                    summary_acc      = format_val(rv[2] if len(rv) > 2 else 0, is_percentage=True)
                    summary_kill     = format_val(rv[3] if len(rv) > 3 else 0)
                    summary_dmg      = format_val(rv[4] if len(rv) > 4 else 0)
                    summary_mvp      = format_val(rv[5] if len(rv) > 5 else 0)
                    summary_death    = format_val(rv[6] if len(rv) > 6 else 0)
                    summary_revive   = format_val(rv[7] if len(rv) > 7 else 0)
                    summary_assist   = format_val(rv[8] if len(rv) > 8 else 0)  # Colonna R (Assist)
                    summary_oh_shots = format_val(rv[9] if len(rv) > 9 else 0)  # Colonna N
                    summary_oh_hit   = format_val(rv[10] if len(rv) > 10 else 0) # Colonna O
                    summary_oh_acc   = format_val(rv[11] if len(rv) > 11 else 0, is_percentage=True) # Colonna P
                    summary_th_shots = format_val(rv[12] if len(rv) > 12 else 0) # Colonna Q
                    summary_th_hit   = format_val(rv[13] if len(rv) > 13 else 0) # Colonna R
                    summary_th_acc   = format_val(rv[14] if len(rv) > 14 else 0, is_percentage=True) # Colonna S

                j18_l18 = target_ws.get("J18:L18")
                if j18_l18 and len(j18_l18) > 0 and len(j18_l18[0]) > 0:
                    faster_banana_val = format_val(j18_l18[0][0])

                dw_configs = [
                    {"name_range": "H20:I20", "data_range": "H21:S21"},
                    {"name_range": "H23:I23", "data_range": "H24:S24"},
                    {"name_range": "H26:I26", "data_range": "H27:S27"}
                ]

                for cfg in dw_configs:
                    n_data = target_ws.get(cfg["name_range"])
                    w_name = "-"
                    if n_data and len(n_data) > 0:
                        row_n = n_data[0]
                        for cell in row_n:
                            val_str = str(cell).strip()
                            if val_str and val_str.lower() not in ["nan", "none", ""]:
                                w_name = val_str
                                break

                    r_data = target_ws.get(cfg["data_range"])
                    if r_data and len(r_data) > 0:
                        r_w = r_data[0]
                        deadliest_weapons.append({
                            "name": w_name,
                            "dmg": format_val(r_w[3] if len(r_w) > 3 else 0),
                            "acc": format_val(r_w[4] if len(r_w) > 4 else 0, is_percentage=True),
                            "onehand": format_val(r_w[6] if len(r_w) > 6 else 0),
                            "shit_onehand": format_val(r_w[7] if len(r_w) > 7 else 0),
                            "acc_onehand": format_val(r_w[8] if len(r_w) > 8 else 0, is_percentage=True),
                            "twohand": format_val(r_w[9] if len(r_w) > 9 else 0),
                            "shit_twohand": format_val(r_w[10] if len(r_w) > 10 else 0),
                            "acc_twohand": format_val(r_w[11] if len(r_w) > 11 else 0, is_percentage=True)
                        })
                    else:
                        deadliest_weapons.append({
                            "name": w_name, "dmg": "0", "acc": "0.00%", 
                            "onehand": "0", "shit_onehand": "0", "acc_onehand": "0.00%", 
                            "twohand": "0", "shit_twohand": "0", "acc_twohand": "0.00%"
                        })

                # Mappatura tabella armi dettagliate con indici corretti
                weapons_raw = target_ws.get("F33:S74")
                if weapons_raw:
                    for r_data in weapons_raw:
                        if r_data and len(r_data) > 0:
                            w_name = str(r_data[0]).strip()
                            if w_name and w_name.upper() not in ["NAN", "NONE", ""]:
                                weapon_rows_data.append({
                                    "WEAPON": w_name,
                                    "TOT SHOTS": format_val(r_data[1] if len(r_data) > 1 else 0),
                                    "SHOT HIT": format_val(r_data[2] if len(r_data) > 2 else 0),
                                    "ACC%": format_val(r_data[3] if len(r_data) > 3 else 0, is_percentage=True),
                                    "DMG": format_val(r_data[4] if len(r_data) > 4 else 0),
                                    "HEADSHOT": format_val(r_data[5] if len(r_data) > 5 else 0),
                                    "MAX DISTANCE": format_val(r_data[6] if len(r_data) > 6 else 0),
                                    "SHOT ONE": format_val(r_data[8] if len(r_data) > 8 else 0),          # Colonna N
                                    "SHOT HIT ONE": format_val(r_data[9] if len(r_data) > 9 else 0),      # Colonna O
                                    "ACC% ONE": format_val(r_data[10] if len(r_data) > 10 else 0, is_percentage=True), # Colonna P
                                    "SHOT TWO": format_val(r_data[11] if len(r_data) > 11 else 0),        # Colonna Q
                                    "SHOT HIT TWO": format_val(r_data[12] if len(r_data) > 12 else 0),    # Colonna R
                                    "ACC% TWO": format_val(r_data[13] if len(r_data) > 13 else 0, is_percentage=True)  # Colonna S
                                })
        except Exception as e:
            st.warning(f"Error reading dashboard data: {e}")

        # --- RENDER UI: MATCH SUMMARY ---
        st.markdown("<h4 style='color: #93c5fd; font-size: 1rem;'>MATCH SUMMARY</h4>", unsafe_allow_html=True)
        c_grid1, c_grid2, c_grid3 = st.columns(3)
        
        with c_grid1:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>DMG</div><div class='stat-value'>{summary_dmg}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>SHOTS FIRED</div><div class='stat-value'>{summary_fired}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>DEATH</div><div class='stat-value'>{summary_death}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND SHOTS</div><div class='stat-value'>{summary_oh_shots}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND SHOTS</div><div class='stat-value'>{summary_th_shots}</div></div>", unsafe_allow_html=True)

        with c_grid2:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>KILL</div><div class='stat-value'>{summary_kill}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>SHOTS HIT</div><div class='stat-value'>{summary_hit}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>REVIVE</div><div class='stat-value'>{summary_revive}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND HIT</div><div class='stat-value'>{summary_oh_hit}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND HIT</div><div class='stat-value'>{summary_th_hit}</div></div>", unsafe_allow_html=True)

        with c_grid3:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>MVP</div><div class='stat-value'>{summary_mvp}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ACCURACY</div><div class='stat-value'>{summary_acc}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ASSISTS</div><div class='stat-value'>{summary_assist}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND ACC%</div><div class='stat-value'>{summary_oh_acc}</div></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND ACC%</div><div class='stat-value'>{summary_th_acc}</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- RENDER UI: DEADLIEST WEAPONS (1, 2, 3) IN BOXES ---
        st.markdown("<h4 style='color: #93c5fd; font-size: 1rem;'>DEADLIEST WEAPONS</h4>", unsafe_allow_html=True)
        
        for i, dw in enumerate(deadliest_weapons):
            st.markdown(f"""
            <div style='background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
                <p style='color: #93c5fd; font-weight: bold; font-size: 1.1rem; margin-top: 0; margin-bottom: 12px; text-align: center;'>
                    Deadliest Weapon {i+1}: {dw['name']}
                </p>
            """, unsafe_allow_html=True)
            
            dw_r1_c1, dw_r1_c2 = st.columns(2)
            with dw_r1_c1:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>DMG</div><div class='stat-value'>{dw['dmg']}</div></div>", unsafe_allow_html=True)
            with dw_r1_c2:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC%</div><div class='stat-value'>{dw['acc']}</div></div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

            dw_r2_c1, dw_r2_c2, dw_r2_c3 = st.columns(3)
            with dw_r2_c1:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>ONEHAND</div><div class='stat-value'>{dw['onehand']}</div></div>", unsafe_allow_html=True)
            with dw_r2_c2:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>SHIT ONEHAND</div><div class='stat-value'>{dw['shit_onehand']}</div></div>", unsafe_allow_html=True)
            with dw_r2_c3:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC% ONE</div><div class='stat-value'>{dw['acc_onehand']}</div></div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

            dw_r3_c1, dw_r3_c2, dw_r3_c3 = st.columns(3)
            with dw_r3_c1:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>TWOHAND</div><div class='stat-value'>{dw['twohand']}</div></div>", unsafe_allow_html=True)
            with dw_r3_c2:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>SHIT TWOHAND</div><div class='stat-value'>{dw['shit_twohand']}</div></div>", unsafe_allow_html=True)
            with dw_r3_c3:
                st.markdown(f"<div class='stat-card'><div class='stat-label'>ACC% TWO</div><div class='stat-value'>{dw['acc_twohand']}</div></div>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- RENDER UI: WEAPON PERFORMANCE TABLE ---
        st.markdown("<h4 style='color: #93c5fd; text-align: center;'>WEAPON PERFORMANCE</h4>", unsafe_allow_html=True)
        
        if weapon_rows_data:
            df_weapons_final = pd.DataFrame(weapon_rows_data)
        else:
            df_weapons_final = pd.DataFrame(columns=[
                "WEAPON", "TOT SHOTS", "SHOT HIT", "ACC%", "DMG", "HEADSHOT", "MAX DISTANCE", 
                "SHOT ONE", "SHOT HIT ONE", "ACC% ONE", "SHOT TWO", "SHOT HIT TWO", "ACC% TWO"
            ])

        st.dataframe(df_weapons_final, use_container_width=True, hide_index=True)

    else:
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>Player Register</h2>", unsafe_allow_html=True)
        try:
            data = init_connection().open_by_key('1qfq7X9IuAcWEhFUuUbNkFfY2ssrmt04r1MFiaCC6ql0').get_worksheet_by_id(155113138).get('D8:D32')
            df = pd.DataFrame(data, columns=["Player"])
            df.insert(0, "N.", range(1, len(df) + 1))
            st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e: 
            st.error(f"Error: {e}")
