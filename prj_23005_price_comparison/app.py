"""
Code allows to take Excel file with multiply sheets with different versions of pricing
and compare prices for the same product models.

file should contain the following columns:
      ['Model Number', 'Family', 'Product Hierarchy', 'Description',
       'Characteristic', 'Description Characteristic', 'Value',
       'Description Value', 'Variant', 'RSP-EUR', 'LLP-EUR']
All of them or at least:
       ['Model Number', 'Characteristic', 'RSP-EUR' or 'LLP-EUR']
"""
import pandas as pd

# read in the Excel file
xlsx = pd.ExcelFile('data_files/llp.xlsx')

# dictionary to store the dataframes from all excel sheets
dfs = {}

for sheet_name in xlsx.sheet_names:
    dfs[sheet_name] = xlsx.parse(sheet_name)

data_frames = dfs.copy()  # for saving initial data frames

"""
Some of sheets contains 'RSP-EUR' or 'LLP-EUR' or both.  
Depending on this fact it is necessary to prepare dataframes with necessary columns only. 
"Model name", "Characteristic" and "Price" which can be 'RSP-EUR' or 'LLP-EUR' or both. 
To exclude lines with options for product models, it is necessary to exclude line where 
"Characteristic" not empty. 
All prepared dataframes are added to a list which will be used for dataframes merging. 
""" ""
rsp = 'RSP-EUR'
llp = 'LLP-EUR'
l_for_merging = []
for key in dfs.keys():
    # keys - names of sheets in excel and they have explicit name with time line identification
    # they are used for naming columns with price
    if rsp in dfs[key].columns and llp in dfs[key].columns:
        dfs[key] = dfs[key].loc[:, ['Model Number', 'Characteristic', 'RSP-EUR', 'LLP-EUR']]
        dfs[key] = dfs[key][dfs[key]['Characteristic'].isna()]
        dfs[key] = dfs[key].loc[:, ['Model Number', 'RSP-EUR', 'LLP-EUR']]
        dfs[key] = dfs[key].rename(columns={'RSP-EUR': key + '_' + 'RSP-EUR', 'LLP-EUR': key + '_' + 'LLP-EUR'})
        l_for_merging.append(dfs[key])
    elif rsp in dfs[key].columns:
        dfs[key] = dfs[key].loc[:, ['Model Number', 'Characteristic', 'RSP-EUR']]
        dfs[key] = dfs[key][dfs[key]['Characteristic'].isna()]
        dfs[key] = dfs[key].loc[:, ['Model Number', 'RSP-EUR']]
        dfs[key] = dfs[key].rename(columns={'RSP-EUR': key + '_' + 'RSP-EUR'})
        l_for_merging.append(dfs[key])
    elif llp in dfs[key].columns:
        dfs[key] = dfs[key].loc[:, ['Model Number', 'Characteristic', 'LLP-EUR']]
        dfs[key] = dfs[key][dfs[key]['Characteristic'].isna()]
        dfs[key] = dfs[key].loc[:, ['Model Number', 'LLP-EUR']]
        dfs[key] = dfs[key].rename(columns={'LLP-EUR': key + '_' + 'LLP-EUR'})
        l_for_merging.append(dfs[key])

# determination of the dataframe with the biggest quantity of product models
max_l = 0
for i, df in enumerate(l_for_merging):
    if len(l_for_merging) >= max_l:
        max_l = len(l_for_merging)
        max_df = df
        max_i = i
# creation a dataframe with only one column "Model Number" for left-merging for keeping all models
model_df = l_for_merging[max_i].loc[:, ['Model Number']]
# l_for_merging = [l_for_merging, *f]

# creation of final dataframe with all prices columns for all products models
final_df = model_df.copy()
for df in l_for_merging:
    final_df = final_df.merge(df, how='left', left_on='Model Number', right_on='Model Number')

# it is necessary to understand price different in % for 22 and 23 years for LLP and RSP prices
final_df['difference LLP'] = round((final_df['LLP23_LLP-EUR'] / final_df['LLP22_LLP-EUR'] * 100 - 100), 0)
final_df['difference RSP'] = round((final_df['LLP23_RSP-EUR'] / final_df['RSP22_RSP-EUR'] * 100 - 100), 0)
# if price difference not 15% as it was announced, it is necessary to check later in Excel
final_df.loc[final_df['difference LLP'] != 15, 'difference LLP'] = 'check'
final_df.loc[final_df['difference RSP'] != 15, 'difference RSP'] = 'check'

# saving results in Excel file for further use
writer = pd.ExcelWriter('data_files/price_summary.xlsx', engine='xlsxwriter')
final_df.to_excel(writer, sheet_name='summary')
writer.save()
print('You file is ready')