import pickle
from pathlib import Path
import streamlit as st
from datetime import date
import streamlit_authenticator as stauth
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

st.set_page_config(page_title="Stock Forecast App", page_icon=":bar_chart:", layout="wide")

# Searching stock function
def search_stock(query):
    # Search for stock symbols matching the query
    results = yf.Ticker(query)
    
    # Get the info of the first result
    info = results.info
    
    # Print the symbol and name of the stock
    st.experimental_set_query_params(stock_symbol=info['symbol'])
    st.write("Symbol:", info['symbol'])
    st.write("Name:", info['longName'])
    
    # You can print more information as needed
    # For example: sector, industry, etc.
    st.write("Sector:", info.get('sector', 'N/A'))
    st.write("Industry:", info.get('industry', 'N/A'))
    st.write("Country:", info.get('country', 'N/A'))

#---USER AUTHENTICATION---

names=["Saumya dhakad","Sparsh modi","Shivam singh","Shivam jaiswal"]
usernames=["SD","esper","shivam","SJ"]

# Load hashed passwords
file_path = Path(__file__).parent / "hp.pkl"
with file_path.open("rb") as file:
    hashed_password = pickle.load(file)
      
authenticator = stauth.Authenticate(names, usernames, hashed_password, "sales_dashboard", "abcdef", cookie_expiry_days=1)

names, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")
      
if authentication_status == True:
    st.title("STOCK FORECAST APP")
    st.sidebar.title(f"Welcome {names}")
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    
    search_query = st.sidebar.text_input("Enter a stock symbol or company name:")

    if st.sidebar.button("Search"):
        if search_query:
            search_stock(search_query)
        else:
            st.warning("Please enter a stock symbol or company name.")
    
    n_years = st.sidebar.slider('Years of prediction:', 1, 4)
    period = n_years * 365
    st.sidebar.write("#\n#\n#\n#\n#\n#\n#") 
    authenticator.logout("Logout","sidebar")

    if "stock_symbol" in st.query_params:
        stock_symbol = st.query_params["stock_symbol"]
        data = yf.download(stock_symbol, START, TODAY)
        data.reset_index(inplace=True)
        
        st.subheader('Raw data')
        st.write(data.tail())

        # Plot raw data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text="Time Series data with Rangeslider", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
        
        st.markdown("""---""")

        # Predict forecast with Prophet
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        # Show and plot forecast
        st.subheader('Forecast data')
        st.write(forecast.tail())
        
        st.write('Forecast plot for ', n_years ,' years')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)
        
        st.markdown("""---""")

        st.write("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
