import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='FCAT Waste Heat Reuse Demo - V3', layout='wide')

st.title('FCAT Waste Heat Reuse Demo')
st.markdown('Select cooling system type, location, and offtaker application.')


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

# Placeholder values for demo; replace later if you have case-specific values
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


def get_eta(T_avail_C, application):
    if application == 'ORC':
        return float(eta_use_orc(np.array([T_avail_C]))[0])
    return None


@st.cache_data
def load_results_table(csv_path):
    df = pd.read_csv(csv_path)

    expected_cols = [
        'cooling system type',
        'climate zone',
        'Location',
        'PUE mean',
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError('Missing required columns in CSV: ' + ', '.join(missing))

    df['cooling system type'] = pd.to_numeric(df['cooling system type'], errors='coerce').astype('Int64')
    df['Location'] = df['Location'].astype(str).str.strip()
    df['climate zone'] = df['climate zone'].astype(str).str.strip()
    df['_location_norm'] = df['Location'].apply(normalize_text)

    return df


def get_locations_for_case(df, case_num):
    return sorted(df[df['cooling system type'] == case_num]['Location'].dropna().astype(str).unique())


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
        eta = None
        erf = None
        ere = None

    return {
        'PUE mean': pue,
        'eta': eta,
        'ERF mean': erf,
        'ERE mean': ere,
        'effective_temp': effective_temp,
        'f_case': f_case,
    }


csv_file = st.sidebar.text_input("CSV file", "6Locations.csv")
df = load_results_table(csv_file)

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
    if not locations:
        st.warning("No locations found for this case in CSV.")
        st.stop()

    location = st.selectbox("Location", locations)
    application = st.selectbox("Offtaker", APPLICATION_OPTIONS)

matched = df[
    (df['cooling system type'] == case_num) &
    (df['_location_norm'] == normalize_text(location))
]

if matched.empty:
    st.warning("No matching row found in CSV.")
    st.stop()

row = matched.iloc[0]

outputs = calculate_outputs(case_num, row, application, temp, asic)

st.subheader("Selected Inputs")
st.dataframe(pd.DataFrame([{
    "Cooling system type": case_label,
    "Climate zone": row["climate zone"],
    "Location": row["Location"],
    "Offtaker application": application,
    "Recommended waste heat temperature (°C)": default_temp,
    "User-entered waste heat temperature (°C)": temp,
    "ASIC checked": asic,
    "Effective waste heat temperature (°C)": outputs["effective_temp"],
    "Recoverable heat factor (f_case)": outputs["f_case"],
}]))

st.subheader("Results")

if application == "ORC":
    st.dataframe(pd.DataFrame([{
        "Cooling system type": case_label,
        "Climate zone": row["climate zone"],
        "Location": row["Location"],
        "PUE mean": outputs["PUE mean"],
        "eta": outputs["eta"],
        "ERF mean": outputs["ERF mean"],
        "ERE mean": outputs["ERE mean"],
    }]))
else:
    st.dataframe(pd.DataFrame([{
        "Cooling system type": case_label,
        "Climate zone": row["climate zone"],
        "Location": row["Location"],
        "PUE mean": outputs["PUE mean"],
        "eta": "Not used",
        "ERF mean": "Not used",
        "ERE mean": "Not used",
    }]))

st.subheader("Metrics")
c1, c2, c3, c4 = st.columns(4)

c1.metric("PUE", f"{outputs['PUE mean']:.4f}")
c3.metric("ERF", f"{outputs['ERF mean']:.4f}" if outputs["ERF mean"] is not None else "N/A")
c4.metric("ERE", f"{outputs['ERE mean']:.4f}" if outputs["ERE mean"] is not None else "N/A")

with st.expander("Show source table currently loaded"):
    st.dataframe(
        df[['cooling system type', 'climate zone', 'Location', 'PUE mean']],
        use_container_width=True
    )

st.caption(
    "PUE values are based on the PUE prediction study under review. "
    "Waste heat temperature assumptions are based on the waste heat temperature study under review."
)
