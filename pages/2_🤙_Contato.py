import streamlit as st
from pathlib import Path
import base64

# Config Page Style and overall data
st.set_page_config(page_title="Contato", page_icon="🤙", layout="centered")
file_ = open(Path(__file__).parent/"utils/ROCS.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()
#Sidebar
st.sidebar.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100" height="100" alt="cat gif">',unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.header("Contato")
st.write('Me envie uma mensagem!')

contact_form = """
<form action="https://formsubmit.co/bot.crescento@gmail.COM" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

local_css("style/style.css")
