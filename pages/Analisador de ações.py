import streamlit as st
import datetime
hj=datetime.datetime.today().__str__()[:10]
#corta


import yfinance as yf
st.set_page_config(page_title="Bug report", page_icon="🐞", layout="centered")
st.header(' OI')

periodos_possíveis = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

def pega_ação(quote_name,start='2010-01-01',end=hj,period='1d'):
    quote = yf.Ticker(quote_name)
    dados = quote.history(start=start,end=end,period=period)['Close']
    return dados

Formulário1=st.form('Histórico')

with Formulário1:
    c1, c2= st.columns(2)
    c3, c4 = st.columns(2)
    start_=c3.date_input(
        "Inicío",
        datetime.date(2019, 7, 6))
    end_=c4.date_input(
        "Fim",
        datetime.date(2020, 7, 6))
    quote_ = c1.text_input('Selecione a ação', 'PETR4.SA')
    period_ = c2.selectbox('Selecione a frequência dos dados',options=periodos_possíveis)
    atualizar=st.form_submit_button('Visalizar')

if atualizar:
    st.write(quote_)
    st.write(f'De {start_} até {end_}')
    tab1,tab2 = st.tabs(["Tabela","Gráfico" ])
    dados = pega_ação(quote_name=quote_, start=start_, end=end_, period=period_)

    with tab1:
        st.dataframe(dados)

    with tab2:
       st.line_chart(dados)
st.write('Valor')