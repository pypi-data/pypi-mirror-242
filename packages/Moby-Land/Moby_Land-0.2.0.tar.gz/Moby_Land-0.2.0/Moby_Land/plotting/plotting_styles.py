"""Functions used to stylize matplotlib stuff."""
from typing import Union

import matplotlib as mpl
import matplotlib.pyplot as plt


def make_plots_scientific(fs: Union[float, int] = 12):
    """Make the fonts in all plots more scientific.
    Params:
        fs (str, float): The fontsize to use.
    """
    plt.rc('text', usetex=True)
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = 'cmr10'  # Computer Modern Roman
    mpl.rcParams['font.size'] = fs  # Adjust the font size as needed


def make_colors_gg() -> list:
    """Sets the colors to the ggplot colors.
    Returns:
        A list of the hex codes for the colors"""
    plt.style.use('ggplot')
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    plt.style.use('default')
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)

    return colors
