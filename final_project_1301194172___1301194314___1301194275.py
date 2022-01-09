import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

# Read dataset
df = pd.read_csv("country_wise_latest.csv")
df.head(5)

data = df[["Country/Region", "Confirmed", "Deaths", "Recovered", "Active", "New cases", "New deaths", "New recovered", "Confirmed last week", "WHO Region"]]
data.rename(columns={'Country/Region':'Negara', 'Confirmed':'Terkonfirmasi', 'Deaths':'Kasus_Kematian', 'Recovered':'Sembuh', 'Active':'Aktif', 'New cases':'Kasus_Baru', 'New recovered':'Baru_Pulih', 'New deaths':'Kasus_Kematian_Baru', 'Confirmed last week':'Terkonfirmasi_Minggu_Lalu', 'WHO Region':'Benua'}, inplace=True)
data.set_index('Negara', inplace=True)

benua_list = data.Benua.unique().tolist()

mapper = CategoricalColorMapper(factors=benua_list, palette=Spectral6)

# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'       : data.Terkonfirmasi,
    'y'       : data.Sembuh,
    'Kasus Kematian' : data.Kasus_Kematian,
    'Aktif'     : data.Aktif,
    'Benua'  : data.Benua,
})

# Create the figure: plot
plot = figure(title='1970', x_axis_label='Terkonfirmasi (children per woman)', y_axis_label='Kasus_Kematian Expectancy (years)',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@Negara')])

# Add a circle glyph to the figure p
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='Benua', transform=mapper), legend='Benua')

# Set the legend and axis attributes
plot.legend.location = 'top_left'

# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `negara` name to `slider.value` and `source.data = new_data`
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # new data
    new_data = {
    'x'       : data.loc[x],
    'y'       : data.loc[y],
    'Kasus Kematian' : data.Kasus_Kematian,
    'Aktif'     : data.Aktif,
    'Benua'  : data.Benua,
    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'Gapminder data for %d' % negara

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['Terkonfirmasi', 'Kasus_Kematian', 'Sembuh', 'Aktif'],
    value='Terkonfirmasi',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['Terkonfirmasi', 'Kasus_Kematian', 'Sembuh', 'Aktif'],
    value='Kasus_Kematian',
    title='y-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)
    
# Create layout and add to current document
layout = row(widgetbox(x_select, y_select), plot)
curdoc().add_root(layout)
