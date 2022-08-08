# Sumber data: https://www.kaggle.com/ardisragen/indonesia-coronavirus-cases/version/39
# Dataset yang digunakan adalah 'province.csv' dan 'cases.csv'

import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import TableColumn, DataTable, Tabs
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


fig_line.legend.location = 'top_left'

fig_line.xaxis.major_label_orientation = math.pi/3

tooltips = [('Total Kasus', '@acc_confirmed'),
            ('Kasus baru', '@new_confirmed'),
            ('Sembuh', '@new_released'),
            ('Meninggal', '@new_deceased')]

acc_hover_glyph = fig_line.circle(x='date', y='acc_confirmed', source=cases_cds,
                                  size=15, alpha=0,
                                  hover_fill_color='black', hover_alpha=0.5)

new_confirmed_hover_glyph = fig_line.circle(x='date', y='new_confirmed', source=cases_cds,
                                            size=15, alpha=0,
                                            hover_fill_color='black', hover_alpha=0.1)

new_released_hover_glyph = fig_line.circle(x='date', y='new_released', source=cases_cds,
                                           size=15, alpha=0,
                                           hover_fill_color='black', hover_alpha=0.1)

new_deceased_hover_glyph = fig_line.circle(x='date', y='new_deceased', source=cases_cds,
                                          size=15, alpha=0,
                                          hover_fill_color='black', hover_alpha=0.1)


fig_line.add_tools(HoverTool(tooltips=tooltips, renderers=[new_confirmed_hover_glyph,
                                                           new_released_hover_glyph,
                                                           new_deceased_hover_glyph,                                                          
                                                           acc_hover_glyph]))

fig_line.legend.click_policy = 'hide'

tab2 = Panel(child=fig_line, title='Plot Jumlah Kasus')


# Menggabungkan semua tab yang sudah dibuat

tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)
