#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modifying https://github.com/sergiocorreia/panflute-filters/filters/figure.py
to rotate given image by desired angle
applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

# ---------------------------
# Imports
# ---------------------------

import os

import panflute as pf
from PIL import Image
from collections import OrderedDict
from pandoc_pandocker_filters.rotatesvg import rotatesvg
from pandoc_pandocker_filters.BitField import BitField


# ---------------------------
# Functions
# ---------------------------


def prepare(doc):
    pass


def finalize(doc):
    pass


class RotateImage(object):

    def __init__(self):
        self.bf = BitField()
        self.rs = rotatesvg()

    def rotate(self, filename="", angle=0):

        # pf.debug(angle)
        angle = angle % 360.0
        path, ext = os.path.splitext(filename)
        if (angle == 0):
            pass
        else:
            if (angle < 0):
                angle = 360 - abs(angle)
            # pf.debug(angle)

            if (ext in [".svg", ".pdf"]):
                filename = "".join([path, ".svg"])
                tmp = self.rs.rotate(filename, angle)
                renamed = "%s_r%+03d%s" % (path, angle, ".svg")
            else:
                tmp = self.do_rotate(filename, angle)
                renamed = "%s_r%+03d%s" % (path, angle, ext)

            if not os.path.exists(renamed):
                tmp.save(renamed)
            if (ext == ".pdf"):
                self.bf.svg_filename = renamed
                self.bf.convert_to_pdf = True
                self.bf.convert_to_png = False
                self.bf.convert_to_eps = False
                self.bf.basename = os.path.splitext(renamed)[0]
                self.bf.render_images()
                renamed = self.bf.pdf_filename
                # pf.debug("pdf", self.bf.pdf)

            filename = renamed

        return filename

    def do_rotate(self, filename, angle):
        with Image.open(filename) as img:
            # print angle
            tmp = img.rotate(angle, expand=True)
        return tmp

    def figure(self, options, data, element, doc):

        # pf.debug(doc.get_metadata("include", "no hoge"))
        # pf.debug(element.attributes)
        # pf.debug(element.parent)
        # pf.debug("prev", element.prev)
        # pf.debug(element)
        # pf.debug("next", element.next)
        # Para(
        #     Image(
        #         Strong(Str(caption));
        #         url="../images/front-image.png",
        #         title="fig:",
        #         attributes=OrderedDict([("width", "50%")])
        #     )
        # )

        # Get options
        fn = options.get("source")
        pf.debug("rotate image of", fn)
        fn = os.path.abspath(fn).replace("\\", "/")
        title = options.get("title", "fig:")
        caption = options.get("caption")
        label = options.get("label", os.path.splitext(os.path.basename(fn))[0])
        angle = options.get("angle", 0)
        attr = options.get("attr", {})

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
    return pf.run_filter(pf.yaml_filter, tag="rotate", function=ri.figure,
                         doc=doc)


# ---------------------------
# Main
# ---------------------------

if __name__ == "__main__":
    main()
