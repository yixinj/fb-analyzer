# Load the preprocessed csv
import pandas as pd
NAME = 'Initials'
PATH = "processed/pp_" + NAME + ".csv"
df = pd.read_csv(PATH, encoding="ISO-8859-1")
df = df.drop(['name', 'datetime'], axis=1)

df['text'] = df.text.str.split(" ")
df = df.text.dropna()
import re
# Remove non-alphabetic
df = df.apply(lambda row: [re.sub('[^a-zA-Z]', '', val) for val in row])
# Lowercase everything!
df = df.apply(lambda row: [val.lower() for val in row])

big_list = []
for row in df:
    big_list += row

# Word counts
from collections import Counter
word_count = Counter(big_list)

import matplotlib.pyplot as plt
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Create and generate a word cloud image:
text = " ".join(big_list)
wordcloud = WordCloud(width=1920, height=1080, background_color="white", max_words=1000).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
