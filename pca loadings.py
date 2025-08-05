# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(NUMERIC_ENTRY)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load and clean data from Power BI
data = dataset.dropna(subset=['TEXT_ID', 'NAME', 'NUMERIC_ENTRY'])

# Pivot the data
pivoted_data = data.pivot_table(index='TEXT_ID', columns='NAME', values='NUMERIC_ENTRY', aggfunc='mean')
pivoted_data = pivoted_data.fillna(0)  # Replace NaN with 0

# Check if pivoted data is empty
if pivoted_data.empty:
    raise ValueError("No data available after pivoting and cleaning. Check the input dataset.")

# Standardize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(pivoted_data)

# Perform PCA
pca = PCA(n_components=2)  # Use 2 components for visualization
pca.fit(data_scaled)

# Extract PCA loadings
loadings = pca.components_.T
test_names = pivoted_data.columns

# Set color and style
text_color = "#78082A"
bg_color = "#F3EDE0"
gridline_color = "#E0D1B1"

# Create PCA Loadings Plot
plt.figure(figsize=(10, 8), facecolor=bg_color)

# Plot points
plt.scatter(loadings[:, 0], loadings[:, 1], color=text_color, edgecolor="black", zorder=2)

# Static label adjustment to avoid overlap
for i, test in enumerate(test_names):
    x, y = loadings[i, 0], loadings[i, 1]
    
    # Adjust the position statically based on the index
    x_offset = 0.02 if i % 2 == 0 else -0.02  # Alternate x offsets
    y_offset = 0.05 + (i % 3) * 0.02  # Slightly stagger y offsets

    plt.text(
        x + x_offset, 
        y + y_offset, 
        f"{test}\n({x:.2f}, {y:.2f})", 
        fontsize=10, 
        color=text_color, 
        ha="center", 
        va="center", 
        bbox=dict(facecolor=bg_color, edgecolor='none', boxstyle='round,pad=0.3')  # Text background
    )

# Customize the plot
plt.xlabel("Principal Component 1", fontsize=12, color=text_color)
plt.ylabel("Principal Component 2", fontsize=12, color=text_color)
plt.axhline(0, color=text_color, linestyle='--', linewidth=0.5, zorder=1)
plt.axvline(0, color=text_color, linestyle='--', linewidth=0.5, zorder=1)
plt.title("PCA Loadings Visualization (Tests)", fontsize=14, color=text_color)

# Add gridlines
plt.grid(color=gridline_color, linestyle='--', linewidth=0.5)

# Update background color
plt.gca().set_facecolor(bg_color)

# Show the plot
plt.show()