# importing general packages
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from datetime import date

# import bokeh objects and functions
from bokeh.io import output_notebook, show, curdoc
from bokeh.plotting import figure
from bokeh.layouts import gridplot, column
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import TextInput, Button, Paragraph, Select, DateRangeSlider


# function that grabs data from Yahoo Finance
def get_data(symbol, start_date, end_date):
    # grabbing data
    df_spy = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
    df_spy = df_spy.round(2)
    # wrangling DataFrame
    df_spy.reset_index(inplace=True)
    df_spy.columns = df_spy.columns.str.lower().str.replace(' ','_')
    lst_cols = ['high', 'low', 'open', 'adj_close', 'volume',]
    df_spy.drop(columns=lst_cols, inplace=True)
    # adding columns
    df_spy['ret'] = df_spy['close'] / df_spy['close'].shift(1) - 1
    df_spy['realized_vol'] = df_spy['ret'].rolling(42).std() * np.sqrt(252)
    return(df_spy)


date_slider = DateRangeSlider(title="Date Range: ", 
                            start=date(2000, 1, 1), 
                            end=date.today(), 
                            value=(date(2015, 1, 1), date.today()),
                            step=90)
input_stock = TextInput(value='SPY')
button = Button(label="Update Graph")

# putting df_spy into a ColumnDataSource object
start_date = date_slider.value_as_date[0]
end_date = date_slider.value_as_date[1]
cds_spy = ColumnDataSource(data=get_data('SPY', 
                                            start_date=start_date, 
                                            end_date=end_date,))

# add a callbacks to widgets
start_date = date_slider.value_as_date[0]
end_date = date_slider.value_as_date[1]
cds_spy.data = get_data(input_stock.value, start_date, end_date)
button.on_click(update_data)def update_data():
 


# defining the three plots
plot_options = dict(width=600, height=250, x_axis_type='datetime', 
                    tools=['wheel_zoom,reset,box_zoom'])
#my_title = input_stock.value + ": " + start_date.strftime('%m/%d/%Y') + " - " + end_date.strftime('%m/%d/%Y')
#p1 = figure(title=my_title, **plot_options)
p1 = figure(**plot_options)
p1.line(x='date', y='close', source=cds_spy)
p1.title.text_font_size = '14pt'

p2 = figure(x_range=p1.x_range, **plot_options)
p2.line(x='date', y='ret', source=cds_spy)

p3 = figure(x_range=p1.x_range, **plot_options)
p3.line(x='date', y='realized_vol', source=cds_spy)

# putting three plots into a gridplot
p = gridplot([[p1], 
              [p2], 
              [p3],],
              toolbar_location='right'
            )

# create a layout for everything
layout = column(date_slider, input_stock, button, p,)

 # add the layout to curdoc
curdoc().add_root(layout)