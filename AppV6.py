import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------------------------------------------
# Page setup
# -------------------------------------------------------------------
st.set_page_config(page_title="FCAT Waste Heat Reuse Demo - V6", layout="wide")

st.title("FCAT Waste Heat Reuse Demo")
st.markdown(
    "Select cooling system type, state, county, and offtaker application. "
    "This version includes ORC, absorption chiller, and water reclamation URE formulations."
)

# -------------------------------------------------------------------
# Cooling system metadata
# -------------------------------------------------------------------
CASE_METADATA = {
    1: {
        "label": "Case 1 - Large - Airside economizer + adiabatic cooling + (water-cooled)",
        "default_temp_c": 45.0,
        "size": "Large",
        "heat_removal": "Airside economizer + adiabatic cooling",
        "chiller": "Water-cooled",
        "economizer": "Airside economizer",
        "liquid_cooling": "No",
        "short_description": "Large data center with airside economizer and adiabatic cooling, using a water-cooled system.",
    },
    2: {
        "label": "Case 2 - Large - Water economizer + (water-cooled)",
        "default_temp_c": 45.0,
        "size": "Large",
        "heat_removal": "Water economizer",
        "chiller": "Water-cooled",
        "economizer": "Water economizer",
        "liquid_cooling": "No",
        "short_description": "Large data center using a water economizer with a water-cooled system.",
    },
    3: {
        "label": "Case 3 - Midsize - Airside economizer + (water-cooled chiller)",
        "default_temp_c": 45.0,
        "size": "Midsize",
        "heat_removal": "Airside economizer",
        "chiller": "Water-cooled chiller",
        "economizer": "Airside economizer",
        "liquid_cooling": "No",
        "short_description": "Midsize data center with airside economizer and water-cooled chiller.",
    },
    4: {
        "label": "Case 4 - Midsize - Water economizer + (water-cooled)",
        "default_temp_c": 45.0,
        "size": "Midsize",
        "heat_removal": "Water economizer",
        "chiller": "Water-cooled",
        "economizer": "Water economizer",
        "liquid_cooling": "No",
        "short_description": "Midsize data center using a water economizer with water-cooled equipment.",
    },
    5: {
        "label": "Case 5 - Midsize - Water-cooled chiller",
        "default_temp_c": 45.0,
        "size": "Midsize",
        "heat_removal": "Mechanical cooling",
        "chiller": "Water-cooled chiller",
        "economizer": "None",
        "liquid_cooling": "No",
        "short_description": "Midsize data center using a water-cooled chiller without economizer.",
    },
    6: {
        "label": "Case 6 - Midsize - Airside economizer + (air-cooled chiller)",
        "default_temp_c": 45.0,
        "size": "Midsize",
        "heat_removal": "Airside economizer",
        "chiller": "Air-cooled chiller",
        "economizer": "Airside economizer",
        "liquid_cooling": "No",
        "short_description": "Midsize data center with airside economizer and air-cooled chiller.",
    },
    7: {
        "label": "Case 7 - Midsize - Air-cooled chiller",
        "default_temp_c": 45.0,
        "size": "Midsize",
        "heat_removal": "Mechanical cooling",
        "chiller": "Air-cooled chiller",
        "economizer": "None",
        "liquid_cooling": "No",
        "short_description": "Midsize data center using an air-cooled chiller without economizer.",
    },
    8: {
        "label": "Case 8 - Small - Water-cooled chiller",
        "default_temp_c": 45.0,
        "size": "Small",
        "heat_removal": "Mechanical cooling",
        "chiller": "Water-cooled chiller",
        "economizer": "None",
        "liquid_cooling": "No",
        "short_description": "Small data center using a water-cooled chiller.",
    },
    9: {
        "label": "Case 9 - Small - Air-cooled chiller",
        "default_temp_c": 45.0,
        "size": "Small",
        "heat_removal": "Mechanical cooling",
        "chiller": "Air-cooled chiller",
        "economizer": "None",
        "liquid_cooling": "No",
        "short_description": "Small data center using an air-cooled chiller.",
    },
    10: {
        "label": "Case 10 - Small - Direct expansion (DX) system",
        "default_temp_c": 45.0,
        "size": "Small",
        "heat_removal": "Direct expansion cooling",
        "chiller": "DX system",
        "economizer": "None",
        "liquid_cooling": "No",
        "short_description": "Small data center using direct expansion (DX) cooling.",
    },
    11: {
        "label": "Case 11 - Large - Airside economizer + (air-cooled chiller)",
        "default_temp_c": 45.0,
        "size": "Large",
        "heat_removal": "Airside economizer",
        "chiller": "Air-cooled chiller",
        "economizer": "Airside economizer",
        "liquid_cooling": "No",
        "short_description": "Large data center with airside economizer and air-cooled chiller.",
    },
    12: {
        "label": "Case 12 - Large - Cold Plate + Water-cooled chiller + dry cooling tower + free cooling + 25% CRAC",
        "default_temp_c": 45.0,
        "size": "Large",
        "heat_removal": "Free cooling + dry cooling tower + Cold Plate",
        "chiller": "Water-cooled chiller",
        "economizer": "Free cooling",
        "liquid_cooling": "Yes - Cold plate",
        "short_description": "Large data center using cold plate cooling, water-cooled chiller, dry cooling tower, free cooling, and 25% CRAC.",
    },
    13: {
        "label": "Case 13 - Large - Immersion + Water-cooled chiller + dry cooling tower + free cooling",
        "default_temp_c": 55.0,
        "size": "Large",
        "heat_removal": "Immersion cooling",
        "chiller": "Air-cooled chiller",
        "economizer": "Free cooling",
        "liquid_cooling": "Yes - Immersion",
        "short_description": "Large data center with immersion cooling, air-cooled chiller, and free cooling.",
    },
    14: {
        "label": "Case 14 - Large - Cold-Plate + Air-cooled chiller + free cooling",
        "default_temp_c": 50.0,
        "size": "Large",
        "heat_removal": "Cold-plate cooling",
        "chiller": "Air-cooled chiller",
        "economizer": "Free cooling",
        "liquid_cooling": "Yes - Cold plate",
        "short_description": "Large data center with cold-plate cooling, air-cooled chiller, and free cooling.",
    },
}

APPLICATION_OPTIONS = [
    "ORC",
    "Cold water generation using an absorption chiller",
    "Water reclamation",
]

ABSORPTION_EVAP_OPTIONS = [-10, -5, 0]

# Advisor-requested conversion factor:
# This is NOT the absorption chiller COP.
# It is only used to convert cooling thermal output to electric-equivalent output.
DX_CHILLER_COP = 3.0

# Heat pump COP model for waste heat boosting.
# COP_HP = 52.94 * (DeltaT_lift)^(-0.716), where DeltaT_lift = T_boosted - T_available.
HP_COP_MODEL_NAME = "Bever et al. (2024) high-temperature heat pump temperature-lift correlation"

# Fraction of IT heat assumed available for reuse for each cooling system case.
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

WR_CASE_COLUMN_MAP = {
    "A": {
        "WRE": "WR_CaseA_WRE_g_per_kJ",
        "DWF": "WR_CaseA_DWF_L_per_kWh",
        "DWSF": "WR_CaseA_DWSF_L_per_kWh",
    },
    "B": {
        "WRE": "WR_CaseB_WRE_g_per_kJ",
        "DWF": "WR_CaseB_DWF_L_per_kWh",
        "DWSF": "WR_CaseB_DWSF_L_per_kWh",
    },
}

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def normalize_text(x):
    return str(x).strip().lower()


def eta_use_orc(T_C):
    """Second-order polynomial fit for ORC efficiency as a function of waste heat temperature."""
    T_C = np.asarray(T_C, dtype=float)
    T_C = np.clip(T_C, 42.7314, 84.3096)

    a = -9.77832291e-04
    b = 1.91002705e-01
    c = -4.50769764e00

    eta_percent = a * T_C**2 + b * T_C + c
    eta_percent = np.clip(eta_percent, 0.0, None)
    return eta_percent / 100.0


def cop_use_absorption(T_gen_C, T_evap_C):
    """Polynomial fits for absorption chiller COP at selected evaporator temperatures."""
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
    if application == "ORC":
        return float(eta_use_orc(np.array([T_avail_C]))[0])

    if application == "Cold water generation using an absorption chiller":
        if abs_evap_temp_c is None:
            raise ValueError("abs_evap_temp_c is required for the absorption chiller application.")
        return float(cop_use_absorption(np.array([T_avail_C]), abs_evap_temp_c)[0])

    return None


def heat_pump_cop_heating(T_in_C, T_out_C):
    """
    Heating-mode heat pump COP for waste heat boosting.

    T_in_C: available waste heat temperature going into the booster.
    T_out_C: selected boosted temperature delivered to the offtaker.

    COP_HP = 52.94 * (DeltaT_lift)^(-0.716)
    DeltaT_lift = T_out_C - T_in_C.
    """
    delta_t_lift = float(T_out_C) - float(T_in_C)

    if delta_t_lift <= 0:
        return None

    cop_hp = 52.94 * (delta_t_lift ** -0.716)

    # Heating COP must be above 1 to compute W = Q_waste / (COP_HP - 1).
    return max(float(cop_hp), 1.01)


def calculate_heat_pump_boost(p_wh_use, T_in_C, boost_enabled=False, boosted_temp_c=None):
    """
    Waste heat boosting calculation.

    Without boost:
        E_boost = 0
        Q_heat_to_offtaker = Pwh,use

    With boost:
        COP_HP = Q_hot / W_HP
        Q_hot = Q_waste + W_HP
        W_HP = Q_waste / (COP_HP - 1)
        Q_heat_to_offtaker = Q_waste + W_HP
    """
    p_wh_use = float(p_wh_use)

    if not boost_enabled:
        return {
            "boost_enabled": False,
            "T_source_C": float(T_in_C),
            "T_offtaker_in_C": float(T_in_C),
            "COP_HP": None,
            "E_boost": 0.0,
            "Q_heat_to_offtaker": p_wh_use,
            "HP_COP_model": HP_COP_MODEL_NAME,
        }

    if boosted_temp_c is None:
        raise ValueError("A boosted temperature is required when waste heat boosting is enabled.")

    if float(boosted_temp_c) <= float(T_in_C):
        raise ValueError("Boosted temperature must be greater than the available waste heat temperature.")

    cop_hp = heat_pump_cop_heating(T_in_C=T_in_C, T_out_C=boosted_temp_c)
    if cop_hp is None or cop_hp <= 1.0:
        raise ValueError("Heat pump COP must be greater than 1. Check boosted temperature selection.")

    e_boost = p_wh_use / (cop_hp - 1.0)
    q_heat_to_offtaker = p_wh_use + e_boost

    return {
        "boost_enabled": True,
        "T_source_C": float(T_in_C),
        "T_offtaker_in_C": float(boosted_temp_c),
        "COP_HP": cop_hp,
        "E_boost": e_boost,
        "Q_heat_to_offtaker": q_heat_to_offtaker,
        "HP_COP_model": HP_COP_MODEL_NAME,
    }


def get_water_reclamation_case(case_info):
    """
    Map FCAT cooling cases to Megan's water reclamation cases.

    Current implementation uses IT-side liquid-cooling configuration:
        - No IT-side liquid cooling -> Megan Case A
        - Cold plate or immersion/hybrid IT cooling -> Megan Case B

    This means water-cooled chiller cases without IT-side liquid cooling are mapped to Case A.
    """
    liquid_label = normalize_text(case_info.get("liquid_cooling", "No"))
    if liquid_label.startswith("yes"):
        return "B"
    return "A"


# -------------------------------------------------------------------
# URE formulations
# -------------------------------------------------------------------
def calculate_ure_orc(e_elect, e_boost, e_it):
    """URE_ORC = (electric output - boost electricity) / IT energy."""
    return (float(e_elect) - float(e_boost)) / float(e_it)


def calculate_ure_absorption(q_cooling_thermal, e_boost, e_it, dx_chiller_cop=DX_CHILLER_COP):
    """
    Absorption chiller URE.

    COP_absorption is used upstream to calculate Q_cooling_thermal.
    COP_DX = 3.0 is only a conversion factor from thermal cooling to electric-equivalent benefit.

    URE_abs = ((Q_cooling_thermal / COP_DX) - E_boost) / E_IT
    """
    q_cooling_thermal = float(q_cooling_thermal)
    e_boost = float(e_boost)
    e_it = float(e_it)
    dx_chiller_cop = float(dx_chiller_cop)

    if dx_chiller_cop <= 0:
        raise ValueError("DX chiller COP must be greater than zero.")
    if e_it <= 0:
        raise ValueError("E_IT must be greater than zero.")

    cooling_electric_equivalent = q_cooling_thermal / dx_chiller_cop
    ure_abs = (cooling_electric_equivalent - e_boost) / e_it
    return ure_abs, cooling_electric_equivalent


def calculate_ure_water_reclamation(dwsf_l_per_kwh, swi_l_per_kwh, e_wr, e_it):
    """
    Water reclamation URE using the corrected formulation from unit analysis.

    Megan's normalized DWSF is interpreted as:
        DWSF_Megan = Delta_WSF / E_WR

    where E_WR is the energy input to the water reclamation system.
    In this app, E_WR is represented by heat pump boost electricity:
        E_WR = E_boost

    Therefore:
        Delta_WSF_total = DWSF_Megan * E_WR
        URE_water = -Delta_WSF_total / (SWI * E_IT)

    Do NOT multiply DWSF directly by Q_heat_to_application here.
    Do NOT add SWI * E_boost separately here, because that penalty is already included
    in DWSF_Megan per unit E_WR.
    """
    dwsf_l_per_kwh = float(dwsf_l_per_kwh)
    swi_l_per_kwh = float(swi_l_per_kwh)
    e_wr = float(e_wr)
    e_it = float(e_it)

    if swi_l_per_kwh <= 0:
        raise ValueError("WR_SWI_L_per_kWh must be greater than zero.")
    if e_it <= 0:
        raise ValueError("E_IT must be greater than zero.")
    if e_wr < 0:
        raise ValueError("E_WR must be non-negative.")

    delta_wsf_total = dwsf_l_per_kwh * e_wr
    ure_water = -delta_wsf_total / (swi_l_per_kwh * e_it)
    water_scarcity_benefit = -delta_wsf_total

    return ure_water, delta_wsf_total, water_scarcity_benefit


def calculate_ure_carbon_future(m_co2_removed, cef, e_boost, e_it):
    """Future placeholder: URE_CCS = ((m_CO2_removed / CEF) - E_boost) / E_IT."""
    if cef <= 0:
        raise ValueError("CEF must be greater than zero.")
    carbon_energy_equivalent = m_co2_removed / cef
    return (carbon_energy_equivalent - e_boost) / e_it


# -------------------------------------------------------------------
# Data loading and filtering
# -------------------------------------------------------------------
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
        "State",
        "County",
        "cooling system type",
        "climate zone",
        "PUE mean",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns in input file: " + ", ".join(missing))

    optional_cols = [
        "WR_reference_city",
        "WR_reference_county",
        "WR_EWIF_L_per_kWh",
        "WR_AWARE_CF",
        "WR_SWI_L_per_kWh",
        "WR_CaseA_WRE_g_per_kJ",
        "WR_CaseA_DWF_L_per_kWh",
        "WR_CaseA_DWSF_L_per_kWh",
        "WR_CaseB_WRE_g_per_kJ",
        "WR_CaseB_DWF_L_per_kWh",
        "WR_CaseB_DWSF_L_per_kWh",
    ]
    for col in optional_cols:
        if col not in df.columns:
            df[col] = np.nan

    df["State"] = df["State"].astype(str).str.strip()
    df["County"] = df["County"].astype(str).str.strip()
    df["climate zone"] = df["climate zone"].astype(str).str.strip()
    df["cooling system type"] = pd.to_numeric(df["cooling system type"], errors="coerce").astype("Int64")
    df["PUE mean"] = pd.to_numeric(df["PUE mean"], errors="coerce")

    numeric_optional_cols = [
        "WR_EWIF_L_per_kWh",
        "WR_AWARE_CF",
        "WR_SWI_L_per_kWh",
        "WR_CaseA_WRE_g_per_kJ",
        "WR_CaseA_DWF_L_per_kWh",
        "WR_CaseA_DWSF_L_per_kWh",
        "WR_CaseB_WRE_g_per_kJ",
        "WR_CaseB_DWF_L_per_kWh",
        "WR_CaseB_DWSF_L_per_kWh",
    ]
    for col in numeric_optional_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["State", "County", "cooling system type"])
    df["_state_norm"] = df["State"].apply(normalize_text)
    df["_county_norm"] = df["County"].apply(normalize_text)
    return df


def get_states(df):
    return sorted(df["State"].dropna().astype(str).unique())


def get_counties_for_state(df, selected_state):
    filtered = df[df["_state_norm"] == normalize_text(selected_state)]
    return sorted(filtered["County"].dropna().astype(str).unique())


# -------------------------------------------------------------------
# Main calculation
# -------------------------------------------------------------------
def calculate_outputs(
    case_num,
    row,
    application,
    temp,
    asic,
    phi_use=1.0,
    boost_enabled=False,
    boosted_temp_c=None,
    pue_override_enabled=False,
    pue_override_value=None,
    eta_override_enabled=False,
    eta_override_value=None,
    abs_evap_temp_c=None,
):
    # Normalized IT load. Because P_IT = 1.0, all power/energy values are normalized by IT load.
    p_it = 1.0

    effective_temp = float(temp) + (5.0 if asic else 0.0)

    pue_from_file = None if pd.isna(row["PUE mean"]) else float(row["PUE mean"])
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

    # ERF and ERE are based on reused data-center waste heat before any heat-pump electricity addition.
    erf = p_wh_use / p_dc if p_dc != 0 else np.nan
    ere = (p_dc - p_wh_use) / p_it

    boost_outputs = calculate_heat_pump_boost(
        p_wh_use=p_wh_use,
        T_in_C=effective_temp,
        boost_enabled=boost_enabled,
        boosted_temp_c=boosted_temp_c,
    )

    e_boost = boost_outputs["E_boost"]
    p_total_to_offtaker = boost_outputs["Q_heat_to_offtaker"]
    t_offtaker_in = boost_outputs["T_offtaker_in_C"]

    # Default output placeholders.
    eta_model = None
    eta_used = None
    eta_source = "Not used"
    p_orc = None
    cop_abs = None
    q_cooling = None
    q_cooling_electric_equiv = None
    wr_case = None
    wr_dwsf = None
    wr_swi = None
    wr_wre = None
    wr_dwf = None
    wr_ewif = None
    wr_acf = None
    wr_reference_city = row.get("WR_reference_city", None)
    wr_reference_county = row.get("WR_reference_county", None)
    wr_e_wr = None
    wr_delta_wsf_total = None
    wr_scarcity_benefit = None
    useful_output = None
    ure = None
    ure_basis = "Not applicable"

    if application == "ORC":
        if eta_override_enabled:
            eta_used = float(eta_override_value)
            eta_source = "Manual override"
            eta_model = get_offtaker_performance(t_offtaker_in, application)
        else:
            eta_model = get_offtaker_performance(t_offtaker_in, application)
            eta_used = eta_model
            eta_source = "Internal ORC model"

        p_orc = eta_used * p_total_to_offtaker
        useful_output = p_orc
        ure = calculate_ure_orc(e_elect=p_orc, e_boost=e_boost, e_it=p_it)
        ure_basis = "ORC: electric output minus heat pump boost electricity, normalized by IT load"

    elif application == "Cold water generation using an absorption chiller":
        if eta_override_enabled:
            cop_abs = float(eta_override_value)
            eta_source = "Manual override"
            eta_model = get_offtaker_performance(t_offtaker_in, application, abs_evap_temp_c=abs_evap_temp_c)
        else:
            eta_model = get_offtaker_performance(t_offtaker_in, application, abs_evap_temp_c=abs_evap_temp_c)
            cop_abs = eta_model
            eta_source = "Internal absorption chiller COP model"

        eta_used = cop_abs
        q_cooling = cop_abs * p_total_to_offtaker
        ure, q_cooling_electric_equiv = calculate_ure_absorption(
            q_cooling_thermal=q_cooling,
            e_boost=e_boost,
            e_it=p_it,
            dx_chiller_cop=DX_CHILLER_COP,
        )
        useful_output = q_cooling_electric_equiv
        ure_basis = (
            "Absorption chiller: cooling output converted to electric-equivalent using "
            f"DX COP = {DX_CHILLER_COP:.1f}, minus heat pump boost electricity, normalized by IT load"
        )

    elif application == "Water reclamation":
        wr_case = get_water_reclamation_case(CASE_METADATA[case_num])
        wr_cols = WR_CASE_COLUMN_MAP[wr_case]

        wr_dwsf = None if pd.isna(row[wr_cols["DWSF"]]) else float(row[wr_cols["DWSF"]])
        wr_wre = None if pd.isna(row[wr_cols["WRE"]]) else float(row[wr_cols["WRE"]])
        wr_dwf = None if pd.isna(row[wr_cols["DWF"]]) else float(row[wr_cols["DWF"]])
        wr_swi = None if pd.isna(row["WR_SWI_L_per_kWh"]) else float(row["WR_SWI_L_per_kWh"])
        wr_ewif = None if pd.isna(row["WR_EWIF_L_per_kWh"]) else float(row["WR_EWIF_L_per_kWh"])
        wr_acf = None if pd.isna(row["WR_AWARE_CF"]) else float(row["WR_AWARE_CF"])

        if wr_dwsf is None or wr_swi is None:
            raise ValueError(
                f"Water reclamation requires {wr_cols['DWSF']} and WR_SWI_L_per_kWh "
                "in the input file for the selected county/climate zone."
            )

        # Corrected unit-consistent interpretation:
        # DWSF_Megan = Delta_WSF / E_WR.
        # In the app, E_WR is represented by the heat-pump boost electricity.
        wr_e_wr = e_boost
        ure, wr_delta_wsf_total, wr_scarcity_benefit = calculate_ure_water_reclamation(
            dwsf_l_per_kwh=wr_dwsf,
            swi_l_per_kwh=wr_swi,
            e_wr=wr_e_wr,
            e_it=p_it,
        )
        useful_output = wr_scarcity_benefit
        eta_source = f"Megan Ward Case {wr_case} DWSF/SWI table mapped by climate zone"
        ure_basis = (
            f"Water reclamation: Megan Case {wr_case} DWSF scaled by E_WR, "
            "where E_WR is the energy input to the water reclamation/boosting system. "
            "URE_water = -(DWSF × E_WR) / (SWI × E_IT)."
        )

    return {
        "PIT": p_it,
        "PDC": p_dc,
        "PUE mean": pue,
        "PUE source": pue_source,
        "PUE file value": pue_from_file,
        "Qavail": q_avail,
        "phi_use": phi_use,
        "Pwh_avail": p_wh_avail,
        "Pwh_use": p_wh_use,
        "ERF mean": erf,
        "ERE mean": ere,
        "effective_temp": effective_temp,
        "boost_enabled": boost_outputs["boost_enabled"],
        "boosted_temp_c": boosted_temp_c if boost_outputs["boost_enabled"] else None,
        "Tsource_HP_C": boost_outputs["T_source_C"],
        "Tofftaker_in": t_offtaker_in,
        "COP_HP": boost_outputs["COP_HP"],
        "Eboost": e_boost,
        "HP_COP_model": boost_outputs["HP_COP_model"],
        "Ptotal_offtaker": p_total_to_offtaker,
        "eta_model": eta_model,
        "eta_used": eta_used,
        "eta_source": eta_source,
        "PORC": p_orc,
        "COP_abs": cop_abs,
        "Q_cooling": q_cooling,
        "Q_cooling_electric_equiv": q_cooling_electric_equiv,
        "DX_chiller_COP": DX_CHILLER_COP,
        "WR_case_used": wr_case,
        "WR_reference_city": wr_reference_city,
        "WR_reference_county": wr_reference_county,
        "WR_WRE_g_per_kJ": wr_wre,
        "WR_DWF_L_per_kWh": wr_dwf,
        "WR_DWSF_L_per_kWh": wr_dwsf,
        "WR_EWIF_L_per_kWh": wr_ewif,
        "WR_AWARE_CF": wr_acf,
        "WR_SWI_L_per_kWh": wr_swi,
        "WR_E_WR": wr_e_wr,
        "WR_delta_wsf_total": wr_delta_wsf_total,
        "WR_scarcity_benefit": wr_scarcity_benefit,
        "useful_output": useful_output,
        "URE": ure,
        "URE basis": ure_basis,
        "abs_evap_temp_c": abs_evap_temp_c,
    }


# -------------------------------------------------------------------
# File input
# -------------------------------------------------------------------
data_file = st.sidebar.text_input(
    "PUE + water reclamation data file (.csv or .xlsx)",
    "based_on_state_county_add_w_reclamation_v2.csv",
)

try:
    df = load_pue_table(data_file)
except FileNotFoundError:
    st.error(f"File not found: {data_file}. Make sure the file is in the GitHub repo root and the name matches exactly.")
    st.stop()
except Exception as e:
    st.error(f"Could not load input file. {e}")
    st.stop()


# -------------------------------------------------------------------
# UI inputs
# -------------------------------------------------------------------
st.subheader("Inputs")

case_label = st.selectbox(
    "Cooling system type",
    [CASE_METADATA[k]["label"] for k in CASE_METADATA],
    index=13,
)
case_num = int(case_label.split("-")[0].replace("Case", "").strip())
default_temp = CASE_METADATA[case_num]["default_temp_c"]
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
        help="Available fitted COP curves are for T_evap = -10, -5, and 0 °C.",
    )
else:
    abs_evap_temp_c = None

temp = st.number_input("Waste heat temperature (°C)", value=float(default_temp))
asic = st.checkbox("ASIC chips (+5°C)")
effective_temp_preview = float(temp) + (5.0 if asic else 0.0)

phi_use_percent = st.slider(
    "Used fraction of available waste heat (%)",
    min_value=0,
    max_value=100,
    value=100,
    step=5,
    help="Fraction of available data-center waste heat that is actually reused.",
)
phi_use = phi_use_percent / 100.0

# -------------------------------------------------------------------
# Waste heat boosting
# -------------------------------------------------------------------
st.subheader("Waste Heat Boosting")

boost_default = True if application == "Water reclamation" else False
boost_enabled = st.checkbox(
    "Boost waste heat temperature using a heat pump",
    value=boost_default,
    help=(
        "When enabled, the app estimates heat pump electricity required to raise waste heat "
        "from the available temperature to the selected boosted temperature. For water reclamation, "
        "this boost electricity is used as E_WR in the corrected URE formulation."
    ),
)

if boost_enabled:
    min_boost_temp = effective_temp_preview + 0.1
    default_boost_temp = max(effective_temp_preview + 5.0, 70.0)
    boosted_temp_c = st.number_input(
        "Boosted waste heat temperature delivered to offtaker (°C)",
        min_value=float(min_boost_temp),
        value=float(default_boost_temp),
        step=1.0,
        format="%.1f",
    )

    st.caption(
        "Heat pump COP is estimated using a high-temperature industrial heat pump correlation: "
        "COP_HP = 52.94 × ΔT_lift^(-0.716), where ΔT_lift = T_boosted - T_available."
    )

    try:
        hp_preview = calculate_heat_pump_boost(
            p_wh_use=Q_AVAIL_FACTOR[case_num] * phi_use,
            T_in_C=effective_temp_preview,
            boost_enabled=True,
            boosted_temp_c=boosted_temp_c,
        )
        st.info(
            f"Estimated heat pump COP = {hp_preview['COP_HP']:.3f}; "
            f"estimated boost electricity = {hp_preview['E_boost']:.4f} per unit IT load; "
            f"heat delivered to offtaker = {hp_preview['Q_heat_to_offtaker']:.4f} per unit IT load."
        )
    except Exception as e:
        st.warning(f"Boosting calculation issue: {e}")
else:
    boosted_temp_c = None
    if application == "Water reclamation":
        st.warning(
            "Water reclamation URE uses E_WR, the energy input to the water reclamation system. "
            "With boosting disabled, E_WR is currently modeled as 0, so water reclamation URE will be 0."
        )


# -------------------------------------------------------------------
# Case details
# -------------------------------------------------------------------
st.subheader("Cooling System Case Details")

wr_case_preview = get_water_reclamation_case(case_info)
case_details_df = pd.DataFrame([
    {
        "Case": f"Case {case_num}",
        "System size": case_info["size"],
        "Primary heat removal approach": case_info["heat_removal"],
        "Chiller/system type": case_info["chiller"],
        "Economizer type": case_info["economizer"],
        "IT-side liquid cooling": case_info["liquid_cooling"],
        "Megan WR case mapping": f"Case {wr_case_preview}",
        "Recommended waste heat temperature (°C)": case_info["default_temp_c"],
        "Q_avail factor": Q_AVAIL_FACTOR[case_num],
    }
])
st.dataframe(case_details_df, use_container_width=True)
st.info(case_info["short_description"])

if application == "Water reclamation" and wr_case_preview == "A" and "water-cooled" in normalize_text(case_info["chiller"]):
    st.warning(
        "This case uses water-cooled equipment at the chiller/system level but has no IT-side liquid cooling. "
        "It is currently mapped to Megan Case A based on IT-side cooling configuration, pending advisor confirmation."
    )


# -------------------------------------------------------------------
# Find matching row
# -------------------------------------------------------------------
matched = df[
    (df["_state_norm"] == normalize_text(state))
    & (df["_county_norm"] == normalize_text(county))
    & (df["cooling system type"] == case_num)
]

if matched.empty:
    st.warning("No matching row found for the selected state, county, and cooling system type.")
    st.stop()
row = matched.iloc[0]


# -------------------------------------------------------------------
# Optional overrides
# -------------------------------------------------------------------
st.subheader("Optional Overrides")
col1, col2 = st.columns(2)

with col1:
    pue_override_enabled = st.checkbox("Override PUE value")
    if pue_override_enabled:
        default_pue_for_override = float(row["PUE mean"]) if not pd.isna(row["PUE mean"]) else 1.20
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
        preview_primary_temp = boosted_temp_c if boost_enabled else effective_temp_preview
        eta_preview = get_offtaker_performance(
            preview_primary_temp,
            application,
            abs_evap_temp_c=abs_evap_temp_c,
        )

        eta_override_enabled = st.checkbox("Override offtaker performance")
        if application == "ORC":
            default_manual_value = float(eta_preview * 100.0)
            label_text = "Manual ORC efficiency (%)"
            min_val, max_val, step_val, format_val = 0.0, 100.0, 0.1, "%.2f"
        else:
            default_manual_value = float(eta_preview)
            label_text = "Manual absorption chiller COP"
            min_val, max_val, step_val, format_val = 0.0, 10.0, 0.01, "%.4f"

        if eta_override_enabled:
            manual_value = st.number_input(
                label_text,
                min_value=min_val,
                max_value=max_val,
                value=default_manual_value,
                step=step_val,
                format=format_val,
            )
            eta_override_value = manual_value / 100.0 if application == "ORC" else manual_value
        else:
            eta_override_value = None
    else:
        eta_override_enabled = False
        eta_override_value = None
        st.info("Water reclamation uses Megan's WR DWSF and SWI values from the input file; no performance override is used.")


# -------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------
if pd.isna(row["PUE mean"]) and not pue_override_enabled:
    st.warning(
        "PUE mean is not filled yet for the selected state, county, and cooling system type. "
        "Please use the PUE override option to continue."
    )
    st.stop()

if application == "Water reclamation":
    wr_case_validation = get_water_reclamation_case(case_info)
    dwsf_col = WR_CASE_COLUMN_MAP[wr_case_validation]["DWSF"]
    if dwsf_col not in row.index or pd.isna(row[dwsf_col]) or pd.isna(row["WR_SWI_L_per_kWh"]):
        st.warning(
            f"Water reclamation requires {dwsf_col} and WR_SWI_L_per_kWh in the input file. "
            "Please use the updated v2 file with Megan Ward's Case A and Case B values."
        )
        st.stop()
    if float(row["WR_SWI_L_per_kWh"]) <= 0:
        st.warning("WR_SWI_L_per_kWh must be greater than zero for the selected row.")
        st.stop()


# -------------------------------------------------------------------
# Calculate outputs
# -------------------------------------------------------------------
try:
    outputs = calculate_outputs(
        case_num=case_num,
        row=row,
        application=application,
        temp=temp,
        asic=asic,
        phi_use=phi_use,
        boost_enabled=boost_enabled,
        boosted_temp_c=boosted_temp_c,
        pue_override_enabled=pue_override_enabled,
        pue_override_value=pue_override_value,
        eta_override_enabled=eta_override_enabled,
        eta_override_value=eta_override_value,
        abs_evap_temp_c=abs_evap_temp_c,
    )
except Exception as e:
    st.error(f"Could not calculate outputs. {e}")
    st.stop()


# -------------------------------------------------------------------
# Selected inputs
# -------------------------------------------------------------------
st.subheader("Selected Inputs")
selected_inputs_df = pd.DataFrame([
    {
        "Cooling system type": case_label,
        "State": state,
        "County": county,
        "Climate zone": row["climate zone"],
        "Offtaker application": application,
        "Recommended waste heat temperature (°C)": default_temp,
        "User-entered waste heat temperature (°C)": temp,
        "ASIC checked": asic,
        "Effective available waste heat temperature (°C)": outputs["effective_temp"],
        "Boost enabled": outputs["boost_enabled"],
        "Boosted offtaker inlet temperature (°C)": outputs["boosted_temp_c"],
        "Heat pump COP model": outputs["HP_COP_model"],
        "Heat pump COP": outputs["COP_HP"],
        "Heat pump boost electricity, E_boost": outputs["Eboost"],
        "Absorption chiller evaporator temperature (°C)": outputs["abs_evap_temp_c"],
        "Q_avail factor": outputs["Qavail"],
        "Used waste heat fraction (%)": outputs["phi_use"] * 100,
        "PUE source": outputs["PUE source"],
        "Performance/data source": outputs["eta_source"],
    }
])
st.dataframe(selected_inputs_df, use_container_width=True)


# -------------------------------------------------------------------
# Results
# -------------------------------------------------------------------
st.subheader("Results")

common_results = {
    "Cooling system type": case_label,
    "State": state,
    "County": county,
    "Climate zone": row["climate zone"],
    "PUE file value": outputs["PUE file value"],
    "PUE used": outputs["PUE mean"],
    "Q_avail": outputs["Qavail"],
    "Pwh,avail (normalized)": outputs["Pwh_avail"],
    "Pwh,use before boost (normalized)": outputs["Pwh_use"],
    "Heat delivered to offtaker after boost (normalized)": outputs["Ptotal_offtaker"],
    "Available waste heat temperature (°C)": outputs["effective_temp"],
    "Offtaker inlet temperature (°C)": outputs["Tofftaker_in"],
    "Heat pump COP": outputs["COP_HP"],
    "Heat pump boost electricity, E_boost": outputs["Eboost"],
    "Useful output after application-specific conversion": outputs["useful_output"],
    "URE basis": outputs["URE basis"],
    "URE": outputs["URE"],
    "ERF mean": outputs["ERF mean"],
    "ERE mean": outputs["ERE mean"],
}

if application == "ORC":
    results_row = {
        **common_results,
        "ORC efficiency used": outputs["eta_used"],
        "ORC electric output": outputs["PORC"],
    }
elif application == "Cold water generation using an absorption chiller":
    results_row = {
        **common_results,
        "Absorption chiller evaporator temperature (°C)": outputs["abs_evap_temp_c"],
        "Absorption chiller COP used": outputs["COP_abs"],
        "Cooling output, thermal": outputs["Q_cooling"],
        "DX chiller COP for electric-equivalent conversion": outputs["DX_chiller_COP"],
        "Cooling output, electric-equivalent": outputs["Q_cooling_electric_equiv"],
    }
elif application == "Water reclamation":
    results_row = {
        **common_results,
        "Megan WR case used": outputs["WR_case_used"],
        "WR reference city": outputs["WR_reference_city"],
        "WR reference county": outputs["WR_reference_county"],
        "WR WRE (g/kJ)": outputs["WR_WRE_g_per_kJ"],
        "WR DWF (L/kWh of E_WR)": outputs["WR_DWF_L_per_kWh"],
        "WR DWSF (L/kWh of E_WR)": outputs["WR_DWSF_L_per_kWh"],
        "WR SWI (L/kWh)": outputs["WR_SWI_L_per_kWh"],
        "WR AWARE CF": outputs["WR_AWARE_CF"],
        "WR energy input, E_WR": outputs["WR_E_WR"],
        "WR total Delta WSF": outputs["WR_delta_wsf_total"],
        "WR scarcity benefit": outputs["WR_scarcity_benefit"],
    }
else:
    results_row = common_results

results_df = pd.DataFrame([results_row])
st.dataframe(results_df, use_container_width=True)


# -------------------------------------------------------------------
# Metrics
# -------------------------------------------------------------------
st.subheader("Metrics")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("PUE", f"{outputs['PUE mean']:.4f}", help="Power Usage Effectiveness = total data center power / IT power.")
with c2:
    st.metric("ERF", f"{outputs['ERF mean']:.4f}", help="Energy Reuse Factor = reused data center waste heat / total data center power.")
with c3:
    st.metric("ERE", f"{outputs['ERE mean']:.4f}", help="Energy Reuse Effectiveness = (total data center power - reused waste heat) / IT power.")
with c4:
    st.metric(
        "URE",
        f"{outputs['URE']:.4f}" if outputs["URE"] is not None else "N/A",
        help=(
            "Useful Reuse Effectiveness. ORC: electric output basis. Absorption: electric-equivalent cooling basis. "
            "Water reclamation: scarcity-footprint benefit normalized by SWI and IT load."
        ),
    )


# -------------------------------------------------------------------
# Metric explanations
# -------------------------------------------------------------------
st.subheader("Metric Explanations")
metric_explanations_rows = [
    {
        "Metric": "PUE",
        "Short description": "Total data center power divided by IT power.",
        "How to interpret": "Lower is generally better.",
    },
    {
        "Metric": "ERF",
        "Short description": "Reused data center waste heat divided by total data center power.",
        "How to interpret": "Higher means more data center heat is being reused.",
    },
    {
        "Metric": "ERE",
        "Short description": "Adjusted effectiveness after subtracting reused data center heat.",
        "How to interpret": "Lower is generally better.",
    },
    {
        "Metric": "URE",
        "Short description": (
            "Application-specific useful output after conversion or normalization. "
            "For ORC this is electric output; for absorption this is electric-equivalent cooling; "
            "for water reclamation this is the reduction in water scarcity footprint normalized by SWI."
        ),
        "How to interpret": "Higher is better. A negative value means the application penalty exceeds the useful benefit.",
    },
]
st.dataframe(pd.DataFrame(metric_explanations_rows), use_container_width=True)


# -------------------------------------------------------------------
# URE formulation structure
# -------------------------------------------------------------------
st.subheader("URE Formulation Structure")
ure_structure_df = pd.DataFrame(
    [
        {
            "Application type": "ORC",
            "Status in current tool": "Active",
            "End product": "Electric output",
            "URE formulation": "(E_elect - E_boost) / E_IT",
            "Required output model or data": "ORC efficiency model",
        },
        {
            "Application type": "Absorption chiller",
            "Status in current tool": "Active",
            "End product": "Cooling output converted to electric-equivalent",
            "URE formulation": "((Q_cooling / COP_DX) - E_boost) / E_IT, with COP_DX = 3.0",
            "Required output model or data": "Absorption chiller COP model and DX COP conversion",
        },
        {
            "Application type": "Water reclamation",
            "Status in current tool": "Active",
            "End product": "Reduction in water scarcity footprint",
            "URE formulation": "-(DWSF_Megan × E_WR) / (SWI × E_IT), with E_WR = E_boost",
            "Required output model or data": "Megan Ward Case A/B DWSF and SWI values mapped by climate zone",
        },
        {
            "Application type": "Carbon capture and storage",
            "Status in current tool": "Future formulation only",
            "End product": "CO2 removed",
            "URE formulation": "((m_CO2 / CEF) - E_boost) / E_IT",
            "Required output model or data": "CO2 removal model",
        },
    ]
)
st.dataframe(ure_structure_df, use_container_width=True)

st.info(
    "Manual E_IN/E_N input has been removed. If waste heat boosting is enabled, the app calculates "
    "heat pump boost electricity from the available waste heat temperature, selected boosted temperature, "
    "and the heat-pump COP temperature-lift correlation. Water reclamation uses DWSF × E_WR, not DWSF × Q_heat."
)


# -------------------------------------------------------------------
# Calculation notes
# -------------------------------------------------------------------
st.subheader("Calculation Notes")
notes = {
    "PUE source": outputs["PUE source"],
    "PUE file value": f"{outputs['PUE file value']:.4f}" if outputs["PUE file value"] is not None else "Missing",
    "PUE used": f"{outputs['PUE mean']:.4f}",
    "Q_avail factor": f"{outputs['Qavail']:.4f}",
    "Used waste heat fraction (phi_use)": f"{outputs['phi_use']:.4f}",
    "Pwh,avail (normalized)": f"{outputs['Pwh_avail']:.4f}",
    "Pwh,use before boost (normalized)": f"{outputs['Pwh_use']:.4f}",
    "Boost enabled": outputs["boost_enabled"],
    "Available waste heat temperature (°C)": f"{outputs['effective_temp']:.2f}",
    "Offtaker inlet temperature after boost (°C)": f"{outputs['Tofftaker_in']:.2f}" if outputs["Tofftaker_in"] is not None else "N/A",
    "Heat pump COP model": outputs["HP_COP_model"],
    "Heat pump COP": f"{outputs['COP_HP']:.4f}" if outputs["COP_HP"] is not None else "N/A",
    "Heat pump boost electricity, E_boost": f"{outputs['Eboost']:.4f}",
    "Heat delivered to offtaker after boost": f"{outputs['Ptotal_offtaker']:.4f}",
    "Useful output after application-specific conversion": f"{outputs['useful_output']:.4f}" if outputs["useful_output"] is not None else "N/A",
    "URE basis": outputs["URE basis"],
    "URE": f"{outputs['URE']:.4f}" if outputs["URE"] is not None else "N/A",
    "ERF": f"{outputs['ERF mean']:.4f}",
    "ERE": f"{outputs['ERE mean']:.4f}",
}

if application == "ORC":
    notes["Performance source"] = outputs["eta_source"]
    notes["Efficiency used"] = f"{outputs['eta_used']:.4f} ({outputs['eta_used'] * 100:.2f}%)"
    notes["ORC electric output"] = f"{outputs['PORC']:.4f}" if outputs["PORC"] is not None else "N/A"
    if outputs["eta_model"] is not None:
        notes["Internal ORC model efficiency"] = f"{outputs['eta_model']:.4f} ({outputs['eta_model'] * 100:.2f}%)"

elif application == "Cold water generation using an absorption chiller":
    notes["Absorption chiller evaporator temperature (°C)"] = outputs["abs_evap_temp_c"]
    notes["Performance source"] = outputs["eta_source"]
    notes["Absorption chiller COP used"] = f"{outputs['COP_abs']:.4f}"
    notes["Cooling output, thermal"] = f"{outputs['Q_cooling']:.4f}" if outputs["Q_cooling"] is not None else "N/A"
    notes["DX chiller COP"] = f"{outputs['DX_chiller_COP']:.1f}"
    notes["Cooling output, electric-equivalent"] = f"{outputs['Q_cooling_electric_equiv']:.4f}" if outputs["Q_cooling_electric_equiv"] is not None else "N/A"
    if outputs["eta_model"] is not None:
        notes["Internal absorption chiller COP model"] = f"{outputs['eta_model']:.4f}"

elif application == "Water reclamation":
    notes["Water reclamation case mapping"] = f"Megan Case {outputs['WR_case_used']}"
    notes["Mapping rule"] = "No IT-side liquid cooling -> Case A; cold plate/immersion/hybrid IT cooling -> Case B"
    notes["Reference city"] = outputs["WR_reference_city"]
    notes["Reference county"] = outputs["WR_reference_county"]
    notes["WR WRE (g/kJ)"] = f"{outputs['WR_WRE_g_per_kJ']:.4f}" if outputs["WR_WRE_g_per_kJ"] is not None else "N/A"
    notes["WR DWSF (L/kWh of E_WR)"] = f"{outputs['WR_DWSF_L_per_kWh']:.4f}"
    notes["WR SWI (L/kWh)"] = f"{outputs['WR_SWI_L_per_kWh']:.4f}"
    notes["WR energy input, E_WR"] = f"{outputs['WR_E_WR']:.4f}"
    notes["WR total Delta WSF"] = f"{outputs['WR_delta_wsf_total']:.4f}"
    notes["WR scarcity benefit"] = f"{outputs['WR_scarcity_benefit']:.4f}"
    notes["Water reclamation interpretation"] = (
        "Beneficial reduction" if outputs["WR_delta_wsf_total"] is not None and outputs["WR_delta_wsf_total"] < 0 else "No benefit or net increase"
    )
    notes["Important correction"] = "DWSF is multiplied by E_WR, not by Q_heat_to_application."

st.dataframe(pd.DataFrame([notes]), use_container_width=True)

st.caption(
    "This version uses P_IT as the normalized base. ERF and ERE are calculated from reused data-center waste heat only. "
    "Manual E_IN/E_N has been removed. Boost electricity is calculated internally when waste heat boosting is enabled. "
    "Absorption chiller cooling is converted to electric-equivalent output using a typical DX chiller COP of 3.0. "
    "Water reclamation uses Megan Ward's DWSF values mapped by climate zone and by Case A/Case B configuration. "
    "The corrected water reclamation formulation is DWSF × E_WR, not DWSF × Q_heat."
)
