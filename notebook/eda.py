"""Exploratory Data Analysis"""
import pandas as pd
import plotly.offline as py
import plotly.tools as tls
import plotly.graph_objs as go


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
    df["generation"] = pd.cut(df.Age, interval, labels=cats)

    df_good = df[df["Risk"] == 'good']
    df_bad = df[df["Risk"] == 'bad']

    good = go.Box(
        y=df_good["Credit amount"],
        x=df_good["generation"],
        name='Good credit',
        marker=dict(
            color='#3D9970'
        )
    )

    bad = go.Box(
        y=df_bad['Credit amount'],
        x=df_bad['generation'],
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


def analyse_per_property(df: pd.DataFrame):
    df_good = df[df["Risk"] == 'good']
    df_bad = df[df["Risk"] == 'bad']

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
        x=df[df["Risk"] == 'good']["Sex"].value_counts().index.values,
        y=df[df["Risk"] == 'good']["Sex"].value_counts().values,
        name='Good credit'
    )

    # First plot 2
    bad = go.Bar(
        x=df[df["Risk"] == 'bad']["Sex"].value_counts().index.values,
        y=df[df["Risk"] == 'bad']["Sex"].value_counts().values,
        name="Bad Credit"
    )

    # Second plot
    trace2 = go.Box(
        x=df[df["Risk"] == 'good']["Sex"],
        y=df[df["Risk"] == 'good']["Credit amount"],
        name=good.name
    )

    # Second plot 2
    trace3 = go.Box(
        x=df[df["Risk"] == 'bad']["Sex"],
        y=df[df["Risk"] == 'bad']["Credit amount"],
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
    df_good = df[df["Risk"] == 'good']
    df_bad = df[df["Risk"] == 'bad']

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

