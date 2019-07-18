# Import dataframe
import pandas as pd
NAME = "Initials"
PATH = "csv/" + NAME + ".csv"
df = pd.read_csv(PATH, encoding="ISO-8859-1")

df.loc[-1] = df.columns  # adding a row
df.index = df.index + 1  # shifting index
df = df.sort_index()  # sorting by index
df.columns = ['name', 'text', 'date']  # add proper headers
df = df[~df.date.str.startswith('<')]  # remove all nondates
df['date'] = df['date'].str.replace(",", "")  # Remove all commas
df['date'] = df['date'].str.split(" ", expand=False)  # Separate by spaces
df_dates = pd.DataFrame(df.date.tolist(),
                        columns=['month', 'day', 'year', 'time', 'am_or_pm'])

# Delete non date (time) to prepare for datetime conversion
df_dates = df_dates.drop(['time', 'am_or_pm'], axis=1)
# Move year to front
cols = list(df_dates)
cols.insert(0, cols.pop(cols.index('year')))
df_dates = df_dates.ix[:, cols]
# Convert month to numerical
import calendar
reverse_calendar = dict((v, k) for k, v in enumerate(calendar.month_abbr))
df_dates['month'] = df_dates['month'].map(reverse_calendar)
# Remove all invalid entries
df_dates = df_dates.dropna()
df_dates = df_dates.astype('int64')
df_dates.dtypes
# Convert to datetime
df_dates = pd.to_datetime(df_dates)

# Delete date from df to prepare for merge
del df['date']
df = pd.concat([df, df_dates], axis=1)
df.columns = ['name', 'text', 'datetime']
df.head()

# Count messages per day (total, doesn't matter who sent it)
OUTPUT_PATH = "processed/pp_" + NAME + ".csv"
df.to_csv(OUTPUT_PATH, index=False)