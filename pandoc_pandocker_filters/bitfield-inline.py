#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" bitfield-inline
Yet another pandoc filter which plays with bitfield interpreter
the filter finds out code block of "bitfield" class,
then throws given code or file to bitfield,
saves generated image in specified directory.
the codeblock will be replaced by an image link

applies MIT License (c) K4ZUKI(k.yamamoto.08136891@gmail.com)
"""

import os
import panflute as pf
from collections import OrderedDict
import json
import yaml
from BitField import BitField


class inline_bitfield(BitField):

    def __init__(self):
        super().__init__()

    def action(self, elem, doc):
        if isinstance(elem, pf.Image) and 'bitfield' in elem.classes:
            self.doc = doc
            # pf.debug("bitfield_inline()")
            # pf.debug(elem)
            fn = elem.url
            # pf.debug(fn)
            options = elem.attributes
            # pf.debug(options)

            with open(fn, 'r', encoding='utf-8') as f:
                data = f.read()
                data = self.validatejson(data)

            self.get_options(options, data, elem, doc)
            assert self.source is not None, "mandatory option 'input' is not set"
            assert os.path.exists(self.source) == 1, "input file does not exist"
            assert isinstance(self.toPNG, bool), "option png is boolean"
            assert isinstance(self.toPDF, bool), "option pdf is boolean"
            assert isinstance(self.toEPS, bool), "option eps is boolean"

            self.json2svg()
            self.svg2image()

            elem.url = self.linkto
            pf.debug("[inline] generate bitfield from", self.linkto)

            # return []
            return elem


def main(doc=None):
    bf = inline_bitfield()
    return pf.run_filter(bf.action, doc=doc)


if __name__ == '__main__':
    main()
