# Sales and GP Trend Analysis for Indirect Sales (Completed Project)

This project focuses on analyzing and visualizing Sales and Gross Profit (GP) trends for indirect sales over a period of five financial years. The analysis was conducted using Python and the source data was provided in xlsx format.

## Overview

The objective of this project was to:

1. Create a unified report of GP and Sales data
2. Enrich the report with company types (direct or indirect sales)
3. Calculate annual GP and Sales figures, separating them by company type (direct or indirect)
4. Plot the trendlines for indirect sales based on the calculated data

## Data Sources

Three separate xlsx files were used as data sources for this project:

1. GP and Sales report for the entire period, excluding the last month
2. GP and Sales report for the last month
3. A table of definitions containing information about company types (direct or indirect sales)

## Methodology

The following steps were taken to complete the project:

1. Data preprocessing: The two GP and Sales reports were merged into a single report, and the table of definitions was joined with the report to identify company types.
2. Data filtering: Only indirect sales data was retained for further analysis.
3. Annual calculations: The annual GP and Sales figures for indirect sales were calculated for each of the five financial years.
4. Visualization: A plot with trendlines was created to illustrate the trends in Sales and GP for indirect sales over the five-year period.

## Technologies and Libraries

This project was implemented using Python, with the following libraries utilized:

- pandas: Data manipulation and analysis
- openpyxl: Reading and writing Excel xlsx files
- matplotlib: Data visualization

The completed project can be found in this repository, including the Jupyter Notebook containing the Python code, the input xlsx files, and the output visualizations. To protect confidential information, all sensitive data, including the original Excel files, are stored in a separate directory called data_files, which is not included in the GitHub repository.
