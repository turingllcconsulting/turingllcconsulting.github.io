# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(NUMERIC_ENTRY)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Clean and prepare
data = dataset.dropna(subset=['SAMPLED_DATE'])
data['SAMPLED_DATE'] = pd.to_datetime(data['SAMPLED_DATE'], errors='coerce')
data = data.dropna(subset=['SAMPLED_DATE'])

# Plant and product info
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
fig, axes = plt.subplots(4, 1, figsize=(14, 16))  # 4 stacked subplots
cp_values = []
cpk_values = []

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

    # Conformance classification
    df['Conformance'] = np.where(
        (df['NUMERIC_ENTRY'] >= lsl) & (df['NUMERIC_ENTRY'] <= usl),
        "Conforming", "Non-Conforming"
    )
    df.set_index('SAMPLED_DATE', inplace=True)

    # Weekly grouping (Sunday–Saturday)
    weekly_counts = df.groupby([pd.Grouper(freq='W-SAT'), 'Conformance']).size().unstack(fill_value=0)
    weekly_counts['Total'] = weekly_counts.sum(axis=1)
    weekly_pct = weekly_counts.div(weekly_counts['Total'], axis=0) * 100

    conforming_pct = weekly_pct.get('Conforming', pd.Series(0, index=weekly_pct.index))
    nonconforming_pct = weekly_pct.get('Non-Conforming', pd.Series(0, index=weekly_pct.index))
    x = weekly_pct.index

    # Plot stacked area
    axes[i].fill_between(x, 0, conforming_pct, label='Conforming', step='mid', alpha=0.6, color='green')
    axes[i].fill_between(x, conforming_pct, conforming_pct + nonconforming_pct, label='Non-Conforming', step='mid', alpha=0.6, color='red')

    axes[i].set_title(f"{measure} | Cp={cp:.2f}, Cpk={cpk:.2f}")
    axes[i].set_ylabel("Conformance (%)")
    axes[i].set_xlabel("Week Ending")
    axes[i].set_ylim(0, 100)
    axes[i].legend(loc='upper right')
    axes[i].grid(True)

# Main title and layout
plt.suptitle(f"{plant_name} | {date_min} - {date_max}\nProduct: {product}\nWeekly Conformance Trends", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Output Cp/Cpk
for measure, cp, cpk in zip(measures, cp_values, cpk_values):
    print(f"{measure}: Cp = {cp:.2f}, Cpk = {cpk:.2f}")