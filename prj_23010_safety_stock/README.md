# Data Preparation

The goal of this project is to analyze orders data for a company's product groups over the period from FY17 to the end of FY22, in order to create a safety stock. The data is stored in two Excel files: `orders_data_fy17_fy21.xlsx` and `orders_data_fy21_fy22.xlsx`. Each file includes the following columns: `year_month, company_code_n, sales_order_so, sold_to_customer_n_latest, bu, bu_n, material, ms_code, order_intake_quantity`, and `order intake EUR`.

To protect confidential information, all sensitive data, including the original Excel files, are stored in a separate directory called data_files, which is not included in the GitHub repository.

To prepare the data for analysis, the following steps were taken:

The two Excel files were loaded into pandas dataframes `orders_fy17_fy21` and `orders_fy21_fy22` using the read_excel function.

The desired columns were selected from the dataframes using the `[['column1', 'column2', ...]]` notation, and a new dataframe `orders_data` was created by concatenating `orders_fy17_fy21` and `orders_fy21_fy22` using the concat function.

The year_month column was parsed into a datetime format using the `pd.to_datetime` function with the format string `%Y%m`. A new `FY` column was created based on whether the month was greater than or equal to April, which marked the beginning of the fiscal year.

A quarter column was created based on the month of the year_month column. Months `4, 5`, and `6` were mapped to `Q1`, months `7`, `8`, and `9` were mapped to `Q2`, months `10, 11`, and `12` were mapped to `Q3`, and months `1, 2`, and `3` were mapped to `Q4`.

A `half_year` column was created based on whether the month was between April and September (`HY1`) or October and March (`HY2`).

The `sold_to_customer_n_latest` column was renamed to `customer`, and the `order intake EUR` column was renamed to `order_intake_EUR`.

The resulting dataframe `orders_data` contained all the desired columns, and included sales data for the period from `FY17` to the end of `FY22`. This dataframe was used for subsequent analysis of the product groups and creation of a safety stock.
