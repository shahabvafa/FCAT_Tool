import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
APP_DIR = Path(__file__).resolve().parent
# -------------------------------------------------------------------
# Page setup
# -------------------------------------------------------------------
st.set_page_config(page_title="FCAT Waste Heat Reuse version 8", layout="wide")

st.title("FCAT Waste Heat Reuse Version 8")
st.markdown(
    "Select cooling system type, state, county, and offtaker application. "
    "This tool calculates URE, ERF, ERE, and PUE for ORC, absorption chiller, "
    "water reclamation, and carbon capture/storage."
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
        "short_description": "Small data center using direct expansion cooling.",
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
        "chiller": "Water-cooled chiller",
        "economizer": "Free cooling",
        "liquid_cooling": "Yes - Immersion",
        "short_description": "Large data center with immersion cooling, water-cooled chiller, dry cooling tower, and free cooling.",
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
    "Carbon capture and storage",
]

ABSORPTION_EVAP_OPTIONS = [-10, -5, 0]

# Advisor-requested conversion factor for cooling electric-equivalent benefit.
# This is NOT the absorption chiller COP.
DX_CHILLER_COP = 3.0

# Heat pump COP model for optional waste heat boosting.
HP_COP_MODEL_NAME = "Bever et al. (2024) high-temperature heat pump temperature-lift correlation"

# Fraction of IT heat assumed available for reuse for each FCAT cooling case.
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

# -------------------------------------------------------------------
# Carbon capture and storage (CCS) constants - Word 7/9/26 standalone formulation
# -------------------------------------------------------------------
# Required waste heat delivery temperature for the solid-sorbent TVSA DAC
# pathway. Two independent sources both fix desorption at 373 K (100 C):
# Postweiler et al. (2025), Table 1, and Cai et al. (2024), Table S3.
# The CCS offtaker always boosts waste heat to this target regardless of
# the user's manual boost settings, since the underlying literature model
# is only valid at this operating temperature.
CCS_TARGET_TEMP_C = 100.0

# Fixed electrical specific energy requirement (SER_electrical), kWh_e per
# kg CO2e removed. From Postweiler et al. (2025), the real-world DACCS
# plant benchmark (Deutz & Bardow, 2021), which includes CO2 compression
# for geologic storage. Kept fixed (not per-county) because both source
# papers report electricity requirement varies only slightly by location,
# unlike the thermal requirement.
CCS_SER_ELECTRICAL_KWH_PER_KG = 0.70

# Conversion factor from kWh (thermal) to MJ, used to match the units of
# CCS_SER_thermal_MJ_per_kg (from the per-county literature-derived input file).
KWH_TO_MJ = 3.6

# -------------------------------------------------------------------
# Water reclamation mapping for FCAT cases
# -------------------------------------------------------------------
# The URE formulation is the same for all cases.
# This map only determines where actual WR performance parameters come from.
# Case 1-11: air-cooled IT side -> Megan Case A proxy.
# Case 12 and 14: cold plate + 25% air -> Megan Case B rerun as 75/25.
# Case 13: immersion currently unsupported unless you provide direct/manual VTAS values.
WR_FCAT_TO_VTAS_MAP = {
    1: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    2: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    3: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    4: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    5: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    6: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    7: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    8: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    9: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    10: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    11: {"wr_config": "A", "label": "Megan Case A proxy", "status": "proxy_air_cooled_it"},
    12: {"wr_config": "B75", "label": "Megan Case B modified, 75% liquid / 25% air", "status": "vtas_rerun_75_25"},
    13: {"wr_config": None, "label": "No direct VTAS mapping for immersion yet", "status": "unsupported_until_immersion_model"},
    14: {"wr_config": "B75", "label": "Megan Case B modified, 75% liquid / 25% air", "status": "vtas_rerun_75_25"},
}

WR_WORD_COLUMN_MAP = {
    "A": {
        "v_water_l_per_kwh_it": "WR_CaseA_Vw_L_per_kWh_IT",
        "e_in_kwh_per_kwh_it": "WR_CaseA_Ein_kWh_per_kWh_IT",
        "baseline_hpd_l_per_kwh": "WR_CaseA_HPD_baseline_L_per_kWh",
        "wre_g_per_kj": "WR_CaseA_WRE_g_per_kJ",
        "wre_l_per_kwh": "WR_CaseA_WRE_L_per_kWh",
    },
    "B75": {
        "v_water_l_per_kwh_it": "WR_CaseB75_Vw_L_per_kWh_IT",
        "e_in_kwh_per_kwh_it": "WR_CaseB75_Ein_kWh_per_kWh_IT",
        "baseline_hpd_l_per_kwh": "WR_CaseB75_HPD_baseline_L_per_kWh",
        "wre_g_per_kj": "WR_CaseB75_WRE_g_per_kJ",
        "wre_l_per_kwh": "WR_CaseB75_WRE_L_per_kWh",
    },
}

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def normalize_text(x):
    return str(x).strip().lower()


def value_from_row(row, col, default=np.nan):
    if row is None or col not in row.index:
        return default
    value = row[col]
    if pd.isna(value):
        return default
    return value


def value_from_row_float(row, col, default=np.nan):
    value = value_from_row(row, col, default)
    try:
        return float(value)
    except Exception:
        return default


def valid_number(x):
    try:
        return np.isfinite(float(x))
    except Exception:
        return False


def safe_default(x, fallback=0.0):
    return float(x) if valid_number(x) else float(fallback)


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
    Heating-mode heat pump COP for optional waste heat boosting.

    COP_HP = 52.94 * DeltaT_lift^(-0.716)
    DeltaT_lift = T_out_C - T_in_C
    """
    delta_t_lift = float(T_out_C) - float(T_in_C)

    if delta_t_lift <= 0:
        return None

    cop_hp = 52.94 * (delta_t_lift ** -0.716)
    return max(float(cop_hp), 1.01)


def calculate_heat_pump_boost(p_wh_use, T_in_C, boost_enabled=False, boosted_temp_c=None):
    """
    Optional heat pump boosting for ORC/absorption calculations.

    Important:
    - For Word 5/22/26 water and carbon formulations, E_in is NOT automatically this E_boost.
    - Water uses E_in_WR from VTAS/EES/data.
    - Carbon uses E_in_CCS from carbon recovery model/data.
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


def get_water_reclamation_mapping(case_num):
    return WR_FCAT_TO_VTAS_MAP.get(
        int(case_num),
        {"wr_config": None, "label": "Unknown", "status": "unsupported"},
    )


# -------------------------------------------------------------------
# URE formulations based on Word 5/22/26
# -------------------------------------------------------------------
def calculate_word_enb(net_benefit, beta_nb, e_in):
    """
    Word 5/22/26 general structure:
        E_NB = NB / beta_NB - E_in

    NB and beta_NB must have consistent benefit units.
    beta_NB has units of benefit per kWh-electric.
    """
    net_benefit = float(net_benefit)
    beta_nb = float(beta_nb)
    e_in = float(e_in)

    if beta_nb <= 0:
        raise ValueError(
            "beta_NB must be positive. The selected baseline conversion factor does not provide a positive net benefit."
        )

    e_nb = (net_benefit / beta_nb) - e_in
    return e_nb


def calculate_ure_orc(e_elect, e_boost, e_it):
    """
    Power generation:
        NB = E_elect
        beta_NB = 1
        URE = (E_elect - E_boost) / E_IT
    """
    e_it = float(e_it)
    if e_it <= 0:
        raise ValueError("E_IT must be greater than zero.")

    e_nb = calculate_word_enb(
        net_benefit=float(e_elect),
        beta_nb=1.0,
        e_in=float(e_boost),
    )
    return e_nb / e_it, e_nb


def calculate_ure_absorption(q_cooling_thermal, e_boost, e_it, dx_chiller_cop=DX_CHILLER_COP):
    """
    Additional cooling:
        NB = Q_cooling
        beta_NB = COP_DX
        E_NB = Q_cooling / COP_DX - E_boost
        URE = E_NB / E_IT

    COP_absorption is used upstream to calculate Q_cooling.
    COP_DX is only the baseline conversion factor from cooling to electric-equivalent benefit.
    """
    q_cooling_thermal = float(q_cooling_thermal)
    e_boost = float(e_boost)
    e_it = float(e_it)
    dx_chiller_cop = float(dx_chiller_cop)

    if dx_chiller_cop <= 0:
        raise ValueError("DX chiller COP must be greater than zero.")
    if e_it <= 0:
        raise ValueError("E_IT must be greater than zero.")

    e_nb = calculate_word_enb(
        net_benefit=q_cooling_thermal,
        beta_nb=dx_chiller_cop,
        e_in=e_boost,
    )
    cooling_electric_equivalent_before_penalty = q_cooling_thermal / dx_chiller_cop
    ure_abs = e_nb / e_it

    return ure_abs, e_nb, cooling_electric_equivalent_before_penalty


def calculate_ure_water_reclamation_standalone(
    v_water_l,
    e_in_wr_kwh,
    ewif_l_per_kwh,
    e_it_kwh,
):
    """
    Water reclamation URE, standalone formulation (Word 7/9/26).

    beta_WR is no longer a comparison against a heat pump dehumidifier
    baseline weighted by water scarcity (AWARE_CF, SWI). Instead, beta_WR
    is the electricity-water intensity factor (EWIF): a fixed, always-
    positive grid-level conversion factor. This removes the beta-goes-to-
    zero singularity that the old baseline-comparison structure produced
    (e.g., Butler County, OH).

    Net benefit (gross water volume, no scarcity weighting for now):
        NB_WR = V_w

    Conversion factor:
        beta_WR = EWIF

    Electrical-equivalent net benefit:
        E_NB_WR = V_w / EWIF - E_in_WR

    URE:
        URE_WR = E_NB_WR / E_IT

    Units:
        V_w: L
        E_in_WR: kWh
        EWIF: L/kWh_e
        E_IT: kWh

    Note:
        A negative URE_WR is a valid, meaningful result: it means the
        electricity input required by the water reclamation system is
        larger than the electrical-equivalent value of the water
        recovered. It is not treated as an error case.
    """
    v_water_l = float(v_water_l)
    e_in_wr_kwh = float(e_in_wr_kwh)
    ewif_l_per_kwh = float(ewif_l_per_kwh)
    e_it_kwh = float(e_it_kwh)

    if v_water_l < 0:
        raise ValueError("V_w must be non-negative.")
    if e_in_wr_kwh < 0:
        raise ValueError("E_in_WR must be non-negative.")
    if e_it_kwh <= 0:
        raise ValueError("E_IT must be greater than zero.")

    actual_wr_l_per_kwh = np.nan
    if e_in_wr_kwh > 0:
        actual_wr_l_per_kwh = v_water_l / e_in_wr_kwh

    if ewif_l_per_kwh <= 0:
        return {
            "URE": np.nan,
            "E_NB": np.nan,
            "NB_WR": v_water_l,
            "beta_WR": ewif_l_per_kwh,
            "actual_WR_L_per_kWh": actual_wr_l_per_kwh,
            "v_water_l": v_water_l,
            "e_in_wr_kwh": e_in_wr_kwh,
            "ewif_l_per_kwh": ewif_l_per_kwh,
            "status": "not_applicable",
            "message": (
                "Water URE is not available because EWIF is missing, zero, or negative. "
                "EWIF is the conversion factor (beta_WR) and must be positive."
            ),
        }

    nb_wr = v_water_l
    beta_wr = ewif_l_per_kwh

    e_nb_wr = calculate_word_enb(
        net_benefit=nb_wr,
        beta_nb=beta_wr,
        e_in=e_in_wr_kwh,
    )

    ure_wr = e_nb_wr / e_it_kwh

    return {
        "URE": ure_wr,
        "E_NB": e_nb_wr,
        "NB_WR": nb_wr,
        "beta_WR": beta_wr,
        "actual_WR_L_per_kWh": actual_wr_l_per_kwh,
        "v_water_l": v_water_l,
        "e_in_wr_kwh": e_in_wr_kwh,
        "ewif_l_per_kwh": ewif_l_per_kwh,
        "status": "ok",
    }


def calculate_ccs_mass_removed(q_wh_use_kwh_th, ser_thermal_mj_per_kg):
    """
    Mass of CO2e removed from waste heat delivered at the CCS operating
    temperature (CCS_TARGET_TEMP_C), using the county-specific thermal
    specific energy requirement (SER_thermal) from Cai et al. (2024).

        m_CO2e,removed = (Q_WH,use@100C * KWH_TO_MJ) / SER_thermal_MJ_per_kg

    Units:
        q_wh_use_kwh_th: kWh_th (waste heat delivered to the CCS system after boosting)
        ser_thermal_mj_per_kg: MJ_th per kg CO2e removed (per county)
        returns: kg CO2e removed
    """
    q_wh_use_kwh_th = float(q_wh_use_kwh_th)
    ser_thermal_mj_per_kg = float(ser_thermal_mj_per_kg)

    if q_wh_use_kwh_th < 0:
        raise ValueError("Q_WH,use must be non-negative.")
    if ser_thermal_mj_per_kg <= 0:
        raise ValueError("CCS_SER_thermal_MJ_per_kg must be greater than zero.")

    return (q_wh_use_kwh_th * KWH_TO_MJ) / ser_thermal_mj_per_kg


def calculate_ccs_ein(m_co2e_removed_kg, e_boost_kwh, ser_electrical_kwh_per_kg=CCS_SER_ELECTRICAL_KWH_PER_KG):
    """
    Total electricity input required by the CCS pathway: the process
    electricity implied by SER_electrical, plus any heat pump boosting
    electricity already required to reach CCS_TARGET_TEMP_C.

        E_in,CCS = (m_CO2e,removed * SER_electrical) + E_boost
    """
    m_co2e_removed_kg = float(m_co2e_removed_kg)
    e_boost_kwh = float(e_boost_kwh)
    ser_electrical_kwh_per_kg = float(ser_electrical_kwh_per_kg)

    if m_co2e_removed_kg < 0:
        raise ValueError("m_CO2e_removed must be non-negative.")
    if e_boost_kwh < 0:
        raise ValueError("E_boost must be non-negative.")
    if ser_electrical_kwh_per_kg < 0:
        raise ValueError("CCS_SER_electrical_kWh_per_kg must be non-negative.")

    return (m_co2e_removed_kg * ser_electrical_kwh_per_kg) + e_boost_kwh


def calculate_ure_ccs_standalone(
    m_co2e_removed_kg,
    e_in_ccs_kwh,
    cef_kgco2e_per_kwh,
    e_it_kwh,
):
    """
    Carbon capture and storage URE, standalone formulation (Word 7/9/26).

    beta_CCS is no longer a comparison against a separate CCS baseline
    removal technology. Instead, beta_CCS is the grid carbon emission
    factor (CEF): a fixed, always-positive, location-specific conversion
    factor.

    Net benefit (gross mass removed):
        NB_CCS = m_CO2e,removed

    Conversion factor:
        beta_CCS = CEF

    Electrical-equivalent net benefit:
        E_NB_CCS = m_CO2e,removed / CEF - E_in,CCS

    URE:
        URE_CCS = E_NB_CCS / E_IT

    Units:
        m_CO2e_removed: kg CO2e
        E_in_CCS: kWh
        CEF: kg CO2e/kWh
        E_IT: kWh

    Note:
        A negative URE_CCS is a valid, meaningful result: it means the
        electricity input required by the CCS system is larger than the
        electrical-equivalent value of the CO2e removed. It is not
        treated as an error case.
    """
    m_co2e_removed_kg = float(m_co2e_removed_kg)
    e_in_ccs_kwh = float(e_in_ccs_kwh)
    cef_kgco2e_per_kwh = float(cef_kgco2e_per_kwh)
    e_it_kwh = float(e_it_kwh)

    if m_co2e_removed_kg < 0:
        raise ValueError("m_CO2e_removed must be non-negative.")
    if e_in_ccs_kwh < 0:
        raise ValueError("E_in_CCS must be non-negative.")
    if e_it_kwh <= 0:
        raise ValueError("E_IT must be greater than zero.")
    if cef_kgco2e_per_kwh <= 0:
        raise ValueError("CEF must be greater than zero.")

    nb_ccs = m_co2e_removed_kg
    beta_ccs = cef_kgco2e_per_kwh

    e_nb_ccs = calculate_word_enb(
        net_benefit=nb_ccs,
        beta_nb=beta_ccs,
        e_in=e_in_ccs_kwh,
    )
    ure_ccs = e_nb_ccs / e_it_kwh

    actual_ccs_kg_per_kwh = np.nan
    if e_in_ccs_kwh > 0:
        actual_ccs_kg_per_kwh = m_co2e_removed_kg / e_in_ccs_kwh

    return {
        "URE": ure_ccs,
        "E_NB": e_nb_ccs,
        "NB_CCS": nb_ccs,
        "beta_CCS": beta_ccs,
        "actual_CCS_kgCO2e_per_kWh": actual_ccs_kg_per_kwh,
        "m_co2e_removed_kg": m_co2e_removed_kg,
        "e_in_ccs_kwh": e_in_ccs_kwh,
        "cef_kgco2e_per_kwh": cef_kgco2e_per_kwh,
        "status": "ok",
    }


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
        # Older WR columns retained for reference/display only.
        "WR_reference_city",
        "WR_reference_county",
        "WR_EWIF_L_per_kWh",
        "WR_AWARE_CF",
        "WR_SWI_L_per_kWh",
        "WR_CaseA_WRE_g_per_kJ",
        "WR_CaseA_WRE_L_per_kWh",
        "WR_CaseA_DWF_L_per_kWh",
        "WR_CaseA_DWSF_L_per_kWh",
        "WR_CaseB_WRE_g_per_kJ",
        "WR_CaseB_WRE_L_per_kWh",
        "WR_CaseB_DWF_L_per_kWh",
        "WR_CaseB_DWSF_L_per_kWh",

        # New Word 5/22/26 WR inputs.
        "WR_CaseA_Vw_L_per_kWh_IT",
        "WR_CaseA_Ein_kWh_per_kWh_IT",
        "WR_CaseA_HPD_baseline_L_per_kWh",
        "WR_CaseB75_Vw_L_per_kWh_IT",
        "WR_CaseB75_Ein_kWh_per_kWh_IT",
        "WR_CaseB75_HPD_baseline_L_per_kWh",
        "WR_CaseB75_WRE_g_per_kJ",
        "WR_CaseB75_WRE_L_per_kWh",

        # Word 7/9/26 standalone CCS inputs. CCS_mCO2e_removed_kg_per_kWh_IT,
        # CCS_Ein_kWh_per_kWh_IT, and CCS_baseline_kgCO2e_per_kWh are no longer
        # read here: mass removed and electricity input are now computed at
        # runtime from CCS_SER_thermal_MJ_per_kg and the fixed
        # CCS_SER_ELECTRICAL_KWH_PER_KG constant (see calculate_ccs_mass_removed
        # and calculate_ccs_ein), the same way ORC/absorption performance is
        # computed at runtime rather than read pre-calculated from the file.
        "CCS_CEF_kgCO2e_per_kWh",
        "CCS_SER_thermal_MJ_per_kg",
    ]

    for col in optional_cols:
        if col not in df.columns:
            df[col] = np.nan

    df["State"] = df["State"].astype(str).str.strip()
    df["County"] = df["County"].astype(str).str.strip()
    df["climate zone"] = df["climate zone"].astype(str).str.strip()
    df["cooling system type"] = pd.to_numeric(df["cooling system type"], errors="coerce").astype("Int64")
    df["PUE mean"] = pd.to_numeric(df["PUE mean"], errors="coerce")

    numeric_cols = [
        "PUE mean",
        "WR_EWIF_L_per_kWh",
        "WR_AWARE_CF",
        "WR_SWI_L_per_kWh",
        "WR_CaseA_WRE_g_per_kJ",
        "WR_CaseA_WRE_L_per_kWh",
        "WR_CaseA_DWF_L_per_kWh",
        "WR_CaseA_DWSF_L_per_kWh",
        "WR_CaseB_WRE_g_per_kJ",
        "WR_CaseB_WRE_L_per_kWh",
        "WR_CaseB_DWF_L_per_kWh",
        "WR_CaseB_DWSF_L_per_kWh",
        "WR_CaseA_Vw_L_per_kWh_IT",
        "WR_CaseA_Ein_kWh_per_kWh_IT",
        "WR_CaseA_HPD_baseline_L_per_kWh",
        "WR_CaseB75_Vw_L_per_kWh_IT",
        "WR_CaseB75_Ein_kWh_per_kWh_IT",
        "WR_CaseB75_HPD_baseline_L_per_kWh",
        "WR_CaseB75_WRE_g_per_kJ",
        "WR_CaseB75_WRE_L_per_kWh",
        "CCS_CEF_kgCO2e_per_kWh",
        "CCS_SER_thermal_MJ_per_kg",
    ]

    for col in numeric_cols:
        if col in df.columns:
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
    wr_override_params=None,
    ccs_override_params=None,
):
    # Normalized base:
    # P_IT = 1.0 kW or 1.0 kWh/h. Therefore all energy/power outputs are per unit IT.
    p_it = 1.0
    e_it = 1.0

    effective_temp = float(temp) + (5.0 if asic else 0.0)

    pue_from_file = None if pd.isna(row["PUE mean"]) else float(row["PUE mean"])
    if pue_override_enabled:
        pue = float(pue_override_value)
        pue_source = "Manual override"
    else:
        pue = pue_from_file
        pue_source = "Input file"

    if pue is None or not np.isfinite(pue):
        raise ValueError("PUE is missing. Use PUE override or provide PUE mean in the input file.")

    q_avail = Q_AVAIL_FACTOR[case_num]
    p_dc = pue * p_it
    p_wh_avail = q_avail * p_it
    p_wh_use = phi_use * p_wh_avail

    # ERF and ERE are based on reused data-center waste heat before any heat-pump electricity addition.
    erf = p_wh_use / p_dc if p_dc != 0 else np.nan
    ere = (p_dc - p_wh_use) / p_it

    # The CCS/DAC pathway is only valid at CCS_TARGET_TEMP_C (see
    # calculate_ccs_mass_removed and its literature basis), so CCS always
    # boosts to that fixed target regardless of the user's manual boost
    # checkbox/temperature. ORC and absorption chiller keep the user's
    # own optional boost settings, unchanged from Version 7.
    if application == "Carbon capture and storage":
        effective_boost_enabled = True
        effective_boosted_temp_c = CCS_TARGET_TEMP_C
    else:
        effective_boost_enabled = boost_enabled
        effective_boosted_temp_c = boosted_temp_c

    boost_outputs = calculate_heat_pump_boost(
        p_wh_use=p_wh_use,
        T_in_C=effective_temp,
        boost_enabled=effective_boost_enabled,
        boosted_temp_c=effective_boosted_temp_c,
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
    useful_output = None
    ure = None
    e_nb = None
    ure_basis = "Not applicable"

    wr_details = {}
    ccs_details = {}

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
        ure, e_nb = calculate_ure_orc(e_elect=p_orc, e_boost=e_boost, e_it=e_it)
        useful_output = e_nb
        ure_basis = "ORC: URE = (E_elect - E_boost) / E_IT"

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

        ure, e_nb, q_cooling_electric_equiv = calculate_ure_absorption(
            q_cooling_thermal=q_cooling,
            e_boost=e_boost,
            e_it=e_it,
            dx_chiller_cop=DX_CHILLER_COP,
        )
        useful_output = e_nb
        ure_basis = (
            "Absorption chiller: URE = ((Q_cooling / COP_DX) - E_boost) / E_IT, "
            f"with COP_DX = {DX_CHILLER_COP:.1f}"
        )

    elif application == "Water reclamation":
        wr_map = get_water_reclamation_mapping(case_num)
        wr_config = wr_map["wr_config"]

        if wr_config is None and not wr_override_params:
            raise ValueError(
                "No direct VTAS mapping is currently available for this FCAT case. "
            )

        if wr_override_params:
            v_water_l_per_kwh_it = float(wr_override_params["v_water_l_per_kwh_it"])
            e_in_wr_kwh_per_kwh_it = float(wr_override_params["e_in_wr_kwh_per_kwh_it"])
            ewif_l_per_kwh = float(wr_override_params["ewif_l_per_kwh"])
            wr_data_source = "Manual override / placeholder research parameters"
            wr_wre_g_per_kj = np.nan
            wr_wre_l_per_kwh = np.nan
        else:
            wr_cols = WR_WORD_COLUMN_MAP[wr_config]
            v_water_l_per_kwh_it = value_from_row_float(row, wr_cols["v_water_l_per_kwh_it"])
            e_in_wr_kwh_per_kwh_it = value_from_row_float(row, wr_cols["e_in_kwh_per_kwh_it"])
            ewif_l_per_kwh = value_from_row_float(row, "WR_EWIF_L_per_kWh")
            wr_wre_g_per_kj = value_from_row_float(row, wr_cols["wre_g_per_kj"])
            wr_wre_l_per_kwh = value_from_row_float(row, wr_cols["wre_l_per_kwh"])
            wr_data_source = f"{wr_map['label']} from input file"

        required_values = {
            "V_w per kWh IT": v_water_l_per_kwh_it,
            "E_in_WR per kWh IT": e_in_wr_kwh_per_kwh_it,
            "EWIF L/kWh": ewif_l_per_kwh,
        }
        missing_values = [name for name, val in required_values.items() if not valid_number(val)]
        if missing_values:
            raise ValueError(
                "Water reclamation standalone formulation requires: "
                + ", ".join(missing_values)
                + ". Fill these columns in the input file or use manual override."
            )

        # Because E_IT = 1 normalized unit, these are already normalized values.
        v_water_l = v_water_l_per_kwh_it * e_it
        e_in_wr_kwh = e_in_wr_kwh_per_kwh_it * e_it

        wr_details = calculate_ure_water_reclamation_standalone(
            v_water_l=v_water_l,
            e_in_wr_kwh=e_in_wr_kwh,
            ewif_l_per_kwh=ewif_l_per_kwh,
            e_it_kwh=e_it,
        )

        ure = wr_details["URE"]
        e_nb = wr_details["E_NB"]
        useful_output = e_nb
        eta_source = wr_data_source
        ure_basis = (
            "Water reclamation standalone: "
            "NB_WR = V_w; "
            "beta_WR = EWIF; "
            "URE_WR = (V_w/EWIF - E_in_WR)/E_IT."
        )

        wr_details.update({
            "WR_case_mapping_label": wr_map["label"],
            "WR_case_mapping_status": wr_map["status"],
            "WR_config": wr_config,
            "WR_reference_city": value_from_row(row, "WR_reference_city", None),
            "WR_reference_county": value_from_row(row, "WR_reference_county", None),
            "WR_wre_g_per_kj_reference": wr_wre_g_per_kj,
            "WR_wre_l_per_kwh_reference": wr_wre_l_per_kwh,
            "WR_data_source": wr_data_source,
        })

    elif application == "Carbon capture and storage":
        if ccs_override_params:
            ser_thermal_mj_per_kg = float(ccs_override_params["ser_thermal_mj_per_kg"])
            ser_electrical_kwh_per_kg = float(ccs_override_params["ser_electrical_kwh_per_kg"])
            cef_kgco2e_per_kwh = float(ccs_override_params["cef_kgco2e_per_kwh"])
            ccs_data_source = "Manual override / placeholder research parameters"
        else:
            ser_thermal_mj_per_kg = value_from_row_float(row, "CCS_SER_thermal_MJ_per_kg")
            ser_electrical_kwh_per_kg = CCS_SER_ELECTRICAL_KWH_PER_KG
            cef_kgco2e_per_kwh = value_from_row_float(row, "CCS_CEF_kgCO2e_per_kWh")
            ccs_data_source = "Cai et al. (2024) SER_thermal by county + Postweiler et al. (2025) fixed SER_electrical"

        required_values = {
            "CCS_SER_thermal_MJ_per_kg": ser_thermal_mj_per_kg,
            "CCS_CEF_kgCO2e_per_kWh": cef_kgco2e_per_kwh,
        }
        missing_values = [name for name, val in required_values.items() if not valid_number(val)]
        if missing_values:
            raise ValueError(
                "Carbon capture standalone formulation requires: "
                + ", ".join(missing_values)
                + ". This county may fall outside the CONUS grid coverage of the "
                "underlying literature model (e.g., Alaska or Hawaii). "
                "Fill these columns in the input file or use manual override."
            )

        # p_total_to_offtaker is the waste heat delivered after boosting to
        # CCS_TARGET_TEMP_C (forced above for this application), already
        # normalized because E_IT = 1.
        m_co2e_removed_kg = calculate_ccs_mass_removed(
            q_wh_use_kwh_th=p_total_to_offtaker,
            ser_thermal_mj_per_kg=ser_thermal_mj_per_kg,
        )
        e_in_ccs_kwh = calculate_ccs_ein(
            m_co2e_removed_kg=m_co2e_removed_kg,
            e_boost_kwh=e_boost,
            ser_electrical_kwh_per_kg=ser_electrical_kwh_per_kg,
        )

        ccs_details = calculate_ure_ccs_standalone(
            m_co2e_removed_kg=m_co2e_removed_kg,
            e_in_ccs_kwh=e_in_ccs_kwh,
            cef_kgco2e_per_kwh=cef_kgco2e_per_kwh,
            e_it_kwh=e_it,
        )

        ure = ccs_details["URE"]
        e_nb = ccs_details["E_NB"]
        useful_output = e_nb
        eta_source = ccs_data_source
        ure_basis = (
            "CCS standalone: "
            "m_CO2e_removed = (Q_WH,use@100C * 3.6) / SER_thermal[county]; "
            "E_in_CCS = m_CO2e_removed*SER_electrical + E_boost; "
            "NB_CCS = m_CO2e_removed; beta_CCS = CEF; "
            "URE_CCS = (NB_CCS/beta_CCS - E_in_CCS)/E_IT."
        )
        ccs_details.update({
            "CCS_data_source": ccs_data_source,
            "CCS_ser_thermal_mj_per_kg": ser_thermal_mj_per_kg,
            "CCS_ser_electrical_kwh_per_kg": ser_electrical_kwh_per_kg,
            "CCS_target_temp_c": CCS_TARGET_TEMP_C,
        })

    else:
        raise ValueError("Unsupported application selected.")

    outputs = {
        "PIT": p_it,
        "EIT": e_it,
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
        "boosted_temp_c": effective_boosted_temp_c if boost_outputs["boost_enabled"] else None,
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
        "Q_cooling_electric_equiv_before_penalty": q_cooling_electric_equiv,
        "DX_chiller_COP": DX_CHILLER_COP,
        "useful_output": useful_output,
        "E_NB": e_nb,
        "URE": ure,
        "URE basis": ure_basis,
        "abs_evap_temp_c": abs_evap_temp_c,
    }

    outputs.update({f"WR_{k}": v for k, v in wr_details.items()})
    outputs.update({f"CCS_{k}": v for k, v in ccs_details.items()})

    return outputs


# -------------------------------------------------------------------
# File input
# -------------------------------------------------------------------
data_file = st.sidebar.text_input(
    "PUE + URE data file (.csv or .xlsx)",
    str(APP_DIR / "FCAT_v8.csv"),
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
# Find matching row before application parameter UI
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
# Waste heat boosting
# -------------------------------------------------------------------
st.subheader("Optional Waste Heat Boosting")

if application == "Carbon capture and storage":
    st.info(
        f"The CCS/DAC pathway is only valid at {CCS_TARGET_TEMP_C:.0f}°C waste heat delivery "
        "(the desorption temperature used by both underlying literature sources). "
        "Heat pump boosting to this fixed target is therefore applied automatically for CCS "
        "and is not user-adjustable here."
    )
    boost_enabled = True
    boosted_temp_c = CCS_TARGET_TEMP_C

    try:
        hp_preview = calculate_heat_pump_boost(
            p_wh_use=Q_AVAIL_FACTOR[case_num] * phi_use,
            T_in_C=effective_temp_preview,
            boost_enabled=True,
            boosted_temp_c=boosted_temp_c,
        )
        st.info(
            f"Estimated heat pump COP = {hp_preview['COP_HP']:.3f}; "
            f"boost electricity = {hp_preview['E_boost']:.4f} per unit IT load; "
            f"heat delivered to offtaker = {hp_preview['Q_heat_to_offtaker']:.4f} per unit IT load."
        )
    except Exception as e:
        st.warning(f"Boosting calculation issue: {e}")
else:
    boost_enabled = st.checkbox(
        "Boost waste heat temperature using a heat pump",
        value=False,
        help=(
            "Used for ORC and absorption calculations when the offtaker needs a higher inlet temperature. "
            "For the standalone water and CCS formulations, E_in must come from the water/CCS system data, "
            "not automatically from this boost calculation."
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

        try:
            hp_preview = calculate_heat_pump_boost(
                p_wh_use=Q_AVAIL_FACTOR[case_num] * phi_use,
                T_in_C=effective_temp_preview,
                boost_enabled=True,
                boosted_temp_c=boosted_temp_c,
            )
            st.info(
                f"Estimated heat pump COP = {hp_preview['COP_HP']:.3f}; "
                f"boost electricity = {hp_preview['E_boost']:.4f} per unit IT load; "
                f"heat delivered to offtaker = {hp_preview['Q_heat_to_offtaker']:.4f} per unit IT load."
            )
        except Exception as e:
            st.warning(f"Boosting calculation issue: {e}")
    else:
        boosted_temp_c = None


# -------------------------------------------------------------------
# Case details
# -------------------------------------------------------------------
st.subheader("Cooling System Case Details")

wr_case_preview = get_water_reclamation_mapping(case_num)
case_details_df = pd.DataFrame([
    {
        "Case": f"Case {case_num}",
        "System size": case_info["size"],
        "Primary heat removal approach": case_info["heat_removal"],
        "Chiller/system type": case_info["chiller"],
        "Economizer type": case_info["economizer"],
        "IT-side liquid cooling": case_info["liquid_cooling"],
        "WR VTAS mapping": wr_case_preview["label"],
        "WR mapping status": wr_case_preview["status"],
        "Recommended waste heat temperature (°C)": case_info["default_temp_c"],
        "Q_avail factor": Q_AVAIL_FACTOR[case_num],
    }
])
st.dataframe(case_details_df, use_container_width=True)
st.info(case_info["short_description"])

if application == "Water reclamation":
    if wr_case_preview["wr_config"] is None:
        st.warning(
            "This FCAT case does not currently have a direct Megan/VTAS water reclamation mapping. "
            "Use manual override values only if you have separate VTAS/model outputs for this case."
        )
    elif wr_case_preview["status"].startswith("proxy"):
        st.warning(
            "This water reclamation mapping is a proxy. FCAT Cases 1–11 are mapped to Megan Case A "
            "because they are air-cooled on the IT side, even if the plant/chiller is water-cooled."
        )


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
        


# -------------------------------------------------------------------
# Water and CCS research-parameter overrides
# -------------------------------------------------------------------
wr_override_params = None
ccs_override_params = None

if application == "Water reclamation":
    st.subheader("Water Reclamation Parameters")

    wr_map = get_water_reclamation_mapping(case_num)
    wr_config = wr_map["wr_config"]

    if wr_config in WR_WORD_COLUMN_MAP:
        wr_cols = WR_WORD_COLUMN_MAP[wr_config]
        file_vw = value_from_row_float(row, wr_cols["v_water_l_per_kwh_it"])
        file_ein = value_from_row_float(row, wr_cols["e_in_kwh_per_kwh_it"])
        file_wre_g = value_from_row_float(row, wr_cols["wre_g_per_kj"])
        file_wre_l = value_from_row_float(row, wr_cols["wre_l_per_kwh"])
    else:
        file_vw = np.nan
        file_ein = np.nan
        file_wre_g = np.nan
        file_wre_l = np.nan

    file_ewif = value_from_row_float(row, "WR_EWIF_L_per_kWh")

    wr_preview_df = pd.DataFrame([{
        "Mapping": wr_map["label"],
        "Status": wr_map["status"],
        "V_w per kWh IT, L/kWh_IT": file_vw,
        "E_in_WR per kWh IT, kWh/kWh_IT": file_ein,
        "EWIF, L/kWh_e": file_ewif,
        "Reference WRE, g/kJ": file_wre_g,
        "Reference WRE, L/kWh": file_wre_l,
    }])
    st.dataframe(wr_preview_df, use_container_width=True)

    st.caption(
        "For the final water URE, WRE is not directly used as URE. "
        "The code uses V_w, E_in_WR, and EWIF in the standalone formulation: "
        "URE_WR = (V_w/EWIF - E_in_WR) / E_IT."
    )

    wr_manual = st.checkbox(
        "Override/add water parameters manually",
        value=False,
        help="Use this if the VTAS annual outputs or EWIF are still being developed for this county.",
    )

    if wr_manual:
        c1, c2 = st.columns(2)
        with c1:
            wr_vw_manual = st.number_input(
                "V_w per kWh IT (L/kWh_IT)",
                min_value=0.0,
                value=safe_default(file_vw, 0.0),
                step=0.1,
                format="%.6f",
            )
            wr_ein_manual = st.number_input(
                "E_in_WR per kWh IT (kWh/kWh_IT)",
                min_value=0.0,
                value=safe_default(file_ein, 0.0),
                step=0.001,
                format="%.6f",
            )
        with c2:
            wr_ewif_manual = st.number_input(
                "EWIF (L/kWh_e)",
                min_value=0.0,
                value=safe_default(file_ewif, 0.0),
                step=0.01,
                format="%.6f",
                help="Electricity-water intensity factor: grid water use per kWh of electricity.",
            )

        wr_override_params = {
            "v_water_l_per_kwh_it": wr_vw_manual,
            "e_in_wr_kwh_per_kwh_it": wr_ein_manual,
            "ewif_l_per_kwh": wr_ewif_manual,
        }

elif application == "Carbon capture and storage":
    st.subheader("Carbon Capture and Storage Parameters (standalone URE)")

    file_ser_thermal = value_from_row_float(row, "CCS_SER_thermal_MJ_per_kg")
    file_cef = value_from_row_float(row, "CCS_CEF_kgCO2e_per_kWh")

    ccs_preview_df = pd.DataFrame([{
        "SER_thermal, MJ/kg CO2e (Cai et al. 2024, by county)": file_ser_thermal,
        "SER_electrical, kWh/kg CO2e (Postweiler et al. 2025, fixed)": CCS_SER_ELECTRICAL_KWH_PER_KG,
        "CEF, kgCO2e/kWh": file_cef,
        "CCS target waste heat temperature, °C": CCS_TARGET_TEMP_C,
    }])
    st.dataframe(ccs_preview_df, use_container_width=True)

    st.caption(
        "m_CO2e_removed and E_in_CCS are calculated at runtime from SER_thermal, "
        "SER_electrical, and the waste heat delivered after boosting to "
        f"{CCS_TARGET_TEMP_C:.0f}°C; they are not read directly from the input file. "
        "SER_thermal is not available for counties outside the CONUS grid coverage "
        "of Cai et al. (2024) (e.g., Alaska, Hawaii)."
    )

    ccs_manual = st.checkbox(
        "Override/add CCS parameters manually",
        value=False,
        help="Use this for sensitivity analysis, or if SER_thermal/CEF are still missing for this county.",
    )

    if ccs_manual:
        c1, c2 = st.columns(2)
        with c1:
            ccs_ser_thermal_manual = st.number_input(
                "SER_thermal (MJ/kg CO2e)",
                min_value=0.0,
                value=safe_default(file_ser_thermal, 0.0),
                step=0.1,
                format="%.6f",
            )
            ccs_ser_electrical_manual = st.number_input(
                "SER_electrical (kWh/kg CO2e)",
                min_value=0.0,
                value=float(CCS_SER_ELECTRICAL_KWH_PER_KG),
                step=0.01,
                format="%.6f",
            )
        with c2:
            ccs_cef_manual = st.number_input(
                "CEF (kgCO2e/kWh)",
                min_value=0.0,
                value=safe_default(file_cef, 0.0),
                step=0.001,
                format="%.6f",
            )

        ccs_override_params = {
            "ser_thermal_mj_per_kg": ccs_ser_thermal_manual,
            "ser_electrical_kwh_per_kg": ccs_ser_electrical_manual,
            "cef_kgco2e_per_kwh": ccs_cef_manual,
        }


# -------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------
if pd.isna(row["PUE mean"]) and not pue_override_enabled:
    st.warning(
        "PUE mean is not filled yet for the selected state, county, and cooling system type. "
        "Please use the PUE override option to continue."
    )
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
        wr_override_params=wr_override_params,
        ccs_override_params=ccs_override_params,
    )
except Exception as e:
    st.error(f"Could not calculate outputs. {e}")
    st.stop()


# -------------------------------------------------------------------
# Selected inputs
# -------------------------------------------------------------------
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
}])
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
    "Electrical-equivalent net benefit, E_NB": outputs["E_NB"],
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
        "Cooling electric-equivalent before E_in penalty": outputs["Q_cooling_electric_equiv_before_penalty"],
    }

elif application == "Water reclamation":
    results_row = {
        **common_results,
        "WR mapping": outputs.get("WR_WR_case_mapping_label"),
        "WR mapping status": outputs.get("WR_WR_case_mapping_status"),
        "WR config": outputs.get("WR_WR_config"),
        "WR reference city": outputs.get("WR_WR_reference_city"),
        "WR reference county": outputs.get("WR_WR_reference_county"),
        "V_w, L": outputs.get("WR_v_water_l"),
        "E_in_WR, kWh": outputs.get("WR_e_in_wr_kwh"),
        "EWIF, L/kWh_e": outputs.get("WR_ewif_l_per_kwh"),
        "Actual WR, L/kWh": outputs.get("WR_actual_WR_L_per_kWh"),
        "NB_WR": outputs.get("WR_NB_WR"),
        "beta_WR": outputs.get("WR_beta_WR"),
        "Reference WRE, g/kJ": outputs.get("WR_WR_wre_g_per_kj_reference"),
        "Reference WRE, L/kWh": outputs.get("WR_WR_wre_l_per_kwh_reference"),
    }

elif application == "Carbon capture and storage":
    results_row = {
        **common_results,
        "m_CO2e removed, kg": outputs.get("CCS_m_co2e_removed_kg"),
        "E_in_CCS, kWh": outputs.get("CCS_e_in_ccs_kwh"),
        "CEF, kgCO2e/kWh": outputs.get("CCS_cef_kgco2e_per_kwh"),
        "SER_thermal, MJ/kg": outputs.get("CCS_ser_thermal_mj_per_kg"),
        "SER_electrical, kWh/kg": outputs.get("CCS_ser_electrical_kwh_per_kg"),
        "CCS target temperature, °C": outputs.get("CCS_target_temp_c"),
        "Actual CCS, kgCO2e/kWh": outputs.get("CCS_actual_CCS_kgCO2e_per_kWh"),
        "NB_CCS": outputs.get("CCS_NB_CCS"),
        "beta_CCS": outputs.get("CCS_beta_CCS"),
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
    ure_display = outputs['URE']
    if ure_display is None or (isinstance(ure_display, float) and np.isnan(float(ure_display))):
        ure_str = "N/A"
    else:
        ure_str = f"{float(ure_display):.4f}"
    st.metric(
        "URE",
        ure_str,
        help="Useful Reuse Effectiveness = electrical-equivalent net benefit divided by IT load.",
    )


# -------------------------------------------------------------------
# Metric explanations
# -------------------------------------------------------------------
if application == "Water reclamation":
    wr_status = outputs.get("WR_status")
    if wr_status == "not_applicable":
        st.warning(
            "⚠️ Water reclamation URE is not available for this county because "
            "EWIF (β_WR) is missing, zero, or negative. EWIF is the grid "
            "electricity-water intensity conversion factor and must be positive. "
            "Fill it in the input file or use manual override."
        )
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
        "How to interpret": "Higher means more data center heat is reused.",
    },
    {
        "Metric": "ERE",
        "Short description": "Adjusted effectiveness after subtracting reused data center heat.",
        "How to interpret": "Lower is generally better.",
    },
    {
        "Metric": "URE",
        "Short description": (
            "Electrical-equivalent net benefit normalized by IT load. "
            "For water and carbon, this follows the Word 5/22/26 NB/beta_NB minus E_in structure."
        ),
        "How to interpret": "Higher is better. A negative value means the input penalty exceeds the useful benefit.",
    },
]
st.dataframe(pd.DataFrame(metric_explanations_rows), use_container_width=True)


# -------------------------------------------------------------------
# URE formulation structure
# -------------------------------------------------------------------
st.subheader("URE Formulation Structure")

ure_structure_df = pd.DataFrame([
    {
        "Application type": "ORC",
        "Status in current tool": "Active",
        "Net benefit, NB": "E_elect",
        "Conversion factor, beta_NB": "1",
        "URE formulation": "(E_elect - E_boost) / E_IT",
        "Required model/data": "ORC efficiency model",
    },
    {
        "Application type": "Absorption chiller",
        "Status in current tool": "Active",
        "Net benefit, NB": "Q_cooling",
        "Conversion factor, beta_NB": "COP_DX",
        "URE formulation": "((Q_cooling / COP_DX) - E_boost) / E_IT",
        "Required model/data": "Absorption COP model and DX COP conversion",
    },
    {
        "Application type": "Water reclamation",
        "Status in current tool": "Active",
        "Net benefit, NB": "V_w",
        "Conversion factor, beta_NB": "EWIF",
        "URE formulation": "((V_w / EWIF) - E_in_WR) / E_IT",
        "Required model/data": "VTAS V_w and E_in_WR; county EWIF",
    },
    {
        "Application type": "Carbon capture and storage",
        "Status in current tool": "Active",
        "Net benefit, NB": "m_CO2e_removed",
        "Conversion factor, beta_NB": "CEF",
        "URE formulation": "((m_CO2e_removed / CEF) - E_in_CCS) / E_IT",
        "Required model/data": "CCS_SER_thermal_MJ_per_kg (by county, Cai et al. 2024); "
                               "fixed SER_electrical (Postweiler et al. 2025); county CEF",
    },
])
st.dataframe(ure_structure_df, use_container_width=True)

st.info(
    "Version 8 uses the standalone URE formulation for all applications: beta_NB is a "
    "conversion factor, not a comparison to a baseline technology. Water reclamation uses "
    "V_w and EWIF (no AWARE_CF, SWI, or heat pump dehumidifier baseline). Carbon capture and "
    "storage uses m_CO2e_removed and CEF, with mass removed and electricity input computed at "
    "runtime from a fixed 100°C waste heat boost, county-level SER_thermal, and fixed "
    "SER_electrical. Negative URE values are kept and reported as meaningful results, not N/A."
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
    "Used waste heat fraction phi_use": f"{outputs['phi_use']:.4f}",
    "Pwh,avail normalized": f"{outputs['Pwh_avail']:.4f}",
    "Pwh,use before boost normalized": f"{outputs['Pwh_use']:.4f}",
    "Boost enabled": outputs["boost_enabled"],
    "Available waste heat temperature, C": f"{outputs['effective_temp']:.2f}",
    "Offtaker inlet temperature after boost, C": f"{outputs['Tofftaker_in']:.2f}" if outputs["Tofftaker_in"] is not None else "N/A",
    "Heat pump COP model": outputs["HP_COP_model"],
    "Heat pump COP": f"{outputs['COP_HP']:.4f}" if outputs["COP_HP"] is not None else "N/A",
    "Heat pump boost electricity, E_boost": f"{outputs['Eboost']:.4f}",
    "Heat delivered to offtaker after boost": f"{outputs['Ptotal_offtaker']:.4f}",
    "E_NB": f"{outputs['E_NB']:.4f}" if outputs["E_NB"] is not None else "N/A",
    "URE basis": outputs["URE basis"],
    "URE": f"{outputs['URE']:.4f}" if outputs["URE"] is not None else "N/A",
    "ERF": f"{outputs['ERF mean']:.4f}",
    "ERE": f"{outputs['ERE mean']:.4f}",
}

if application == "ORC":
    notes["Performance source"] = outputs["eta_source"]
    notes["Efficiency used"] = f"{outputs['eta_used']:.4f} ({outputs['eta_used'] * 100:.2f}%)"
    notes["ORC electric output"] = f"{outputs['PORC']:.4f}" if outputs["PORC"] is not None else "N/A"

elif application == "Cold water generation using an absorption chiller":
    notes["Absorption chiller evaporator temperature, C"] = outputs["abs_evap_temp_c"]
    notes["Performance source"] = outputs["eta_source"]
    notes["Absorption chiller COP used"] = f"{outputs['COP_abs']:.4f}"
    notes["Cooling output, thermal"] = f"{outputs['Q_cooling']:.4f}" if outputs["Q_cooling"] is not None else "N/A"
    notes["DX chiller COP"] = f"{outputs['DX_chiller_COP']:.1f}"
    notes["Cooling electric-equivalent before E_in penalty"] = (
        f"{outputs['Q_cooling_electric_equiv_before_penalty']:.4f}"
        if outputs["Q_cooling_electric_equiv_before_penalty"] is not None
        else "N/A"
    )

elif application == "Water reclamation":
    notes["WR mapping"] = outputs.get("WR_WR_case_mapping_label")
    notes["WR mapping status"] = outputs.get("WR_WR_case_mapping_status")
    notes["WR config"] = outputs.get("WR_WR_config")
    notes["WR reference city"] = outputs.get("WR_WR_reference_city")
    notes["WR reference county"] = outputs.get("WR_WR_reference_county")
    notes["V_w, L"] = f"{outputs.get('WR_v_water_l'):.6f}"
    notes["E_in_WR, kWh"] = f"{outputs.get('WR_e_in_wr_kwh'):.6f}"
    notes["EWIF, L/kWh_e"] = f"{outputs.get('WR_ewif_l_per_kwh'):.6f}"
    notes["Actual WR, L/kWh"] = (
        f"{outputs.get('WR_actual_WR_L_per_kWh'):.6f}"
        if valid_number(outputs.get("WR_actual_WR_L_per_kWh"))
        else "N/A"
    )
    notes["NB_WR"] = f"{outputs.get('WR_NB_WR'):.6f}"
    notes["beta_WR"] = f"{outputs.get('WR_beta_WR'):.6f}"
    notes["Important correction"] = (
        "Water URE is standalone: it no longer compares to a heat pump "
        "dehumidifier baseline weighted by AWARE_CF/SWI. "
        "It is (V_w/EWIF) - E_in_WR, normalized by E_IT."
    )

elif application == "Carbon capture and storage":
    notes["m_CO2e removed, kg"] = f"{outputs.get('CCS_m_co2e_removed_kg'):.6f}"
    notes["E_in_CCS, kWh"] = f"{outputs.get('CCS_e_in_ccs_kwh'):.6f}"
    notes["CEF, kgCO2e/kWh"] = f"{outputs.get('CCS_cef_kgco2e_per_kwh'):.6f}"
    notes["SER_thermal, MJ/kg"] = f"{outputs.get('CCS_ser_thermal_mj_per_kg'):.6f}"
    notes["SER_electrical, kWh/kg"] = f"{outputs.get('CCS_ser_electrical_kwh_per_kg'):.6f}"
    notes["CCS target temperature, °C"] = f"{outputs.get('CCS_target_temp_c'):.1f}"
    notes["Actual CCS, kgCO2e/kWh"] = (
        f"{outputs.get('CCS_actual_CCS_kgCO2e_per_kWh'):.6f}"
        if valid_number(outputs.get("CCS_actual_CCS_kgCO2e_per_kWh"))
        else "N/A"
    )
    notes["NB_CCS"] = f"{outputs.get('CCS_NB_CCS'):.6f}"
    notes["beta_CCS"] = f"{outputs.get('CCS_beta_CCS'):.6f}"
    notes["Important correction"] = (
        "CCS URE is standalone: it no longer compares to a separate CCS "
        "baseline removal technology. "
        "It is m_CO2e_removed/CEF - E_in_CCS, normalized by E_IT, with "
        "m_CO2e_removed and E_in_CCS computed at runtime from SER_thermal, "
        "SER_electrical, and the waste heat boosted to CCS_TARGET_TEMP_C."
    )

st.dataframe(pd.DataFrame([notes]), use_container_width=True)

st.caption(
    "Normalized base: E_IT = 1.0. "
    "Water and CCS parameters should therefore be provided per kWh_IT unless using manual values consistently. "
    "EWIF (water) and CEF (CCS) are county-level conversion factors, not baseline-technology comparisons. "
    "CCS additionally requires county-level SER_thermal (MJ/kg CO2e); SER_electrical is a fixed constant "
    "(CCS_SER_ELECTRICAL_KWH_PER_KG) applied everywhere, and waste heat is always boosted to CCS_TARGET_TEMP_C."
)
