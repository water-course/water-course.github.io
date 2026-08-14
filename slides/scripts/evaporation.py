"""Thornthwaite potential evapotranspiration, Saskatoon 1961.
Worked solution for the evaporation tutorial; coefficients follow
Thornthwaite (1948) and match the lecture slides."""

# Mean monthly air temperature (deg C); months above 0 deg C only.
temperature = {"Apr": 1.8, "May": 11.6, "Jun": 19.7, "Jul": 19.3,
               "Aug": 21.3, "Sep": 8.7, "Oct": 4.6}

# Day-length factors for ~50 deg N (nearest latitude to Saskatoon).
correction = {"Apr": 1.15, "May": 1.33, "Jun": 1.33, "Jul": 1.37,
              "Aug": 1.25, "Sep": 1.06, "Oct": 0.92}

# Step 1 - annual heat index I = sum of (T / 5) ** 1.514.
I = sum((t / 5) ** 1.514 for t in temperature.values())

# Step 2 - exponent a, a cubic in I (Thornthwaite 1948).
a = 6.75e-7 * I**3 - 7.71e-5 * I**2 + 1.792e-2 * I + 0.49239
print(f"Annual heat index I = {I:.2f},  exponent a = {a:.3f}\n")


def E_pt(T_a, factor=1.0):
    """Monthly potential evapotranspiration (cm); 1.6 cm = 16 mm."""
    return factor * 1.6 * (10 * T_a / I) ** a


# Steps 3-4 - raw and day-length-corrected monthly E_pt.
corrected = {}
for m, t in temperature.items():
    corrected[m] = E_pt(t, correction[m])
    print(f"{m}: raw {E_pt(t):.2f}, corrected {corrected[m]:.2f} cm")

# Step 5 - season total, 16 May to 24 Sep. May and September are only
# partly inside the window, so weight them by the month fraction.
fraction = {"May": 16/31, "Jun": 1, "Jul": 1, "Aug": 1, "Sep": 24/30}
total = sum(corrected[m] * f for m, f in fraction.items())
print(f"\nSeason total = {total:.1f} cm ({total*10:.0f} mm)")
