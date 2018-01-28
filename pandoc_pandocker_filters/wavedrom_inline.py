#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" wavedrom-inline
Yet another pandoc filter which plays with bitfield interpreter
the filter finds out code block of "wavedrom" class,
then throws given code or file to wavedrom,
saves generated image in specified directory.
the codeblock will be replaced by an image link

applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

import os
import panflute as pf
from collections import OrderedDict
import json
import yaml
from pandoc_pandocker_filters.BitField import BitField
from shutil import which
import subprocess
import wavedrompy.wavedrom as wavedrom
import attrdict


class wavedrom_inline(BitField):

    def __init__(self):
        super().__init__()

        phantomjs = which("phantomjs")
        phantomjs_nt = "bash \'" + phantomjs.replace("/c", "C:").replace(" ", "\ ") + "\'"
        self.phantomjs = phantomjs if self.unix else phantomjs_nt

        wavedrom = which("wavedrom")
        wavedrom_nt = "bash \'" + wavedrom.replace("/c", "C:").replace(" ", "\ ") + "\'"
        self.wavedrom = wavedrom if self.unix else wavedrom_nt

    def action(self, elem, doc):
        if isinstance(elem, pf.Link) and "wavedrom" in elem.classes:

            fn = elem.url
            options = elem.attributes
            idn = elem.identifier
            caption = elem.content
            with open(fn, "r", encoding="utf-8") as f:
                data = f.read()
                data = self.validatejson(data)

            self.get_options(options, data, elem, doc)
            assert self.source is not None, "mandatory option input is not set"
            assert os.path.exists(self.source) == 1, "input file does not exist"
            assert isinstance(self.toPNG, bool), "option png is boolean"
            assert isinstance(self.toPDF, bool), "option pdf is boolean"
            assert isinstance(self.toEPS, bool), "option eps is boolean"

            self.json2svg()
            self.svg2image()

            pf.debug("[inline] generate wavedrom from", self.linkto)
            # pf.debug(elem)
            elem.classes.remove("wavedrom")
            elem = pf.Image(*caption, classes=elem.classes, url=self.linkto,
                            identifier=idn, title="fig:", attributes=elem.attributes)
            # pf.debug(elem)

            return elem

        if isinstance(elem, pf.Image) and "wavedrom" in elem.classes:
            pf.debug("#")
            pf.debug("# Inline wavedrom in image link syntax, which is *obsolete*, is detected.")
            pf.debug("# Use hyperlink syntax from now - Just remove ! in front.")
            pf.debug("# Removing link for safety.")
            pf.debug("#")
            return []

    def json2svg(self):

        # /Users/yamamoto/.nodebrew/current/bin/phantomjs
        # phantomjs /Users/yamamoto/.nodebrew/current/bin/wavedrom -i Out/wave.wavejson -p images/waves/wave.png
        args = attrdict.AttrDict({"input": self.source, "svg": self.svg})
        wavedrom.main(args)
        # self.toSVG = [self.phantomjs,
        #               self.wavedrom,
        #               "-i", self.source,
        #               "-s", self.svg
        #               ]
        # pf.debug(" ".join(self.toSVG))
        # subprocess.call(self.toSVG)
        # with open(self.svg, "w", encoding="utf-8") as file:
        #     try:
        #         file.write(pf.shell(" ".join(self.toSVG)).decode("utf-8"))
        #     except IOError:
        #         raise


def main(doc=None):
    wd = wavedrom_inline()
    return pf.run_filter(wd.action, doc=doc)


if __name__ == "__main__":
    main()
