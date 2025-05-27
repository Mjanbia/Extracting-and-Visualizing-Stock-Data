
#install required packages 

# pip install yfinance
# pip install bs4
# pip install nbformat
# pip install --upgrade plotly

# import relevant libraries

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = 'iframe'

#ignore all warnings

import warnings
warnongs.filterwarnings('ignore', category=FutureWarning)


#Use yfinance to Extract Stock Data

tesla = yf.Ticker('TSLA')
tesla_data=tesla.history(period='max')
tesla_data.reset_index(inplace=True)
tesla_data.head()

#Use Webscraping to Extract Tesla Revenue Data

url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data=requests.get(url).text
soup=BeautifulSoup(html_data,'html.parser')

tesla_revenue=pd.DataFrame(columns=['Date','Revenue'])

for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    date = col[0].text
    Revenue = col[1].text
    

tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date":[date], "Revenue":[Revenue]})], ignore_index=True)

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail()


#Use yfinance to Extract Stock Data

gamestop=yf.Ticker('GME')
gme_data=gamestop.history(period='max')

gme_data.reset_index(inplace=True)
gme_data.head()

#Use Webscraping to Extract GME Revenue Data

url_2='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'

html_data_2=requests.get(url_2).text

soup_2=BeautifulSoup(html_data_2,'html.parser')

gme_revenue=pd.DataFrame(columns=['Date','Revenue'])

for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    date = col[0].text
    Revenue = col[1].text
    
gme_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date":[date], "Revenue":[Revenue]})], ignore_index=True)
gme_revenue.tail()


#Plot Tesla Stock and GameStop Stock Graph


# Define Graphing Function

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3
    )
    
    # Filter data up to specified dates
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    
    # Clean revenue data (remove '$' and ',', then convert to float)
    revenue_data_specific['Revenue'] = (
        revenue_data_specific['Revenue']
        .str.replace('[\$,]', '', regex=True)  # Remove $ and commas
        .astype(float)  # Convert to float
    )
    
    # Add stock price trace (removed `infer_datetime_format`)
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_data_specific.Date),
            y=stock_data_specific.Close.astype("float"),
            name="Share Price"
        ),
        row=1, col=1
    )
    
    # Add revenue trace (removed `infer_datetime_format`)
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_data_specific.Date),
            y=revenue_data_specific.Revenue,
            name="Revenue"
        ),
        row=2, col=1
    )
    
    # Update axes and layout
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )
    
    fig.show()


make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'gameStop')
