import numpy as np

# Data for each month representing some measured values
# These could be temperature, precipitation, etc.
data = {
    "Apr": 1.8,
    "May": 11.6,
    "Jun": 19.7,
    "Jul": 19.3,
    "Aug": 21.3,
    "Sep": 8.7,
    "Oct": 4.6,
}

# Correction factors for each month
# These might be used to adjust the data for some known bias or error
correction = {
    "Apr": 1.15,
    "May": 1.33,
    "Jun": 1.33,
    "Jul": 1.37,
    "Aug": 1.25,
    "Sep": 1.06,
    "Oct": 0.92,
}

# Calculating the mean heat index (I)
# This is a sum of transformed data values, which might represent some kind of energy or heat index
I = np.sum(np.asarray([(val / 5) ** (3/2) for val in data.values()]))

# Step 2: Calculate the coefficient 'a'
# This is a polynomial function of the heat index 'I'
# The coefficients are likely derived from empirical data or a theoretical model
a = 0.492 + 0.0119 * I - 0.0000771 * I**2 + 0.000000675 * I**3

# Print the calculated values of 'a' and 'I'
print(f"Values for a, and I are respectively: {a:.2f}, and {I:.2f}")

# Function to calculate potential evaporation (E_pt)
# T_a is the average temperature for the month
# Correction is a factor to adjust the calculation
# The formula is based on the heat index 'I' and coefficient 'a'


def E_pt(T_a, correction=1.0):
    return correction * 1.62 * (10 * T_a / I) ** a


# Loop through each month and calculate both corrected and uncorrected evaporation
# Print the results for each month
for month in data.keys():
    print(f"{month}: corrected = {E_pt(T_a=data.get(month, 0.0), correction=correction.get(month, 1.0)):.3f}, uncorrected = {E_pt(T_a=data.get(month, 0.0), correction=1.0):.3f}")
