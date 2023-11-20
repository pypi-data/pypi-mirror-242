import numpy as np
from ._figure_base import FigureBase


class PixelContourFig(FigureBase):
    def __init__(self):
        super().__init__()

        # control parameters
        self._color_axes = None
        self._color_bar = None
        self._pixel_contour = None

    def get_pixel_contour(self):
        return self._pixel_contour

    def hide_color_outline(self):
        self._color_bar.outline.set_edgecolor("none")

    def set_data(self, X, Y, Z, colorbar=True, lim=None):
        # filter data
        if lim is not None:
            Z = np.clip(Z, lim[0], lim[1])

        # draw
        self._pixel_contour = self._axes.pcolormesh(X, Y, Z, shading="flat", cmap="viridis")

        # color bar
        if colorbar:
            axes_pos = self._axes.get_position()
            self._color_axes = self._fig.add_axes([axes_pos.x1+0.02, axes_pos.y0, 0.02, axes_pos.height])
            self._color_bar = self._fig.colorbar(self._pixel_contour, cax=self._color_axes, orientation='vertical')

    def set_color_lim(self, lim):
        self._color_bar.ax.set_ylim(lim)
        self._pixel_contour.set_clim(lim)

    def set_color_ticks(self, ticks):
        self._color_bar.set_ticks(ticks)

    def set_color_title(self, title):
        self._color_bar.ax.set_title(title, loc="center")
