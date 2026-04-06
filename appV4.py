import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='FCAT Waste Heat Reuse Demo - V4', layout='wide')

st.title('FCAT Waste Heat Reuse Demo')
st.markdown('Select cooling system type, state, county, and offtaker application.')

CASE_METADATA = {
    1: {
        'label': 'Case 1 - Large - Airside economizer + adiabatic cooling + (water-cooled)',
        'default_temp_c': 45.0,
        'size': 'Large',
        'heat_removal': 'Airside economizer + adiabatic cooling',
        'chiller': 'Water-cooled',
        'economizer': 'Airside economizer',
        'liquid_cooling': 'No',
        'short_description': 'Large data center with airside economizer and adiabatic cooling, using a water-cooled system.'
    },
    2: {
        'label': 'Case 2 - Large - Water economizer + (water-cooled)',
        'default_temp_c': 45.0,
        'size': 'Large',
        'heat_removal': 'Water economizer',
        'chiller': 'Water-cooled',
        'economizer': 'Water economizer',
        'liquid_cooling': 'No',
        'short_description': 'Large data center using a water economizer with a water-cooled system.'
    },
    3: {
        'label': 'Case 3 - Midsize - Airside economizer + (water-cooled chiller)',
        'default_temp_c': 45.0,
        'size': 'Midsize',
        'heat_removal': 'Airside economizer',
        'chiller': 'Water-cooled chiller',
        'economizer': 'Airside economizer',
        'liquid_cooling': 'No',
        'short_description': 'Midsize data center with airside economizer and water-cooled chiller.'
    },
    4: {
        'label': 'Case 4 - Midsize - Water economizer + (water-cooled)',
        'default_temp_c': 45.0,
        'size': 'Midsize',
        'heat_removal': 'Water economizer',
        'chiller': 'Water-cooled',
        'economizer': 'Water economizer',
        'liquid_cooling': 'No',
        'short_description': 'Midsize data center using a water economizer with water-cooled equipment.'
    },
    5: {
        'label': 'Case 5 - Midsize - Water-cooled chiller',
        'default_temp_c': 45.0,
        'size': 'Midsize',
        'heat_removal': 'Mechanical cooling',
        'chiller': 'Water-cooled chiller',
        'economizer': 'None',
        'liquid_cooling': 'No',
        'short_description': 'Midsize data center using a water-cooled chiller without economizer.'
    },
    6: {
        'label': 'Case 6 - Midsize - Airside economizer + (air-cooled chiller)',
        'default_temp_c': 45.0,
        'size': 'Midsize',
        'heat_removal': 'Airside economizer',
        'chiller': 'Air-cooled chiller',
        'economizer': 'Airside economizer',
        'liquid_cooling': 'No',
        'short_description': 'Midsize data center with airside economizer and air-cooled chiller.'
    },
    7: {
        'label': 'Case 7 - Midsize - Air-cooled chiller',
        'default_temp_c': 45.0,
        'size': 'Midsize',
        'heat_removal': 'Mechanical cooling',
        'chiller': 'Air-cooled chiller',
        'economizer': 'None',
        'liquid_cooling': 'No',
        'short_description': 'Midsize data center using an air-cooled chiller without economizer.'
    },
    8: {
        'label': 'Case 8 - Small - Water cooled chiler',
        'default_temp_c': 45.0,
        'size': 'Small',
        'heat_removal': 'Mechanical cooling',
        'chiller': 'Water-cooled chiller',
        'economizer': 'None',
        'liquid_cooling': 'No',
        'short_description': 'Small data center using a water-cooled chiller.'
    },
    9: {
        'label': 'Case 9 - Small - Air-cooled chiller',
        'default_temp_c': 45.0,
        'size': 'Small',
        'heat_removal': 'Mechanical cooling',
        'chiller': 'Air-cooled chiller',
        'economizer': 'None',
        'liquid_cooling': 'No',
        'short_description': 'Small data center using an air-cooled chiller.'
    },
    10: {
        'label': 'Case 10 - Small - Direct expansion (DX) system',
        'default_temp_c': 45.0,
        'size': 'Small',
        'heat_removal': 'Direct expansion cooling',
        'chiller': 'DX system',
        'economizer': 'None',
        'liquid_cooling': 'No',
        'short_description': 'Small data center using direct expansion (DX) cooling.'
    },
    11: {
        'label': 'Case 11 - Large - Airside economizer + (air-cooled chiller)',
        'default_temp_c': 45.0,
        'size': 'Large',
        'heat_removal': 'Airside economizer',
        'chiller': 'Air-cooled chiller',
        'economizer': 'Airside economizer',
        'liquid_cooling': 'No',
        'short_description': 'Large data center with airside economizer and air-cooled chiller.'
    },
    12: {
        'label': 'Case 12 - Large - Water cooled chiler + dry cooling tower + free cooling',
        'default_temp_c': 45.0,
        'size': 'Large',
        'heat_removal': 'Free cooling + dry cooling tower',
        'chiller': 'Water-cooled chiller',
        'economizer': 'Free cooling',
        'liquid_cooling': 'No',
        'short_description': 'Large data center using water-cooled chiller, dry cooling tower, and free cooling.'
    },
    13: {
        'label': 'Case 13 - Large - Immersion + Air coold chiler + free coling',
        'default_temp_c': 55.0,
        'size': 'Large',
        'heat_removal': 'Immersion cooling',
        'chiller': 'Air-cooled chiller',
        'economizer': 'Free cooling',
        'liquid_cooling': 'Yes - Immersion',
        'short_description': 'Large data center with immersion cooling, air-cooled chiller, and free cooling.'
    },
    14: {
        'label': 'Case 14 - Large - Cold-Plate + Air coold chiler + free coling',
        'default_temp_c': 50.0,
        'size': 'Large',
        'heat_removal': 'Cold-plate cooling',
        'chiller': 'Air-cooled chiller',
        'economizer': 'Free cooling',
        'liquid_cooling': 'Yes - Cold plate',
        'short_description': 'Large data center with cold-plate cooling, air-cooled chiller, and free cooling.'
    },
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
    Used internally unless user overrides the value.
    """
    T_C = np.asarray(T_C, dtype=float)

    # Keep temperatures inside fitted data range
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
def load_pue_table(file_path):
    file_path = str(file_path).strip()

    if file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.lower().endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx")

    expected_cols = [
        'State',
        'County',
        'cooling system type',
        'climate zone',
        'PUE mean',
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError('Missing required columns in input file: ' + ', '.join(missing))

    df['State'] = df['State'].astype(str).str.strip()
    df['County'] = df['County'].astype(str).str.strip()
    df['climate zone'] = df['climate zone'].astype(str).str.strip()
    df['cooling system type'] = pd.to_numeric(df['cooling system type'], errors='coerce').astype('Int64')
    df['PUE mean'] = pd.to_numeric(df['PUE mean'], errors='coerce')

    # Keep rows even if PUE mean is empty, so all states/counties still appear
    df = df.dropna(subset=['State', 'County', 'cooling system type'])

    df['_state_norm'] = df['State'].apply(normalize_text)
    df['_county_norm'] = df['County'].apply(normalize_text)

    return df


def get_states(df):
    return sorted(df['State'].dropna().astype(str).unique())


def get_counties_for_state(df, selected_state):
    filtered = df[df['_state_norm'] == normalize_text(selected_state)]
    return sorted(filtered['County'].dropna().astype(str).unique())


def calculate_outputs(
    case_num,
    row,
    application,
    temp,
    asic,
    pue_override_enabled=False,
    pue_override_value=None,
    eta_override_enabled=False,
    eta_override_value=None,
):
    effective_temp = float(temp)

    if asic:
        effective_temp += 5.0

    pue_from_file = None if pd.isna(row['PUE mean']) else float(row['PUE mean'])

    if pue_override_enabled:
        pue = float(pue_override_value)
        pue_source = "Manual override"
    else:
        pue = pue_from_file
        pue_source = "Input file"

    f_case = RECOVERABLE_HEAT_FACTOR[case_num]

    if application == 'ORC':
        eta_model = get_eta(effective_temp, application)

        if eta_override_enabled:
            eta = float(eta_override_value)
            eta_source = "Manual override"
        else:
            eta = eta_model
            eta_source = "Internal ORC model"

        erf = (eta * f_case) / pue
        ere = pue - (eta * f_case)
    else:
        eta_model = None
        eta = None
        eta_source = "Not used"
        erf = None
        ere = None

    return {
        'PUE mean': pue,
        'PUE source': pue_source,
        'PUE file value': pue_from_file,
        'ERF mean': erf,
        'ERE mean': ere,
        'effective_temp': effective_temp,
        'f_case': f_case,
        'eta_model': eta_model,
        'eta_used': eta,
        'eta_source': eta_source,
    }


# -----------------------------
# File input
# -----------------------------
data_file = st.sidebar.text_input("PUE data file (.csv or .xlsx)", "based_on_state_countiy.csv")

try:
    df = load_pue_table(data_file)
except FileNotFoundError:
    st.error(f"File not found: {data_file}. Make sure the file is in the GitHub repo root and the name matches exactly.")
    st.stop()
except Exception as e:
    st.error(f"Could not load input file. {e}")
    st.stop()

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
case_info = CASE_METADATA[case_num]

# 2) State
states = get_states(df)
if not states:
    st.warning("No states found in the input file.")
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
# Case details (Request 5)
# -----------------------------
st.subheader("Cooling System Case Details")

st.caption("Additional details for the selected cooling system case.")

case_details_df = pd.DataFrame([{
    "Case": f"Case {case_num}",
    "System size": case_info["size"],
    "Primary heat removal approach": case_info["heat_removal"],
    "Chiller/system type": case_info["chiller"],
    "Economizer type": case_info["economizer"],
    "Liquid cooling": case_info["liquid_cooling"],
    "Recommended waste heat temperature (°C)": case_info["default_temp_c"],
    "Recoverable heat factor (f_case)": RECOVERABLE_HEAT_FACTOR[case_num],
}])

st.dataframe(case_details_df, use_container_width=True)
st.info(case_info["short_description"])

# -----------------------------
# Find matching row directly
# -----------------------------
matched = df[
    (df['_state_norm'] == normalize_text(state)) &
    (df['_county_norm'] == normalize_text(county)) &
    (df['cooling system type'] == case_num)
]

if matched.empty:
    st.warning("No matching row found for the selected state, county, and cooling system type.")
    st.stop()

row = matched.iloc[0]

# -----------------------------
# Optional Overrides
# -----------------------------
st.subheader("Optional Overrides")

col1, col2 = st.columns(2)

with col1:
    pue_override_enabled = st.checkbox("Override PUE value")

    if pue_override_enabled:
        default_pue_for_override = float(row['PUE mean']) if not pd.isna(row['PUE mean']) else 1.20
        pue_override_value = st.number_input(
            "Manual PUE value",
            min_value=0.0001,
            value=default_pue_for_override,
            step=0.01,
            format="%.4f",
        )
    else:
        pue_override_value = None

with col2:
    if application == "ORC":
        effective_temp_preview = float(temp) + (5.0 if asic else 0.0)
        eta_preview = get_eta(effective_temp_preview, application)
        eta_preview_percent = float(eta_preview * 100.0) if eta_preview is not None else 1.0

        eta_override_enabled = st.checkbox("Override offtaker efficiency")

        if eta_override_enabled:
            eta_override_percent = st.number_input(
                "Manual offtaker efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=eta_preview_percent,
                step=0.1,
                format="%.2f",
            )
            eta_override_value = eta_override_percent / 100.0
        else:
            eta_override_value = None
    else:
        eta_override_enabled = False
        eta_override_value = None
        st.info("Offtaker efficiency override is only used for ORC.")

# -----------------------------
# Validation
# -----------------------------
if pd.isna(row['PUE mean']) and not pue_override_enabled:
    st.warning(
        "PUE mean is not filled yet for the selected state, county, and cooling system type. "
        "Please use the PUE override option to continue."
    )
    st.stop()

# -----------------------------
# Calculate outputs
# -----------------------------
outputs = calculate_outputs(
    case_num=case_num,
    row=row,
    application=application,
    temp=temp,
    asic=asic,
    pue_override_enabled=pue_override_enabled,
    pue_override_value=pue_override_value,
    eta_override_enabled=eta_override_enabled,
    eta_override_value=eta_override_value,
)

# -----------------------------
# Selected inputs
# -----------------------------
st.subheader("Selected Inputs")
selected_inputs_df = pd.DataFrame([{
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
    "PUE source": outputs["PUE source"],
    "Efficiency source": outputs["eta_source"],
}])
st.dataframe(selected_inputs_df, use_container_width=True)

# -----------------------------
# Results
# -----------------------------
st.subheader("Results")

if application == "ORC":
    results_df = pd.DataFrame([{
        "Cooling system type": case_label,
        "State": state,
        "County": county,
        "Climate zone": row["climate zone"],
        "PUE file value": outputs["PUE file value"],
        "PUE used": outputs["PUE mean"],
        "Efficiency used": outputs["eta_used"],
        "ERF mean": outputs["ERF mean"],
        "ERE mean": outputs["ERE mean"],
    }])
else:
    results_df = pd.DataFrame([{
        "Cooling system type": case_label,
        "State": state,
        "County": county,
        "Climate zone": row["climate zone"],
        "PUE file value": outputs["PUE file value"],
        "PUE used": outputs["PUE mean"],
        "ERF mean": "Not used",
        "ERE mean": "Not used",
    }])

st.dataframe(results_df, use_container_width=True)

# -----------------------------
# Metrics (Request 6)
# -----------------------------
st.subheader("Metrics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "PUE",
        f"{outputs['PUE mean']:.4f}",
        help="Power Usage Effectiveness (PUE) = Total facility energy / IT energy. Lower values indicate better overall data center energy performance."
    )

with c2:
    st.metric(
        "ERF",
        f"{outputs['ERF mean']:.4f}" if outputs["ERF mean"] is not None else "N/A",
        help="Energy Reuse Factor (ERF) is the fraction of total data center energy that is recovered and reused. Higher values are generally better."
    )

with c3:
    st.metric(
        "ERE",
        f"{outputs['ERE mean']:.4f}" if outputs["ERE mean"] is not None else "N/A",
        help="Energy Reuse Effectiveness (ERE) adjusts PUE by accounting for recovered energy. Lower values are generally better."
    )

# -----------------------------
# Quick metric explanations
# -----------------------------
st.subheader("Metric Explanations")

metric_explanations_df = pd.DataFrame([
    {
        "Metric": "PUE",
        "Short description": "Total facility energy divided by IT energy.",
        "How to interpret": "Lower is better."
    },
    {
        "Metric": "ERF",
        "Short description": "Fraction of total data center energy that is recovered and reused.",
        "How to interpret": "Higher is better."
    },
    {
        "Metric": "ERE",
        "Short description": "Adjusted PUE after accounting for recovered/reused energy.",
        "How to interpret": "Lower is better."
    }
])

st.dataframe(metric_explanations_df, use_container_width=True)

# -----------------------------
# Calculation Notes
# -----------------------------
st.subheader("Calculation Notes")

notes = {
    "PUE source": outputs["PUE source"],
    "PUE file value": (
        f"{outputs['PUE file value']:.4f}"
        if outputs["PUE file value"] is not None else "Missing"
    ),
    "PUE used": f"{outputs['PUE mean']:.4f}",
}

if application == "ORC":
    notes["Efficiency source"] = outputs["eta_source"]
    notes["Efficiency used"] = f"{outputs['eta_used']:.4f} ({outputs['eta_used'] * 100:.2f}%)"
    if outputs["eta_model"] is not None:
        notes["Internal ORC model efficiency"] = (
            f"{outputs['eta_model']:.4f} ({outputs['eta_model'] * 100:.2f}%)"
        )

st.dataframe(pd.DataFrame([notes]), use_container_width=True)

st.caption(
    "PUE is normally read from the state/county input file for the selected cooling system type, "
    "unless the user overrides it. For ORC, offtaker efficiency is normally taken from the internal "
    "ORC efficiency model, unless the user overrides it."
)
