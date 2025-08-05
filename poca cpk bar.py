# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(NUMERIC_ENTRY)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and clean data (Power BI dataset will provide this dynamically)
data = dataset.dropna(subset=['SAMPLED_DATE'])  # Remove rows where SAMPLED_DATE is NaN

# Convert date column safely
data['SAMPLED_DATE'] = pd.to_datetime(data['SAMPLED_DATE'], errors='coerce')

# Handle missing values for date range (Avoid NaT errors)
if data['SAMPLED_DATE'].isna().all():
    date_min, date_max = "Unknown", "Unknown"
else:
    date_min = data['SAMPLED_DATE'].dropna().min().strftime('%m/%d/%y')
    date_max = data['SAMPLED_DATE'].dropna().max().strftime('%m/%d/%y')

# Define the four measures for analysis
measures = ['Protein', 'Moisture', 'Fat', 'Ash']

# Extract plant, product information
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

# Prepare figure for multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 grid for 4 measures
axes = axes.flatten()  # Flatten for easy iteration

# Loop through each measure
cpk_values = []
cp_values = []

for i, measure in enumerate(measures):
    # Retrieve user-defined specification limits for each measure
    lsl = data[f'{measure}_LSL'].dropna().iloc[0] if f'{measure}_LSL' in data.columns else -float('inf')
    usl = data[f'{measure}_USL'].dropna().iloc[0] if f'{measure}_USL' in data.columns else float('inf')

    # Extract data for the current measure
    measure_data = data[data['NAME'] == measure][['TEXT_ID', 'NUMERIC_ENTRY']].copy()

    # Calculate mean and standard deviation
    mean = measure_data['NUMERIC_ENTRY'].mean()
    std_dev = measure_data['NUMERIC_ENTRY'].std()

    # Calculate Cp and Cpk
    if std_dev > 0:
        cp = (usl - lsl) / (6 * std_dev)
        cpk = min((usl - mean) / (3 * std_dev), (mean - lsl) / (3 * std_dev))
    else:
        cp = 0
        cpk = 0

    cp_values.append(cp)
    cpk_values.append(cpk)

    # Bar chart of conformance
    total_count = len(measure_data)
    conforming_count = measure_data[
        (measure_data['NUMERIC_ENTRY'] >= lsl) & (measure_data['NUMERIC_ENTRY'] <= usl)
    ].shape[0]
    proportion_conformance = (conforming_count / total_count) * 100 if total_count > 0 else 0

    # Classify data as "Conforming" or "Non-Conforming"
    measure_data['Conformance'] = np.where(
        (measure_data['NUMERIC_ENTRY'] >= lsl) & (measure_data['NUMERIC_ENTRY'] <= usl),
        "Conforming",
        "Non-Conforming"
    )
    conformance_counts = measure_data['Conformance'].value_counts()

    axes[i].bar(conformance_counts.index, conformance_counts.values, color=['green', 'red'])
    axes[i].set_title(f"{measure} | Cp={cp:.2f}, Cpk={cpk:.2f}\nProportion Conforming: {proportion_conformance:.2f}%\nLSL={lsl}, USL={usl}")
    axes[i].set_ylabel("Count")
    axes[i].set_xlabel("Conformance Category")
    axes[i].grid(axis='y')

# Adjust layout for readability
plt.suptitle(f"{plant_name} | {date_min} - {date_max}\nProduct: {product}\nCp and Cpk Analysis")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Display the plot
plt.show()

# Display overall Cp and Cpk values
for measure, cp, cpk in zip(measures, cp_values, cpk_values):
    print(f"{measure}: Cp = {cp:.2f}, Cpk = {cpk:.2f}")