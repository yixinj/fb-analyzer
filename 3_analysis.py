# Load the preprocessed csv
import pandas as pd
NAME = 'Initials'
PATH = "processed/pp_" + NAME + ".csv"
df = pd.read_csv(PATH, encoding="ISO-8859-1")

# df2 is the value counts per day (messages per day)
df2 = df.datetime
df2.describe()
s = df2.value_counts()
s = s.sort_index()
# Range of dates
r = pd.date_range(start=s.index.min(), end=s.index.max())
s.index = pd.DatetimeIndex(s.index)
s = s.reindex(r, fill_value=0)

# PLOT THE GRAPH
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set up the plot
fig, ax = plt.subplots()
ax.plot(s)
fig.suptitle('Messages over time')
ax.set_xlabel('Date')
ax.set_ylabel('#Messages')

plt.show()