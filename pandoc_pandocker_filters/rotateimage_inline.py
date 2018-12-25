#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pandoc filter using panflute
applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

import io
import csv
import panflute as pf
import codecs
from pandoc_pandocker_filters.RotateImage import RotateImage


class rotateimage_inline(RotateImage):

    def __init__(self):
        super().__init__()

    def action(self, elem, doc, **args):
        # pf.debug("action()")
        if isinstance(elem, pf.Image) and "rotate" in elem.classes:
            self.doc = doc  # type: pf.Doc
            fn = elem.url
            pf.debug("[inline] rotate image of", fn)
            options = elem.attributes
            angle = int(options.get("angle", 0))
            fn = self.rotate(fn, angle)

            elem.url = fn

            elem.classes.remove("rotate")

            # pf.debug(elem)
        return elem


def main(doc=None):
    ri = rotateimage_inline()
    return pf.run_filter(ri.action,
                         doc=doc)


def listed(doc=None):
    inline = rotateimage_inline()
    block = RotateImage()
    return pf.run_filters([inline.action, pf.yaml_filter], tag="rotate", function=block.figure, doc=doc)


if __name__ == "__main__":
    main()
