from typing import Any, Dict, List, Tuple
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt

from tmll.common.services.logger import Logger
from tmll.ml.visualization.plot_factory import PlotFactory
from tmll.tmll_client import TMLLClient

class BaseModule(ABC):

    def __init__(self, client: TMLLClient):
        """
        Initialize the base module with the given TMLL client.

        :param client: The TMLL client to use
        :type client: TMLLClient
        """
        self.client = client
        
        self.logger = Logger(self.__class__.__name__)
    
    def _plot(self, plots: List[Dict[str, Any]], plot_size: Tuple[float, float] = (15, 10), **kwargs) -> None:
        """
        Plot the given plots. 

        :param plots: The plots to plot. Each plot should be a dictionary with the following keys:
            - plot_type (PLOT_TYPES): The type of the plot (e.g., 'time_series' or 'scatter')
            - data (Any): The data to plot
            - x (str): The name of the x-axis column
            - y (str): The name of the y-axis column
            - hue (str, optional): The name of the hue column. Default is None
            - color (str, optional): The color of the plot. Default is 'blue'
        :type plots: List[Dict[str, Any]]
        :param plot_size: The size of the plot. Default is (15, 10)
        :type plot_size: Tuple[int, int], optional
        :param kwargs: Additional keyword arguments to pass to the plot
            - title (str): The title of the plot
            - x (str): The name of the x-axis
            - y (str): The name of the y-axis
        :type kwargs: dict
        :return: None
        """
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=plot_size)

        # Set the default x-axis and y-axis limits
        x_min, x_max = float('inf'), float('-inf')

        # Plot each plot
        for plot_info in plots:
            plot_type = plot_info['plot_type']
            data = plot_info['data']

            # Update the plot_info with the additional keyword arguments
            # These parameters will be used in each plot (if required)
            kwargs.update({k: v for k, v in plot_info.items() if k not in ['plot_type', 'data']})

            # Update the x-axis limits
            if data is not None and kwargs.get('x') is not None:
                x_min = min(x_min, data[kwargs.get('x')].min())
                x_max = max(x_max, data[kwargs.get('x')].max())

            # Create the plot
            plot_strategy = PlotFactory.create_plot(plot_type)
            plot_strategy.plot(ax, data, **kwargs)

        # Set the title, x-axis label, and y-axis label of the plot
        ax.set_title(kwargs.get('fig_title', ''))
        ax.set_xlabel(kwargs.get('fig_xlabel', ''))
        ax.set_ylabel(kwargs.get('fig_ylabel', ''))

        # Add the legend to the plot (remove duplicates)
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))   
        ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.025, 1), borderaxespad=0.)

        # Set the x-axis limits
        ax.set_xlim(x_min, x_max)

        # Display the plot
        plt.tight_layout()
        plt.show()

    @abstractmethod
    def process(self):
        """
        An abstract method to process the module.
        Each concrete module should implement this method.

        :return: None
        """
        pass