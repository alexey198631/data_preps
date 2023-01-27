import pandas as pd
import jellyfish

# Read the Excel file
df = pd.read_excel("data_files/the_first_iteration.xlsx")

# Extract the column of company names
company_names = df["test"].tolist()
final_result = pd.DataFrame()

# Set a threshold for similarity score
threshold = 0.90
border = len(company_names)
counter = 0

# Compare each pair of company names
for i in range(border):
    for j in range(i+1, border):
        # Calculate Jaro-Winkler distance
        distance = jellyfish.jaro_winkler(company_names[i], company_names[j])

        # Check if the distance is greater than the threshold
        if threshold < distance < 1:
            final_result.loc[counter, ['company']] = company_names[i]
            final_result.loc[counter, ['similar']] = company_names[j]
            final_result.loc[counter, ['distance']] = round(distance, 2)
            counter += 1
            print(counter, i, j, company_names[i], company_names[j], round(distance, 2))

final_result = final_result.sort_values(by=['distance'], ascending=False)

writer = pd.ExcelWriter('data_files/similar.xlsx', engine='xlsxwriter')
final_result.to_excel(writer, sheet_name='similarity_check')
writer.save()