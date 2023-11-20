class LineStyle:
    def __init__(self):
        # control parameters
        self.color = None
        self.dashes = None
        self.label = None
        self.line_style = None
        self.line_width = None
        self.marker = None
        self.marker_edge_color = None

    def decorate_line(self, line):
        if self.color is not None: line.set_color(self.color)
        if self.dashes is not None: line.set_dashes(self.dashes)
        if self.label is not None: line.set_label(self.label)
        if self.line_style is not None: line.set_linestyle(self.line_style)
        if self.line_width is not None: line.set_linewidth(self.line_width)
        if self.marker is not None: line.set_marker(self.marker)
        if self.marker_edge_color is not None: line.set_markeredgecolor(self.marker_edge_color)


class LineStyleLib:
    def __init__(self):
        pass

    @staticmethod
    def BlueCircle():
        style = LineStyle()
        style.color = (0, 0, 0, 0)
        style.marker = "o"
        style.marker_edge_color = (38/255, 148/255, 171/255, 1)

        return style

    @staticmethod
    def BrownSquare():
        style = LineStyle()
        style.color = (0, 0, 0, 0)
        style.marker = "s"
        style.marker_edge_color = (194/255, 157/255, 115/255, 1)

        return style

    @staticmethod
    def GreenDiamond():
        style = LineStyle()
        style.color = (0, 0, 0, 0)
        style.marker = "D"
        style.marker_edge_color = (126/255, 188/255, 89/255, 1)

        return style

    @staticmethod
    def RedLine():
        style = LineStyle()
        style.color = (234/255, 112/255, 112/255, 1)

        return style
