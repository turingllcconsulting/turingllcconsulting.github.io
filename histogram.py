# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(NUMERIC_ENTRY)
# dataset = dataset.drop_duplicates()

# Paste or type your script code here:

# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Isolating result column
result_data = dataset["NUMERIC_ENTRY"]

# Descriptive Statistics
mean_result = result_data.mean()
median_result = result_data.median()
std_dev_result = result_data.std()
max_result = result_data.max()
min_result = result_data.min()
variance_result = result_data.var()
std_error_result = std_dev_result / np.sqrt(len(result_data))
count_result = result_data.count()

# Plotting Histogram and stats
plt.figure(figsize=(10, 6), facecolor='#F3EDE0')
plt.gca().set_facecolor('#F3EDE0')
plt.hist(result_data, bins=20, alpha=0.7, color='#FED141', edgecolor='#78082A', density=True)
plt.axvline(mean_result, color='black', linestyle='-', label=f"Mean: {mean_result:.2f}")
plt.axvline(median_result, color='#8B5B29', linestyle=':', label=f"Median: {median_result:.2f}")
plt.axvline(mean_result + std_dev_result, color='#78082A', linestyle=':', label=f"+1 SD: {mean_result + std_dev_result:.2f}")
plt.axvline(mean_result - std_dev_result, color='#78082A', linestyle=':', label=f"-1 SD: {mean_result - std_dev_result:.2f}")

# Customer Colors (Tyson Brand Guide)
ax = plt.gca()
ax.tick_params(axis='x', colors='#78082A')
ax.tick_params(axis='y', colors='#78082A')
for spine in ax.spines.values():
    spine.set_edgecolor('#78082A')

# Adding descriptive stats to the legend
plt.plot([], [], ' ', label=f"SD: {std_dev_result:.2f}")
plt.plot([], [], ' ', label=f"Max: {max_result:.2f}")
plt.plot([], [], ' ', label=f"Min: {min_result:.2f}")
plt.plot([], [], ' ', label=f"Var: {variance_result:.2f}")
plt.plot([], [], ' ', label=f"Std. Err.: {std_error_result:.2f}")
plt.plot([], [], ' ', label=f"Count: {count_result:}")

# Histogram labels
plt.title("Histogram", color='#78082A')
plt.xlabel("Result", color='#78082A')
plt.ylabel("Density", color='#78082A')
plt.legend(edgecolor='#78082A', facecolor='#F3EDE0')
plt.grid(alpha=0.3, color='#E0D1B1')
plt.tight_layout()
plt.show()