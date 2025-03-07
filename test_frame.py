import plotly.graph_objects as go

fig = go.Figure(data=[go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='markers',
    marker=dict(
        size=20,
        color='blue',
        line=dict(
            width=2,
            color='black'
        )
    )
)])

fig.show()