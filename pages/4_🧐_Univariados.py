import pandas as pd
import streamlit as st
import datetime
import yfinance as yf
from pathlib import Path
import statsmodels.tsa.api as tsa
from scipy.stats import boxcox
from numpy import log
from numpy import exp
import base64

file_ = open(Path(__file__).parent/"utils/ROCS.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


def boxcox_inverse(value, lam):
    if lam == 0:
        return exp(value)
    return exp(log(lam * value + 1) / lam)


st.set_page_config(page_title="Analise Univariada", page_icon="🧐", layout="centered")
st.write('Em desenvolvimento 🏗️')
hj=datetime.datetime.today().__str__()[:10]
periodos_possíveis = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

#Sidebar
st.sidebar.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100" height="100" alt="cat gif">',unsafe_allow_html=True)

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
stocks.insert(0,'PETR4.SA')


with Formulário1:

    quote_ = st.selectbox(label="Selecione as ações", options=stocks)

    c2, c3, c4 = st.columns(3)

    start_ = c3.date_input(
        "Inicío",
        datetime.date(2019, 7, 6))
    end_ = c4.date_input(
        "Fim",
        datetime.date(2020, 7, 6))

    period_ = c2.selectbox('Selecione a frequência dos dados',options=periodos_possíveis)

    atualizar = st.form_submit_button('Visualizar')

dados = pega_ação(quote_name=[quote_], start=start_, end=end_, period=period_)

graph_cols=st.columns(2)

acf=tsa.stattools.acf(dados)
pacf=tsa.stattools.pacf(dados)

graph_cols[0].write("ACF")
graph_cols[0].bar_chart(acf)

graph_cols[1].write("PACF")
graph_cols[1].bar_chart(pacf,x=range(1,len(pacf)))

cols=st.columns(3)

AR_=cols[0].number_input('AR',step=1,min_value=0,max_value=5)
I_=cols[1].number_input('I',step=1,min_value=0,max_value=5)
MA_=cols[2].number_input('MA',step=1,min_value=0,max_value=5)

check = st.checkbox('Aplicar BOXCOX')
n_dias = st.number_input("Dias para simular", step=1, value=10)

Testar=st.button("Testar")

#dados=df.copy().to_frame()
if Testar:
    st.write(dados)
    dados_2 = dados.copy()
    if check:
        data_alterated,lambda_=boxcox(dados[dados.columns[0]])
        dados = pd.Series(index=dados.index,data= data_alterated)

    model=tsa.ARIMA(endog=dados,order=(AR_,I_,MA_))

    fitted=model.fit()
    st.text(fitted.summary())

    valores_projetados = fitted.fittedvalues
    fore = fitted.get_forecast(n_dias).summary_frame().iloc[:, [0, 2, 3]]
    if check:
        fore = boxcox_inverse(fore , lambda_)
        valores_projetados = boxcox_inverse(valores_projetados , lambda_)

    projetado = pd.concat([dados_2,valores_projetados], axis=1).rename({0: f'Modelo ARIMA({AR_, I_, MA_})   '}, axis=1)


    fore.columns = [projetado.columns[1], 'Limite inferior', 'Limite superior']
    ultdia = projetado.index[-1] + pd.offsets.Day(1)

    index_future = pd.date_range(periods=n_dias, freq='d', start=ultdia)
    fore.index = index_future

    dfproj = pd.concat([projetado, fore])
    st.line_chart(dfproj)

    csv = dfproj.to_csv().encode('utf-8')
    st.download_button(
        label="Download dados projetados como CSV",
        data=csv,
        file_name=f'{quote_}.csv',
        mime='text/csv',
    )
    # Update n_dias, start_,end_,periods_,quote_name_
    text_of_script=Path(__file__).parent/'utils/forecasts.txt'
    text_of_script=open(text_of_script,'r').read()
    text=text_of_script.replace('n_dias',str(n_dias)).replace('start_',str(start_)).replace('end_',str(end_)).replace('period_',period_).replace('quote_name_',quote_)
    text=text.replace('AR_',str(AR_)).replace('I_',str(I_)).replace('MA_',str(MA_))
    if check:
        text = text.replace('check_','True')
    else:
        text = text.replace('check_','False')

    with st.expander('Códigos em Python'):
        st.text(text)
        st.download_button(
            label="Download dos códigos em python",
            data=text,
            file_name=f'{quote_}.py',
            mime='text',
        )




