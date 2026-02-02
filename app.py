import numpy as np
import io
import datetime
import pandas as pd
import streamlit as st

# ================== Page Config ==================
st.set_page_config(page_title="IDSMED - Mediva Buyback Tracker", page_icon="🔄", layout="wide")
DATE_TODAY = datetime.date.today()

# ================== Global Styles (IDsMED Blue) ==================
st.markdown("""
<style>
/* Base */
html, body, [data-testid="stAppViewContainer"] {
    background: #f5f8ff; /* very light blue */
    font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* Header (IDsMED blue gradient) */
.hero {
    background: linear-gradient(135deg, #005AA9 0%, #1E88E5 100%);
    color: white;
    padding: 26px 28px;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.12);
    margin-bottom: 18px;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.06);
    border: 1px solid #e7f0ff; /* blue-ish border */
}
.metric-title { color: #5b6b7f; font-size: 13px; margin: 0 0 6px 0; }
.metric-value { color: #0f172a; font-weight: 700; font-size: 24px; margin: 0; }

/* Progress bar - blue */
.progress {
    width: 100%;
    height: 12px;
    background: #eaf2ff;
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid #d8e7ff;
}
.progress > span {
    display: block;
    height: 100%;
    background: linear-gradient(90deg, #38BDF8, #1E40AF);
}

/* Chips */
.chips { display: flex; gap: 8px; flex-wrap: wrap; }
.chip {
    display: inline-block;
    padding: 4px 10px;
    font-size: 12px;
    border-radius: 999px;
    border: 1px solid transparent;
}
.chip-gray  { background: #f3f4f6; color: #374151; border-color: #e5e7eb; }           /* Belum */
.chip-cyan  { background: #ecfeff; color: #0e7490; border-color: #a5f3fc; }           /* Sudah sebagian */
.chip-blue  { background: #e6f2ff; color: #0b5cab; border-color: #b5daff; }           /* Sudah */

/* Sidebar */
.sidebar-box {
    background: linear-gradient(180deg, #f7fbff 0%, #eef6ff 100%);
    border: 1px solid #e0eeff;
    border-radius: 14px;
    padding: 14px;
}

/* Buttons (primary) */
.stButton > button, .stDownloadButton > button {
    background-color: #1E88E5 !important;
    color: #ffffff !important;
    border: 1px solid #1E88E5 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #1565C0 !important;
    border-color: #1565C0 !important;
}

/* Inputs focus */
input:focus, textarea:focus, select:focus {
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(30,136,229,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ================== Embedded Data ==================
INITIAL_DATA = [

{"NO": 	1	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	ASY-13438	, DESCRIPTION": "	ASSY 100 PAC KEY SCULPSURE BODY 1PK SEC	, QTY": 	5	},
{"NO": 	2	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	700-4001-200	, DESCRIPTION": "	HVPS, 1200V, 4KJ/SEC, CYNERGY	, QTY": 	1	},
{"NO": 	3	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7017-019	, DESCRIPTION": "	ASSY, AIMING BEAM, REVLITE (REV. 4)	, QTY": 	6	},
{"NO": 	4	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7012-130	, DESCRIPTION": "	ASSY, IGBT/SIMMER, PICO	, QTY": 	1	},
{"NO": 	5	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7012-130	, DESCRIPTION": "	ASSY, IGBT/SIMMER, PICO	, QTY": 	1	},
{"NO": 	6	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-086	, DESCRIPTION": "	ASSY, DISPLAY, PICOSURE	, QTY": 	2	},
{"NO": 	7	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-086	, DESCRIPTION": "	ASSY, DISPLAY, PICOSURE	, QTY": 	1	},
{"NO": 	8	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-900	, DESCRIPTION": "	HR MIRROR OXID ARTIC ARM 755 & 650 (WINDOW)	, QTY": 	20	},
{"NO": 	9	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7002-100	, DESCRIPTION": "	CHAMBER CYNERGY DYE	, QTY": 	1	},
{"NO": 	10	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7002-100	, DESCRIPTION": "	CHAMBER CYNERGY DYE	, QTY": 	1	},
{"NO": 	11	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7002-030	, DESCRIPTION": "	CAPACITOR BANK, CYNERGY	, QTY": 	1	},
{"NO": 	12	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7002-030	, DESCRIPTION": "	CAPACITOR BANK, CYNERGY	, QTY": 	1	},
{"NO": 	13	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7002-110	, DESCRIPTION": "	IGBT/SIMMER, CYNERGY	, QTY": 	1	},
{"NO": 	14	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	424-0017	, DESCRIPTION": "	PUMP, DIRECT DRIVE 24VDC	, QTY": 	10	},
{"NO": 	15	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	990-8006-200	, DESCRIPTION": "	FLASHLAMP, LIN, 6ARC, 7X9MM, 200T (PDL)	, QTY": 	8	},
{"NO": 	16	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7017-018	, DESCRIPTION": "	ASSY, AIMING BEAM, MEDLITE (REV. 7)	, QTY": 	3	},
{"NO": 	17	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7012-200	, DESCRIPTION": "	ASSY, MULTIWAVE SMART HPA, PICO	, QTY": 	1	},
{"NO": 	18	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7012-200	, DESCRIPTION": "	ASSY, MULTIWAVE SMART HPA, PICO	, QTY": 	1	},
{"NO": 	19	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-051	, DESCRIPTION": "	HANDPIECE ZOOM	, QTY": 	2	},
{"NO": 	20	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-0138-110	, DESCRIPTION": "	ASSY PCB, ETX COMPUTER INTERFACE	, QTY": 	1	},
{"NO": 	21	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	800-1580-001	, DESCRIPTION": "	REFL, PARTIAL, 70%R, 585NM, ROHS	, QTY": 	8	},
{"NO": 	22	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-0198-310	, DESCRIPTION": "	ASSY, PCB, 4.5KV POCKELS CELL DRIVER	, QTY": 	1	},
{"NO": 	23	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-0198-310	, DESCRIPTION": "	ASSY, PCB, 4.5KV POCKELS CELL DRIVER	, QTY": 	1	},
{"NO": 	24	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	S100-7012-567	, DESCRIPTION": "	SERV, ASSY, OUTPUT SHUTTER, PICO	, QTY": 	4	},
{"NO": 	25	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	800-5580-010	, DESCRIPTION": "	REFL, FLAT MAXR 585 F SIL 2NDS, ROHS	, QTY": 	8	},
{"NO": 	26	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-0182-610	, DESCRIPTION": "	ASSY, PCB, MODULATOR, PICO	, QTY": 	1	},
{"NO": 	27	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7002-022	, DESCRIPTION": "	ASSY, DYE PUMP, W/J, GUEST, CYNERGY	, QTY": 	1	},
{"NO": 	28	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7002-022	, DESCRIPTION": "	ASSY, DYE PUMP, W/J, GUEST, CYNERGY	, QTY": 	1	},
{"NO": 	29	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-136	, DESCRIPTION": "	ASSY, HEATER, PICO	, QTY": 	2	},
{"NO": 	30	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	101-9008	, DESCRIPTION": "	LENS, +60MM FL X 15MM DIA	, QTY": 	9	},
{"NO": 	31	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	105-0116	, DESCRIPTION": "	MIRROR, 3/4 DIA DOUBLE PEAK, ROHS2	, QTY": 	5	},
{"NO": 	32	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	105-0117	, DESCRIPTION": "	MIRROR, 1 DIA DOUBLE PEAK, ROHS2	, QTY": 	5	},
{"NO": 	33	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7002-790	, DESCRIPTION": "	ASSY, LIGHT GUIDE, CYNERGY	, QTY": 	1	},
{"NO": 	34	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7002-175	, DESCRIPTION": "	ASSY SHUTTER BEAM BLOCK	, QTY": 	1	},
{"NO": 	35	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	659-0613	, DESCRIPTION": "	O-RING KIT HEAD KIT, FOR 647-1800 HEAD ASSY	, QTY": 	12	},
{"NO": 	36	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-052	, DESCRIPTION": "	HANDPIECE 10 MM	, QTY": 	1	},
{"NO": 	37	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-053	, DESCRIPTION": "	HANDPIECE 8 MM	, QTY": 	1	},
{"NO": 	38	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	661-0053-9	, DESCRIPTION": "	ASSY, I/O CONTROLLER, NOT PROGRAMMED	, QTY": 	1	},
{"NO": 	39	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-020	, DESCRIPTION": "	REFL, HR,3.2MCC,755NM,1 DIA,ROHS (PCMR)	, QTY": 	1	},
{"NO": 	40	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-020	, DESCRIPTION": "	REFL, HR,3.2MCC,755NM,1 DIA,ROHS (PCMR)	, QTY": 	1	},
{"NO": 	41	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-025	, DESCRIPTION": "	REFL,HR,6.0MCX,755NM,1 DIA,ROHS (HMR)	, QTY": 	1	},
{"NO": 	42	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-025	, DESCRIPTION": "	REFL,HR,6.0MCX,755NM,1 DIA,ROHS (HMR)	, QTY": 	1	},
{"NO": 	43	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-025	, DESCRIPTION": "	REFL,HR,6.0MCX,755NM,1 DIA,ROHS (HMR)	, QTY": 	1	},
{"NO": 	44	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-025	, DESCRIPTION": "	REFL,HR,6.0MCX,755NM,1 DIA,ROHS (HMR)	, QTY": 	1	},
{"NO": 	45	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-7012-025	, DESCRIPTION": "	REFL,HR,6.0MCX,755NM,1 DIA,ROHS (HMR)	, QTY": 	1	},
{"NO": 	46	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	809-5000-039	, DESCRIPTION": "	PROTECTIVE EYEWEAR, 532NM, 755NM, 1064NM (PATIENT)	, QTY": 	1	},
{"NO": 	47	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-8045-000	, DESCRIPTION": "	ASSY YAG SMART BOARD PCB, ROHS	, QTY": 	1	},
{"NO": 	48	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-8045-000	, DESCRIPTION": "	ASSY YAG SMART BOARD PCB, ROHS	, QTY": 	1	},
{"NO": 	49	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-8045-000	, DESCRIPTION": "	ASSY YAG SMART BOARD PCB, ROHS	, QTY": 	1	},
{"NO": 	50	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	710-8045-000	, DESCRIPTION": "	ASSY YAG SMART BOARD PCB, ROHS	, QTY": 	1	},
{"NO": 	51	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-056	, DESCRIPTION": "	SPACER FIXED HANDPIECE	, QTY": 	1	},
{"NO": 	52	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7017-012	, DESCRIPTION": "	ASSY, CABLE, SHUTTER OUT	, QTY": 	1	},
{"NO": 	53	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	706-0173-000	, DESCRIPTION": "	WRENCH LOCKNUT HP	, QTY": 	2	},
{"NO": 	54	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	102-0189	, DESCRIPTION": "	LENS,  +60MM X 20MM DIA, ROHS 2 (HF I)	, QTY": 	1	},
{"NO": 	55	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	345-0000-009	, DESCRIPTION": "	FILTER, DEIONIZER, 2 1/4 X 5, LG, ROHS	, QTY": 	1	},
{"NO": 	56	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-7012-064	, DESCRIPTION": "	SPACER ZOOM HANDPIECE	, QTY": 	1	},
{"NO": 	57	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-1836-005	, DESCRIPTION": "	LENS, PL/CX, 18X36FL, 585, 755, 1064, ROHS	, QTY": 	1	},
{"NO": 	58	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-1224-005	, DESCRIPTION": "	LENS, PL/CX, 12X24FL, 585, 755, 1064, ROHS	, QTY": 	1	},
{"NO": 	59	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-1248-005	, DESCRIPTION": "	LENS, PL/CX, 12X48FL, 585, 755, 1064, ROHS	, QTY": 	1	},
{"NO": 	60	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	805-1530-005	, DESCRIPTION": "	LENS, PL/CX, 15X30FL, 585, 755, 1064, ROHS	, QTY": 	1	},
{"NO": 	61	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	601-7012-000	, DESCRIPTION": "	CABEL, SAMTEC, COAX	, QTY": 	2	},
{"NO": 	62	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	345-0001-001	, DESCRIPTION": "	CARTRIDGE CARBON VENT, ROHS	, QTY": 	3	},
{"NO": 	63	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-1757-070	, DESCRIPTION": "	HANDPIECE 7MM	, QTY": 	1	},
{"NO": 	64	, "PRINCIPAL": "CYNOSURE", "PART NUMBER": "	100-1757-070	, DESCRIPTION": "	HANDPIECE 7MM	, QTY": 	1	},



]

# ================== Helpers ==================
def update_status(df: pd.DataFrame) -> pd.DataFrame:
    # Sisa Qty
    df["Qty_Buyback"] = df.get("Qty_Buyback", 0).fillna(0).astype(int)
    df["Sisa_Qty"] = (df["QTY"] - df["Qty_Buyback"]).clip(lower=0).astype(int)
    # Status otomatis
    conditions = [
        (df["Qty_Buyback"] == 0),
        (df["Qty_Buyback"] > 0) & (df["Sisa_Qty"] > 0),
        (df["Sisa_Qty"] == 0),
    ]
    choices = ["Belum", "Sudah sebagian", "Sudah"]
    df["Status"] = pd.Categorical(np.select(conditions, choices, default="Belum"),
                                  categories=choices, ordered=True)
    return df

def load_data() -> pd.DataFrame:
    df = pd.DataFrame(INITIAL_DATA)
    for col, default in [("Status", "Belum"), ("Tanggal_Buyback", pd.NaT), ("Catatan", ""), ("Qty_Buyback", 0)]:
        if col not in df.columns: df[col] = default
    df["Tanggal_Buyback"] = pd.to_datetime(df["Tanggal_Buyback"], errors="coerce").dt.date
    df = df.reset_index(drop=True)
    df.insert(0, "_ROW_ID", range(1, len(df)+1))
    df = update_status(df)
    return df

def write_excel_to_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        export_df = df.drop(columns=["_ROW_ID"], errors="ignore")
        export_df.to_excel(writer, index=False, sheet_name="Sheet1")
    buf.seek(0)
    return buf.read()

def build_progress_html(pct: float) -> str:
    pct = max(0.0, min(pct, 1.0))
    pct_txt = f"{int(pct*100)}%"
    return f'''
    <div class="progress"><span style="width:{pct*100:.2f}%"></span></div>
    <div style="font-size:12px;color:#5b6b7f;margin-top:6px;">Progress Buyback: <b>{pct_txt}</b></div>
    '''

# ================== Data ==================
df = load_data()

# ================== Header ==================
st.markdown(f"""
<div class="hero">
  <h1 style="margin:0 0 6px 0;">🔄 IDSMED - Mediva Batch 2</h1>
  <div style="opacity:.95;">IDSMED–Mediva Spare Parts Buyback Tracking System · Location: Logos · Managed by Akmaludin Agustian for Heru Utomo</div>
</div>
""", unsafe_allow_html=True)

# ================== KPI & Progress ==================
total_item = len(df)
total_qty = int(df["QTY"].sum())
total_qty_buyback = int(df["Qty_Buyback"].sum())
total_sisa_qty = int(df["Sisa_Qty"].sum())
progress = (total_qty_buyback / total_qty) if total_qty else 0

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-card"><div class="metric-title">Total Line</div><div class="metric-value">'
                f'{total_item}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><div class="metric-title">Total Qty</div><div class="metric-value">'
                f'{total_qty}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><div class="metric-title">Buyback Qty</div><div class="metric-value">'
                f'{total_qty_buyback}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><div class="metric-title">Sisa Qty</div><div class="metric-value">'
                f'{total_sisa_qty}</div></div>', unsafe_allow_html=True)

st.markdown(build_progress_html(progress), unsafe_allow_html=True)

# Legend chips (biru)
st.markdown("""
<div class="chips" style="margin: 6px 0 2px 0;">
  <span class="chip chip-gray">Belum</span>
  <span class="chip chip-cyan">Sudah sebagian</span>
  <span class="chip chip-blue">Sudah</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ================== Sidebar Filters ==================
with st.sidebar:
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
    st.subheader("Filter")
    q = st.text_input("Cari (bebas: nama/serial/kode)", "", key="q",
                      placeholder="Contoh: eyeshield / 809-5000 / Medlite")
    status_options = ["Belum", "Sudah sebagian", "Sudah"]
    status_filter = st.multiselect("Status", options=status_options, default=[], key="status_filter")
    only_outstanding = st.toggle("Outstanding saja (Sisa > 0)", value=False, key="only_outstanding")
    sort_by = st.selectbox(
        "Urutkan",
        ["Default (NO)", "Sisa Qty ↓", "Buyback Qty ↓", "Tanggal Buyback ↓", "Principal + Part Number"],
        index=0, key="sort_by"
    )

    colr1, colr2 = st.columns(2)
    with colr1:
        reset = st.button("Reset filter")
    with colr2:
        st.markdown("")  # spacer
    if reset:
        st.session_state.q = ""
        st.session_state.status_filter = []
        st.session_state.only_outstanding = False
        st.session_state.sort_by = "Default (NO)"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================== Apply Filters ==================
view = df.copy()

# Status filter
if status_filter:
    view = view[view["Status"].astype(str).isin(status_filter)]

# Search filter (di semua kolom object/string)
if q:
    mask = pd.Series(False, index=view.index)
    for col in view.columns:
        if view[col].dtype == "O":
            mask = mask | view[col].fillna("").astype(str).str.contains(q, case=False, na=False)
    view = view[mask]

# Outstanding filter
if only_outstanding:
    view = view[view["Sisa_Qty"] > 0]

# Sorting
if sort_by == "Sisa Qty ↓":
    view = view.sort_values(["Sisa_Qty", "QTY"], ascending=[False, False])
elif sort_by == "Buyback Qty ↓":
    view = view.sort_values(["Qty_Buyback", "QTY"], ascending=[False, False])
elif sort_by == "Tanggal Buyback ↓":
    view = view.sort_values("Tanggal_Buyback", ascending=False, na_position="last")
elif sort_by == "Principal + Part Number":
    view = view.sort_values(["PRINCIPAL", "PART NUMBER"], ascending=[True, True])
else:
    view = view.sort_values("NO", ascending=True)

# ================== Tabs ==================
tab1, tab2 = st.tabs(["📋 List Data", "📈 Ringkasan"])

with tab1:
    st.subheader("Data Buyback")

    # Simpan _ROW_ID untuk sinkron update
    row_ids = view["_ROW_ID"].copy()

    # Tampilkan tanpa kolom _ROW_ID
    view_display = view.drop(columns=["_ROW_ID"], errors="ignore").copy()

    # Kolom editable
    editable_cols = ["Qty_Buyback", "Tanggal_Buyback", "Catatan"]

    # Siapkan column_config (non-editable untuk kolom lain)
    cfg = {}
    for col in view_display.columns:
        disabled = col not in editable_cols

        if col in ["QTY", "Qty_Buyback", "Sisa_Qty", "NO"]:
            cfg[col] = st.column_config.NumberColumn(
                col if col != "Sisa_Qty" else "Sisa Qty",
                disabled=disabled,
                min_value=0,
                step=1,
                help=("Jumlah unit tersedia" if col == "QTY" else
                      "Jumlah sudah dibuyback (maks. = QTY)" if col == "Qty_Buyback" else
                      "Sisa unit yang belum dibuyback (otomatis)" if col == "Sisa_Qty" else "")
            )
        elif col == "Tanggal_Buyback":
            cfg[col] = st.column_config.DateColumn("Tanggal Buyback", format="YYYY-MM-DD", disabled=disabled)
        else:
            label = col
            if col == "PART NUMBER": label = "Part Number"
            if col == "DESCRIPTION": label = "Description"
            if col == "PRINCIPAL": label = "Principal"
            cfg[col] = st.column_config.TextColumn(label, disabled=disabled)

    # Render editor
    edited = st.data_editor(
        view_display,
        use_container_width=True,
        hide_index=True,
        column_config=cfg,
        num_rows="fixed",
        key="editor"
    )

    # Balikkan _ROW_ID untuk update
    edited["_ROW_ID"] = row_ids.values

    # Validasi
    invalid_rows = edited[edited["Qty_Buyback"] > edited["QTY"]]
    if not invalid_rows.empty:
        st.warning("⚠️ Ada baris dengan Qty Buyback melebihi QTY. Mohon koreksi nilainya.", icon="⚠️")

    # Apply Changes (hanya jika valid)
    if invalid_rows.empty:
        # Hitung ulang Sisa dan Status untuk edited
        edited["Qty_Buyback"] = edited["Qty_Buyback"].fillna(0).astype(int)
        edited["Sisa_Qty"] = (edited["QTY"] - edited["Qty_Buyback"]).clip(lower=0).astype(int)
        # Update df utama pada kolom editable saja
        base = df.set_index("_ROW_ID")
        upd = edited.set_index("_ROW_ID")
        for c in editable_cols:
            if c in upd.columns:
                base.loc[upd.index, c] = upd[c]
        df = base.reset_index()
        # Recompute status & sisa setelah update
        df = update_status(df)

with tab2:
    st.subheader("Ringkasan")

    # Ringkasan per status
    statuses = ["Belum", "Sudah sebagian", "Sudah"]
    cols = st.columns(3)
    for i, stt in enumerate(statuses):
        subset = df[df["Status"].astype(str) == stt]
        cnt = len(subset)
        sisa = int(subset["Sisa_Qty"].sum()) if not subset.empty else 0
        chip_cls = "chip-gray" if stt == "Belum" else ("chip-cyan" if stt == "Sudah sebagian" else "chip-blue")
        with cols[i]:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-title">Status</div>'
                f'<div class="chips"><span class="chip {chip_cls}">{stt}</span></div>'
                f'<div style="height:10px"></div>'
                f'<div class="metric-title">Total Line</div><div class="metric-value">{cnt}</div>'
                f'<div class="metric-title" style="margin-top:8px;">Sisa Qty</div><div class="metric-value">{sisa}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown(" ")
    # Tabel ringkasan agregat
    sum_df = (df.assign(Status=df["Status"].astype(str))
                .groupby("Status", as_index=False)
                .agg(Total_Line=("NO", "count"),
                     Total_Qty=("QTY", "sum"),
                     Buyback_Qty=("Qty_Buyback", "sum"),
                     Sisa_Qty=("Sisa_Qty", "sum"))
                .sort_values("Status"))
    st.dataframe(sum_df, use_container_width=True, hide_index=True)

# ================== Download ==================
st.markdown("### 💾 Download Data")
bytes_xlsx = write_excel_to_bytes(update_status(df.copy()))
st.download_button(
    "⬇️ Download Excel yang sudah diupdate",
    data=bytes_xlsx,
    file_name=f"Data Buyback Mediva - updated {DATE_TODAY}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.markdown("<hr><div style='text-align:center;color:#5b6b7f;'>© 2025 IDSMED - Mediva Buyback Tracking System</div>", unsafe_allow_html=True)
