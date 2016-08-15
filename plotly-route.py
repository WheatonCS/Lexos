@app.route('/plotly')
def plotly():
    import plotly
    import pandas as pd
    import numpy as np
    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    graphs = [
        dict(
            data=[
                dict(
                    x=[1, 2, 3],
                    y=[10, 20, 30],
                    type='scatter'
                ),
            ],
            layout=dict(
                title='Scatterplot'
            )
        ),

        dict(
            data=[
                dict(
                    x=[1, 3, 5],
                    y=[10, 50, 30],
                    type='bar'
                ),
            ],
            layout=dict(
                title='Bar Graph'
            )
        ),

        dict(
            data=[
                dict(
                    x=ts.index,  # Can use the pandas data structures directly
                    y=ts
                )
            ],
            layout=dict(
                title='Line Graph',
                displayModeBar=True,
                displaylogo=False
            )
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # Try to generate a dendrogram
    from plotly.tools import FigureFactory as FF
    import numpy as np
    X = np.random.rand(10, 10)
    names = ['红楼梦', 'Oxana', 'John', 'Chelsea', 'Mark', 'Alice', 'Charlie', 'Rob', 'Lisa', 'Lily']
    dendro = FF.create_dendrogram(X, labels=names)
    # config = dict(
    #     width=850,
    #     height=800,
    #     showLink=False,
    #     staticPlot=False,
    #     displaylogo=False,
    #     displayModeBar=True,
    #     scrollZoom=True
    # )
    config = dict(
        width=850,
        height=800
    )
    dendro['layout'].update(config)
    plotly.offline.plot(dendro, filename='static/plotly/simple_dendrogram.html', auto_open=False, show_link=False)

    return render_template('plotly.html', ids=ids, graphJSON=graphJSON)
