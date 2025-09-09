"""Exploratory Data Analysis"""
import pandas as pd
import plotly.offline as py
import plotly.tools as tls
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt


def analyse_target_distribution(df: pd.DataFrame):
    """Analyse the target label (good load or bad loan)
    Args:
        df: data
    """
    good = go.Bar(
        x=df[df["Risk"] == False]["Risk"].value_counts().index.values,
        y=df[df["Risk"] == False]["Risk"].value_counts().values,
        name='Good credit'
    )

    bad = go.Bar(
        x=df[df["Risk"] == True]["Risk"].value_counts().index.values,
        y=df[df["Risk"] == True]["Risk"].value_counts().values,
        name='Bad credit'
    )

    data = [good, bad]
    layout = go.Layout(
        yaxis=dict(
            title='Count'
        ),
        xaxis=dict(
            title='Risk Variable'
        ),
        title='Target label distribution'
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='grouped-bar')


def analyse_per_generation(df: pd.DataFrame):
    # Age bins
    interval = (18, 25, 35, 60, 100)
    cats = ['Student', 'Young', 'Adult', 'Senior']
    df["Generation"] = pd.cut(df.Age, interval, labels=cats)

    df_good = df[df["Risk"] == False]
    df_bad = df[df["Risk"] == True]

    good = go.Box(
        y=df_good["Credit amount"],
        x=df_good["Generation"],
        name='Good credit',
        marker=dict(
            color='#3D9970'
        )
    )

    bad = go.Box(
        y=df_bad['Credit amount'],
        x=df_bad['Generation'],
        name='Bad credit',
        marker=dict(
            color='#FF4136'
        )
    )

    data = [good, bad]
    layout = go.Layout(
        title='Age Categorical',
        yaxis=dict(
            title='Credit Amount (US Dollar)',
            zeroline=False
        ),
        xaxis=dict(
            title='Age category'
        ),
        boxmode='group',
        annotations=[
            dict(
                x=0.5,
                y=1.2,
                xref='paper',
                yref='paper',
                showarrow=False,
                text="Senior (60-100), Adult (35-60), Young (25-35), Student (18-25)",
                font=dict(size=14)
            )
        ]
    )
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='box-age-cat')


def risk_per_generation(df: pd.DataFrame):
    interval = (18, 25, 35, 60, 100)
    cats = ['Student', 'Young', 'Adult', 'Senior']
    df["Generation"] = pd.cut(df.Age, interval, labels=cats)

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
    # Bin credit amount into 10 intervals (equal-width bins)
    interval = (0, 5000, 10000, 15000, 20000)
    cats = [0, 1, 2, 3]
    df["Amount"] = pd.cut(df['Credit amount'], interval, labels=cats)

    # Create subplots for each generation
    generations = df['Generation'].unique()
    n_generations = len(generations)

    fig, axes = plt.subplots(2, 2, figsize=(15, 6))
    axes = axes.flatten()

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
    # custom_ylim = (0, 0.1)

    # Setting the values for all axes.
    # plt.setp(axes, ylim=custom_ylim)
    plt.show()


def analyse_per_property(df: pd.DataFrame):
    df_good = df[df["Risk"] == False]
    df_bad = df[df["Risk"] == True]

    good = go.Box(
        x=df_good["Housing"],
        y=df_good["Credit amount"],
        name='Good credit',
        marker=dict(
            color='#3D9970'
        )
    )
    bad = go.Box(
        x=df_bad['Housing'],
        y=df_bad['Credit amount'],
        name="Bad Credit",
        marker=dict(
            color='#FF4136'
        )
    )

    data = [good, bad]
    layout = go.Layout(
        title='Property Categorical',
        yaxis=dict(
            title='Credit Amount (US Dollar)',
            zeroline=False
        ),
        xaxis=dict(
            title='Property Category'
        ),
        boxmode='group',
    )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='Housing-Grouped')
    
    
def analyse_per_gender(df: pd.DataFrame):
    good = go.Bar(
        x=df[df["Risk"] == False]["Sex"].value_counts().index.values,
        y=df[df["Risk"] == False]["Sex"].value_counts().values,
        name='Good credit'
    )

    # First plot 2
    bad = go.Bar(
        x=df[df["Risk"] == True]["Sex"].value_counts().index.values,
        y=df[df["Risk"] == True]["Sex"].value_counts().values,
        name="Bad Credit"
    )

    # Second plot
    trace2 = go.Box(
        x=df[df["Risk"] == False]["Sex"],
        y=df[df["Risk"] == False]["Credit amount"],
        name=good.name
    )

    # Second plot 2
    trace3 = go.Box(
        x=df[df["Risk"] == True]["Sex"],
        y=df[df["Risk"] == True]["Credit amount"],
        name=bad.name
    )

    data = [good, bad, trace2, trace3]

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
    df_good = df[df["Risk"] == False]
    df_bad = df[df["Risk"] == True]

    count_good = go.Bar(
        x=df_good["Saving accounts"].value_counts().index.values,
        y=df_good["Saving accounts"].value_counts().values,
        name='Good credit'
    )
    count_bad = go.Bar(
        x=df_bad["Saving accounts"].value_counts().index.values,
        y=df_bad["Saving accounts"].value_counts().values,
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


def risk_correlation(df: pd.DataFrame, categorical_cols):
    import seaborn as sns
    import matplotlib.pyplot as plt

    ncols = 3
    nrows = (len(categorical_cols) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(18, 12))
    axes = axes.flatten()

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
    heatmap_data = pd.DataFrame()

    for col in categorical_cols:
        prop = df.groupby(col)['Risk'].mean()  # works if target is 0/1
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
        cbar_kws={'label': 'Proportion of Risk=True'},
        center=0.25,  # values > 0.3 shift towards red, < 0.3 towards blue
        linewidths=.5,
        linecolor='gray'
    )
    plt.title('Categorical Feature vs Risk Proportion')
    plt.ylabel('Categorical Feature')
    plt.xlabel('Category')
    plt.show()
