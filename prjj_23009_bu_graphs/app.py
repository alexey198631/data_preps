"""
file columns:
       ['company_code_n', 'Country', 'FY', 'customer_name', 'Indirect_direct',
       'channel', 'type', 'for_bu', 'order_intake_amount_eur']


"""
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

from datetime import datetime
from scipy.stats import linregress


init = pd.read_excel('data_files/data.xlsx', sheet_name='data')
source = init.copy()


def plot_graphs(df, nm):
    summary_df = df.copy()
    # keeping necessary columns only
    summary_df = source.loc[:, ['FY', 'for_bu', 'order_intake_amount_eur']]
    grouped_df = summary_df.groupby(by=['for_bu', 'FY']).order_intake_amount_eur.sum().reset_index()
    grouped_df['order_intake_amount_eur'] = grouped_df['order_intake_amount_eur'] / 1000

    # keeping necessary bu only
    bu_list = ['PCI Transmitters', 'PCI Flowmeters', 'PCI Analytics',
               'PCI Netsol']  # grouped_df['for_bu'].unique().tolist()
    n_plots = len(bu_list)

    # graph size 2 rows and 2 columns
    fig, axs = plt.subplots(2, 2, figsize=(20, 10))
    plt.rcParams['font.family'] = 'Arial'

    for i, name in enumerate(bu_list):
        group = grouped_df[grouped_df['for_bu'] == name]
        ax = axs[i // 2, i % 2]
        bars = ax.bar(group['FY'], group['order_intake_amount_eur'], color=(0 / 255, 49 / 255, 108 / 255), width=0.5,
                      edgecolor='None')
        # ax.set_xlabel('FY')
        ax.set_ylabel('Order Intake')
        ax.set_title(f'{name}', fontsize=18, weight='bold')

        x_labels = ['FY' + str(x)[2:] for x in group['FY']]
        ax.set_xticks(group['FY'])
        ax.set_xticklabels(x_labels, fontsize=14, weight='bold')

        x = group['FY'].astype(float)
        y = group['order_intake_amount_eur'].astype(float)
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        trend_line = slope * x + intercept
        color = 'g' if slope > 0 else 'grey'
        ax.plot(x, trend_line, color, label='Trend Line')
        ax.legend(loc="upper left")

        for bar in bars:
            height = bar.get_height()
            ax.annotate('{:,.0f} k€'.format(height), xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=14, weight='bold')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f} M€'.format(x / 1000)))

        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['right'].set_color('white')
        ax.spines['top'].set_color('white')

    # saving as a separate file with date infromation
    plt.tight_layout()
    current_time = datetime.now().strftime("%d_%m_%Y")
    plt.savefig(f'data_files/{nm}_{current_time}.png', dpi=600, bbox_inches='tight')
    #plt.show()

# summary graphs per BU for years in bars (column - for_bu) (4 graphs) x 1 file
mask1 = source.for_bu == 'PCI Analytics'
mask2 = source.for_bu == 'PCI Flowmeters'
mask3 = source.for_bu == 'PCI Transmitters'
mask4 = source.for_bu == 'PCI Netsol'
source = source[mask1 | mask2 | mask3 | mask4]
plot_graphs(source, 'summary')

#affiliates graphs per BU for years in bars (column - for_bu) (4 graphs) x 16 files
affiliates = init.company_code_n.unique().tolist()

for affiliate in affiliates:
    source = init[init.company_code_n == affiliate]
    plot_graphs(source, affiliate)

print('Done!')