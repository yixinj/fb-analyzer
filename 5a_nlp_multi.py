# vader sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def score(sentence):
    """
    Score a string
    """
    score = analyser.polarity_scores(sentence)
    return score['compound']


# Load the preprocessed csv
import pandas as pd
NAME = 'Initials'
PATH = "processed/pp_" + NAME + ".csv"
df = pd.read_csv(PATH, encoding="ISO-8859-1")

# Sort by date, remove nan
df = df.sort_values(by=['datetime'])
df = df.dropna()

# Process text
df.text = df.text.str.split(" ")
import re
df.text = df.text.apply(lambda row:
                        [re.sub('[^a-zA-Z]', '', val) for val in row])
df.text = df.text.apply(lambda row: [val.lower() for val in row])

r = pd.date_range(start=df.datetime.min(), end=df.datetime.max())


def process_and_plot(name, df, r, ax):
    """
    Process a dataframe
    """
    temp_df = df[df.name == name]
    temp_df = temp_df.drop(['name'], axis=1)
    # Get all words spoken on each day (thanks stackoverflow)
    temp_df = temp_df.groupby('datetime').agg({'text': 'sum'})
    # Reindex (fill in all the missing dates)
    temp_df.index = pd.DatetimeIndex(temp_df.index)
    temp_df = temp_df.reindex(r, fill_value=[])
    # So now we have each day, and all the words spoken by each person per that day

    temp_df['string'] = temp_df.text.apply(" ".join)
    temp_df['score'] = temp_df.string.apply(score)
    s = temp_df.drop(['text', 'string'], axis=1)
    ax.plot(s, label=name)

# PLOT THE GRAPH
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Set up the plot
fig, ax = plt.subplots(nrows=3)

names = df.name.unique()

for name in names[0:3]:
    # Plot
    process_and_plot(name, df, r, ax[0])
for name in names[3:6]:
    # Plot
    process_and_plot(name, df, r, ax[1])
for name in names[6:9]:
    # Plot
    process_and_plot(name, df, r, ax[2])


fig.suptitle('Sentiment over time')
ax.set_xlabel('Date')
ax.set_ylabel('Sentiment')

# Limit axis
import datetime
fig.autofmt_xdate()
ax.set_xlim([df.datetime.min(), df.datetime.max()])
ax[0].legend()
ax[1].legend()
ax[2].legend()
plt.show()