import streamlit as st
import math

# ============================================================
# PAGE SETTINGS (white background clean UI)
# ============================================================
st.set_page_config(page_title="Solar Calculator", layout="centered")

# FIXED WHITE BACKGROUND + DARK TEXT
st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;   /* Putih */
            color: #000000;              /* Tulisan Hitam */
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: #111111 !important;   /* Semua text gelap & jelas */
        }
    </style>
""", unsafe_allow_html=True)

st.title("☀️ Solar PV Calculator")
st.write("**Minimalist & Professional Edition**")

# ============================================================
# STEP 1 — FTEMP + AREA + EOUT
# ============================================================
st.header("🔶 STEP 1 — Temperature, Area & Energy Output")

# ----------------------- FTEMP -----------------------
st.subheader("1️⃣ Temperature Factor (ftemp)")

use_ftemp = st.checkbox("Use ftemp in Eout?", value=True)

Pcoef = st.number_input("Temperature Coefficient Pcoef (%/°C)", value=-0.3500, format="%.4f")
Tavg = st.number_input("Average Temperature Tavg (°C)", value=35.0000, format="%.4f")
Tstc = st.number_input("STC Temperature Tstc (°C)", value=25.0000, format="%.4f")

ftemp = 1 + ((Pcoef / 100) * (Tavg - Tstc))
st.success(f"Calculated ftemp = **{ftemp:.4f}**")

if not use_ftemp:
    ftemp = 1.0000   # ignore in calculation

# ----------------------- AREA -----------------------
st.subheader("2️⃣ Solar Panel Area (Length × Width)")

panel_length = st.number_input("Panel Length (m)", value=2.0000, format="%.4f")
panel_width  = st.number_input("Panel Width  (m)", value=1.1000, format="%.4f")

area = panel_length * panel_width
st.success(f"Panel Area = **{area:.4f} m²**")

# ----------------------- EOUT -----------------------
st.subheader("3️⃣ Energy Output (Eout)")

# ON/OFF SWITCHES FOR MAIN PARAMETERS
use_PSH = st.checkbox("Use PSH?", value=True)
use_PASTC = st.checkbox("Use PASTC?", value=True)

PSH = st.number_input("Peak Sun Hours (PSH)", value=4.5000, format="%.4f")
PASTC = st.number_input("Panel Max Power at STC (W)", value=550.0000, format="%.4f")

if not use_PSH:
    PSH = 1.0000
if not use_PASTC:
    PASTC = 1.0000

# OPTIONAL FACTORS (ON/OFF)
st.write("### ⚙️ Optional Correction Factors")

def factor_switch(label, default_value):
    on = st.checkbox(f"Use {label}?", value=True)
    if on:
        val = st.number_input(f"{label}", value=default_value, format="%.4f")
    else:
        val = 1.0000
    return val

fmm        = factor_switch("fmm", 1.0000)
fclean     = factor_switch("fclean", 0.9800)
fdegrad    = factor_switch("fdegrad", 0.9800)
fsunshade  = factor_switch("fsunshade", 1.0000)
eta_cable  = factor_switch("Cable Efficiency", 0.9800)
eta_inv    = factor_switch("Inverter Efficiency", 0.9700)

# EOUT CALCULATION
Eout = (PSH * PASTC * fmm * ftemp * fclean *
        fdegrad * fsunshade * eta_cable * eta_inv) / area

st.success(f"⚡ **Estimated Eout = {Eout:.4f} Wh per m²**")

st.markdown("---")

# ============================================================
# STEP 2 — PANEL FIT CALCULATION
# ============================================================
st.header("🔷 STEP 2 — Landscape vs Portrait Panel Count")

st.subheader("📏 Roof & Panel Dimensions")

Wroof = st.number_input("Roof Width (m)", value=10.0000, format="%.4f")
Lroof = st.number_input("Roof Length (m)", value=20.0000, format="%.4f")
spacing = st.number_input("Panel Spacing Δ (m)", value=0.1000, format="%.4f")

# LANDSCAPE CALCULATION
N_land_up = math.floor(Wroof / (panel_width + spacing))
N_land_across = math.floor(Lroof / (panel_length + spacing))
N_land_total = N_land_up * N_land_across

# PORTRAIT CALCULATION
N_port_up = math.floor(Wroof / (panel_length + spacing))
N_port_across = math.floor(Lroof / (panel_width + spacing))
N_port_total = N_port_up * N_port_across

# DISPLAY RESULTS
col1, col2 = st.columns(2)

with col1:
    st.write("### 🟧 Landscape Mode")
    st.write(f"Up: **{N_land_up}**")
    st.write(f"Across: **{N_land_across}**")
    st.write(f"➡️ Total = **{N_land_total} panels**")

with col2:
    st.write("### 🟦 Portrait Mode")
    st.write(f"Up: **{N_port_up}**")
    st.write(f"Across: **{N_port_across}**")
    st.write(f"➡️ Total = **{N_port_total} panels**")

st.markdown("---")

# RECOMMENDATION SECTION
st.header("📌 Recommendation")

if N_land_total > N_port_total:
    st.success(f"✔ Landscape recommended: **{N_land_total} panels** (more than Portrait {N_port_total})")
elif N_port_total > N_land_total:
    st.success(f"✔ Portrait recommended: **{N_port_total} panels** (more than Landscape {N_land_total})")
else:
    st.info(f"Both orientations fit the same number of panels: **{N_land_total}**")

