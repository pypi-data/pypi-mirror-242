import matplotlib as mpl
import matplotlib.pyplot as plt


class FigureBase:
    def __init__(self, base_figure=None):
        # initialization
        if base_figure:
            if not isinstance(base_figure, FigureBase):
                raise TypeError("The input figure must be a type of 'FigureBase'.")

            self._fig = base_figure.get_fig()
            self._axes = base_figure.get_axes()
        else:
            self._fig = plt.figure(figsize=(8, 8))
            self._axes = self._fig.add_subplot()

    def get_fig(self):
        return self._fig

    def get_axes(self):
        return self._axes

    def hide_axes(self):
        self._axes.axis("Off")

    def save_fig(self, filename, dpi):
        self._fig.savefig(filename, dpi=dpi)

    def set_content_margin(self, left, bottom, right, top):
        self._fig.subplots_adjust(left, bottom, right, top)

    def set_x_label(self, label):
        if not isinstance(label, str):
            raise TypeError("The label type is not 'str'.")
        else:
            self._axes.set_xlabel(label)

    def set_x_lim(self, lim):
        self._axes.set_xlim(lim)

    def set_x_ticks(self, ticks):
        self._axes.xaxis.set_ticks(ticks)

    def set_y_label(self, label):
        if not isinstance(label, str):
            raise TypeError("The label type is not 'str'.")
        else:
            self._axes.set_ylabel(label)

    def set_y_lim(self, lim):
        self._axes.set_ylim(lim)

    def set_y_ticks(self, ticks):
        self._axes.yaxis.set_ticks(ticks)

    def show_fig(self):
        plt.show()
