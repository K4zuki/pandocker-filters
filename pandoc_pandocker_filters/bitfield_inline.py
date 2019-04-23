#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" bitfield-inline
Yet another pandoc filter which plays with bitfield interpreter
the filter finds out code block of "bitfield" class,
then throws given code or file to bitfield,
saves generated image in specified directory.
the codeblock will be replaced by an image link

applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

import os
import panflute as pf
from pandoc_pandocker_filters.BitField import BitField


class inline_bitfield(BitField):

    def __init__(self):
        super().__init__()

    def action(self, elem, doc, **args):
        if isinstance(elem, pf.Link) and "bitfield" in elem.classes:
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
            assert isinstance(self.convert_to_png, bool), "option png is boolean"
            assert isinstance(self.convert_to_pdf, bool), "option pdf is boolean"
            assert isinstance(self.convert_to_eps, bool), "option eps is boolean"

            self.json2svg()
            self.render_images()

            pf.debug("[inline] generate bitfield from", self.linkto)
            # pf.debug(elem)
            elem.classes.remove("bitfield")
            elem = pf.Image(*caption, classes=elem.classes, url=self.linkto,
                            identifier=idn, title="fig:", attributes=elem.attributes)
            # pf.debug(elem)

            return elem

        if isinstance(elem, pf.Image) and "bitfield" in elem.classes:
            pf.debug("#")
            pf.debug("# Inline bitfield in image link syntax, which is *obsolete*, is detected.")
            pf.debug("# Use hyperlink syntax from now - Just remove ! in front.")
            pf.debug("# Removing link for safety.")
            pf.debug("#")
            return []


def main(doc=None):
    bf = inline_bitfield()
    return pf.run_filter(bf.action, doc=doc)


def listed(doc=None):
    inline = inline_bitfield()
    block = BitField()
    return pf.run_filters([inline.action, pf.yaml_filter], tag="bitfield", function=block.generate, doc=doc)


if __name__ == "__main__":
    main()
