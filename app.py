import streamlit as st
from agent import founder_agent

st.set_page_config(page_title="Founder BI Agent", layout="wide")

st.title("📊 Founder's BI Agent")

query = st.text_input(
    "Ask a question about your business data:",
    placeholder="How is our pipeline looking for the energy sector?"
)

if query:
    with st.spinner("Analyzing live monday.com data..."):
        result, trace = founder_agent(query)

    st.subheader("Answer")
    st.json(result)

    st.subheader("Agent Trace")
    for step in trace:
        st.write("✅", step)