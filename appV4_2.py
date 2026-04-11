import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='FCAT Waste Heat Reuse Demo - V5', layout='wide')

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
        'label': 'Case 8 - Small - Water-cooled chiller',
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
        'label': 'Case 12 - Large -Cold Plate + Water-cooled chiller + dry cooling tower + free cooling + 25% CRAC',
        'default_temp_c': 45.0,
        'size': 'Large',
        'heat_removal': 'Free cooling + dry cooling tower + Cold Plate',
        'chiller': 'Water-cooled chiller',
        'economizer': 'Free cooling',
        'liquid_cooling': 'No',
        'short_description': 'Large data center using Cold Plate, water-cooled chiller, dry cooling tower, and free cooling + 25% CRAC.'
    },
    13: {
        'label': 'Case 13 - Large - Immersion + Air-cooled chiller + free cooling',
        'default_temp_c': 55.0,
        'size': 'Large',
        'heat_removal': 'Immersion cooling',
        'chiller': 'Air-cooled chiller',
        'economizer': 'Free cooling',
        'liquid_cooling': 'Yes - Immersion',
        'short_description': 'Large data center with immersion cooling, air-cooled chiller, and free cooling.'
    },
    14: {
        'label': 'Case 14 - Large - Cold-Plate + Air-cooled chiller + free cooling',
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
    'Cold water generation using an absorption chiller',
]

ABSORPTION_EVAP_OPTIONS = [-10, -5, 0]

Q_AVAIL_FACTOR = {
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
    T_C = np.clip(T_C, 42.7314, 84.3096)

    a = -9.77832291e-04
    b = 1.91002705e-01
    c = -4.50769764e+00

    eta_percent = a * T_C**2 + b * T_C + c
    eta_percent = np.clip(eta_percent, 0.0, None)

    return eta_percent / 100.0


def cop_use_absorption(T_gen_C, T_evap_C):
    T_gen_C = np.asarray(T_gen_C, dtype=float)

    if T_evap_C == -10:
        cop = -1.390e-05 * T_gen_C**2 + 3.05662e-03 * T_gen_C + 0.35476099
    elif T_evap_C == -5:
        cop = 2.39e-06 * T_gen_C**2 - 1.07259e-03 * T_gen_C + 0.62829248
    elif T_evap_C == 0:
        cop = 1.143e-05 * T_gen_C**2 - 3.31724e-03 * T_gen_C + 0.78234054
    else:
        raise ValueError("T_evap_C must be one of -10, -5, or 0.")

    return np.clip(cop, 0.0, None)


def get_offtaker_performance(T_avail_C, application, abs_evap_temp_c=None):
    if application == 'ORC':
        return float(eta_use_orc(np.array([T_avail_C]))[0])

    if application == 'Cold water generation using an absorption chiller':
        if abs_evap_temp_c is None:
            raise ValueError("abs_evap_temp_c is required for the absorption chiller application.")
        return float(cop_use_absorption(np.array([T_avail_C]), abs_evap_temp_c)[0])

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
    phi_use=1.0,
    pue_override_enabled=False,
    pue_override_value=None,
    eta_override_enabled=False,
    eta_override_value=None,
    abs_evap_temp_c=None,
):
    p_it = 1.0

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

    q_avail = Q_AVAIL_FACTOR[case_num]

    p_dc = pue * p_it
    p_wh_avail = q_avail * p_it
    p_wh_use = phi_use * p_wh_avail

    erf = p_wh_use / p_dc
    ere = (p_dc - p_wh_use) / p_it

    p_total_to_offtaker = p_wh_use
    t_offtaker_in = effective_temp

    if application == 'ORC':
        if eta_override_enabled:
            eta = float(eta_override_value)
            eta_source = "Manual override"
            eta_model = get_offtaker_performance(t_offtaker_in, application) if t_offtaker_in is not None else None
        else:
            eta_model = get_offtaker_performance(t_offtaker_in, application) if t_offtaker_in is not None else 0.0
            eta = eta_model
            eta_source = "Internal ORC model"

        p_orc = eta * p_total_to_offtaker
        cop_abs = None
        useful_output = p_orc

    elif application == 'Cold water generation using an absorption chiller':
        if eta_override_enabled:
            cop_abs = float(eta_override_value)
            eta_source = "Manual override"
            eta_model = get_offtaker_performance(
                t_offtaker_in,
                application,
                abs_evap_temp_c=abs_evap_temp_c
            ) if t_offtaker_in is not None else None
        else:
            eta_model = get_offtaker_performance(
                t_offtaker_in,
                application,
                abs_evap_temp_c=abs_evap_temp_c
            ) if t_offtaker_in is not None else 0.0
            cop_abs = eta_model
            eta_source = "Internal absorption chiller COP model"

        p_orc = None
        eta = cop_abs
        useful_output = cop_abs * p_total_to_offtaker

    else:
        eta_model = None
        eta = None
        eta_source = "Not used"
        p_orc = None
        cop_abs = None
        useful_output = None

    ure = useful_output / p_it if useful_output is not None else None

    return {
        'PIT': p_it,
        'PDC': p_dc,
        'PUE mean': pue,
        'PUE source': pue_source,
        'PUE file value': pue_from_file,
        'Qavail': q_avail,
        'phi_use': phi_use,
        'Pwh_avail': p_wh_avail,
        'Pwh_use': p_wh_use,
        'ERF mean': erf,
        'ERE mean': ere,
        'effective_temp': effective_temp,
        'Ptotal_offtaker': p_total_to_offtaker,
        'Tofftaker_in': t_offtaker_in,
        'eta_model': eta_model,
        'eta_used': eta,
        'eta_source': eta_source,
        'PORC': p_orc,
        'COP_abs': cop_abs,
        'URE': ure,
        'abs_evap_temp_c': abs_evap_temp_c,
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

case_label = st.selectbox(
    "Cooling system type",
    [CASE_METADATA[k]['label'] for k in CASE_METADATA],
    index=13
)

case_num = int(case_label.split("-")[0].replace("Case", "").strip())
default_temp = CASE_METADATA[case_num]['default_temp_c']
case_info = CASE_METADATA[case_num]

states = get_states(df)
if not states:
    st.warning("No states found in the input file.")
    st.stop()

state = st.selectbox("State", states)

counties = get_counties_for_state(df, state)
if not counties:
    st.warning("No counties found for the selected state.")
    st.stop()

county = st.selectbox("County", counties)

application = st.selectbox("Offtaker", APPLICATION_OPTIONS)

if application == "Cold water generation using an absorption chiller":
    abs_evap_temp_c = st.selectbox(
        "Absorption chiller evaporator temperature (°C)",
        ABSORPTION_EVAP_OPTIONS,
        index=1,
        help="Available fitted COP curves are for T_evap = -10, -5, and 0 °C."
    )
else:
    abs_evap_temp_c = None

temp = st.number_input("Waste heat temperature (°C)", value=float(default_temp))
asic = st.checkbox("ASIC chips (+5°C)")

phi_use_percent = st.slider(
    "Used fraction of available waste heat (%)",
    min_value=0,
    max_value=100,
    value=100,
    step=5,
    help="Fraction of available data-center waste heat that is actually reused."
)
phi_use = phi_use_percent / 100.0

# -----------------------------
# Case details
# -----------------------------
st.subheader("Cooling System Case Details")

case_details_df = pd.DataFrame([{
    "Case": f"Case {case_num}",
    "System size": case_info["size"],
    "Primary heat removal approach": case_info["heat_removal"],
    "Chiller/system type": case_info["chiller"],
    "Economizer type": case_info["economizer"],
    "Liquid cooling": case_info["liquid_cooling"],
    "Recommended waste heat temperature (°C)": case_info["default_temp_c"],
    "Q_avail factor": Q_AVAIL_FACTOR[case_num],
}])

st.dataframe(case_details_df, use_container_width=True)
st.info(case_info["short_description"])

# -----------------------------
# Find matching row
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
    if application in ["ORC", "Cold water generation using an absorption chiller"]:
        preview_primary_temp = float(temp) + (5.0 if asic else 0.0)

        eta_preview = get_offtaker_performance(
            preview_primary_temp,
            application,
            abs_evap_temp_c=abs_evap_temp_c
        ) if preview_primary_temp is not None else 0.0

        eta_override_enabled = st.checkbox("Override offtaker performance")

        if application == "ORC":
            default_manual_value = float(eta_preview * 100.0)
            label_text = "Manual ORC efficiency (%)"
            min_val = 0.0
            max_val = 100.0
            step_val = 0.1
            format_val = "%.2f"
        else:
            default_manual_value = float(eta_preview)
            label_text = "Manual absorption chiller COP"
            min_val = 0.0
            max_val = 10.0
            step_val = 0.01
            format_val = "%.4f"

        if eta_override_enabled:
            manual_value = st.number_input(
                label_text,
                min_value=min_val,
                max_value=max_val,
                value=default_manual_value,
                step=step_val,
                format=format_val,
            )

            if application == "ORC":
                eta_override_value = manual_value / 100.0
            else:
                eta_override_value = manual_value
        else:
            eta_override_value = None
    else:
        eta_override_enabled = False
        eta_override_value = None

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
    phi_use=phi_use,
    pue_override_enabled=pue_override_enabled,
    pue_override_value=pue_override_value,
    eta_override_enabled=eta_override_enabled,
    eta_override_value=eta_override_value,
    abs_evap_temp_c=abs_evap_temp_c,
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
    "Absorption chiller evaporator temperature (°C)": outputs["abs_evap_temp_c"],
    "Q_avail factor": outputs["Qavail"],
    "Used waste heat fraction (%)": outputs["phi_use"] * 100,
    "PUE source": outputs["PUE source"],
    "Performance source": outputs["eta_source"],
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
        "Q_avail": outputs["Qavail"],
        "Pwh,avail (normalized)": outputs["Pwh_avail"],
        "Pwh,use (normalized)": outputs["Pwh_use"],
        "Total heat to offtaker (normalized)": outputs["Ptotal_offtaker"],
        "Offtaker inlet temperature (°C)": outputs["Tofftaker_in"],
        "ORC efficiency used": outputs["eta_used"],
        "URE": outputs["URE"],
        "ERF mean": outputs["ERF mean"],
        "ERE mean": outputs["ERE mean"],
    }])

elif application == "Cold water generation using an absorption chiller":
    results_df = pd.DataFrame([{
        "Cooling system type": case_label,
        "State": state,
        "County": county,
        "Climate zone": row["climate zone"],
        "PUE file value": outputs["PUE file value"],
        "PUE used": outputs["PUE mean"],
        "Q_avail": outputs["Qavail"],
        "Pwh,avail (normalized)": outputs["Pwh_avail"],
        "Pwh,use (normalized)": outputs["Pwh_use"],
        "Total heat to offtaker (normalized)": outputs["Ptotal_offtaker"],
        "Offtaker inlet temperature (°C)": outputs["Tofftaker_in"],
        "Absorption chiller evaporator temperature (°C)": outputs["abs_evap_temp_c"],
        "Absorption chiller COP used": outputs["COP_abs"],
        "URE": outputs["URE"],
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
        "Q_avail": outputs["Qavail"],
        "Pwh,avail (normalized)": outputs["Pwh_avail"],
        "Pwh,use (normalized)": outputs["Pwh_use"],
        "ERF mean": outputs["ERF mean"],
        "ERE mean": outputs["ERE mean"],
    }])

st.dataframe(results_df, use_container_width=True)

# -----------------------------
# Metrics
# -----------------------------
st.subheader("Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "PUE",
        f"{outputs['PUE mean']:.4f}",
        help="Power Usage Effectiveness = total data center power / IT power."
    )

with c2:
    st.metric(
        "ERF",
        f"{outputs['ERF mean']:.4f}",
        help="Energy Reuse Factor = reused data center waste heat / total data center power."
    )

with c3:
    st.metric(
        "ERE",
        f"{outputs['ERE mean']:.4f}",
        help="Energy Reuse Effectiveness = (total data center power - reused waste heat) / IT power."
    )

with c4:
    st.metric(
        "URE",
        f"{outputs['URE']:.4f}" if outputs["URE"] is not None else "N/A",
        help="Useful Reuse Effectiveness = useful output from the selected application normalized by IT power."
    )

# -----------------------------
# Metric Explanations
# -----------------------------
st.subheader("Metric Explanations")

metric_explanations_rows = [
    {
        "Metric": "PUE",
        "Short description": "Total data center power divided by IT power.",
        "How to interpret": "Lower is generally better."
    },
    {
        "Metric": "ERF",
        "Short description": "Reused data center waste heat divided by total data center power.",
        "How to interpret": "Higher means more data center heat is being reused."
    },
    {
        "Metric": "ERE",
        "Short description": "Adjusted effectiveness after subtracting reused data center heat.",
        "How to interpret": "Lower is generally better."
    },
    {
        "Metric": "URE",
        "Short description": "Useful Reuse Effectiveness = useful output from the selected application divided by IT power.",
        "How to interpret": "Higher means the recovered waste heat is producing more useful output, such as electricity from ORC or cooling from an absorption chiller."
    }
]

metric_explanations_df = pd.DataFrame(metric_explanations_rows)
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
    "Q_avail factor": f"{outputs['Qavail']:.4f}",
    "Used waste heat fraction (phi_use)": f"{outputs['phi_use']:.4f}",
    "Pwh,avail (normalized)": f"{outputs['Pwh_avail']:.4f}",
    "Pwh,use (normalized)": f"{outputs['Pwh_use']:.4f}",
    "Total heat to offtaker (normalized)": f"{outputs['Ptotal_offtaker']:.4f}",
    "ERF": f"{outputs['ERF mean']:.4f}",
    "ERE": f"{outputs['ERE mean']:.4f}",
    "URE": f"{outputs['URE']:.4f}" if outputs["URE"] is not None else "N/A",
}

if application == "ORC":
    notes["Offtaker inlet temperature (°C)"] = (
        f"{outputs['Tofftaker_in']:.2f}" if outputs["Tofftaker_in"] is not None else "N/A"
    )
    notes["Performance source"] = outputs["eta_source"]
    notes["Efficiency used"] = f"{outputs['eta_used']:.4f} ({outputs['eta_used'] * 100:.2f}%)"
    if outputs["eta_model"] is not None:
        notes["Internal ORC model efficiency"] = (
            f"{outputs['eta_model']:.4f} ({outputs['eta_model'] * 100:.2f}%)"
        )

elif application == "Cold water generation using an absorption chiller":
    notes["Offtaker inlet temperature (°C)"] = (
        f"{outputs['Tofftaker_in']:.2f}" if outputs["Tofftaker_in"] is not None else "N/A"
    )
    notes["Absorption chiller evaporator temperature (°C)"] = outputs["abs_evap_temp_c"]
    notes["Performance source"] = outputs["eta_source"]
    notes["Absorption chiller COP used"] = f"{outputs['COP_abs']:.4f}"
    if outputs["eta_model"] is not None:
        notes["Internal absorption chiller COP model"] = f"{outputs['eta_model']:.4f}"

st.dataframe(pd.DataFrame([notes]), use_container_width=True)

st.caption(
    "This version uses P_IT as the base for data-center waste heat recovery. "
    "ERF and ERE are calculated from reused data-center waste heat only. "
    "URE represents the useful output generated by the selected application, normalized by IT power."
)
