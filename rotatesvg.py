#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# simple SVG rotate script
# great hint from
# https://stackoverflow.com/questions/43199869/rotate-and-scale-a-complete-svg-document-using-python
# MIT license (c) K4ZUKI(k.yamamoto.08136891@gmail.com)
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
        newx = float(x) * abs(math.cos(rad)) + float(y) * abs(math.sin(rad))
        newy = float(x) * abs(math.sin(rad)) + float(y) * abs(math.cos(rad))
        return (abs(newx), abs(newy))

    def get_offset(self, width, height, angle):
        offset_x = 0
        offset_y = 0
        debug(angle)
        if(0 < angle <= 90):
            offset_x = float(height) * abs(math.sin(math.radians(angle)))
        elif(90 < angle <= 180):
            offset_x = float(width) * abs(math.cos(math.radians(angle))) + \
                float(height) * abs(math.sin(math.radians(angle)))
            # offset_y = float(width) * abs(math.sin(math.radians(angle)))
            offset_y = float(height) * abs(math.sin(math.radians(angle)))
        elif(180 < angle <= 270):
            offset_x = float(width) * abs(math.cos(math.radians(angle))) + \
                float(height) * abs(math.sin(math.radians(angle)))
            offset_y = float(width) * abs(math.sin(math.radians(angle)))
        elif(270 < angle < 360):
            offset_y = float(width) * abs(math.sin(math.radians(angle)))
        else:
            pass
        # debug(offset_x, offset_y)
        return (offset_x, offset_y)

    def rotate(self, filename, angle):
        svg = svgutils.transform.fromfile(filename)
        originalSVG = svgutils.compose.SVG(filename)
        originalSVG.rotate(angle)
        offset_x, offset_y = self.get_offset(svg.width, svg.height, angle)
        debug("offset=", offset_x, offset_y)
        originalSVG.move(offset_x, offset_y)

        newx, newy = self.resize(svg.width, svg.height, angle)
        figure = svgutils.compose.Figure(
            newx, newy,
            originalSVG)
        return figure
