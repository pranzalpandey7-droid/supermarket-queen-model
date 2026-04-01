import streamlit as st
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Supermarket Queue Model", layout="wide")

# CUSTOM CSS
st.markdown("""
<style>
body {
background-color: #0e1117;
}
h1, h2, h3 {
color: #00ffd5;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown("""
# 🛒 Supermarket Checkout Queue Model
### 🚀 Smart Simulation with Visual Analysis
""")

st.divider()

# DESCRIPTION
st.markdown("""
## 📖 Project Description

This system uses a simplified **M/M/c queue model** to analyze:
- Waiting time
- System efficiency
- Effect of multiple counters
""")

# INPUT
st.markdown("## 🎮 Live Simulation")

col1, col2, col3 = st.columns(3)

with col1:
    arrival = st.slider("Arrival Rate", 1, 20, 10)

with col2:
    service = st.slider("Service Rate", 1, 10, 4)

with col3:
    cashiers = st.slider("Cashiers", 1, 10, 3)

# FUNCTION (FIXED)
def calculate(arrival, service, cashiers):
    rho = arrival / (cashiers * service)

    if rho >= 1:
        return rho, None

    wait = rho / (cashiers * service * (1 - rho))
    return rho, wait

# LOADER (just visual)
with st.spinner("Running analysis..."):
    time.sleep(1)

rho, wait = calculate(arrival, service, cashiers)

# RESULTS
st.markdown("## 📊 Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Utilization", round(rho, 2))

with col2:
    if wait is not None:
        st.metric("Waiting Time", f"{round(wait, 2)} min")
    else:
        st.metric("Waiting Time", "∞")

with col3:
    if rho < 0.5:
        st.success("Efficient")
    elif rho < 0.9:
        st.warning("Moderate")
    else:
        st.error("Overloaded")

# STATUS
if wait is None:
    st.error("System Unstable")
else:
    st.success("System Stable")

st.divider()

# GRAPH
st.markdown("## 📈 Performance Graph")

arr = []
waits = []

for a in range(1, 25):
    r, w = calculate(a, service, cashiers)
    if w is not None:
        arr.append(a)
        waits.append(w)

fig, ax = plt.subplots()
ax.plot(arr, waits, marker='o')
ax.set_title("Waiting Time vs Arrival Rate")

st.pyplot(fig)

st.divider()

# INSIGHT
st.markdown("## 🔍 Live Insight")

progress = min(int(rho * 100), 100)
st.progress(progress)

# FOOTER
st.markdown("""
---
<center>
Developed by Arpita
</center>
""", unsafe_allow_html=True)