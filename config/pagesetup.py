import streamlit as st
from streamlit_extras.stylable_container import stylable_container as sc

def get_page_styling():
    with open("assets/styling/styles.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


def set_header(title: str, subtitle: str, divider: bool=True):
    st.markdown(f"""<span style="font-weight: bold; font-size: 2em; color:#4A90E2;">{title} </span> <span style="font-weight: bold; color:#333333; font-size:1.3em;">{subtitle}</span>""", unsafe_allow_html=True)
    if divider:
        st.divider()