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
temp = init.copy()
temp['for_bu'] = 'Total'
source = pd.concat([init, temp])


def count_non_zero(lst): #necessary for trend line
    count = 0
    for item in lst:
        if item != 0:
            count += 1
    return count


def plot_graphs(df, nm):
    summary_df = df.copy()
    # keeping necessary columns only

    summary_df = summary_df.loc[:, ['FY', 'for_bu', 'order_intake_amount_eur']]
    grouped_df = summary_df.groupby(by=['for_bu', 'FY']).order_intake_amount_eur.sum().reset_index()
    grouped_df['order_intake_amount_eur'] = grouped_df['order_intake_amount_eur'] / 1000


    # keeping necessary bu only
    bu_list = ['PCI Transmitters', 'PCI Flowmeters', 'PCI Analytics',
               'PCI Netsol', 'Systems&ADS', 'Total']
    #bu_list = grouped_df['for_bu'].unique().tolist()

    # graph size 2 rows and 2 columns
    #fig, axs = plt.subplots(2, 2, figsize=(20, 10))

    n = len(bu_list)
    rows = (n + 1) // 2
    cols = 2
    fig, axs = plt.subplots(rows, cols, figsize=(16, 5 * rows))
    fig.suptitle(nm, fontsize=24, weight='bold')
    axs = axs.flatten()
    plt.rcParams['font.family'] = 'Arial'


    for i, name in enumerate(bu_list):
        group = grouped_df[grouped_df['for_bu'] == name]
        ax = axs[i]
        if group.empty:
            ax.set_title(f'{name}', fontsize=18, weight='bold')
            ax.text(0.5, 0.5, 'N/A', fontsize=18, ha='center', va='center')
            ax.axis('off')
            continue
        elif len(group['FY'].unique().tolist()) < 2:
            ax.set_title(f'{name}', fontsize=18, weight='bold')
            ax.text(0.5, 0.5, 'N/A', fontsize=18, ha='center', va='center')
            ax.axis('off')
            continue
        #ax = axs[i // 2, i % 2]

        bars = ax.bar(group['FY'], group['order_intake_amount_eur'], color=(0 / 255, 49 / 255, 108 / 255), width=0.5,
                      edgecolor='None')
        # ax.set_xlabel('FY')
        ax.set_ylabel('Order Intake')
        ax.set_title(f'{name}', fontsize=18, weight='bold')
        ax.set_ylim(bottom=0)

        x_labels = ['FY' + str(x)[2:] for x in group['FY']]
        ax.set_xticks(group['FY'])
        ax.set_xticklabels(x_labels, fontsize=14, weight='bold')

        x = group['FY'].astype(float)
        y = group['order_intake_amount_eur'].astype(float)

        if count_non_zero(list(y)) > 1:
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            trend_line = slope * x + intercept
            #if (trend_line < 0).any():
             #   continue
            color = 'g' if slope > 0 else 'grey'
            ax.plot(x, trend_line, color, label='Trend Line')
            ax.legend() #loc="upper left"

        for bar in bars:
            height = bar.get_height()
            ax.annotate('{:,.0f} k€'.format(height), xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=14, weight='bold')

        if (y > 750).all():
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f} M€'.format(x / 1000)))
        else:
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f} k€'.format(x)))

        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['right'].set_color('white')
        ax.spines['top'].set_color('white')

    # saving as a separate file with date infromation
    plt.tight_layout()
    #current_time = datetime.now().strftime("%d_%m_%Y")
    #plt.savefig(f'data_files/{nm}_{current_time}.png', dpi=600, bbox_inches='tight')
    plt.savefig(f'data_files/{nm}.png', dpi=300, bbox_inches='tight')
    #plt.show()

# summary graphs per BU for years in bars (column - for_bu)
plot_graphs(source, 'OVERVIEW')

#affiliates graphs per BU for years in bars
affiliates = source.company_code_n.unique().tolist()
for affiliate in affiliates:
    print(affiliate)
    affiliate_df = source[source.company_code_n == affiliate]
    plot_graphs(affiliate_df, affiliate)

#companies graphs per BU for years in bars (column - for_bu)
companies = source.customer_name.unique().tolist()
for company in companies:
    print(company)
    company_df = source[source.customer_name == company]
    temp = company_df.reset_index()
    affl = temp.company_code_n[0]
    nm = affl + '_' + company
    plot_graphs(company_df, nm)

#type of partner graphs per BU for years in bars (column - for_bu)
types = source.type.unique().tolist()
for t in types:
    print(t)
    types_df = source[source.type == t]
    plot_graphs(types_df, t)

print('Done!')