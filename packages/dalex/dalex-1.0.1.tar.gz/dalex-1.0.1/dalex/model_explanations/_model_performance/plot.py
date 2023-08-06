import numpy as np
import pandas as pd
import plotly.graph_objects as go

def ecdf(x):
    # https://community.plot.ly/t/plot-the-empirical-cdf/29045
    x = np.sort(x)

    def result(v):
        return np.searchsorted(x, v, side='right') / x.size

    return result


def plot_ecdf(df_list, colors, title):
    fig = go.Figure()

    for i, _df in enumerate(df_list):
        _abs_residuals = np.abs(_df['residuals'])
        _unique_abs_residuals = np.unique(_abs_residuals)

        fig.add_scatter(
            x=_unique_abs_residuals,
            y=1 - ecdf(_abs_residuals)(_unique_abs_residuals),
            line_shape='hv',
            name=_df.iloc[0, _df.columns.get_loc('label')],
            marker=dict(color=colors[i])
        )

    fig.update_yaxes({'type': 'linear', 'gridwidth': 2, 'zeroline': False, 'automargin': True, 'ticks': 'outside',
                    'tickcolor': 'white', 'ticklen': 10, 'fixedrange': True, 'tickformat': ',.0%'})

    fig.update_xaxes({'type': 'linear', 'gridwidth': 2, 'zeroline': False, 'automargin': True, 'ticks': "outside",
                    'tickcolor': 'white', 'ticklen': 10, 'fixedrange': True, 'title_text': '|residual|'})
    
    title = "Reverse cumulative distribution of |residual|" if title is None else title
    fig.update_layout(title_text=title, title_x=0.15, font={'color': "#371ea3"}, template="none",
                    margin={'t': 78, 'b': 71, 'r': 30})
    
    return fig


def plot_roc(df_list, colors, title):
    fig = go.Figure()
    grid_points = 101
    idx = np.arange(df_list[0].shape[0], step=int(df_list[0].shape[0]/grid_points))
    for i, _df in enumerate(df_list):
        _df = _df.sort_values('y_hat', ascending=False)
        _df = _df.assign(TPR=np.cumsum(_df.y)/np.sum(_df.y),
                         FPR=(np.cumsum(1-_df.y)/np.sum(1-_df.y)))
        if _df.shape[0] > grid_points:
            _df = _df.iloc[idx,:].sort_values('FPR', ascending=True)

        fig.add_scatter(
            x=_df.FPR,
            y=_df.TPR,
            line_shape='hv',
            name=_df.iloc[0, _df.columns.get_loc('label')],
            marker=dict(color=colors[i])
        )

    fig.update_yaxes({'type': 'linear', 'gridwidth': 2, 'zeroline': False, 'automargin': True, 'ticks': 'outside',
                    'tickcolor': 'white', 'ticklen': 10, 'fixedrange': True, 'title_text': 'True positive rate'})

    fig.update_xaxes({'type': 'linear', 'gridwidth': 2, 'zeroline': False, 'automargin': True, 'ticks': "outside",
                    'tickcolor': 'white', 'ticklen': 10, 'fixedrange': True, 'title_text': 'False positive rate'})
    title = "Receiver Operating Characteristic" if title is None else title
    fig.update_layout(title_text=title, title_x=0.15, font={'color': "#371ea3"}, template="none",
                      margin={'t': 78, 'b': 71, 'r': 30})
    
    return fig

def plot_lift(df_list, colors, title):
    fig = go.Figure()
    grid_points = 101
    idx = np.arange(df_list[0].shape[0], step=int(df_list[0].shape[0]/grid_points))
    _temp_df = pd.concat(df_list)
    max_lift = _temp_df.y.sum()/_temp_df.shape[0]
           
    for i, _df in enumerate(df_list):
        _df = _df.sort_values('y_hat', ascending=False)
        n = _df.shape[0]
        lift = np.cumsum(_df.y)/n
        pr = np.linspace(0, 1, n)
        _df = _df.assign(lift=lift/pr, pr=pr)
        if _df.shape[0] > grid_points:
            _df = _df.iloc[idx,:].sort_values('pr', ascending=True)
            
        fig.add_scatter(
            x=_df.pr,
            y=_df.lift/max_lift,
            line_shape='hv',
            name=_df.iloc[0, _df.columns.get_loc('label')],
            marker=dict(color=colors[i])
        )
        
    fig.update_yaxes({'type': 'linear', 'gridwidth': 2, 'zeroline': False, 'automargin': True, 'ticks': 'outside',
                    'tickcolor': 'white', 'ticklen': 10, 'fixedrange': True, 'title_text': 'Lift'})

    fig.update_xaxes({'type': 'linear', 'gridwidth': 2, 'zeroline': False, 'automargin': True, 'ticks': "outside",
                    'tickcolor': 'white', 'ticklen': 10, 'fixedrange': True, 'title_text': 'Positive rate'})
    title = "LIFT chart" if title is None else title
    fig.update_layout(title_text=title, title_x=0.15, font={'color': "#371ea3"}, template="none",
                      margin={'t': 78, 'b': 71, 'r': 30})
    
    return fig

