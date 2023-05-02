### MyPython

## Data preparation projects

Here you can find different apps for data preparation with Pandas.

1. **prj_23001_dashborad_prep**: file as customer definition table for Tableau dashboard;

2. **prj_23002_links_for_companies**: list of web links for companies from my list;

3. **prj_23003_clean_customer_list**:clean legal forms from long list of customers;

4. **prj_23004_check_indirect_customers**: check types of customers in long customer list for identifying those which has different types;

5. **prj_23005_values_comparison**: finding the difference between different column with values;

6. **prj_23006_contact_list**: create file with contacts for different countries based on initial contact information;

7. **prj_23007_company_type_ident**: using open information from company db to understand a customer type - service provider / manufacturer / etc;

8. **prj_23008_new_layout**: it creates new excel table from existing one with better layout for pivoting;

9. **prjj_23009_bu_graphs**

10. **prj_23010_safety_stock**

11. **prj_23011_sales_and_GP_trend_analysis_for_Indirect_Sales**

12. **prj_23012_order_intake_file_update**

13. [**prj_23013_attendee_report**](https://github.com/alexey198631/data_preps/tree/main/prj_23013_attendee_report)

This Python application is designed to extract data from a CSV file and create separate pandas DataFrames 
for specific rows that contain key words such as 'Host Details', 'Panelist Details', and 'Attendee Details'. 
The program reads the CSV file row by row and detects the target rows containing the key words using a flag variable. 
When a target row is found, the program creates a new DataFrame and appends the subsequent rows to it until the next 
target row is found. Once all the target rows have been processed, the program returns a list of 
DataFrames containing the data from the CSV file that corresponds to each of the target rows. This application 
can be useful for data processing and analysis tasks that require separate DataFrames for different types of data, 
such as attendance reports or meeting logs.
