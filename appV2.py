import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='FCAT Waste Heat Reuse Demo - V2', layout='wide')

st.title('FCAT Waste Heat Reuse Demo')
st.markdown('Select cooling system type, location, and offtaker application.')


# =========================
# Case metadata
# =========================
CASE_METADATA = {
    1: {'label': 'Case 1 - Large - Airside economizer + adiabatic cooling + (water-cooled)', 'default_temp_c': 30.0},
    2: {'label': 'Case 2 - Large - Water economizer + (water-cooled)', 'default_temp_c': 30.0},
    3: {'label': 'Case 3 - Midsize - Airside economizer + (water-cooled chiller)', 'default_temp_c': 30.0},
    4: {'label': 'Case 4 - Midsize - Water economizer + (water-cooled)', 'default_temp_c': 30.0},
    5: {'label': 'Case 5 - Midsize - Water-cooled chiller', 'default_temp_c': 30.0},
    6: {'label': 'Case 6 - Midsize - Airside economizer + (air-cooled chiller)', 'default_temp_c': 30.0},
    7: {'label': 'Case 7 - Midsize - Air-cooled chiller', 'default_temp_c': 27.0},
    8: {'label': 'Case 8 - Small - Water cooled chiler', 'default_temp_c': 27.0},
    9: {'label': 'Case 9 - Small - Air-cooled chiller', 'default_temp_c': 27.0},
    10: {'label': 'Case 10 - Small - Direct expansion (DX) system', 'default_temp_c': 25.0},
    11: {'label': 'Case 11 - Large - Airside economizer + (air-cooled chiller)', 'default_temp_c': 30.0},
    12: {'label': 'Case 12 - Large - Water cooled chiler + dry cooling tower + free cooling', 'default_temp_c': 45.0},
    13: {'label': 'Case 13 - Large - Immersion + Air coold chiler + free coling', 'default_temp_c': 55.0},
    14: {'label': 'Case 14 - Large - Cold-Plate + Air coold chiler + free coling', 'default_temp_c': 50.0},
}

APPLICATION_OPTIONS = [
    'ORC',
    'Cold water generation using an absorption chiller (not used)',
]


# =========================
# Functions
# =========================
def normalize_text(x):
    return str(x).strip().lower()


def eta_use_orc(T_C):
    T_C = np.asarray(T_C, dtype=float)

    T0 = 40.0
    T1 = 43.0
    e1 = 0.019
    T2 = 81.0
    e2 = 0.046

    eta = np.zeros_like(T_C, dtype=float)

    idx = (T_C >= T0) & (T_C < T1)
    eta[idx] = (e1 / (T1 - T0)) * (T_C[idx] - T0)

    idx = (T_C >= T1) & (T_C <= T2)
    eta[idx] = e1 + ((e2 - e1) / (T2 - T1)) * (T_C[idx] - T1)

    idx = (T_C > T2)
    eta[idx] = e2

    return eta


def get_erf(T_avail_C, application):
    if application == 'ORC':
        return float(eta_use_orc(np.array([T_avail_C]))[0])
    return None


@st.cache_data
def load_results_table(csv_path):
    df = pd.read_csv(csv_path)

    df['cooling system type'] = pd.to_numeric(df['cooling system type'], errors='coerce').astype('Int64')
    df['Location'] = df['Location'].astype(str).str.strip()
    df['climate zone'] = df['climate zone'].astype(str).str.strip()
    df['_location_norm'] = df['Location'].apply(normalize_text)

    return df


def get_locations_for_case(df, case_num):
    return sorted(df[df['cooling system type'] == case_num]['Location'].dropna().astype(str).unique())


def calculate_outputs(row, application, temp, asic):
    if asic:
        temp += 5

    pue = float(row['PUE mean'])

    if application == 'ORC':
        erf = get_erf(temp, application)
        ere = pue * (1 - erf)
    else:
        erf, ere = None, None

    return pue, erf, ere, temp


# =========================
# Load CSV
# =========================
csv_file = st.sidebar.text_input("CSV file", "6Locations.csv")
df = load_results_table(csv_file)


# =========================
# UI
# =========================
col1, col2 = st.columns(2)

with col1:
    case_label = st.selectbox(
        "Cooling system type",
        [CASE_METADATA[k]['label'] for k in CASE_METADATA],
        index=13
    )

    case_num = int(case_label.split("-")[0].replace("Case", "").strip())
    default_temp = CASE_METADATA[case_num]['default_temp_c']

    temp = st.number_input("Waste heat temperature (°C)", value=float(default_temp))
    asic = st.checkbox("ASIC chips (+5°C)")

with col2:
    locations = get_locations_for_case(df, case_num)
    location = st.selectbox("Location", locations)

    application = st.selectbox("Offtaker", APPLICATION_OPTIONS)


# =========================
# Match row
# =========================
matched = df[
    (df['cooling system type'] == case_num) &
    (df['_location_norm'] == normalize_text(location))
]

if matched.empty:
    st.warning("No matching row found in the CSV for the selected cooling system type and location.")
    st.stop()

row = matched.iloc[0]


# =========================
# Calculate
# =========================
pue, erf, ere, eff_temp = calculate_outputs(row, application, temp, asic)


# =========================
# Output
# =========================
st.subheader("Selected Inputs")
st.dataframe(pd.DataFrame([{
    "Cooling system type": case_label,
    "Climate zone": row["climate zone"],
    "Location": row["Location"],
    "Offtaker application": application,
    "Default waste heat temperature (°C)": default_temp,
    "User-entered waste heat temperature (°C)": temp,
    "ASIC checked": asic,
    "Effective waste heat temperature (°C)": eff_temp
}]))

st.subheader("Results")

if application == "ORC":
    st.dataframe(pd.DataFrame([{
        "Cooling system type": case_label,
        "Climate zone": row["climate zone"],
        "Location": row["Location"],
        "PUE mean": pue,
        "ERF mean": erf,
        "ERE mean": ere
    }]))
else:
    st.dataframe(pd.DataFrame([{
        "Cooling system type": case_label,
        "Climate zone": row["climate zone"],
        "Location": row["Location"],
        "PUE mean": pue,
        "ERF mean": "Not used",
        "ERE mean": "Not used"
    }]))

st.subheader("Metrics")
c1, c2, c3 = st.columns(3)

c1.metric("PUE", f"{pue:.4f}")
c2.metric("ERF", f"{erf:.4f}" if erf is not None else "N/A")
c3.metric("ERE", f"{ere:.4f}" if ere is not None else "N/A")


with st.expander("Show source table currently loaded"):
    st.dataframe(
        df[[
            'cooling system type',
            'climate zone',
            'Location',
            'PUE mean',
            'ERF mean',
            'ERE mean'
        ]],
        use_container_width=True
    )
