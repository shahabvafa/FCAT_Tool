import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='FCAT Waste Heat Reuse Demo - V4', layout='wide')

st.title('FCAT Waste Heat Reuse Demo')
st.markdown('Select cooling system type, state, county, and offtaker application.')

CASE_METADATA = {
    1: {'label': 'Case 1 - Large - Airside economizer + adiabatic cooling + (water-cooled)', 'default_temp_c': 45.0},
    2: {'label': 'Case 2 - Large - Water economizer + (water-cooled)', 'default_temp_c': 45.0},
    3: {'label': 'Case 3 - Midsize - Airside economizer + (water-cooled chiller)', 'default_temp_c': 45.0},
    4: {'label': 'Case 4 - Midsize - Water economizer + (water-cooled)', 'default_temp_c': 45.0},
    5: {'label': 'Case 5 - Midsize - Water-cooled chiller', 'default_temp_c': 45.0},
    6: {'label': 'Case 6 - Midsize - Airside economizer + (air-cooled chiller)', 'default_temp_c': 45.0},
    7: {'label': 'Case 7 - Midsize - Air-cooled chiller', 'default_temp_c': 45.0},
    8: {'label': 'Case 8 - Small - Water cooled chiler', 'default_temp_c': 45.0},
    9: {'label': 'Case 9 - Small - Air-cooled chiller', 'default_temp_c': 45.0},
    10: {'label': 'Case 10 - Small - Direct expansion (DX) system', 'default_temp_c': 45.0},
    11: {'label': 'Case 11 - Large - Airside economizer + (air-cooled chiller)', 'default_temp_c': 45.0},
    12: {'label': 'Case 12 - Large - Water cooled chiler + dry cooling tower + free cooling', 'default_temp_c': 45.0},
    13: {'label': 'Case 13 - Large - Immersion + Air coold chiler + free coling', 'default_temp_c': 55.0},
    14: {'label': 'Case 14 - Large - Cold-Plate + Air coold chiler + free coling', 'default_temp_c': 50.0},
}

APPLICATION_OPTIONS = [
    'ORC',
    'Cold water generation using an absorption chiller (not used)',
]

RECOVERABLE_HEAT_FACTOR = {
    1: 0.80,
    2: 0.80,
    3: 0.75,
    4: 0.75,
    5: 0.70,
    6: 0.70,
    7: 0.65,
    8: 0.60,
    9: 0.60,
    10: 0.55,
    11: 0.80,
    12: 0.85,
    13: 0.90,
    14: 0.85,
}


def normalize_text(x):
    return str(x).strip().lower()


def eta_use_orc(T_C):
    """
    ORC efficiency from a 2nd-order polynomial fit to the digitized eta curve.
    Used internally only. Not displayed in the app.
    """
    T_C = np.asarray(T_C, dtype=float)
    T_C = np.clip(T_C, 42.7314, 84.3096)

    a = -9.77832291e-04
    b = 1.91002705e-01
    c = -4.50769764e+00

    eta_percent = a * T_C**2 + b * T_C + c
    eta_percent = np.clip(eta_percent, 0.0, None)

    return eta_percent / 100.0


def get_eta(T_avail_C, application):
    if application == 'ORC':
        return float(eta_use_orc(np.array([T_avail_C]))[0])
    return None


@st.cache_data
def load_pue_table(excel_path, sheet_name=0):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    expected_cols = [
        'State',
        'County',
        'cooling system type',
        'climate zone',
        'PUE mean',
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError('Missing required columns in Excel file: ' + ', '.join(missing))

    df['State'] = df['State'].astype(str).str.strip()
    df['County'] = df['County'].astype(str).str.strip()
    df['climate zone'] = df['climate zone'].astype(str).str.strip()
    df['cooling system type'] = pd.to_numeric(df['cooling system type'], errors='coerce').astype('Int64')
    df['PUE mean'] = pd.to_numeric(df['PUE mean'], errors='coerce')

    df = df.dropna(subset=['State', 'County', 'cooling system type', 'PUE mean'])

    df['_state_norm'] = df['State'].apply(normalize_text)
    df['_county_norm'] = df['County'].apply(normalize_text)

    return df


def get_states(df):
    return sorted(df['State'].dropna().astype(str).unique())


def get_counties_for_state(df, selected_state):
    return sorted(
        df[df['_state_norm'] == normalize_text(selected_state)]['County']
        .dropna()
        .astype(str)
        .unique()
    )


def calculate_outputs(case_num, row, application, temp, asic):
    effective_temp = float(temp)

    if asic:
        effective_temp += 5.0

    pue = float(row['PUE mean'])
    f_case = RECOVERABLE_HEAT_FACTOR[case_num]

    if application == 'ORC':
        eta = get_eta(effective_temp, application)
        erf = (eta * f_case) / pue
        ere = pue - (eta * f_case)
    else:
        erf = None
        ere = None

    return {
        'PUE mean': pue,
        'ERF mean': erf,
        'ERE mean': ere,
        'effective_temp': effective_temp,
        'f_case': f_case,
    }


# -----------------------------
# File input
# -----------------------------
excel_file = st.sidebar.text_input("PUE Excel file", "county_pue_data_sample.xlsx")
sheet_name = st.sidebar.text_input("Sheet name or index", "0")

try:
    sheet_name_parsed = int(sheet_name)
except ValueError:
    sheet_name_parsed = sheet_name

df = load_pue_table(excel_file, sheet_name=sheet_name_parsed)

# -----------------------------
# UI
# -----------------------------
st.subheader("Inputs")

# 1) Cooling system type
case_label = st.selectbox(
    "Cooling system type",
    [CASE_METADATA[k]['label'] for k in CASE_METADATA],
    index=13
)

case_num = int(case_label.split("-")[0].replace("Case", "").strip())
default_temp = CASE_METADATA[case_num]['default_temp_c']

# 2) State
states = get_states(df)
if not states:
    st.warning("No states found in the Excel file.")
    st.stop()

state = st.selectbox("State", states)

# 3) County
counties = get_counties_for_state(df, state)
if not counties:
    st.warning("No counties found for the selected state.")
    st.stop()

county = st.selectbox("County", counties)

# 4) Offtaker
application = st.selectbox("Offtaker", APPLICATION_OPTIONS)

# Extra inputs
temp = st.number_input("Waste heat temperature (°C)", value=float(default_temp))
asic = st.checkbox("ASIC chips (+5°C)")

# -----------------------------
# Find matching row directly
# -----------------------------
matched = df[
    (df['_state_norm'] == normalize_text(state)) &
    (df['_county_norm'] == normalize_text(county)) &
    (df['cooling system type'] == case_num)
]

if matched.empty:
    st.warning("No matching row found in the Excel file for the selected state, county, and cooling case.")
    st.stop()

row = matched.iloc[0]
outputs = calculate_outputs(case_num, row, application, temp, asic)

# -----------------------------
# Selected inputs
# -----------------------------
st.subheader("Selected Inputs")
st.dataframe(pd.DataFrame([{
    "Cooling system type": case_label,
    "State": state,
    "County": county,
    "Climate zone": row["climate zone"],
    "Offtaker application": application,
    "Recommended waste heat temperature (°C)": default_temp,
    "User-entered waste heat temperature (°C)": temp,
    "ASIC checked": asic,
    "Effective waste heat temperature (°C)": outputs["effective_temp"],
    "Recoverable heat factor (f_case)": outputs["f_case"],
}]))

# -----------------------------
# Results
# -----------------------------
st.subheader("Results")

if application == "ORC":
    st.dataframe(pd.DataFrame([{
        "Cooling system type": case_label,
        "State": state,
        "County": county,
        "Climate zone": row["climate zone"],
        "PUE mean": outputs["PUE mean"],
        "ERF mean": outputs["ERF mean"],
        "ERE mean": outputs["ERE mean"],
    }]))
else:
    st.dataframe(pd.DataFrame([{
        "Cooling system type": case_label,
        "State": state,
        "County": county,
        "Climate zone": row["climate zone"],
        "PUE mean": outputs["PUE mean"],
        "ERF mean": "Not used",
        "ERE mean": "Not used",
    }]))

# -----------------------------
# Metrics
# -----------------------------
st.subheader("Metrics")
c1, c2, c3 = st.columns(3)

c1.metric("PUE", f"{outputs['PUE mean']:.4f}")
c2.metric("ERF", f"{outputs['ERF mean']:.4f}" if outputs["ERF mean"] is not None else "N/A")
c3.metric("ERE", f"{outputs['ERE mean']:.4f}" if outputs["ERE mean"] is not None else "N/A")

st.caption(
    "PUE is read directly from the county/state Excel table for the selected cooling system type. "
    "ERF and ERE are then calculated from the selected PUE and the internal ORC efficiency model."
)
