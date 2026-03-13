import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="FCAT Tool", layout="centered")

# --------------------------------------------------
# Load case 14 data
# --------------------------------------------------
@st.cache_data
def load_case14_data():
    csv_path = Path("case14_results.csv")

    if not csv_path.exists():
        st.error("File 'case14_results.csv' was not found next to app.py")
        st.stop()

    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]

    required_cols = [
        "cooling_system_type",
        "climate_zone",
        "Location",
        "PUE_mean",
        "Qavail_mean_kW",
        "eta_mean",
        "ERE_mean",
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing required columns in case14_results.csv: {missing}")
        st.stop()

    return df


df = load_case14_data()

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("FCAT Web App")
st.subheader("Cooling System Type + ASHRAE Climate Zone")

st.write(
    "Select a cooling system type and climate zone to view meanPUE, "
    "Qavail_mean, eta_mean, and ERE_mean."
)

cooling_options = list(range(1, 16))
climate_options = ["1A", "2A", "2B", "3A", "3B", "3C", "4A", "4B", "4C", "5A", "5B", "6A", "6B", "7", "8"]

selected_cooling = st.selectbox("Cooling System Type", cooling_options, index=13)
selected_zone = st.selectbox("ASHRAE Climate Zone", climate_options)

st.markdown("---")

# --------------------------------------------------
# Lookup logic
# --------------------------------------------------
if selected_cooling != 14:
    st.warning(
        f"Cooling system type {selected_cooling} has not been loaded yet. "
        "Currently, only Case 14 has data."
    )
else:
    result = df[
        (df["cooling_system_type"] == selected_cooling) &
        (df["climate_zone"].astype(str) == selected_zone)
    ]

    if result.empty:
        st.warning("No matching result found for this climate zone in Case 14.")
    else:
        row = result.iloc[0]

        st.success(f"Showing results for Cooling System Type 14 ({row['Location']})")

        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)

        c1.metric("meanPUE", f"{row['PUE_mean']:.6f}")
        c2.metric("Qavail_mean_kW", f"{row['Qavail_mean_kW']:.6f}")
        c3.metric("eta_mean", f"{row['eta_mean']:.6f}")
        c4.metric("ERE_mean", f"{row['ERE_mean']:.6f}")

        st.markdown("---")
        st.write("Selected Inputs")
        st.write({
            "Cooling System Type": selected_cooling,
            "ASHRAE Climate Zone": selected_zone,
            "Representative Location": row["Location"],
        })

        st.write("Matched Row")
        st.dataframe(result, use_container_width=True)

# --------------------------------------------------
# Reference table
# --------------------------------------------------
with st.expander("Climate Zone Reference"):
    reference_df = pd.DataFrame({
        "Climate Zone": ["1A", "2A", "2B", "3A", "3B", "3C", "4A", "4B", "4C", "5A", "5B", "6A", "6B", "7", "8"],
        "Representative Location": [
            "Miami", "Houston", "Phoenix", "Atlanta", "Las Vegas", "San Francisco",
            "Baltimore", "Albuquerque", "Seattle", "Chicago", "Denver",
            "Minneapolis", "Helena", "Duluth", "Fairbanks"
        ]
    })
    st.dataframe(reference_df, use_container_width=True)
