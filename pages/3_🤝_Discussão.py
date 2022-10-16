from streamlit_disqus import st_disqus
import streamlit as st
from pathlib import Path

import base64

# Config Page Style and overall data
st.set_page_config(page_title="Fórum", page_icon="🤝", layout="centered")
file_ = open(Path(__file__).parent/"utils/ROCS.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()
#Sidebar
st.sidebar.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100" height="100" alt="cat gif">',unsafe_allow_html=True)

st.header('Fórum')
st_disqus("forum-tblgopfijx")
