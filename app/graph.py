import altair as alt
from pandas import DataFrame

def chart(df: DataFrame, x: str, y: str, target: str) -> alt.Chart:
    """
    Parameters:
    - df: the data source for the chart
    - x: the x-axis
    - y: the y-axis
    - target: represented by color

    Returns:
    - alt.Chart: a customized chart that is using alt that works well
    """
    graph = alt.Chart(
        df,
        title=f"{y} by {x} for {target}"
    ).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X(x, axis=alt.Axis(labelColor='white', titleColor='white')),
        y=alt.Y(y, axis=alt.Axis(labelColor='white', titleColor='white')),
        color=alt.Color(
            target,
            legend=alt.Legend(title=target, labelColor='white', titleColor='white'),
            scale=alt.Scale(scheme= 'dark2')
        ),
        tooltip=[alt.Tooltip(c) for c in df.columns.to_list()]
    ).properties(
        width=700,
        height=500,
        background='#1e1e1e',
        padding=20
    ).configure_title(
        color='white',
        fontSize=20,
        font='Helvetica',
        anchor='start'
    ).configure_legend(
        labelColor='white',
        titleColor='white',
        labelFontSize=12,
        titleFontSize=14,
        gradientLength=200
    ).configure_axis(
        grid=False,
        domainColor='gray',
        tickColor='gray'
    ).configure_view(
        strokeWidth=0
    )

    return graph