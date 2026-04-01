import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Page config
st.set_page_config(page_title="Supermarket Queue Model", layout="wide")

# DARK THEME
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.title("🛒 Supermarket Checkout Optimization System")
st.markdown("### Based on M/M/c Queue Theory")

# DESCRIPTION
st.write("""
This project analyzes a supermarket checkout system using queue theory.

- Customers arrive at a certain rate (λ)
- Cashiers serve customers (μ)
- Multiple counters reduce waiting time

Goal: Optimize system performance and reduce queue delay.
""")

st.divider()

# SIDEBAR INPUT
st.sidebar.header("⚙️ Control Panel")

arrival_rate = st.sidebar.slider("Arrival Rate (λ)", 1, 20, 10)
service_rate = st.sidebar.slider("Service Rate (μ)", 1, 20, 5)
servers = st.sidebar.slider("Number of Cashiers (c)", 1, 10, 3)

# CORE FUNCTION (ONLY ONE - CORRECT)
def calculate(arrival, service, servers):
    rho = arrival / (servers * service)

    if rho >= 1:
        return rho, None

    wait = rho / (servers * service * (1 - rho))
    return rho, wait

# LOADER
with st.spinner("Running analysis..."):
    time.sleep(1)

rho, wait = calculate(arrival_rate, service_rate, servers)

# RESULTS
st.subheader("📊 System Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Utilization (ρ)", round(rho, 2))

with col2:
    if wait is not None:
        st.metric("Waiting Time", f"{round(wait, 2)} min")
    else:
        st.metric("Waiting Time", "∞")

with col3:
    if rho < 0.5:
        st.success("🟢 Efficient System")
    elif rho < 0.9:
        st.warning("🟡 Moderate Load")
    else:
        st.error("🔴 Overloaded System")

# STATUS
if wait is None:
    st.error("⚠️ System is unstable! Increase service rate or cashiers.")
else:
    st.success("✅ System is stable.")

st.divider()

# GRAPH (MULTI-CASHIER COMPARISON)
st.subheader("📈 Waiting Time Comparison (Cashiers)")

fig, ax = plt.subplots(figsize=(10, 5))

x = range(1, 25)

def get_wait(arrival, service, servers):
    rho = arrival / (servers * service)
    if rho >= 1:
        return None
    return rho / (servers * service * (1 - rho))

y1 = [get_wait(i, service_rate, 1) for i in x]
y2 = [get_wait(i, service_rate, 2) for i in x]
y3 = [get_wait(i, service_rate, 3) for i in x]

# Replace None with NaN
y1 = [np.nan if v is None else v for v in y1]
y2 = [np.nan if v is None else v for v in y2]
y3 = [np.nan if v is None else v for v in y3]

# Colored lines
ax.plot(x, y1, marker='o', linewidth=2, label="1 Cashier", color='#ff4b4b')
ax.plot(x, y2, marker='o', linewidth=2, label="2 Cashiers", color='#1f77b4')
ax.plot(x, y3, marker='o', linewidth=2, label="3 Cashiers", color='#2ecc71')

ax.set_title("Waiting Time vs Arrival Rate")
ax.set_xlabel("Arrival Rate")
ax.set_ylabel("Waiting Time")

ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()

st.pyplot(fig)

st.divider()

# SMART RECOMMENDATION
st.subheader("🤖 Smart Recommendation")

best_cashiers = None
best_wait = float("inf")

for c in range(1, 15):
    r, w = calculate(arrival_rate, service_rate, c)
    if w is not None and w < best_wait:
        best_wait = w
        best_cashiers = c

if best_cashiers is not None:
    st.success(f"✅ Optimal Cashiers Required: {best_cashiers}")
    st.info(f"💡 Waiting time can be reduced to {round(best_wait, 2)} minutes")

st.divider()

# SYSTEM LOAD
st.subheader("🔍 System Load Indicator")

progress = min(int(rho * 100), 100)
st.progress(progress)

st.divider()

# THEORY
st.subheader("📘 Model Explanation")

st.write("""
This system is based on the M/M/c queue model:

- M: Poisson arrival process  
- M: Exponential service time  
- c: Number of servers  

Formula:
ρ = λ / (c × μ)

If ρ ≥ 1 → System becomes unstable  
If ρ < 1 → System operates efficiently  
""")

# FOOTER
st.markdown("---")
st.markdown("<center><small>Developed by Arpita</small></center>", unsafe_allow_html=True)