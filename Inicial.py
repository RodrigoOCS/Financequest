import streamlit as st
from streamlit_lottie import st_lottie  # pip install streamlit-lottie #lotties='https://lottiefiles.com/'
import json


st.set_page_config(page_title="Inicial", page_icon="👋", layout="centered")

st.header('Página inicial')

st.write('Olá!')
st.write('Esse é meu aplicativo de acompanhamento financeiro')

lt_path=Path(__file__).parent / "utils/lottiev1.json"
with open(lt_path, "r") as f:
    lt_data = json.load(f)

st_lottie(lt_data)
