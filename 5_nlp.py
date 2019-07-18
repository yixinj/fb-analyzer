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

# Split into person 1 and person 2
p1 = "Person 1"
p2 = "Person 2"
df1 = df[df.name == p1]
df2 = df[df.name == p2]

r = pd.date_range(start=df.datetime.min(), end=df.datetime.max())


def process(df, r):
    """
    Process a dataframe
    """
    df = df.drop(['name'], axis=1)
    # Get all words spoken on each day (thanks stackoverflow)
    df = df.groupby('datetime').agg({'text': 'sum'})
    # Reindex (fill in all the missing dates)
    df.index = pd.DatetimeIndex(df.index)
    df = df.reindex(r, fill_value=[])
    # So now we have each day, and all the words spoken by each person per that day

    df['string'] = df.text.apply(" ".join)
    return df


df1 = process(df1, r)
df2 = process(df2, r)

# vader sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def score(sentence):
    """
    Score a string
    """
    score = analyser.polarity_scores(sentence)
    return score['compound']


# Score the different people
df1['score'] = df1.string.apply(score)
df2['score'] = df2.string.apply(score)

# Transform to series
s1 = df1.drop(['text', 'string'], axis=1)
s2 = df2.drop(['text', 'string'], axis=1)

# PLOT THE GRAPH
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set up the plot
fig, ax = plt.subplots()
ax.plot(s1, '-b', label="Person 1")
ax.plot(s2, '-g', label="Person 2")
fig.suptitle('Sentiment over time')
ax.set_xlabel('Date')
ax.set_ylabel('Sentiment')

# Limit axis
import datetime
fig.autofmt_xdate()
ax.set_xlim([datetime.date(2018, 12, 10), datetime.date(2019, 5, 28)])
ax.legend()
plt.show()