# Import the necessary libraries
import pandas as pd

# Read in the search results
results = pd.read_csv('search_results.txt', delimiter='\t')

# Filter the results to ensure that the listed vehicles are available for purchase and are not priced over MSRP
filtered_results = results[(results['Availability'] == 'In Stock') & (results['Price'] <= results['MSRP'])]

# Save the filtered results to a new file
filtered_results.to_csv('filtered_results.txt', sep='\t', index=False)
