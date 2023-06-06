import streamlit as st
import pandas as pd
import plotly.express as px
import itertools
import plotly.graph_objects as go
from plotly.subplots import make_subplots



upload_files = st.file_uploader('Choose a CSV file', type='csv', accept_multiple_files=True)

data = pd.DataFrame()
for upload_file in upload_files:
    if upload_file:
        st.markdown('-----')
        df = pd.read_csv(upload_file)
        st.dataframe(df)
        data = pd.concat([data, df])

# convert TimeStamp column to datetime type
data['Open Time'] = pd.to_datetime(data['Open Time'])

# Parameters
# extract hours
data['hourly'] = data['Open Time'].dt.hour
# extract days
data['days'] = data['Open Time'].dt.day_name()

# profit data to plot
# hours profit
hourly_profit = data.groupby('hourly')[['Profit_x', 'Profit_y']].agg('sum')
# daily profit
daily_profit = data.groupby('days')[['Profit_x', 'Profit_y']].agg('sum').round(2)


# trades data to plot
trades_hourly = data.groupby('hourly')['TicketNo.'].agg('count')
trades_daily = data.groupby('days')['TicketNo.'].agg('count')



# P/L plots

# Hourly plots

trace1 = go.Bar(
   x = hourly_profit.index, 
   y=hourly_profit['Profit_x'],
   name = 'Profit Close'
)
trace2 = go.Bar(
   x = hourly_profit.index,
     y=hourly_profit['Profit_y'],
     name = 'Profit Open'
)

figures = [trace1, trace2]
layout = go.Layout(barmode = 'group')
fig = go.Figure(data = figures, layout = layout)


fig.update_layout(title=dict(text="P/L hourly"),
   xaxis = dict(
      tickmode = 'linear')
)

fig.show()


fig = go.Figure(data=[go.Bar(x=daily_profit.index, y=daily_profit, text=daily_profit)])


# Daily P/L
trace1 = go.Bar(
   x = daily_profit.index, 
   y=daily_profit['Profit_x'],
   name = 'Profit Close'
)
trace2 = go.Bar(
   x = daily_profit.index,
     y=daily_profit['Profit_y'],
     name = 'Profit Open'
)

figures = [trace1, trace2]
layout = go.Layout(barmode = 'group')
fig = go.Figure(data = figures, layout = layout)


fig.update_layout(title=dict(text="P/L hourly"),
   xaxis = dict(
      tickmode = 'linear')
)

fig.show()


# Hourly trades
fig = go.Figure(data=[go.Bar(x=trades_hourly.index, y=trades_hourly)])

# add the title
fig.update_layout(title=dict(text="Trades hourly"))
fig.show()

# Daily Trades
fig = go.Figure(data=[go.Bar(x=trades_daily.index, y=trades_daily)])

# add the title
fig.update_layout(title=dict(text="Trades daily"))
fig.show()
