import matplotlib as mpl
from .line_fig import LineFig
from .line_style import LineStyle

# set global font
mpl.rcParams["font.family"] = ["Times New Roman"]
# set global font size
mpl.rcParams["font.size"] = 20
# set global math font
mpl.rcParams["mathtext.fontset"] = "stix"
# set round numbers
mpl.rcParams["axes.autolimit_mode"] = "round_numbers"
