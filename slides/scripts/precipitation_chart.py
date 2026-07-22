import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Paired_Gauges_Table.csv', parse_dates=['Date'])
df.plot(x='Date', kind='bar', width=0.85)
plt.ylabel('Daily rainfall (mm)')
plt.title('Forest vs Pasture Gauge – Pará, 10–23 Feb')
plt.xticks(rotation=45, ha='right')
plt.legend(['Forest', 'Pasture'])
plt.tight_layout()
plt.show()
