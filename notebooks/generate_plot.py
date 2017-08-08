#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plotly import tools
from plotly import graph_objs as go
import numpy as np

from settings.artistinfo import LINKIN_PARK_ALBUMS


coords = []
for i in xrange(1, 5):
    for j in xrange(2):
        coords.append((i, j % 2 + 1))


def rel_freq_plot(df):

    fig = tools.make_subplots(
        rows=4, cols=2,
        subplot_titles=tuple(
            i.title().replace("-", " ") for i in LINKIN_PARK_ALBUMS
        )
    )

    for i in xrange(len(LINKIN_PARK_ALBUMS)):
        fig.append_trace(
            go.Bar(x=df[i]["term"], y=df[i]["freq"],
                   showlegend=False),
            coords[i][0], coords[i][-1]
        )

    fig["layout"].update(
        height=2500, width=1000,
        title="Top Relative Frequency of Terms",
        margin=go.Margin(r=150, b=100),
    )

    return fig


def cos_sim_plot(df):

    # set colorscale
    colorscale = [[0, "rgb(255, 255, 255)"], [1.0, "rgb(204, 12, 12)"]]
    fig = tools.make_subplots(
        rows=4, cols=2,
        subplot_titles=tuple(i.title().replace("-", " ")
                             for i in LINKIN_PARK_ALBUMS)
    )

    for i in xrange(len(LINKIN_PARK_ALBUMS)):
        mask = np.zeros_like(df[i].values)
        mask[np.tril_indices_from(mask, k=-1)] = 1
        mask *= df[i].values

        fig.append_trace(
            go.Heatmap(
                z=mask,
                x=list(df[i]),
                y=df[i].index,
                colorscale=colorscale,
                showlegend=False,
                zmin=0,
                zmax=0.5,
                colorbar={
                    "title": "Similarity",
                }
            ),
            coords[i][0], coords[i][-1]
        )

    for attr in fig["layout"]:
        if "xaxis" in attr:
            fig["layout"][attr].update(tickangle=90)

    fig["layout"].update(
        height=2000, width=900,
        title="Cosine Similarity",
        margin=go.Margin(l=190, b=150),
    )

    return fig


def phrase_sent_plot(df):

    values = df["sent_score"]
    colors = [
        "rgba(226, 43, 43, 0.7)" if x < 0
        else "rgba(82, 183, 77, 0.7)" for x in values
    ]

    data = [go.Bar(
        x=values,
        y=df["phrase"],
        name="SF Zoo",
        orientation="h",
        marker=dict(color=colors),
    )]

    layout = go.Layout(
        autosize=False,
        margin=go.Margin(l=400, pad=4),
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def doc_sent_plot(df):

    data = []
    for album in LINKIN_PARK_ALBUMS:
        norm_sent = df["norm_comp"][df["album"] == album]
        data.append(go.Box(
            y=norm_sent,
            name=album.title().replace("-", " "),
            boxpoints="all",
            jitter=0.5,
            whiskerwidth=0.2,
            line=dict(width=1),
            showlegend=False,
        ))

    return data


def phrase_sent_scatter(df):

    data = []
    for album in LINKIN_PARK_ALBUMS:
        data.append(
            go.Scatter(
                x=df["num_words"][df["album"] == album],
                y=df["sent_score"][df["album"] == album],
                mode="markers",
                marker=dict(
                    size=14,
                    line=dict(width=1),
                    color=album,
                    opacity=0.5
                ),
                name=album.title().replace("-", " "),
                text=df["phrase"][df["album"] == album]
            )
        )

    layout = go.Layout(
        title="Sentiment Score of Phrases",
        hovermode="closest",
        xaxis=dict(
            title="Number of words",
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title="Sentiment Score",
            ticklen=5,
            gridwidth=2,
        ),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)

    return fig
