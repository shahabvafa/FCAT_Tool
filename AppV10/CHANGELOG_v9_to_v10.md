# PURE v9 to v10 changelog

## FCAT_v10.csv

Shape: 44,030 rows (same), 41 to 46 columns. Row order and `cooling system type` are the same as v9.

| Column | Change | Rows |
|---|---|---|
| `PUE mean` | New value for Cases 1-10. Cases 11-14 keep the v9 value | 31,450 |
| `PUE lower`, `PUE upper` | New column. Filled for Cases 1-10, blank for Cases 11-14 | 31,450 filled |
| `WUE lower`, `WUE mean`, `WUE upper` | New column, L/kWh_IT. Filled for Cases 1-10, blank for Cases 11-14 | 31,450 filled |
| `WR_SWI_L_per_kWh` | Refreshed from `eGRID_Metrics_2023_v2_SWIfix.xlsx` | 43,526 (3,109 counties) |
| `WR_SWI_hydro_L_per_kWh` | Same | 43,526 |
| `WR_SWI_withdrawal_L_per_kWh` | Same | 43,526 |
| `County`, `CCS_CEF_kgCO2e_per_kWh`, `WR_EWIF_L_per_kWh`, `WR_EWIF_hydro_L_per_kWh`, `WR_EWIF_withdrawal_L_per_kWh`, `WR_AWARE_CF` | `Doña Ana County` only: name repaired, stale values replaced from the grid file | 14 |
| The other 31 columns | Byte-identical to v9 | 0 |

### County reconciliation

- All 3,145 counties stay in the file.
- 3,108 counties match the grid file by state and normalized name.
- `Oglala Lakota County` (SD) takes the `Shannon County` row.
- 36 counties have no 2023 grid row and keep their v9 values: Alaska (30), Hawaii (5), `Bedford city` (VA).
- Row 3,109 of the grid file is `Bedford city` (FIPS 51515), with no name and no values.

## AppV10.py

- Added `URE_sw = (A_CF * V_w / SWI - E_in) / E_IT`, with `beta_sw = SWI / A_CF`. It is shown next to URE for water reclamation. The existing URE is unchanged.
- `URE_sw` follows the water basis selector. It is N/A on the v8 keying, where SWI is zero or negative, and where `WR_AWARE_CF` is blank.
- Added WUE and the PUE and WUE 5th-95th percentile range. Cases 11-14 show N/A for WUE.
- Case 1-10 labels follow the new system names.
- Cases 11-14 are unchanged from v9: labels, metadata, `Q_AVAIL_FACTOR`, `default_temp_c` and `WR_FCAT_TO_VTAS_MAP`.
- Case 13 with water reclamation now shows PUE, ERF and ERE, leaves URE and URE_sw blank, and shows "No immersion model available". In v9 this stopped the page.
- ORC shows a warning when the inlet temperature is below the curve's fitted range (42.7 C).
- Fixed a v9 bug: three CCS lookups returned `None`, so Calculation Notes crashed for carbon capture.

## Not included

- The four new liquid-cooling systems (CP-DC, CP-CT, IM-DC, IM-CT) in `County_Results_14_Systems_2023.xlsx`.

## Open items

- Cases 12 and 14 are labelled 75% liquid / 25% air. The VTAS deck behind them has `heatfrac 0.5`, and running it reproduces the existing results.
- Six South Dakota rows in the grid file have a name and FIPS that do not agree (file FIPS 46102-46111). The join uses names, as v9 did.

## Checks run

- Cell-level diff of v10 against v9 gives the table above.
- None of the 150 Case 1-10 and climate zone PUE pairs equals v9. Mean goes from 1.6249 to 1.6604.
- `CASE_METADATA` entries 11-14, `Q_AVAIL_FACTOR` and `WR_FCAT_TO_VTAS_MAP` are text-identical to v9.
- App run headless: 116 of 116 checks passed.
  - URE for Cases 1, 10, 11, 12, 13 and 14 equals v9 on the off-takers tested.
  - PUE, ERF and ERE for Cases 11-14 equal v9.
  - URE_sw matches a separate calculation from the CSV.
- `URE_sw` function matches the formula for every county with data, with a maximum difference of 1.4e-14.
