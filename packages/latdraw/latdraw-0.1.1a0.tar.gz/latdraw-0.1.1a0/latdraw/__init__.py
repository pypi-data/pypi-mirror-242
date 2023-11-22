"""Top-level package for latdraw."""

__author__ = """Stuart Derek Walker"""
__email__ = 'stuart.walker@desy.de'
__version__ = '0.1.0'


from latdraw.interfaces import read, read_bdsim_survey, read_mad8, read_madx
from latdraw.latdraw import draw, draw_survey
from latdraw.plot import subplots_with_lattice, subplots_with_lattices, plot_optics, two_axes_figure

from . import optics

# from latdraw.lattice import Beamline

import warnings

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import ocelot
    from latdraw.interfaces import lattice_from_ocelot
except ImportError:
    pass
