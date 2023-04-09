# Project 23010 Safety Stock Assessment

## Data Preparation

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

The `check_unique_values` function is used to optimise the memory usage and performance of the `orders_data_opt` DataFrame.
By converting columns with less than 50 unique values to the categorical data type, the memory usage of the DataFrame is reduced without sacrificing any important information.

Then I deleted rows where `ms_code` contains text with `BOP`, it is not products but some service lines

## XYZ analysis

The purpose of this code block is to summarise the `orders_data_opt` DataFrame by different time periods and to categorise products based on their standard deviation of `order_intake_quantity`. The resulting pivot tables are written to an Excel file for further analysis.

## ABC analysis for BU + XYZ analysis results

The purpose of this code block is to perform an ABC + XYZ analysis for each `bu` value in the `orders_data_opt` DataFrame. The results of the analysis, including the total `order_intake_EUR`, `share`, `cumulative sum` and `percentage`, and `ABC group`, are written to an Excel file for each `bu` value. Additionally, the new DataFrame is merged with the `pivot_table_month`, `pivot_table_half_quarter`, and `pivot_table_half_year` DataFrames to add columns for `mean`, `standard deviation`, and `category` XYZ for different periods of time - month, quarter and half year. 
