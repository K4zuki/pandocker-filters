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

import panflute as pf


class BitField(object):

    def __init__(self):
        self.bitfield = str(pf.shell("which bitfield").strip())

    def generate(self, options, data, element, doc):
        # pf.debug("generate()")
        source = options.get('input')
        assert source is not None, "mandatory option 'input' is not set"
        vspace = str(options.get('vspace', 80))
        hspace = str(options.get('hspace', 640))
        lanes = str(options.get('lanes', 2))
        bits = str(options.get('bits', 16))
        fontfamily = '"' + options.get('fontfamily', '"source code pro"') + '"'
        fontsize = str(options.get('fontsize', 16))
        fontweight = options.get('fontweight', "normal")

        # pf.debug(bitfield)
        # pf.debug(source)
        # pf.debug(vspace)
        # pf.debug(hspace)
        # pf.debug(lanes)
        # pf.debug(bits)
        # pf.debug(fontfamily)
        # pf.debug(fontsize)
        # pf.debug(fontweight)
        pf.debug(" ".join([self.bitfield,
                           "--input", source,
                           "--vspace", vspace,
                           "--hspace", hspace,
                           "--lanes", lanes,
                           "--bits", bits,
                           "--fontfamily", fontfamily,
                           "--fontsize", fontsize,
                           "--fontweight", fontweight
                           ]))
        return


def main(doc=None):
    bf = BitField()
    return pf.run_filter(pf.yaml_filter, tag='bitfield', function=bf.generate,
                         doc=doc)


if __name__ == "__main__":
    main()
