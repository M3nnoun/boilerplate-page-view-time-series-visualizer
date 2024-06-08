import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from calendar import month_name

register_matplotlib_converters()

# Import data (Make sure to parse dates and set the index column to 'date')
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
top_ = df['value'].quantile(0.975)  # Top 97.5th percentile
bottom_ = df['value'].quantile(0.025)  # Bottom 2.5th percentile
filter_out = (df['value'] > bottom_) & (df['value'] < top_)
df_f = df[filter_out]

# Reset index to make 'date' a column
df_f = df_f.reset_index()

# print(df_f.head())

# # Plotting with Seaborn
# fig, ax = plt.subplots(figsize=(16, 6))  # Create figure and axis objects
# sns.lineplot(x='date', y='value', data=df_f, color='red', ax=ax)
# ax.set(xlabel='Date',ylabel='Pages Views',title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

# # plt.title('Filtered Data Line Plot')
# # plt.xlabel('Date')
# # plt.ylabel('Value')
# # plt.xticks(rotation=45)
# # plt.tight_layout()

# # Save the figure
# print(type(fig),type(ax))
# print(ax.get_title())
# fig.figure.savefig('filtered_data_plot_2.png')
# plt.show()
df_bar = df.copy().reset_index()
# months = month_name[1:]

# df_bar['Months'] = pd.Categorical(df_bar.date.dt.strftime('%B'), categories=months, ordered=False)
df_bar['Months'] = df_bar.date.dt.month_name()
df_bar['Years'] = df_bar.date.dt.year
df_bar = pd.DataFrame(df_bar.groupby(["Years", "Months"], sort=False)["value"].mean().round())
df_bar.rename(columns={
    'value':"Average Page Views"
},inplace=True)
df_bar.dropna(inplace=True)
df_bar=df_bar.reset_index()
# print(df_bar)
# fig,ax=plt.subplots(figsize=(12,8))
# ax.set_title('Daily freeCodeCamp Forum Average Page Views per Month')
# chart = sns.barplot(data=df_bar, x="Years", y="Average Page Views", hue="Months", palette="tab10")
# chart.set_xticklabels(chart.get_xticklabels(), rotation=90, horizontalalignment='center')
# fig.savefig('me_bar_plot.png')
df_bar = df.copy()
df_bar['year'] = df.index.year
df_bar['month'] = df.index.month_name()
df_bar_group = df_bar.groupby(['year', 'month'])['value'].mean()
df_bar_group = df_bar_group.unstack(level='year')

print(df_bar_group)