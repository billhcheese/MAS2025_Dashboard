import streamlit as st

pg = st.navigation([st.Page("Metro_Summary.py"), st.Page("Demographic_Breakdown.py"), st.Page("FAQ.py")], position="top")
pg.run()