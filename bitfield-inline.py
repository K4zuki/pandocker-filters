#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" pandoc-bitfield
Yet another pandoc filter which plays with bitfield interpreter
the filter finds out code block of "bitfield" class,
then throws given code or file to bitfield,
saves generated image in specified directory.
the codeblock will be replaced by an image link
pandoc
bitfield
panflute

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
            pf.debug("\bitfield()")
            pf.debug(elem)
            fn = elem.url
            pf.debug(fn)
            elem.url = "foo"
            pf.debug(elem)
            options = elem.attributes
            pf.debug(options)

            with open(fn, 'r', encoding='utf-8') as f:
                data = f.read()
                data = self.validatejson(data)

            self.get_options(options, data, elem, doc)

            return []
            return elem


def main(doc=None):
    bf = inline_bitfield()
    return pf.run_filter(bf.action, doc=doc)


if __name__ == '__main__':
    main()
