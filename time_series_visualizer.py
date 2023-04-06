import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=True, index_col="date")

# Clean data
df = df[(df["value"] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]

# Used to sort months into calendar order because data starts in May
order = [8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7]

def draw_line_plot():
    plt.clf()
    # Draw line plot
    lp = sns.lineplot(data=df)
    lp.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    lp.set_xlabel("Date")
    lp.set_ylabel("Page Views")

    fig = lp.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    plt.clf()
    # Copy and modify data for monthly bar plot
    monthly_df = df.copy()


    monthly_df["year"] = monthly_df.index.year
    monthly_df["month"] = monthly_df.index.month_name()
    months = monthly_df["month"].unique()
    years = monthly_df["year"].unique()
    for year in years:
        for month in months:
            monthly_df.loc[(monthly_df["month"] == month) & (monthly_df["year"] == year), "value"] = monthly_df.loc[(monthly_df["month"] == month) & (monthly_df["year"] == year), "value"].sum()
    monthly_df = monthly_df.drop_duplicates()

    # print(monthly_df)
    # print(monthly_df.info())
    # print(monthly_df.describe())
    # return

    # Draw bar plot
    bp = sns.barplot(data=monthly_df, x="year", y="value", hue="month", hue_order=[months[i] for i in order])
    bp.set_xlabel("Years")
    bp.set_ylabel("Average Page Views")
    bp.legend(title="Months")

    fig = bp.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    plt.clf()
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    months = df_box["month"].unique()
    

    # Draw box plots (using Seaborn)
    plt.rcParams["figure.figsize"] = (15, 5)
    fig, axes = plt.subplots(1, 2)
    
    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    sns.boxplot(data=df_box, x="month", y="value", ax=axes[1], order=[months[i] for i in order])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
