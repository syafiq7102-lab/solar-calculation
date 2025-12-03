import streamlit as st
import math

st.set_page_config(page_title="Solar Calculator", layout="centered")
st.title("☀️ Solar PV Calculator (Step 1 & Step 2)")

# ============================================================
# STEP 1 — FTEMP + AREA + EOUT
# ============================================================
st.header("🔶 STEP 1 — Calculate ftemp, Area & Energy Output (Eout)")

# ----------------------- FTEMP -----------------------
st.subheader("1️⃣ Temperature Factor (ftemp)")

Pcoef = st.number_input("Temperature Coefficient (Pcoef) (%/°C)", value=-0.35)
Tavg = st.number_input("Average Temperature (Tavg, °C)", value=35.0)
Tstc = st.number_input("STC Temperature (Tstc, °C)", value=25.0)

ftemp = 1 + ((Pcoef / 100) * (Tavg - Tstc))
st.success(f"Calculated ftemp = **{ftemp:.4f}**")

# ----------------------- AREA -----------------------
st.subheader("2️⃣ Solar Panel Area")

panel_length = st.number_input("Panel Length (m)", value=2.0)
panel_width = st.number_input("Panel Width (m)", value=1.1)

area = panel_length * panel_width
st.success(f"Panel Area = **{area:.3f} m²**")

# ----------------------- EOUT -----------------------
st.subheader("3️⃣ Energy Output (Eout)")

PSH = st.number_input("Peak Sun Hours (PSH)", value=4.5)
PASTC = st.number_input("Panel Max Power at STC (Watt)", value=550)

# SWITCHES (ON / OFF)
st.write("### ⚙️ Optional Correction Factors (ON/OFF)")

use_fmm = st.checkbox("Use fmm?", value=True)
use_fclean = st.checkbox("Use fclean?", value=True)
use_fdegrad = st.checkbox("Use fdegrad?", value=True)
use_fsunshade = st.checkbox("Use fsunshade?", value=True)
use_cable = st.checkbox("Use Cable Efficiency?", value=True)
use_inverter = st.checkbox("Use Inverter Efficiency?", value=True)

# Inputs (only shown if ON)
if use_fmm:
    fmm = st.number_input("Manufacturing Tolerance (fmm)", value=1.00)
else:
    fmm = 1

if use_fclean:
    fclean = st.number_input("Cleaning Factor (fclean)", value=0.98)
else:
    fclean = 1

if use_fdegrad:
    fdegrad = st.number_input("Degradation Factor (fdegrad)", value=0.98)
else:
    fdegrad = 1

if use_fsunshade:
    fsunshade = st.number_input("Sun Shading Factor (fsunshade)", value=1.00)
else:
    fsunshade = 1

if use_cable:
    eta_cable = st.number_input("Cable Efficiency", value=0.98)
else:
    eta_cable = 1

if use_inverter:
    eta_inv = st.number_input("Inverter Efficiency", value=0.97)
else:
    eta_inv = 1

# EOUT formula
Eout = (PSH * PASTC * fmm * ftemp * fclean *
        fdegrad * fsunshade * eta_cable * eta_inv) / area

st.success(f"⚡ Estimated Energy Output (Eout) = **{Eout:.2f} Wh per m²**")

st.markdown("---")

# ============================================================
# STEP 2 — PANEL CALCULATION
# ============================================================
st.header("🔷 STEP 2 — Landscape vs Portrait Panel Calculation")

st.subheader("📏 Roof & Panel Dimensions")

Wroof = st.number_input("Roof Width (m)", value=10.0)
Lroof = st.number_input("Roof Length (m)", value=20.0)
spacing = st.number_input("Panel Spacing Δ (m)", value=0.1)

# Landscape
N_land_up = math.floor(Wroof / (panel_width + spacing))
N_land_across = math.floor(Lroof / (panel_length + spacing))
N_land_total = N_land_up * N_land_across

# Portrait
N_port_up = math.floor(Wroof / (panel_length + spacing))
N_port_across = math.floor(Lroof / (panel_width + spacing))
N_port_total = N_port_up * N_port_across

# Display
col1, col2 = st.columns(2)

with col1:
    st.write("### 🟧 Landscape")
    st.write(f"Panels Up = **{N_land_up}**")
    st.write(f"Panels Across = **{N_land_across}**")
    st.write(f"➡️ Total = **{N_land_total} panels**")

with col2:
    st.write("### 🟦 Portrait")
    st.write(f"Panels Up = **{N_port_up}**")
    st.write(f"Panels Across = **{N_port_across}**")
    st.write(f"➡️ Total = **{N_port_total} panels**")

st.markdown("---")

# Recommendation
st.header("📌 Recommendation")

if N_land_total > N_port_total:
    st.success(
        f"✔ **Landscape is recommended.** It fits **{N_land_total} panels**, "
        f"more than Portrait ({N_port_total}).")
elif N_port_total > N_land_total:
    st.success(
        f"✔ **Portrait is recommended.** It fits **{N_port_total} panels**, "
        f"more than Landscape ({N_land_total}).")
else:
    st.info(f"Both orientations fit the same number of panels: **{N_land_total}**.")
