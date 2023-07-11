import streamlit as st
import pandas as pd
import plotly.express as px
import itertools
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pages_folder = "pages"

# Create the main page
# with open("/app.py", "w") as f:
#     f.write("st.title('Main Page')\n\n")

# Create the first page
# with open(pages_folder + "/optimizeing_trading_strategies.py", "r") as f:
#     f.write("st.title('Optimizeing Trading Strategies')\n\n")



st.set_page_config(page_title= 'CSV Plotter')
st.title('CSV Plotter')
st.subheader('Feed me with your CSV file')

# Create the main page
# with open(pages_folder + "/main.py", "w") as f:
#     f.write("import streamlit as st\n\n"
#             "st.title('Main Page')\n\n"
#             "st.sidebar.selectbox('Select a page', ['Page 1', 'Page 2'])")

# # Create the first page
# with open(pages_folder + "/page_1.py", "w") as f:
#     f.write("import streamlit as st\n\n"
#             "st.title('Page 1')\n\n"
#             "st.write('This is page 1.')")






def sum_lists_itertools(lst):
    transposed = itertools.zip_longest(*lst, fillvalue=0)
    return [sum(x) for x in transposed]
 


upload_files = st.file_uploader('Choose a CSV file', type='csv', accept_multiple_files=True)
for upload_file in upload_files:
    if upload_file:
        st.markdown('-----')
        df_list = []
        df = pd.read_csv(upload_file)
        if 'TimeStamp' in df.columns:
            # print('Open')

    # convert TimeStamp column to datetime type
            df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])

            # select the desired columns to plot
            x = df['TimeStamp']
            profit = df['Profit']
            price = df['Price']
            volume = df['Volume']
            atr = df['ATR']
            closed = df['ClosedP/L']
            session = df[['London','NewYork', 'Tokyo', 'Sydney']]
            news = df[['EUR_FF', 'EUR_FPT', 'JPY_FF', 'JPY_FPT','GBP_FF', 'GBP_FPT', 'CHF_FF', 
                    'CHF_FPT', 'AUD_FF', 'AUD_FPT', 'CAD_FF','CAD_FPT', 'USD_FF', 'USD_FPT',
                    'CNY_FF', 'CNY_FPT', 'NZD_FF','NZD_FPT']]
            
            profitOfNotNullJpyGbp= df[~((df['JPY_FF'].notna() == True) | (df['JPY_FPT'].notna() == True) | \
                            (df['GBP_FF'].notna() == True) | (df['GBP_FPT'].notna() == True))]['Profit']
            dateOfNotNullJpyGbp = df[~((df['JPY_FF'].notna() == True) | (df['JPY_FPT'].notna() == True) | \
                            (df['GBP_FF'].notna() == True) | (df['GBP_FPT'].notna() == True))]['TimeStamp']
            
            
            # analyze for positive profit 
            Profit_positive = df[df['Profit'] > 0] 
            # get whole number for positive profit 
            whole_number_positive = []
            unique_sequence_positive = Profit_positive['SequenceNo'].unique()
            for i in range(len(unique_sequence_positive)):
                max_profit_positive = int(Profit_positive[Profit_positive['SequenceNo'] == unique_sequence_positive[i]]['Profit'].max())
                if max_profit_positive >= 0:
                    whole_number_positive.append(list(range(1, max_profit_positive+1)))
            # calculate sum for each category whole number 
            result_positive = sum_lists_itertools(whole_number_positive)
            # get the largest array to plot each category of whole number
            max_len_positive = max(whole_number_positive, key=lambda coll: len(coll))

            ## analyze for negative profit
            Profit_negative = df[df['Profit'] < 0] 
            whole_number_negative = []
            unique_sequence_negative = Profit_negative['SequenceNo'].unique()
            for i in range(len(unique_sequence_negative)):
                max_profit_positive = int(Profit_negative[Profit_negative['SequenceNo'] == unique_sequence_negative[i]]['Profit'].min())
                if max_profit_positive <= 0:
                    whole_number_negative.append(sorted(list(range(max_profit_positive, 0)), reverse=True))
            # calculate sum for each category whole number
            result_negative = sum_lists_itertools(whole_number_negative)
            # get the largest array to plot each category of whole number
            max_len_negative = max(whole_number_negative, key=lambda coll: len(coll))

            



            
            # # Create figure with secondary y-axis
            fig = make_subplots(rows=3, cols=1, specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]], shared_xaxes=True)

            fig.add_trace(
                go.Scatter(x =x, y=price, name="Price"), row=1, col=1,
                secondary_y=False
            )

            # Add traces
            fig.add_trace(
                go.Scatter(x=x, y=profit, name="Profit"),row=1, col=1,
                secondary_y=True
            )

            fig.add_trace(
                go.Scatter(x=x, y=closed, name="Closed"),row=2, col=1,
                secondary_y=False,
            )

            fig.add_trace(
                go.Scatter(x=x, y=volume, name="Volume"),row=2, col=1,
                secondary_y=True,
            )

            fig.add_trace(
                go.Scatter(x=x, y=session['Sydney'], name="Sydney"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=session['London'], name="London"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=session['NewYork'], name="NewYork"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=session['Tokyo'], name="Tokyo"),row=3, col=1,
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=x, y=news['EUR_FF'], name="EUR_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['EUR_FPT'], name="EUR_FPT"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['JPY_FF'], name="JPY_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['JPY_FPT'], name="JPY_FPT"),row=3, col=1,
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=x, y=news['GBP_FF'], name="GBP_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['GBP_FPT'], name="GBP_FPT"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['CHF_FF'], name="CHF_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['CHF_FPT'], name="CHF_FPT"),row=3, col=1,
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=x, y=news['AUD_FF'], name="AUD_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['AUD_FPT'], name="AUD_FPT"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['CAD_FF'], name="CAD_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['CAD_FPT'], name="CAD_FPT"),row=3, col=1,
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=x, y=news['USD_FF'], name="USD_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['USD_FPT'], name="USD_FPT"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['CNY_FF'], name="CNY_FF"),row=3, col=1,
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=x, y=news['CNY_FPT'], name="CNY_FPT"),row=3, col=1,
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=x, y=news['NZD_FF'], name="NZD_FF"),row=3, col=1,
                secondary_y=False
            )
            
            fig.add_trace(
                go.Scatter(x=x, y=news['NZD_FPT'], name="NZD_FPT"),row=3, col=1,
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=x, y=atr, name="ATR"),row=3, col=1,
                secondary_y=True,
            )    
            st.plotly_chart(fig)

            fig_large = go.Figure(data=go.Scatter(x=result_positive, y=max_len_positive, mode='markers'))

            # Set x-axis title
            fig_large.update_xaxes(title_text="Whole Number Sum for Large Data")

            # Set y-axes titles
            fig_large.update_yaxes(title_text="Whole Number Category for Large Data")

            st.plotly_chart(fig_large)


            fig_negative = go.Figure(data=go.Scatter(x=result_negative, y=max_len_negative, mode='markers'))

            # Set x-axis title
            fig_negative.update_xaxes(title_text="Whole Number Sum for Large Data")

            # Set y-axes titles
            fig_negative.update_yaxes(title_text="Whole Number Category for Large Data")
            # plot the graph
            st.plotly_chart(fig_negative)

        else:
            # print('Close')
            
            # P/L plots
            # convert TimeStamp column to datetime type
            df['OpenTime'] = pd.to_datetime(df['OpenTime'])

            # Parameters
            # extract hours
            df['hourly'] = df['OpenTime'].dt.hour
            # extract days
            df['days'] = df['OpenTime'].dt.day_name()

            # profit data to plot
            # hours profit
            hourly_profit = df.groupby('hourly')[['Profit']].agg('sum')
            # daily profit
            daily_profit = df.groupby('days')[['Profit']].agg('sum').round(2)


            # trades data to plot
            trades_hourly = df.groupby('hourly')['TicketNo'].agg('count')
            trades_daily = df.groupby('days')['TicketNo'].agg('count')

            ## Analyzing for Whole number Dataset  

            # Hourly plots

            trace1 = go.Bar(
                x = hourly_profit.index, 
                y=hourly_profit['Profit'],
                name = 'Profit Close'
            )
            # trace2 = go.Bar(
            #     x = hourly_profit.index,
            #     y=hourly_profit['Profit_y'],
            #     name = 'Profit Open'
            # )

            figures = [trace1]
            layout = go.Layout(barmode = 'group')
            fig_hourly_pl = go.Figure(data = figures, layout = layout)


            fig_hourly_pl.update_layout(title=dict(text="P/L hourly"),
                xaxis = dict(
                    tickmode = 'linear')
            )

            st.plotly_chart(fig_hourly_pl)

            # fig = go.Figure(data=[go.Bar(x=daily_profit.index, y=daily_profit, text=daily_profit)])


            # Daily P/L
            trace1 = go.Bar(
                x = daily_profit.index, 
                y=daily_profit['Profit'],
                name = 'Profit Close'
            )
            # trace2 = go.Bar(
            #     x = daily_profit.index,
            #     y=daily_profit['Profit_y'],
            #     name = 'Profit Open'
            # )

            figures = [trace1]
            layout = go.Layout(barmode = 'group')
            fig_daily_pl = go.Figure(data = figures, layout = layout)


            fig_daily_pl.update_layout(title=dict(text="P/L Daily"),
                xaxis = dict(
                    tickmode = 'linear')
            )
            st.plotly_chart(fig_daily_pl)

            # Hourly trades
            fig_hourly_trades = go.Figure(data=[go.Bar(x=trades_hourly.index, y=trades_hourly)])

            # add the title
            fig_hourly_trades.update_layout(title=dict(text="Trades hourly"),
                                            xaxis = dict(tickmode = 'linear')
            )
            
            st.plotly_chart(fig_hourly_trades)

            # Daily Trades
            fig_daily_trades = go.Figure(data=[go.Bar(x=trades_daily.index, y=trades_daily)])

            # add the title
            fig_daily_trades.update_layout(title=dict(text="Trades daily"),
                                           xaxis = dict(tickmode = 'linear'))

            st.plotly_chart(fig_daily_trades)








