from PIL import Image
import streamlit as st
import base64
from pathlib import Path
# Config Page Style and overall data
st.set_page_config(page_title="Fórum", page_icon="🤝", layout="centered")
file_ = open(Path(__file__).parent/"utils/ROCS.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()
#Sidebar

st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100" height="100" alt="cat gif">',unsafe_allow_html=True)
image=Image.open(Path(__file__).parent/'utils/Fotinha.jpeg')

"""
    Olá, sou Rodrigo Carvalho.

Sou estudante de economia, e embora a literatura econômica até seja de meu interesse, o que eu realmente pretendo fazer no dia a dia é programar e passar as ideias para scrits.

Aplicações de machine learning fazem meus olhos brilharem, especialmente aplicações em jogos e esportes.

"""
col1, col2, col3 = st.columns(3)
col2.image(image, caption='')
