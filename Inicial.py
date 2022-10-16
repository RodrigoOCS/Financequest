import streamlit as st
from streamlit_lottie import st_lottie  # pip install streamlit-lottie #lotties='https://lottiefiles.com/'
import json
from pathlib import Path
import base64

file_ = open(Path(__file__).parent/"ROCS.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


st.set_page_config(page_title="Inicial", page_icon="👋", layout="centered")
st.sidebar.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100" height="100" alt="cat gif">',unsafe_allow_html=True)


st.header('Página inicial')

st.write('Olá!')
st.write('Esse é meu aplicativo de modelagem de dados financeiros.')
st.write('Ele auxlia no processo de importar, modelar e salvar os dados.')
st.write('E principalmente - automatiza o processo de programar os modelos!')

lt_path = Path(__file__).parent / "pages/utils/lottiev1.json"
with open(lt_path, "r") as f:
    lt_data = json.load(f)

st_lottie(lt_data)
