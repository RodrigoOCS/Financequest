import pandas as pd
import streamlit as st
import datetime
import yfinance as yf
from pathlib import Path


# Config Page Style and overall data
st.set_page_config(page_title="Análise de ações", page_icon="🧐", layout="centered")

hj=datetime.datetime.today().__str__()[:10]
periodos_possíveis = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']


    # config page funcs


def pega_ação(quote_name,start='2010-01-01',end=hj,period='1d'):
    if len(quote_name)>1:
        print('a')
        df = yf.Tickers(quote_name).history(start=start,end=end,period=period)['Close']
    else:
        df = yf.Ticker(quote_name[0]).history(start=start,end=end,period=period)['Close'].to_frame()
        df.columns = quote_name

    df.index.name='Data'
    return df

# Page code
st.header('Análise as ações e ETFS pelo código!')

Formulário1 = st.form('Histórico')
df_stocks=Path(__file__).parent/'utils/file.xlsx'
df_stocks = pd.read_excel(df_stocks,index_col=0)
stocks=[ e+'.SA' for e in set(df_stocks.values.reshape(1,-1)[0]) if type(e)==str]


with Formulário1:

    quote_ = st.multiselect(label="Selecione as ações", options=stocks,default='PETR4.SA')

    c2, c3, c4 = st.columns(3)

    start_ = c3.date_input(
        "Inicío",
        datetime.date(2019, 7, 6))
    end_ = c4.date_input(
        "Fim",
        datetime.date(2020, 7, 6))

    period_ = c2.selectbox('Selecione a frequência dos dados',options=periodos_possíveis)

    atualizar = st.form_submit_button('Visualizar')



#if visu:


dados = pega_ação(quote_name=quote_, start=start_, end=end_, period=period_)

cont = st.columns(len(dados.columns))
ncols=len(dados.columns)
for n in range(ncols):
    e=dados.columns[n]
    d1 = dados.loc[:, e]

    ret = round(d1.iloc[-1] - d1.iloc[0], 2)
    retpct = str(round((d1.iloc[-1] / d1.iloc[0]) - 1, 2)) + "%"

    cont[n].metric(f'Retorno {e}',ret,retpct)


st.write(f'De {start_} até {end_}')

tab1,tab2,tab3,tab4 = st.tabs(["Tabela","Gráfico de valor","Gráfico de retorno","Volatilômetro" ])

with tab1:
    st.dataframe(dados)

with tab2:
   st.line_chart(dados)
with tab3:
   st.line_chart(dados.pct_change())
with tab4:
    horizonte = st.slider('Horizonte',1,365,7)
    visu=True
    volatilizado = dados.rolling(horizonte).std().dropna()

    st.line_chart(volatilizado)

csv = dados.to_csv().encode('utf-8')

st.download_button(
    label="Download dados como CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)

