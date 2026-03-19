import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="FCAT Waste Heat Reuse Demo - V2",
    layout="wide"
)

st.title("FCAT Waste Heat Reuse Demo")
st.markdown("Select cooling system type, location, and offtaker application.")


# =========================
# Case metadata
# =========================
CASE_METADATA = {
    1: {
        "label": "Case 1 - Large - Airside economizer + adiabatic cooling + (water-cooled)",
        "default_temp_c": 30.0
    },
    2: {
        "label": "Case 2 - Large - Water economizer + (water-cooled)",
        "default_temp_c": 30.0
    },
    3: {
        "label": "Case 3 - Midsize - Airside economizer + (water-cooled chiller)",
        "default_temp_c": 30.0
    },
    4: {
        "label": "Case 4 - Midsize - Water economizer + (water-cooled)",
        "default_temp_c": 30.0
    },
    5: {
        "label": "Case 5 - Midsize - Water-cooled chiller",
        "default_temp_c": 30.0
    },
    6: {
        "label": "Case 6 - Midsize - Airside economizer + (air-cooled chiller)",
        "default_temp_c": 30.0
    },
    7: {
        "label": "Case 7 - Midsize - Air-cooled chiller",
        "default_temp_c": 27.0
    },
    8: {
        "label": "Case 8 - Small - Water cooled chiler",
        "default_temp_c": 27.0
    },
    9: {
        "label": "Case 9 - Small - Air-cooled chiller",
        "default_temp_c": 27.0
    },
    10: {
        "label": "Case 10 - Small - Direct expansion (DX) system",
        "default_temp_c": 25.0
    },
    11: {
        "label": "Case 11 - large - Airside economizer + (air-cooled chiller)",
        "default_temp_c": 30.0
    },
    12: {
        "label": "Case 12 - large - water cooled chiler + dry cooling tower + free cooling",
        "default_temp_c": 45.0
    },
    13: {
        "label": "Case 13 - large - Immersion + Air coold chiler + free coling",
        "default_temp_c": 55.0
    },
    14: {
        "label": "Case 14 - large - Cold-Plate + Air coold chiler + free coling",
        "default_temp_c": 50.0
    },
}


# فقط همین 6 لوکیشن
ALLOWED_LOCATIONS = [
    "Fargo ND",
    "Knoxville TN",
    "Lubbock TX",
    "Midland TX",
    "Nashville TN",
    "Omaha NE",
]

# فعلاً فقط ORC فعال است
APPLICATION_OPTIONS = [
    "ORC",
    "Cold water generation using an absorption chiller",
]


# =========================
# Helper functions
# =========================
def normalize_text(x):
    return str(x).strip().lower()


def eta_use_orc(T_C):
    """
    ORC utilization efficiency as a function of waste heat temperature.
    Output is fraction, e.g. 0.02 = 2%
    """
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


def get_eta_use(T_avail_C, application):
    app = str(application).strip()

    if app == "ORC":
        return float(eta_use_orc(np.array([T_avail_C]))[0])

    # فعلاً فقط نمایشی است و محاسبه فعال نیست
    return None


@st.cache_data
def load_results_table(csv_path):
    df = pd.read_csv(csv_path)

    expected_cols = [
        "cooling system type",
        "climate zone",
        "Location",
        "PUE mean",
        "Qavail mean kW",
        "eta mean",
        "ERE mean",
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(
            "Missing required columns in CSV: " + ", ".join(missing)
        )

    # force case column to string for robust matching
    df["cooling system type"] = df["cooling system type"].astype(str).str.strip()
    df["Location"] = df["Location"].astype(str).str.strip()
    df["climate zone"] = df["climate zone"].astype(str).str.strip()

    df["_cooling_norm"] = df["cooling system type"].apply(normalize_text)
    df["_location_norm"] = df["Location"].apply(normalize_text)

    return df


def get_default_temperature(case_num):
    return CASE_METADATA[case_num]["default_temp_c"]


def parse_case_number_from_option(option_text):
    """
    option_text example:
    'Case 14 - large - Cold-Plate + Air coold chiler+free coling'
    """
    first_part = option_text.split("-")[0].strip()
    case_num = int(first_part.replace("Case", "").strip())
    return case_num


def calculate_outputs_from_row(row, selected_application, waste_temp_input_c, asic_checked):
    effective_temp_c = float(waste_temp_input_c)
    if asic_checked:
        effective_temp_c += 5.0

    pue_mean = float(row["PUE mean"])
    qavail_mean_kw = float(row["Qavail mean kW"])

    if selected_application == "ORC":
        eta = get_eta_use(effective_temp_c, selected_application)
        ere_mean = pue_mean * (1.0 - eta)
    else:
        eta = None
        ere_mean = None

    return {
        "PUE mean": pue_mean,
        "Qavail mean kW": qavail_mean_kw,
        "eta mean": eta,
        "ERE mean": ere_mean,
        "effective_temp_c": effective_temp_c,
    }


# =========================
# File path
# =========================
DEFAULT_CSV = "fcat_case_location_table.csv"

st.sidebar.header("Data Source")
csv_file = st.sidebar.text_input(
    "Results table CSV file",
    value=DEFAULT_CSV
)

st.sidebar.caption(
    "Update this CSV in GitHub later. The app reads the table from this file."
)


# =========================
# Load data
# =========================
try:
    df_results = load_results_table(csv_file)
except Exception as e:
    st.error(f"Could not load results table: {e}")
    st.stop()


# =========================
# UI selections
# =========================
left_col, right_col = st.columns([1, 1])

with left_col:
    case_options = [CASE_METADATA[k]["label"] for k in sorted(CASE_METADATA.keys())]
    selected_case_option = st.selectbox(
        "Cooling system type",
        options=case_options,
        index=13  # default = Case 14
    )

    selected_case_num = parse_case_number_from_option(selected_case_option)

    st.caption(f"Selected system: {CASE_METADATA[selected_case_num]['label']}")

    default_temp_c = get_default_temperature(selected_case_num)

    waste_temp_input_c = st.number_input(
        "Waste heat temperature (°C) - editable",
        min_value=0.0,
        max_value=120.0,
        value=float(default_temp_c),
        step=1.0
    )

    asic_checked = st.checkbox("ASIC chips (+5 °C)", value=False)

with right_col:
    selected_location = st.selectbox(
        "Location",
        options=ALLOWED_LOCATIONS
    )

    selected_application = st.selectbox(
        "Offtaker application",
        options=APPLICATION_OPTIONS,
        index=0
    )

    if selected_application != "ORC":
        st.info("This application is display-only for now. Only ORC is active.")


# =========================
# Match row in CSV
# =========================
selected_location_norm = normalize_text(selected_location)
selected_case_str = str(selected_case_num).strip()

matched = df_results[
    (df_results["cooling system type"].astype(str).str.strip() == selected_case_str) &
    (df_results["_location_norm"] == selected_location_norm)
]

if matched.empty:
    st.warning(
        "No matching row found in the CSV for the selected cooling system type and location."
    )
    st.stop()

row = matched.iloc[0]


# =========================
# Calculations
# =========================
outputs = calculate_outputs_from_row(
    row=row,
    selected_application=selected_application,
    waste_temp_input_c=waste_temp_input_c,
    asic_checked=asic_checked
)


# =========================
# Display selected input summary
# =========================
st.subheader("Selected Inputs")

summary_df = pd.DataFrame([{
    "Cooling system type": selected_case_option,
    "Climate zone": row["climate zone"],
    "Location": row["Location"],
    "Offtaker application": selected_application,
    "Default waste heat temperature (°C)": default_temp_c,
    "User-entered waste heat temperature (°C)": waste_temp_input_c,
    "ASIC checked": asic_checked,
    "Effective waste heat temperature (°C)": outputs["effective_temp_c"],
}])

st.dataframe(summary_df, use_container_width=True)


# =========================
# Main results
# =========================
st.subheader("Results")

if selected_application == "ORC":
    results_df = pd.DataFrame([{
        "cooling system type": selected_case_option,
        "climate zone": row["climate zone"],
        "Location": row["Location"],
        "PUE mean": outputs["PUE mean"],
        "Qavail mean kW": outputs["Qavail mean kW"],
        "eta mean": outputs["eta mean"],
        "ERE mean": outputs["ERE mean"],
    }])
else:
    results_df = pd.DataFrame([{
        "cooling system type": selected_case_option,
        "climate zone": row["climate zone"],
        "Location": row["Location"],
        "PUE mean": outputs["PUE mean"],
        "Qavail mean kW": outputs["Qavail mean kW"],
        "eta mean": "Not active yet",
        "ERE mean": "Not active yet",
    }])

st.dataframe(results_df, use_container_width=True)


# =========================
# Quick metrics
# =========================
st.subheader("Key Metrics")

m1, m2, m3, m4 = st.columns(4)

m1.metric("PUE mean", f"{outputs['PUE mean']:.4f}")
m2.metric("Qavail mean kW", f"{outputs['Qavail mean kW']:.2f}")
m3.metric(
    "eta mean",
    f"{outputs['eta mean']:.4f}" if outputs["eta mean"] is not None else "N/A"
)
m4.metric(
    "ERE mean",
    f"{outputs['ERE mean']:.4f}" if outputs["ERE mean"] is not None else "N/A"
)


# =========================
# Show source table
# =========================
with st.expander("Show source table currently loaded"):
    st.dataframe(
        df_results[
            [
                "cooling system type",
                "climate zone",
                "Location",
                "PUE mean",
                "Qavail mean kW",
                "eta mean",
                "ERE mean",
            ]
        ],
        use_container_width=True
    )


# =========================
# Download current displayed result
# =========================
csv_download = results_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download displayed result as CSV",
    data=csv_download,
    file_name="selected_result_v2.csv",
    mime="text/csv"
)
