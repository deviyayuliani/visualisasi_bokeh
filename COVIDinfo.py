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

# Tab 2: line & bar plot jumlah kasus per hari

cases_cds = ColumnDataSource(df_cases)

fig_line = figure(plot_height=600, plot_width=800,
                  title='Jumlah Terkonfirmasi Positif Maret 2020',
                  x_axis_label='Tanggal', y_axis_label='Jumlah kasus',
                  x_range=df_cases.get('date'),
                  toolbar_location='right')

fig_line.line(x='date', y='acc_confirmed',
              line_color='black',
              legend_label='Kasus akumulasi',
              source=cases_cds)

fig_line.vbar(x='date', top='new_confirmed',
              width=0.8,
              alpha=0.3,
              fill_color='#47A1BF',
              legend_label='Terkonfirmasi positif harian',
              source=cases_cds)

fig_line.vbar(x='date', top='new_released',
              width=0.8,
              alpha=0.3,
              fill_color='#E332B4',
              legend_label='Sembuh harian',
              source=cases_cds)

fig_line.vbar(x='date', top='new_deceased',
              width=0.8,
              alpha=0.3,
              fill_color='#99E332',
              legend_label='Meninggal harian',
              source=cases_cds)

fig_line.vbar(x='date', top='new_tested',
              width=0.8,
              alpha=0.3,
              fill_color='#FFD036',
              legend_label='Tes harian',
              source=cases_cds)

fig_line.vbar(x='date', top='being_checked',
              width=0.8,
              alpha=0.3,
              fill_color='#FC0339',
              legend_label='Tes dalam proses',
              source=cases_cds)

fig_line.legend.location = 'top_left'

fig_line.xaxis.major_label_orientation = math.pi/3

tooltips = [('Total Kasus', '@acc_confirmed'),
            ('Kasus baru', '@new_confirmed'),
            ('Sembuh', '@new_released'),
            ('Meninggal', '@new_deceased'),
            ('Jumlah tes baru', '@new_tested'),
            ('Dalam proses tes', '@being_checked')]


fig_line.add_tools(HoverTool(tooltips=tooltips, renderers=[new_confirmed_hover_glyph,
                                                           new_released_hover_glyph,
                                                           new_deceased_hover_glyph,
                                                           new_tested_hover_glyph,
                                                           being_checked_hover_glyph,
                                                           acc_hover_glyph]))

fig_line.legend.click_policy = 'hide'

tab2 = Panel(child=fig_line, title='Plot Jumlah Kasus')


# Menggabungkan semua tab yang sudah dibuat

tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)
