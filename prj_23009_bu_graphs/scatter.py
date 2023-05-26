import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

init = pd.read_excel('data_files/data.xlsx', sheet_name='data')
temp = init.copy()


# Creating a sample dataframe

df = temp.loc[:,['customer_name','for_bu', 'order_intake_amount_eur']]

# Plotting the clusters
sns.scatterplot(x='order_intake_amount_eur', y='customer_name', hue='for_bu', data=df)

# Customizing the plot
plt.xlabel('Partners')
plt.ylabel('Order Intake Amount (Euro)')
plt.title('Clusters of Partners for BU N')

# Show the plot
plt.show()
