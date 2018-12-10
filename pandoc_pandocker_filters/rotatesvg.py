# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# simple SVG rotate script
# great hint from
# https://stackoverflow.com/questions/43199869/rotate-and-scale-a-complete-svg-document-using-python
applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""
import svgutils
import math
import sys


def debug(*args, **kwargs):
    """
    Same as print, but prints to ``stderr``
    (which is not intercepted by Pandoc).
    """
    print(file=sys.stderr, *args, **kwargs)


class rotatesvg(object):

    def __init__(self):
        pass

    def resize(self, x, y, deg):
        rad = math.radians(deg)
        x = float(x.split("px")[0])
        y = float(y.split("px")[0])
        newx = float(x) * abs(math.cos(rad)) + float(y) * abs(math.sin(rad))
        newy = float(x) * abs(math.sin(rad)) + float(y) * abs(math.cos(rad))
        return (abs(newx), abs(newy))

    def get_offset(self, width, height, angle):
        offset_x = 0
        offset_y = 0
        rad = math.radians(angle)
        w = float(width.split("px")[0])
        h = float(height.split("px")[0])
        if (0 < angle <= 180):
            offset_x = h * abs(math.sin(rad))
            # debug("0 < ", angle, " <= 180")
            if (90 < angle <= 180):
                offset_x += w * abs(math.cos(rad))
                # offset_y = w * abs(math.sin(rad))
                offset_y = h * abs(math.cos(rad))
                # debug("90 < ", angle, " <= 180")
        elif (180 < angle < 360):
            offset_y = w * abs(math.sin(rad))
            # debug("180 < ", angle, " < 360")
            if (180 < angle <= 270):
                offset_x = w * abs(math.cos(rad))
                offset_y += h * abs(math.cos(rad))
                # debug("180 < ", angle, " <= 270")
        else:
            pass
        # debug(offset_x, offset_y)
        return (offset_x, offset_y)

    def rotate(self, filename, angle):
        svg = svgutils.transform.fromfile(filename)
        originalSVG = svgutils.compose.SVG(filename)
        originalSVG.rotate(angle)
        offset_x, offset_y = self.get_offset(svg.width, svg.height, angle)
        # debug("offset=", offset_x, offset_y)
        originalSVG.move(offset_x, offset_y)

        newx, newy = self.resize(svg.width, svg.height, angle)
        figure = svgutils.compose.Figure(
            newx, newy,
            originalSVG)
        return figure
