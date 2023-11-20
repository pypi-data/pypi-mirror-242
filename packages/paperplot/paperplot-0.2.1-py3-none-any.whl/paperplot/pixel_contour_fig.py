from ._figure_base import FigureBase


class PixelContourFig(FigureBase):
    def __init__(self):
        super().__init__()

    def set_data(self, X, Y, Z):
        self._axes.pcolormesh(X, Y, Z, shading="flat", cmap="viridis")
