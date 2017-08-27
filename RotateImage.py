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
        self.processed_images = []
        self.angles = [90, 180, 270]
        self.angle_str = {90: "+090", 180: "_180", 270: "-090"}

    def rotate(self, filename="", angle=0):

        with Image.open(filename) as img:
            path, ext = os.path.splitext(filename)
            rotater = {90: img.transpose(Image.ROTATE_90),
                       180: img.transpose(Image.ROTATE_180),
                       270: img.transpose(Image.ROTATE_270),
                       }
            angle = angle % 360
            if(angle == 0):
                pass
            else:
                if(angle < 0):
                    angle = 360 - abs(angle)
                if angle in self.angles:
                    filename = "%s_r%s%s" % (path, self.angle_str[angle], ext)
                    tmp = rotater[angle]
                else:
                    # print angle
                    filename = "%s_r%+03d%s" % (path, angle, ext)
                    tmp = img.rotate(angle, expand=True)
                if not os.path.exists(filename):
                    tmp.save(filename)

        return filename

    def figure(self, options, data, element, doc):

        # pf.debug(doc.get_metadata('include', 'no hoge'))
        # pf.debug(element.attributes)
        # pf.debug(element.parent)
        # pf.debug("prev", element.prev)
        # pf.debug(element)
        # pf.debug("next", element.next)
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
        pf.debug("rotate image of", fn)
        fn = os.path.abspath(fn).replace('\\', '/')
        title = options.get('title', 'fig:')
        caption = options.get('caption')
        label = options.get('label', os.path.splitext(os.path.basename(fn))[0])
        angle = options.get('angle', 0)
        attr = options.get('attr', {})

        # pf.debug(attr)

        fn = self.rotate(fn, angle)
        title = pf.convert_text(title)

        if not attr:
            attr = OrderedDict({})

        # assert len(title) == 1, title

        title = title[0]
        title_text = pf.stringify(title).strip()

        # pf.debug(caption)
        if caption:
            caption = pf.convert_text(caption)
            caption = caption[0].content
            img = pf.Image(*caption, url=fn, title=title_text, attributes=attr)
        else:
            img = pf.Image(url=fn, attributes=attr)
        ans = pf.Para(img)
        # pf.debug("ans", ans)
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
