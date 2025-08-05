# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(NUMERIC_ENTRY)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
from scipy.stats import spearmanr, pearsonr

# Load and clean data from Power BI
data = dataset.dropna()

# Retrieve the selected categories from the measures
x_category = data['SelectedX'].iloc[0]
y_category = data['SelectedY'].iloc[0]

# Ensure selected categories are valid
if x_category == "None" or y_category == "None":
    raise ValueError("Please select categories for both X and Y axes.")

# Extract date range, plant, and product information
date_min = pd.to_datetime(data['SAMPLED_DATE']).min().strftime('%m/%d/%y')  
date_max = pd.to_datetime(data['SAMPLED_DATE']).max().strftime('%m/%d/%y')  

plant_name = (
    "Multiple Plants" if 'CUSTOMER_NAME' in data.columns and data['CUSTOMER_NAME'].nunique() > 1
    else data['CUSTOMER_NAME'].iloc[0] if 'CUSTOMER_NAME' in data.columns
    else "Unknown Plant"
)

product = (
    "Multiple Products" if 'PRODUCT' in data.columns and data['PRODUCT'].nunique() > 1
    else data['PRODUCT'].iloc[0] if 'PRODUCT' in data.columns
    else "Unknown Product"
)

# Retrieve user-defined filters
x_min = round(data['X_Min'].iloc[0], 1) if 'X_Min' in data.columns else -float('inf')
x_max = round(data['X_Max'].iloc[0], 1) if 'X_Max' in data.columns else float('inf')
y_min = round(data['Y_Min'].iloc[0], 1) if 'Y_Min' in data.columns else -float('inf')
y_max = round(data['Y_Max'].iloc[0], 1) if 'Y_Max' in data.columns else float('inf')

# Filter data for the selected categories
x_data = data[data['NAME'] == x_category][['TEXT_ID', 'NUMERIC_ENTRY']]
y_data = data[data['NAME'] == y_category][['TEXT_ID', 'NUMERIC_ENTRY']]

# Merge X and Y data on TEXT_ID
merged_data = pd.merge(x_data, y_data, on='TEXT_ID', suffixes=('_X', '_Y'))

# Apply user-defined filters
merged_data = merged_data[
    (merged_data['NUMERIC_ENTRY_X'] >= x_min) & (merged_data['NUMERIC_ENTRY_X'] <= x_max) &
    (merged_data['NUMERIC_ENTRY_Y'] >= y_min) & (merged_data['NUMERIC_ENTRY_Y'] <= y_max)
]

if merged_data.empty:
    raise ValueError("No matching data for the selected categories after filtering.")

# Extract aligned X and Y data
x_values = merged_data['NUMERIC_ENTRY_X'].values.reshape(-1, 1)
y_values = merged_data['NUMERIC_ENTRY_Y'].values

# Fit a linear regression model
reg = LinearRegression()
reg.fit(x_values, y_values)
y_pred = reg.predict(x_values)

# Calculate statistics
r2 = r2_score(y_values, y_pred)
slope = reg.coef_[0] 
intercept = reg.intercept_
variance_x = np.var(x_values)    
variance_y = np.var(y_values)    
pearson_corr, _ = pearsonr(x_values.flatten(), y_values)  # Pearson Correlation
spearman_corr, _ = spearmanr(x_values.flatten(), y_values)  # Spearman Correlation
mean_x = np.mean(x_values)      
mean_y = np.mean(y_values)      
std_x = np.std(x_values)        
std_y = np.std(y_values)        
num_points = len(x_values)      

# Confidence Interval
confidence = 1.96 * np.std(y_pred - y_values) / np.sqrt(len(x_values))
upper_bound = y_pred + confidence
lower_bound = y_pred - confidence

# Generate the plot
plt.figure(figsize=(12, 8))

# Scatter plot with color coding for points above and below the regression line
above_line = y_values > y_pred
below_line = ~above_line

plt.scatter(x_values[above_line], y_values[above_line], color='blue', label="Above Line")
plt.scatter(x_values[below_line], y_values[below_line], color='green', label="Below Line")

# Plot the regression line
plt.plot(x_values, y_pred, color='red', label=f"Regression Line\nR² = {r2:.3f}\nSlope = {slope:.3f}\nIntercept = {intercept:.3f}")

# Confidence interval
plt.fill_between(x_values.flatten(), lower_bound, upper_bound, color='gray', alpha=0.3, label="95% Confidence Interval")

# Customize the plot
plt.title(
    f"{plant_name} | {date_min} - {date_max}\n"
    f"Product: {product}\n"
    f"Regression Plot: {x_category} vs {y_category}\n"
    f"Filters: X [{x_min}, {x_max}], Y [{y_min}, {y_max}]\n"
    f"Pearson Corr = {pearson_corr:.3f}, Spearman Corr = {spearman_corr:.3f}",
    y=1.0
)
plt.xlabel(f"{x_category} (X-axis)")
plt.ylabel(f"{y_category} (Y-axis)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Display the plot
plt.show()