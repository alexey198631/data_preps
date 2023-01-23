import pandas as pd
import jellyfish

# Read the Excel file
df = pd.read_excel("data_files/initial_companies.xlsx")

# Extract the column of company names
company_names = df["Customer Name"].tolist()
final_result = pd.DataFrame()

# Set a threshold for similarity score
threshold = 0.9

# Compare each pair of company names
for i in range(len(company_names)):
    for j in range(i+1, len(company_names)):
        # Calculate Jaro-Winkler distance
        distance = jellyfish.jaro_winkler(company_names[i], company_names[j])

        # Check if the distance is greater than the threshold
        if distance > threshold:
            final_result.loc[i, ['company']] = company_names[i]
            final_result.loc[i, ['similar']] = company_names[j]
            final_result.loc[i, ['distance']] = round(distance, 2)

final_result = final_result.sort_values(by=['distance'], ascending=False)

writer = pd.ExcelWriter('data_files/similar.xlsx', engine='xlsxwriter')
final_result.to_excel(writer, sheet_name='good')
writer.save()