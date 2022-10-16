from statsmodels.tsa.stattools import adfuller
import streamlit as st
import datetime
import yfinance as yf
import pandas as pd
from numpy import log
from pathlib import Path
from scipy.stats import boxcox

import base64

file_ = open(Path(__file__).parent/"pages/utils/ROCS.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


# Config Page Style and overall data
st.set_page_config(page_title="Análise de ações", page_icon="🔎", layout="centered")

st.sidebar.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100" height="100" alt="cat gif">',unsafe_allow_html=True)

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
st.header('Análise as ações pelo código!')

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




só_retornos = st.checkbox('Retornos')
if só_retornos:
    dados=dados.pct_change().iloc[1:]


tab2,tab3,tab4 = st.tabs(["Valores","Transformações","Volatilômetro" ])
dados_transformados = dados.copy()
with tab2:
    st.line_chart(dados)

    with st.expander('Tabela'):
        st.table(dados_transformados)
with tab3:

    n_diff = st.number_input('Número de Diferenciações',value=0,min_value=0,step=1,max_value=5)

    dados_transformados = dados.copy()

    log_ = st.checkbox('Transformação em Log')

    boxcox_ = st.checkbox('Transformação de BOXCOX')
    if log_:
        dados_transformados=log(dados_transformados)

    if boxcox_:
        autolambda = st.checkbox('Escolha automáritca de Lambda',value=True)


        if autolambda:
            for name_col in dados.columns:
                dados_transformados[name_col] = boxcox(dados_transformados[name_col].values)[0]

        else:
            lambda_box = st.number_input('Valor do lambda')
            for name_col in dados.columns:
                dados_transformados[name_col] = boxcox(dados_transformados[name_col].values,lmbda=lambda_box)

    if n_diff!=0:
        dados_transformados = dados_transformados.diff(n_diff).dropna()

    st.line_chart(dados_transformados)
    with st.expander('Tabela'):
        st.table(dados_transformados)


with tab4:
    horizonte = st.slider('Horizonte',1,365,7)
    volatilizado = dados.rolling(horizonte).std().dropna()
    st.line_chart(volatilizado)

with st.expander('Teste ADF'):
    testar_adf=st.button('Testar')
    Série=st.selectbox(options=dados_transformados.columns,label=dados_transformados.columns[0])
    nsig = st.number_input(label='Nível de significância', max_value=0.99, min_value=0.01,value=0.95)

    if testar_adf:
        p_valor = adfuller(dados_transformados[Série], regression='ct')[1]
        if p_valor < 1 - nsig:
            teste = ''
        else:
            teste = 'não'


        textoadf = f'Dado o teste, cujo resultado foi de um p-valor de {str(p_valor)[:6]}, {teste} se pode afirmar que,há um nível de significância de {nsig * 100}%, que o processo contém uma raíz unitária,{teste} sendo portanto fruto de um processo não estacionário.'
        st.write(textoadf)

csv = dados.to_csv().encode('utf-8')
st.download_button(
    label="Download dados como CSV",
    data=csv,
    file_name='Dados.csv',
    mime='text/csv',
)

