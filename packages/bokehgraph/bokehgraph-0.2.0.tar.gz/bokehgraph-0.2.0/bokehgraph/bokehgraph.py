from collections import namedtuple
from math import sqrt

import bokeh.io
import bokeh.plotting
import networkx as nx
from bokeh import models

from .colormap import BokehGraphColorMap


class BokehGraph(object):
    """
    This is instanciated with a (one-mode) networkx graph object with
    BokehGraph(nx.Graph())

    working example:
    import networkx as nx
    graph = nx.barbell_graph(5,6)
    degrees = nx.degree(graph)
    nx.set_node_attributes(graph, dict(degrees), "degree")
    plot = BokehGraph(graph, width=800, height=600, inline=True)
    plot.layout(shrink_factor = 0.6)
    plot.draw(color_by="degree", palette="Category20", max_colors=2)


    The plot is drawn by BokehGraph.draw(node_color="firebrick")
        - node_color, line_color can be set to every value that bokeh
          recognizes, including a bokeh.colors.RGB instance. serveral other
          parameters can be found in the .draw method.


    """

    def __init__(
        self,
        graph,
        width=800,
        height=600,
        inline=True,
        hover_nodes=True,
        hover_edges=False,
    ):
        self.graph = graph

        self.width = width
        self.height = height

        self.hover_nodes = hover_nodes
        self.hover_edges = hover_edges

        self._layout = None
        self._nodes = None
        self._edges = None

        self.colormap = None

        self.figure = None

        self.node_properties = None
        self.node_attributes = sorted(
                {attr for _, data in self.graph.nodes(data=True) for attr in data},
            )
        if self.hover_nodes:
            self._node_tooltips = [("type", "node"), ("node", "@_node")]
            for attr in self.node_attributes:
                self._node_tooltips.append((attr, f"@{attr}"))

        self.edge_properties = None
        if self.hover_edges:
            self.edge_attributes = sorted(
                {attr for _, _, data in self.graph.edges(data=True) for attr in data},
            )
            self._edge_tooltips = [("type", "edge"), ("u", "@_u"), ("v", "@_v")]
            for attr in self.edge_attributes:
                self._edge_tooltips.append((attr, f"@{attr}"))

        # inline for jupyter notebooks
        if inline:
            bokeh.io.output_notebook(hide_banner=True)
            self.show = lambda x: bokeh.plotting.show(x, notebook_handle=True)
        else:
            self.show = lambda x: bokeh.plotting.show(x)

    def gen_edge_coordinates(self):
        if not self._layout:
            self.layout()

        xs = []
        ys = []
        val = namedtuple("edges", "xs ys")

        for edge in self.graph.edges():
            from_node = self._layout[edge[0]]
            to_node = self._layout[edge[1]]
            xs.append([from_node[0], to_node[0]])
            ys.append([from_node[1], to_node[1]])

        return val(xs=xs, ys=ys)

    def gen_node_coordinates(self):
        if not self._layout:
            self.layout()

        names, coords = zip(*self._layout.items())
        xs, ys = zip(*coords)
        val = namedtuple("nodes", "names xs ys")

        return val(names=names, xs=xs, ys=ys)

    def layout(self, layout=None, shrink_factor=0.8, iterations=50, scale=1, seed=None):
        self._nodes = None
        self._edges = None
        if not layout:
            self._layout = nx.spring_layout(
                self.graph,
                k=1 / (sqrt(self.graph.number_of_nodes() * shrink_factor)),
                iterations=iterations,
                scale=scale,
                seed=seed,
            )
        else:
            self._layout = layout
        return

    def prepare_figure(self):
        fig = bokeh.plotting.figure(
            width=self.width,
            height=self.height,
            tools=["box_zoom", "reset", "wheel_zoom", "pan"],
        )

        fig.toolbar.logo = None
        fig.axis.visible = False
        fig.xgrid.grid_line_color = None
        fig.ygrid.grid_line_color = None
        return fig

    def _render_edges(self, figure, edge_color, edge_alpha, edge_size):
        if not self._edges:
            self._edges = self.gen_edge_coordinates()

        self.edge_properties = dict(
            xs=self._edges.xs,
            ys=self._edges.ys,
        )

        if self.hover_edges:
            xs, ys = list(zip(*self.graph.edges()))
            self.edge_properties["_u"] = xs
            self.edge_properties["_v"] = ys
            for attr in self.edge_attributes:
                self.edge_properties[attr] = [
                    data[attr] for _, _, data in self.graph.edges(data=True)
                ]

        # Draw Edges
        source_edges = bokeh.models.ColumnDataSource(self.edge_properties)

        edges = figure.multi_line(
            "xs",
            "ys",
            line_color=edge_color,
            source=source_edges,
            alpha=edge_alpha,
            line_width=edge_size,
        )

        if self.hover_edges:
            formatter = {tip: "printf" for tip, _ in self._edge_tooltips}
            hovertool = models.HoverTool(
                tooltips=self._edge_tooltips,
                formatters=formatter,
                renderers=[edges],
                line_policy="interp"
            )
            figure.add_tools(hovertool)

        return figure

    def _render_nodes(
        self,
        figure,
        node_alpha,
        node_size,
        node_color,
        color_by,
        palette,
        max_colors,
    ):
        if not self._nodes:
            self._nodes = self.gen_node_coordinates()

        self.node_properties = dict(
            xs=self._nodes.xs,
            ys=self._nodes.ys,
            _node=self._nodes.names,
        )

        for attr in self.node_attributes:
            if not self.hover_nodes and attr != color_by:
                continue
            self.node_properties[attr] = [
                self.graph.nodes[n][attr] for n in self._nodes.names
            ]

        if color_by and palette:
            self.colormap = BokehGraphColorMap(palette, max_colors)
            self.node_properties["_colormap"] = self.colormap.map(
                self.node_properties[color_by]
            )
            color = "_colormap"
        else:
            color = node_color

        source_nodes = bokeh.models.ColumnDataSource(self.node_properties)
        nodes = figure.circle(
            "xs",
            "ys",
            fill_color=color,
            line_color=color,
            source=source_nodes,
            alpha=node_alpha,
            size=node_size,
        )

        if self.hover_nodes:
            formatter = {tip: "printf" for tip, _ in self._node_tooltips}
            hovertool = models.HoverTool(
                tooltips=self._node_tooltips,
                formatters=formatter,
                renderers=[nodes],
                attachment="vertical"
            )
            figure.add_tools(hovertool)
        return figure

    def render(
        self,
        node_color="firebrick",
        palette=None,
        color_by=None,
        edge_color="navy",
        edge_alpha=0.17,
        edge_size=1,
        node_alpha=0.7,
        node_size=9,
        max_colors=-1,
    ):
        figure = self.prepare_figure()

        figure = self._render_edges(
            figure=figure,
            edge_color=edge_color,
            edge_alpha=edge_alpha,
            edge_size=edge_size,
        )

        figure = self._render_nodes(
            figure=figure,
            node_alpha=node_alpha,
            node_size=node_size,
            max_colors=max_colors,
            palette=palette,
            color_by=color_by,
            node_color=node_color,
        )

        return figure

    def draw(
        self,
        node_color="firebrick",
        palette=None,
        color_by=None,
        edge_color="navy",
        edge_alpha=0.17,
        edge_size=1,
        node_alpha=0.7,
        node_size=9,
        max_colors=-1,
    ):
        figure = self.render(
            node_color=node_color,
            palette=palette,
            color_by=color_by,
            edge_color=edge_color,
            edge_alpha=edge_alpha,
            edge_size=edge_size,
            node_alpha=node_alpha,
            node_size=node_size,
            max_colors=max_colors,
        )
        self.show(figure)
