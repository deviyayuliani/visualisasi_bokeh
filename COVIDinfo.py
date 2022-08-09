# Sumber data: https://www.kaggle.com/ardisragen/indonesia-coronavirus-cases/version/39
# Dataset yang digunakan adalah 'province.csv' dan 'cases.csv'

import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Panel, TableColumn, DataTable, Tabs
import math


df_province = pd.read_csv('./data/province.csv', index_col=0, encoding = "ISO-8859-1", engine='python')
df_cases = pd.read_csv('./data/cases.csv', encoding = "ISO-8859-1", engine='python')

df_province['province_name'] = df_province['province_name'].str[1:]
df_province = df_province[:-1]


# Tab 1: summary tabel terkonfirmasi

stats = df_province.groupby('island')['confirmed'].describe()
stats = stats.reset_index()

src = ColumnDataSource(stats)

table_columns = [TableColumn(field='island', title='Pulau'),
                 TableColumn(field='min', title='Terkonfirmasi Minimum'),
                 TableColumn(field='mean', title='Terkonfirmasi Rata-Rata'),
                 TableColumn(field='max', title='Terkonfirmasi Maksimum')]

table = DataTable(source=src, columns=table_columns)
tab1 = Panel(child=table, title='Summary Kasus Positif Tiap Pulau')


# Tab 2: scatter plot antara banyak kasus dan kepadatan penduduk

province_cds = ColumnDataSource(df_province)
select_tools = ['pan',
                'box_select',
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
                   color='#3477eb',
                   selection_color='#17cf57',
                   nonselection_color='lightgray',
                   nonselection_alpha='0.3')

tooltips = [('Provinsi', '@province_name'),
           ('Pulau', '@island'),
           ('Ibukota', '@capital_city'),
           ('Kasus positif', '@confirmed'),
           ('Meninggal', '@deceased'),
           ('Sembuh', '@released')]

fig_scatter.add_tools(HoverTool(tooltips=tooltips))

tab2 = Panel(child=fig_scatter, title='Populasi Per KM Persegi & Kasus Terkonfirmasi')


# Menggabungkan semua tab yang sudah dibuat

tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)
