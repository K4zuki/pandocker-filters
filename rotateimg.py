#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modifying https://github.com/sergiocorreia/panflute-filters/filters/figure.py
to rotate given image by desired angle
"""

# ---------------------------
# Imports
# ---------------------------

import os
from string import Template

import panflute as pf
from PIL import Image
from collections import OrderedDict

# ---------------------------
# Functions
# ---------------------------


def prepare(doc):
    pass


def finalize(doc):
    pass


class RotateImage(object):

    def __init__(self):
        pass

    def rotate(filename="", angle=0):

        with Image.open(filename) as img:
            path, ext = os.path.splitext(filename)
            if(angle == 0):
                pass
            elif(angle == 90):
                tmp = img.transpose(Image.ROTATE_90)
                filename = "%s_r+090%s" % (path, ext)
            elif(angle == 180 or angle == -180):
                tmp = img.transpose(Image.ROTATE_180)
                filename = "%s_r180%s" % (path, ext)
            elif(angle == 270 or angle == -90):
                tmp = img.transpose(Image.ROTATE_270)
                filename = "%s_r-090%s" % (path, ext)
            else:
                angle = angle % 360
                if(angle < 0):
                    angle = 360 - abs(angle)
                # print angle
                tmp = img.rotate(angle, expand=True)
                filename = "%s_r%+03d%s" % (path, angle, ext)
            if not os.path.exists(filename):
                tmp.save(filename)

        return filename

    def figure(options, data, element, doc):

        # pf.debug(doc.get_metadata('include', 'no hoge'))
        # pf.debug(element.attributes)
        # pf.debug(element.parent)
        # pf.debug(element.prev)
        # pf.debug(element)
        # pf.debug(element.next)
        # Para(
        #     Image(
        #         Strong(Str(caption));
        #         url='../images/front-image.png',
        #         title='fig:',
        #         attributes=OrderedDict([('width', '50%')])
        #     )
        # )

        # Get options
        fn = options.get('source')
        pf.debug("rotate image of ", fn)
        fn = os.path.abspath(fn).replace('\\', '/')
        title = options.get('title', 'fig:')
        caption = options.get('caption', 'Untitled')
        label = options.get('label', os.path.splitext(os.path.basename(fn))[0])
        angle = options.get('angle', 0)
        attr = options.get('attr', {})

        # pf.debug(attr)

        fn = rotate(fn, angle)
        title = pf.convert_text(title)
        caption = pf.convert_text(caption)

        if not attr:
            attr = OrderedDict({})

        # assert len(title) == 1, title

        title = title[0]
        title_text = pf.stringify(title).strip()

        caption = caption[0]
        caption = caption.content

        img = pf.Image(*caption, url=fn, title=title_text, identifier=label, attributes=attr)
        ans = pf.Para(img)
        # pf.debug(ans)
        return ans


def main(doc=None):
    ri = RotateImage()
    return pf.run_filter(pf.yaml_filter, tag='rotate', function=ri.figure,
                         doc=doc)


# ---------------------------
# Main
# ---------------------------

if __name__ == "__main__":
    main()
