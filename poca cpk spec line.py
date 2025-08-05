# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(NUMERIC_ENTRY)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Clean and prep data
data = dataset.dropna(subset=['SAMPLED_DATE'])
data['SAMPLED_DATE'] = pd.to_datetime(data['SAMPLED_DATE'], errors='coerce')
data = data.dropna(subset=['SAMPLED_DATE'])

# Extract plant and product info
plant_name = (
    "Multiple Plants" if 'CUSTOMER_NAME' in data.columns and data['CUSTOMER_NAME'].nunique() > 1
    else data['CUSTOMER_NAME'].iloc[0] if 'CUSTOMER_NAME' in data.columns and not data['CUSTOMER_NAME'].isna().all()
    else "Unknown Plant"
)

product = (
    "Multiple Products" if 'PRODUCT' in data.columns and data['PRODUCT'].nunique() > 1
    else data['PRODUCT'].iloc[0] if 'PRODUCT' in data.columns and not data['PRODUCT'].isna().all()
    else "Unknown Product"
)

date_min = data['SAMPLED_DATE'].min().strftime('%m/%d/%y')
date_max = data['SAMPLED_DATE'].max().strftime('%m/%d/%y')

# Setup
measures = ['Protein', 'Moisture', 'Fat', 'Ash']
fig, axes = plt.subplots(4, 1, figsize=(14, 16))
cp_values = []
cpk_values = []

# Custom colors
line_color = '#C8102E'
spec_fill_color = '#F3EDE0'

for i, measure in enumerate(measures):
    lsl = data[f'{measure}_LSL'].dropna().iloc[0] if f'{measure}_LSL' in data.columns else -np.inf
    usl = data[f'{measure}_USL'].dropna().iloc[0] if f'{measure}_USL' in data.columns else np.inf

    df = data[data['NAME'] == measure].copy()
    df = df[['SAMPLED_DATE', 'NUMERIC_ENTRY']].dropna()

    if df.empty:
        axes[i].set_title(f"{measure} | No data available")
        continue

    # Cp/Cpk
    mean = df['NUMERIC_ENTRY'].mean()
    std_dev = df['NUMERIC_ENTRY'].std()
    cp = (usl - lsl) / (6 * std_dev) if std_dev > 0 else 0
    cpk = min((usl - mean), (mean - lsl)) / (3 * std_dev) if std_dev > 0 else 0
    cp_values.append(cp)
    cpk_values.append(cpk)

    # Resample
    df.set_index('SAMPLED_DATE', inplace=True)
    weekly_means = df['NUMERIC_ENTRY'].resample('W-SAT').mean()

    x = weekly_means.index
    y = weekly_means.values

    # Plot
    axes[i].fill_between(x, lsl, usl, color=spec_fill_color, alpha=1.0, label='Spec Range')
    axes[i].plot(x, y, label='Weekly Mean', color=line_color, marker='o')

    axes[i].set_title(f"{measure} | Cp={cp:.2f}, Cpk={cpk:.2f}")
    axes[i].set_ylabel(f"{measure} Value")
    axes[i].set_xlabel("Week Ending")
    axes[i].grid(True)
    axes[i].legend(loc='upper right')

# Overall layout
plt.suptitle(f"{plant_name} | {date_min} - {date_max}\nProduct: {product}\nWeekly Mean Values with Spec Limits", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Cp and Cpk output
for measure, cp, cpk in zip(measures, cp_values, cpk_values):
    print(f"{measure}: Cp = {cp:.2f}, Cpk = {cpk:.2f}")