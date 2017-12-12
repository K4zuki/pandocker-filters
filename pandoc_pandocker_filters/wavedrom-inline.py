#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" wavedrom-inline
Yet another pandoc filter which plays with bitfield interpreter
the filter finds out code block of "wavedrom" class,
then throws given code or file to wavedrom,
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
from shutil import which
import subprocess


class wavedrom_inline(BitField):

    def __init__(self):
        super().__init__()

        phantomjs = which("phantomjs")
        phantomjs_nt = 'bash \'' + phantomjs.replace("/c", "C:").replace(" ", "\ ") + '\''
        self.phantomjs = phantomjs if self.unix else phantomjs_nt

        wavedrom = which("wavedrom")
        wavedrom_nt = 'bash \'' + wavedrom.replace("/c", "C:").replace(" ", "\ ") + '\''
        self.wavedrom = wavedrom if self.unix else wavedrom_nt

    def action(self, elem, doc):
        if isinstance(elem, pf.Image) and 'wavedrom' in elem.classes:
            self.doc = doc
            # pf.debug("wavedrom-inline()")
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
            pf.debug("[inline] generate wavedrom from", self.linkto)

            # return []
            return elem

    def json2svg(self):

        # /Users/yamamoto/.nodebrew/current/bin/phantomjs
        # phantomjs /Users/yamamoto/.nodebrew/current/bin/wavedrom -i Out/wave.wavejson -p images/waves/wave.png
        self.toSVG = [self.phantomjs,
                      self.wavedrom,
                      "-i", self.source,
                      "-s", self.svg
                      ]
        # pf.debug(" ".join(self.toSVG))
        subprocess.call(self.toSVG)
        # with open(self.svg, 'w', encoding='utf-8') as file:
        #     try:
        #         file.write(pf.shell(" ".join(self.toSVG)).decode('utf-8'))
        #     except IOError:
        #         raise


def main(doc=None):
    wd = wavedrom_inline()
    return pf.run_filter(wd.action, doc=doc)


if __name__ == '__main__':
    main()
