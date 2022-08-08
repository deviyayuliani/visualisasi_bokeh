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

province_cds = ColumnDataSource(df_province)
select_tools = ['wheel_zoom',
                'box_select',
                'lasso_select',
                'poly_select',
                'tap',
                'reset']

fig_line = figure(plot_height=600, plot_width=800,
                  title='Jumlah Terkonfirmasi Positif Maret 2020',
                  x_axis_label='Tanggal', y_axis_label='Jumlah kasus setiap pulau',
                  x_range=df_province.get('date'),
                  toolbar_location='right')

fig_line.line(x='date', y='acc_confirmed',
              line_color='black',
              legend_label='Kasus akumulasi',
              source=province_cds)

fig_line.vbar(x='date', top='new_confirmed',
              width=0.8,
              alpha=0.3,
              fill_color='#47A1BF',
              legend_label='Terkonfirmasi positif harian',
              source=province_cds)

fig_line.vbar(x='date', top='new_released',
              width=0.8,
              alpha=0.3,
              fill_color='#E332B4',
              legend_label='Sembuh harian',
              source=province_cds)

fig_line.vbar(x='date', top='new_deceased',
              width=0.8,
              alpha=0.3,
              fill_color='#99E332',
              legend_label='Meninggal harian',
              source=province_cds)


fig_line.legend.location = 'top_left'

fig_line.xaxis.major_label_orientation = math.pi/3

tooltips = [('Provinsi', '@province_name'),
           ('Pulau', '@island'),
           ('Ibukota', '@capital_city'),
           ('Total Kasus', '@acc_confirmed'),
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
