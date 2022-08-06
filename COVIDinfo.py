# Sumber data: https://www.kaggle.com/ardisragen/indonesia-coronavirus-cases/version/39
# Dataset yang digunakan adalah 'province.csv' dan 'cases.csv'

import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import TableColumn, DataTable, Tabs
import math


df_province = pd.read_csv('./data/province.csv', index_col=0)
df_cases = pd.read_csv('./data/cases.csv')

df_province['province_name'] = df_province['province_name'].str[1:]
df_province = df_province[:-1]


# Tab 1: population summary table

stats = df_province.groupby('island')['population'].describe()
stats = stats.reset_index()

src = ColumnDataSource(stats)

table_columns = [TableColumn(field='island', title='Island'),
                TableColumn(field='min', title='Minimum Population'),
                TableColumn(field='50%', title='Median Population'),
                TableColumn(field='max', title='Maximum Population')]

table = DataTable(source=src, columns=table_columns, width=1000)
tab1 = Panel(child=table, title='Population Summary')


# Tab 2: summary tabel terkonfirmasi

stats = df_province.groupby('island')['confirmed'].describe()
stats = stats.reset_index()

src = ColumnDataSource(stats)

table_columns = [TableColumn(field='island', title='Pulau'),
                 TableColumn(field='min', title='Terkonfirmasi Minimum'),
                 TableColumn(field='mean', title='Terkonfirmasi Rata-Rata'),
                 TableColumn(field='max', title='Terkonfirmasi Maksimum')]

table = DataTable(source=src, columns=table_columns)
tab2 = Panel(child=table, title='Summary Kasus Positif Tiap Pulau')

# Tab 3: scatter plot antara banyak kasus dan kepadatan penduduk

province_cds = ColumnDataSource(df_province)
select_tools = ['wheel_zoom',
                'box_select',
                'lasso_select',
                'poly_select',
                'tap',
                'reset']

fig_scatter = figure(plot_height=600, plot_width=800,
                     x_axis_label='Populasi per KM persegi',
                     y_axis_label='Kasus terkonfirmasi',
                     title='Perbandingan Kasus Positif terhadap Kepadatan Penduduk',
                     toolbar_location='right',
                     tools=select_tools)

fig_scatter.square(x='population_kmsquare',
                   y='confirmed',
                   source=province_cds,
                   color='#34EB6E',
                   selection_color='#17CF7F',
                   nonselection_color='lightgray',
                   nonselection_alpha='0.3')

tooltips = [('Provinsi', '@province_name'),
           ('Pulau', '@island'),
           ('Ibukota', '@capital_city'),
           ('Kasus positif', '@confirmed'),
           ('Meninggal', '@deceased'),
           ('Sembuh', '@released')]

fig_scatter.add_tools(HoverTool(tooltips=tooltips))

tab3 = Panel(child=fig_scatter, title='Populasi Per KM Persegi & Kasus Terkonfirmasi')


# Menggabungkan semua tab yang sudah dibuat

tabs = Tabs(tabs=[tab1, tab2, tab3])

curdoc().add_root(tabs)
