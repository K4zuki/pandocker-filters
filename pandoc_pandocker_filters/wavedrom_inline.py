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
from pandoc_pandocker_filters.BitField import BitField
import wavedrom


class wavedrom_inline(BitField):

    def __init__(self):
        super().__init__()

    def action(self, elem, doc):
        if isinstance(elem, pf.Link) and (("wavedrom" in elem.classes) or ("bitfield" in elem.classes)):
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

            output = wavedrom.render(data, self.svg_filename)
            output.saveas(self.svg_filename)
            # pf.debug(output.tostring())

            self.render_images()

            pf.debug("[inline] generate wavedrom from", self.linkto)
            # pf.debug(elem)
            try:
                elem.classes.remove("wavedrom")
            except:
                elem.classes.remove("bitfield")

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


def main(doc=None):
    wd = wavedrom_inline()
    return pf.run_filter(wd.action, doc=doc)


if __name__ == "__main__":
    main()
