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
        # self.unix = True if (os.name) != "nt" else False
        # bitfield = pf.shell("which bitfield").decode('utf-8').strip()
        # bitfield_nt = "cmd '" + bitfield.replace("/c", "C:").replace(" ", "\ ") + "'"
        # self.bitfield = bitfield if self.unix else bitfield_nt
        # self.counter = 0
        # self.pdfconvert = None
        # self.pngconvert = None
        # self.epsconvert = None
        # if self.unix:
        #     self.pdfconvert = pf.shell("which rsvg-convert").decode('utf-8').strip()
        #     self.pngconvert = self.pdfconvert
        #     self.epsconvert = self.pdfconvert
        # else:
        #     svg2png = pf.shell("which svg2png").decode('utf-8').strip()
        #     svg2pdf = pf.shell("which svg2pdf").decode('utf-8').strip()
        #     self.pdfconvert = "cmd '" + str(svg2pdf.replace("/c", "C:").replace(" ", "\ ")) + "'"
        #     self.pngconvert = "cmd '" + str(svg2png.replace("/c", "C:").replace(" ", "\ ")) + "'"
        #     pf.debug("non-UNIX OS!")
        # self.defaultdir_to = "svg"
        # self.svg = ""
        # self.png = ""
        # self.pdf = ""
        # self.eps = ""

    def prepare(self, doc):
        pass

    def action(self, elem, doc):
        if isinstance(elem, pf.Image) and 'bitfield' in elem.classes:
            pf.debug("\bitfield()")
            pf.debug(elem)
            fn = elem.url
            pf.debug(fn)
            elem.url = "foo"
            pf.debug(elem)

            with codecs.open(fn, 'r', 'utf-8') as f:
                data = f.read()
                data = self.validatejson(data)

            return []

    def make_emph(self, elem, doc):
        if isinstance(elem, pf.Code) and 'bitfield' in elem.classes:
            pf.debug("\tmake_emph()")
            fn = elem.text
            # with codecs.open(fn, 'r', 'utf-8') as f:
            #     raw = f.read()
            #
            #     new_elems = pf.convert_text(raw)
            #     # i = (item.walk(make_emph, doc) for item in new_elems)
            #     # pf.debug(i)
            #     d = pf.Doc(*new_elems, format='md')
            #     e = d.walk(make_emph)
            #     pf.debug(e.content)
            #     return e.content
            # return new_elems
        pf.debug("")
        # return pf.Emph(elem)
        # data = pypandoc.convert_file(fn, 'json')
        # _doc = pf.load(io.StringIO(data))
        # _doc = pf.run_filter(action, prepare=prepare, doc=_doc)
        # return _doc

    def finalize(self, doc):
        pass


def main(doc=None):
    bf = inline_bitfield()
    return pf.run_filter(bf.action,
                         prepare=bf.prepare,
                         finalize=bf.finalize,
                         doc=doc)


if __name__ == '__main__':
    main()
