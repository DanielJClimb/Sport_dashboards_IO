
import streamlit as st

col1, col2, col3 = st.columns([1, 5, 1], border=False)

with col1:
    st.write(' ')
with col2:
    st.header('SCOS', divider=True)
    st.write('SCOS, which stands for Scrutiny of Sport, is an application that aims to allow the user to view player statistics and visualizations after each match. '
             'Based on data downloaded via an API from the Statsbomb website, after selecting a player and a specific match, a short report of performance will appear, which then can be downloaded in PDF format.'
             'We hope you find our app useful! ')
    st.markdown('<div style="text=align: right;">', unsafe_allow_html=True)
    if st.button("Click to start", use_container_width=True,  type='primary'):
        st.switch_page("pages\\main.py")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.write(' ')
