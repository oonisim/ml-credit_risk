"""Exploratory Data Analysis
DO NOT mutate the data to explore. Transformation and exploration are separate concerns.
"""
from typing import (
    List,
    Sequence,
    Tuple,
)
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import plotly.offline as py
import plotly.tools as tls
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt


def add_generation_category(
        df: pd.DataFrame,
        bins: Sequence[int] = (18, 25, 35, 60, 100),
        labels: Sequence[str] = ("Student", "Young", "Adult", "Senior"),
) -> pd.DataFrame:
    """
    Discretize numerical ages into categorical age groups.
    Args:
        df (pd.DataFrame): Input DataFrame containing an 'Age' column.
        bins (Sequence[int]): Boundaries of age intervals (default: (18, 25, 35, 60, 100)).
        labels (Sequence[str]): Labels for the intervals (default: "Student", "Young", "Adult", "Senior").

    Returns:
        pd.DataFrame: A copy of the DataFrame with an additional 'Generation' categorical column.
    """
    df_copy = df.copy()
    df_copy["Generation"] = pd.cut(df_copy["Age"], bins=bins, labels=labels)
    return df_copy


def add_credit_amount_category(
        df,
        bins=(0, 5000, 10000, 15000, 20000, float("inf")),
        labels=("<5K", "5-10K", "10-15K", "15-20K", "20K+")
) -> pd.DataFrame:
    """
    Discretize numerical ages into categorical age groups.
    Args:
        df (pd.DataFrame): Input DataFrame containing a 'Credit amount' column.
        bins (Sequence[int]): Boundaries of credit amount intervals (default: (0, 5000, 10000, 15000, 20000, inf)).
        labels (Sequence[str]): Labels for the intervals (default: ("<5K", "5-10K", "10-15K", "15-20K", "20K+")).

    Returns:
        pd.DataFrame: Transformed DataFrame with new 'Amount' categorical column added.
    """
    df_copy= df.copy()
    df_copy["Amount"] = pd.cut(df_copy["Credit amount"], bins=bins, labels=labels)
    return df_copy


def run_eda_enrich_pipeline(
        df: pd.DataFrame,
        categorical_cols: List[str],
        numeric_cols: List[str]
) -> Tuple[pd.DataFrame, List[str], List[str]]:
    """Apply feature engineering transformations on the input DataFrame.
    Steps:
        1. Bin 'Age' into categorical 'Generation' groups.
        2. Bin 'Credit amount' into categorical intervals.

    Args:
        df (pd.DataFrame): Input DataFrame with columns 'Age' and 'Credit amount'.
        categorical_cols: categorical column names in df
        numeric_cols: numeric column names in df

    Returns: Tuple(
        A copy of the DataFrame with an additional 'Amount' and 'Generation' categorical columns,
        List of categorical columns,
        List of numerical columns
    )
    """
    age_transformer = FunctionTransformer(add_generation_category, validate=False)
    credit_amount_transformer = FunctionTransformer(add_credit_amount_category, validate=False)

    transformation_pipeline = Pipeline([
        ("age_binning", age_transformer),
        ("credit_binning", credit_amount_transformer),
    ])
    categorical_cols += ["Generation", "Amount"]
    numeric_cols.remove('Age')
    numeric_cols.remove('Credit amount')

    return transformation_pipeline.fit_transform(df), categorical_cols, numeric_cols


def analyse_target_distribution(df: pd.DataFrame):
    """
    Visualize the distribution of the target variable 'Risk' as a grouped bar chart.

    This function separates the target values into 'Good credit' (Risk=False)
    and 'Bad credit' (Risk=True), counts their occurrences, and plots them using Plotly.

    Args:
        df (pd.DataFrame): Input DataFrame containing a boolean or 0/1 'Risk' column.

    Returns:
        None. Displays an interactive Plotly bar chart showing the target distribution.
    """
    good = go.Bar(
        x=df[~df["Risk"].astype(bool)]["Risk"].value_counts().index.values,
        y=df[~df["Risk"].astype(bool)]["Risk"].value_counts().values,
        name='Good credit'
    )

    bad = go.Bar(
        x=df[df["Risk"].astype(bool)]["Risk"].value_counts().index.values,
        y=df[df["Risk"].astype(bool)]["Risk"].value_counts().values,
        name='Bad credit'
    )

    data = [good, bad]
    layout = go.Layout(
        yaxis={"title": 'Count'},
        xaxis={"title": 'Risk Variable'},
        title='Target label distribution'
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='grouped-bar')


def analyse_per_generation(df: pd.DataFrame):
    """Analyze generation category to credit amount correlation.
    Args:
        df: data to explore
    """
    # Age bins
    interval = (18, 25, 35, 60, 100)
    cats = ['Student', 'Young', 'Adult', 'Senior']
    df["Generation"] = pd.cut(df.Age, interval, labels=cats)

    df_good = df[~df["Risk"].astype(bool)]
    df_bad = df[df["Risk"].astype(bool)]

    good = go.Box(
        y=df_good["Credit amount"],
        x=df_good["Generation"],
        name='Good credit',
        marker={'color': '#3D9970'}
    )

    bad = go.Box(
        y=df_bad['Credit amount'],
        x=df_bad['Generation'],
        name='Bad credit',
        marker={'color': '#FF4136'}
    )

    data = [good, bad]
    layout = go.Layout(
        title='Age Categorical',
        yaxis={
            "title": "Credit Amount (US Dollar)",
            "zeroline": False
        },
        xaxis={
            "title": "Age category"
        },
        boxmode='group',
        annotations=[{
            "x": 0.5,
            "y": 1.2,
            "xref": 'paper',
            "yref": 'paper',
            "showarrow": False,
            "text": "Senior(60 - 100), Adult(35 - 60), Young(25 - 35), Student(18 - 25)",
            "font": {"size": 14}
        }]
    )
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='box-age-cat')


def risk_per_generation(df: pd.DataFrame):
    """
    Plot the mean risk for each generation.

    Args:
        df (pd.DataFrame): DataFrame containing at least the columns:
            - 'Generation': categorical generation label
            - 'Risk': binary or numeric risk indicator (0/1 or proportion)

    Returns:
        None: Displays a bar plot showing the mean risk per generation.
    """
    plt.figure(figsize=(4,3))
    sns.barplot(
        x='Generation',
        y='Risk',
        data=df,
        ci=None,
        palette=sns.color_palette("Reds_r")
    )
    plt.ylabel('Mean Risk (proportion of bad)')
    plt.title('Mean Risk by Generation')
    plt.show()


def risk_per_credit_amount_bin(df: pd.DataFrame):
    """
    Plot credit amount distribution and mean risk per bin for each generation.

    This function creates a subplot for each unique generation in the 'Generation'
    column. Each subplot shows:
        - A bar chart (left y-axis) of counts of samples in each credit amount bin.
        - A bar chart (right y-axis) of mean risk for each credit amount bin.

    Args:
        df (pd.DataFrame): Input DataFrame containing at least the columns:
            - 'Generation': categorical generation label
            - 'Amount': credit amount bins
            - 'Risk': binary or numeric risk indicator (0/1 or proportion)

    Returns:
        None: Displays the plots using matplotlib and seaborn.
    """
    _, axes = plt.subplots(2, 2, figsize=(15, 6))
    axes = axes.flatten()

    generations = df['Generation'].unique()
    for i, gen in enumerate(generations):
        if i >= len(axes):
            break

        # Filter data for current generation
        gen_data = df[df['Generation'] == gen]

        # Compute counts and mean risk per bin for this generation
        counts = gen_data['Amount'].value_counts().sort_index()
        risk_means = gen_data.groupby('Amount')['Risk'].mean()

        # Plot with dual axes
        ax1 = axes[i]

        # Left axis: histogram counts
        sns.barplot(x=counts.index.astype(str), y=counts.values,
                    color="skyblue", ax=ax1)
        ax1.set_ylabel("Count", color="skyblue")
        ax1.set_xlabel("Credit Amount Bins")
        ax1.set_ylim(0, 350)

        # Right axis: mean risk per bin
        ax2 = ax1.twinx()
        sns.barplot(x=risk_means.index.astype(str), y=risk_means.values,
                    color="salmon", alpha=0.7, ax=ax2)
        ax2.set_ylabel("Mean Risk", color="salmon")

        # **Fix the risk scale to 0-1 for all plots**
        ax2.set_ylim(0, 1)

        ax1.set_title(f"Credit Amount Distribution and Mean Risk - {gen} Generation")
        ax1.tick_params(axis='x', rotation=45)

        ax1.grid(True)
        ax2.grid(False)

    # Hide empty subplots if any
    for i in range(len(generations), len(axes)):
        axes[i].set_visible(True)

    plt.tight_layout()
    plt.show()


def analyse_per_property(df: pd.DataFrame):
    """
    Plot grouped box plots of credit amounts per property category,
    split by good vs bad credit risk.

    Args:
        df (pd.DataFrame): Input DataFrame containing at least the columns:
            - 'Housing': categorical property/housing type
            - 'Credit amount': numeric credit amount
            - 'Risk': boolean or 0/1 indicator of credit risk

    Returns:
        None: Displays the plot using Plotly.
    """
    df_good = df[~df["Risk"].astype(bool)]
    df_bad = df[df["Risk"].astype(bool)]

    good = go.Box(
        x=df_good["Housing"],
        y=df_good["Credit amount"],
        name='Good credit',
        marker = {
            "color": "#3D9970"
        }
    )
    bad = go.Box(
        x=df_bad['Housing'],
        y=df_bad['Credit amount'],
        name="Bad Credit",
        marker = {
            "color": "#FF4136"
        }
    )

    data = [good, bad]
    layout = go.Layout(
        title='Property Categorical',
        yaxis={
            "title": "Credit Amount (US Dollar)",
            "zeroline": False
        },
        xaxis={
            "title": "Property Category"
        },
        boxmode='group',
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='Housing-Grouped')


def analyse_per_gender(df: pd.DataFrame):
    """
    Visualize credit risk by gender using both counts and credit amount distributions.

    This function creates a subplot with two visualizations:
    1. Bar plot showing the count of good and bad credit by gender.
    2. Box plot showing the distribution of credit amounts for good and bad credit by gender.

    Args:
        df (pd.DataFrame): Input DataFrame containing at least the columns:
            - "Sex": categorical gender column.
            - "Risk": boolean indicating credit risk (True = bad, False = good).
            - "Credit amount": numerical credit amount.

    Returns:
        None. Displays an interactive Plotly figure with the visualizations.
    """
    good = go.Bar(
        x=df[~df["Risk"].astype(bool)]["Sex"].value_counts().index.values,
        y=df[~df["Risk"].astype(bool)]["Sex"].value_counts().values,
        name='Good credit'
    )

    # First plot 2
    bad = go.Bar(
        x=df[df["Risk"].astype(bool)]["Sex"].value_counts().index.values,
        y=df[df["Risk"].astype(bool)]["Sex"].value_counts().values,
        name="Bad Credit"
    )

    # Second plot
    trace2 = go.Box(
        x=df[~df["Risk"].astype(bool)]["Sex"],
        y=df[~df["Risk"].astype(bool)]["Credit amount"],
        name=good.name
    )

    # Second plot 2
    trace3 = go.Box(
        x=df[df["Risk"].astype(bool)]["Sex"],
        y=df[df["Risk"].astype(bool)]["Credit amount"],
        name=bad.name
    )

    fig = tls.make_subplots(
        rows=1,
        cols=2,
        subplot_titles=('Count per Gender', 'Credit Amount per Gender')
    )

    fig.append_trace(good, 1, 1)
    fig.append_trace(bad, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 1, 2)

    fig['layout'].update(
        height=400, width=800, title='Gender Categorical', boxmode='group'
    )
    py.iplot(fig, filename='sex-subplot')


def analyse_risk_per_saving(df: pd.DataFrame):
    """
    Visualize credit risk by saving amount category (little, moderate, quite rich, rich)

    This function creates a subplot with two visualizations:
    1. Bar plot showing the count of good and bad credit per saving amount category.
    2. Box plot showing the distribution of credit amounts for good and bad credit per saving account category.

    Args:
        df (pd.DataFrame): Input DataFrame containing at least the columns:
            - "Saving accounts": categorical saving account column.
            - "Risk": boolean indicating credit risk (True = bad, False = good).
            - "Credit amount": numerical credit amount.

    Returns:
        None. Displays an interactive Plotly figure with the visualizations.
    """
    df_good = df[~df["Risk"].astype(bool)]
    df_bad = df[df["Risk"].astype(bool)]

    count_good = go.Bar(
        x=df_good["Saving accounts"].value_counts().index.values,
        y=df_good["Saving accounts"].value_counts().values,
        name='Good credit'
    )
    count_bad = go.Bar(
        x=df_bad["Saving accounts"].value_counts().index.values,    # saving amount category
        y=df_bad["Saving accounts"].value_counts().values,          # total per saving amount category
        name='Bad credit'
    )

    box_1 = go.Box(
        x=df_good["Saving accounts"],
        y=df_good["Credit amount"],
        name='Good credit'
    )
    box_2 = go.Box(
        x=df_bad["Saving accounts"],
        y=df_bad["Credit amount"],
        name='Bad credit'
    )

    fig = tls.make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            'Count per Saving', 'Credit Amount per Saving'
        )
    )

    fig.append_trace(count_good, 1, 1)
    fig.append_trace(count_bad, 1, 1)

    fig.append_trace(box_2, 1, 2)
    fig.append_trace(box_1, 1, 2)

    fig['layout'].update(height=400, width=800, title='Saving Amount', boxmode='group')

    py.iplot(fig, filename='combined-savings')


def risk_correlation(df: pd.DataFrame, categorical_cols: List[str]):
    """
    Plot the proportion of Risk (target variable) across multiple categorical features.

    For each categorical column in `categorical_cols`, this function calculates
    the proportion of each Risk value (e.g., 0/1 or True/False) for each category
    and plots it as a bar chart. Multiple plots are arranged in a grid layout.

    Args:
        df (pd.DataFrame): Input DataFrame containing the data.
        categorical_cols (list of str): List of categorical column names to analyze.

    Returns:
        None. Displays a matplotlib figure with subplots for each categorical feature.
    """
    ncols = 3
    nrows = (len(categorical_cols) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(18, 12))
    axes = axes.flatten()

    i = -1  # default value if loop doesn't run
    for i, col in enumerate(categorical_cols):
        ax = axes[i]
        # Categorical: proportions of Risk within each category
        prop_df = (
            df.groupby(col)['Risk']
            .value_counts(normalize=True)  # proportions
            .rename("proportion")
            .reset_index()
        )
        sns.barplot(x=col, y="proportion", hue="Risk", data=prop_df, ax=ax, palette="Set2")
        ax.tick_params(axis='x', rotation=45)
        ax.set_title(f"{col} vs Risk ratio")

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def risk_heatmap(df: pd.DataFrame, categorical_cols):
    """
    Plots a heatmap showing the proportion of risk (target=1)
    for each category of the given categorical features.

    Args:
        df (pd.DataFrame): Input DataFrame containing categorical features and 'Risk' column.
        categorical_cols (list): List of categorical column names to analyze.
    """
    if 'Risk' not in df.columns:
        raise ValueError("DataFrame must contain a 'Risk' column.")

    heatmap_data = pd.DataFrame()
    for col in categorical_cols:
        prop = df.groupby(col)['Risk'].mean().fillna(0)  # works if target is 0/1
        prop.name = col
        heatmap_data = pd.concat([heatmap_data, prop], axis=1)

    # Transpose for better visualization
    heatmap_data = heatmap_data.T

    # Plot heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        heatmap_data,
        annot=True,
        cmap='coolwarm',
        fmt=".2f",
        cbar_kws={'label': 'Proportion of Risk=True'},
        center=0.25,  # values > 0.3 shift towards red, < 0.3 towards blue
        linewidths=.5,
        linecolor='gray'
    )
    plt.title('Categorical Feature vs Risk Proportion')
    plt.ylabel('Categorical Feature')
    plt.xlabel('Category')
    plt.show()
