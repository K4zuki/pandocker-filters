#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" aafigure-inline
Yet another pandoc filter which plays with aafigure interpreter
the filter finds out URL link of "aafigure" class,
then throws given code or file to aafigure,
saves generated image in specified directory.
the URL link will be replaced by an image link

applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""
import os
import panflute as pf
from pandoc_pandocker_filters.AAFigure import AAFigure


class inline_aafigure(AAFigure):

    def __init__(self):
        super().__init__()

    def action(self, elem, doc, **args):
        if isinstance(elem, pf.Link) and "aafigure" in elem.classes:
            fn = elem.url
            options = elem.attributes
            idn = elem.identifier
            caption = elem.content
            with open(fn, "r", encoding="utf-8") as f:
                data = f.read()

            self.render_message = "[inline] generate aafigure from"
            elem = self.render(options, data, elem, doc).content[0]
            elem.content = caption

            return elem


def main(doc=None):
    aaf = inline_aafigure()
    return pf.run_filter(aaf.action, doc=doc)


def listed(doc=None):
    inline = inline_aafigure()
    block = AAFigure()
    return pf.run_filters([inline.action, pf.yaml_filter], tag="aafigure", function=block.render, doc=doc)


if __name__ == "__main__":
    main()
