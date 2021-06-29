
import pandas as pd
from bsedata.bse import BSE
import yfinance as yf
import mplfinance as mpl
import streamlit as st
b = BSE()

#st.subheader("**Visually** Show data on a stock!")

st.markdown("""<br>""",True)
@st.cache(suppress_st_warning=True)
def get_data(ticker,Start,End):
    try:
        stock_data = yf.download(ticker,Start,End)
        return stock_data
    except:
        print(f"No data found for {ticker}")
@st.cache(suppress_st_warning=True)
def get_data_bo(ticker):
    return b.getQuote(ticker)

def get_info(ticker):
    df_bo = get_data_bo(str(int(ticker)))
    st.markdown("""<center><h1><b> Stock Info </b> </h1></center> """,True)
    st.markdown(f"## {df_bo['companyName']}")
    st.markdown(f"Industry - **{df_bo['industry']}**")
    st.markdown(f"Current Value - **{df_bo['currentValue']}**")
    st.markdown(f"Free Float Market Cap - **{df_bo['marketCapFreeFloat']}**")
    st.markdown(f"Full Market Cap - **{df_bo['marketCapFull']}**")
    st.markdown(f"52 Week High - **{df_bo['52weekHigh']}**")
    st.markdown(f"52 Week Low - **{df_bo['52weekLow']}**")


def get_input() :
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    with st.sidebar.form(key='searchform'):
        nav1, nav2 = st.beta_columns([3, 2])

        with nav1:
            search_term = st.selectbox("Select",df['COMPANY'].tolist())
            if search_term == '' :
                search_term = "Abbott India Ltd"
        with nav2:
            st.text("Search ")
            submit_search = st.form_submit_button(label='Get Chart')

    return start_date,end_date,search_term

@st.cache(allow_output_mutation=True)
def read_csv_(file):
    return pd.read_csv(file)

@st.cache(suppress_st_warning=True)
def get_list_info(comp):
    dp_1 = df.where(df['COMPANY'] == comp)
    dp_1 = dp_1.dropna()
    dp_1.reset_index(drop=True, inplace=True)
    tic_comp = dp_1.iloc[0]['ticker']
    return get_data_bo(str(int(tic_comp)))



st.title("Stock Market Analysis Web Application")
st.markdown("""<br>""",True)
st.markdown(""" <center><h2><b>Analize Your Stocks Here</b></h2></center>""",True)
st.markdown("""<br>""",True)

st.image("stock_img.jpg",use_column_width=True)


st.sidebar.header("Input")

# Read CSV File
df = read_csv_("final_all.csv")

#Take Input
srt,et,sqt = get_input()
l = [i for i in range(0,470) ]
df['ind'] = l

st.markdown("""<br>""",True)

dp = df.where(df['COMPANY'] == sqt)
dp = dp.dropna()
dp.reset_index(drop=True, inplace=True)

tic = dp.iloc[0]['ticker1']
tic_bo = dp.iloc[0]['ticker']
stock_data = get_data(tic,srt,et)
# st.write(stock_data)
get_info(tic_bo)




st.markdown("""<br>""",True)
st.markdown("""<br>""",True)
l = ['Close Value',"Compare Stock","Volume","Candlestick"]
p = ['Close Value','Volume','Highest','Lowest','Adj Close','Open']
cp = st.sidebar.selectbox("Select a Graph ",l)

if cp == "Close Value" :
    st.markdown("""<b><center> Closing Price </center></b>""",True)
    st.line_chart(stock_data['Close'],use_container_width=True)

if cp == "Volume" :
    st.markdown("""<b><center> Volume </center></b>""",True)
    st.line_chart(stock_data['Volume'])

if cp == "Compare Stock" :

    with st.sidebar.form(key='searc'):
        nav1, nav2 = st.beta_columns([3, 2])

        with nav1:
            serch_it = st.selectbox("Select",df['COMPANY'].tolist())
            if serch_it  == '' :
                serch_it  = "Abbott India Ltd"
        with nav2:
            st.text("Search ")
            submit_search = st.form_submit_button(label='Get Chart')
    dp = df.where(df['COMPANY'] == serch_it)
    dp = dp.dropna()
    dp.reset_index(drop=True, inplace=True)
    # st.write(dp.iloc[0]['ticker1'])
    tic = dp.iloc[0]['ticker1']
    tic_bo_1 = dp.iloc[0]['ticker']
    stock_data2 = get_data(tic, srt, et)
    kp = st.sidebar.selectbox('Select Parameter to Compare ' ,p)
    get_info(tic_bo_1)
    st.markdown(""" <br>""",True)
    st.markdown(""" <br>""",True)
    st.markdown(f"<center><b>{sqt}</b> &nbsp;  vs &nbsp;  <b>{serch_it}</b></center>",True)
    if kp == "Close Value" :
        # pass
        dec = {sqt : stock_data['Close'],
               serch_it : stock_data2['Close']
               }
        df = pd.DataFrame(dec)
        st.line_chart(df)

    if kp == "Volume" :
        dec = {
            sqt : stock_data['Volume'],
            serch_it : stock_data2['Volume']
        }
        df = pd.DataFrame(dec)
        st.line_chart(df)

    if kp == "Highest" :
        dec = {
            sqt: stock_data['High'],
            serch_it: stock_data2['High']
        }
        df = pd.DataFrame(dec)
        st.line_chart(df)

    if kp == "Lowest" :
        dec = {
            sqt : stock_data['Low'],
            serch_it : stock_data2['Low']
        }
        df = pd.DataFrame(dec)
        st.line_chart(df)
    if kp == "Adj Close" :
        dec = {
            sqt : stock_data['Adj Close'],
            serch_it : stock_data2['Adj Close']
        }
        df = pd.DataFrame(dec)
        st.line_chart(df)
    if kp == "Open" :
        dec = {
            sqt: stock_data['Open'],
            serch_it: stock_data2['Open']
        }
        df = pd.DataFrame(dec)
        st.line_chart(df)


if cp == "Candlestick" :
    st.markdown("""<b><center> CandleStick Chart </center></b>""", True)
    mpl.plot(stock_data, type='candle', style='mike',volume=True,mav=(2,4,6))
    st.pyplot()



df = df = pd.read_csv("final_all.csv")
st.markdown("""<h2><b><center> Quick Price Lookup </center></b></h2>""",True)
comp = st.selectbox("Select",df['COMPANY'].tolist())
df_bo = get_list_info(comp)
st.markdown(f"Current Value - **{df_bo['currentValue']}**")
st.markdown(f"Day's High - **{df_bo['dayHigh']}**")
st.markdown(f"Day's Low - **{df_bo['dayLow']}**")
st.set_option('deprecation.showPyplotGlobalUse', False)



