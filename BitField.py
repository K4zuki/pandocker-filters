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


class BitField(object):

    def __init__(self):
        self.bitfield = "'" + str(pf.shell("which bitfield").decode('utf-8').strip()) + "'"
        self.counter = 0
        self.unix = True if (os.name) != "nt" else False
        self.svg2pdf = None
        self.svg2png = None
        self.svg2eps = None
        if self.unix:
            self.svg2pdf = pf.shell("which rsvg-convert")
            self.svg2png = self.svg2pdf
            self.svg2eps = self.svg2eps
        else:
            self.svg2pdf = "'" + str(pf.shell("which svg2pdf").decode('utf-8').strip()) + "'"
            self.svg2png = "'" + str(pf.shell("which svg2png").decode('utf-8').strip()) + "'"
            pf.debug("non-UNIX OS!")
        self.defaultdir_to = "svg"

    def generate(self, options, data, element, doc):
        # pf.debug("generate()")
        source = options.get('input')
        vspace = str(options.get('vspace', 80))
        hspace = str(options.get('hspace', 640))
        lanes = str(options.get('lanes', 2))
        bits = str(options.get('bits', 16))
        fontfamily = '"' + options.get('fontfamily', 'source code pro') + '"'
        fontsize = str(options.get('fontsize', 16))
        fontweight = options.get('fontweight', "normal")
        caption = options.get('caption')
        dir_to = options.get('directory', self.defaultdir_to)
        toPNG = options.get('png', True)
        toEPS = options.get('eps', True) if self.unix else False
        toPDF = True if doc.format in ["latex"] else options.get('pdf', False)

        # options.get('pdf', False)
        # toPDF = options.get('pdf', False)
        assert source is not None, "mandatory option 'input' is not set"
        assert os.path.exists("./" + source) == 1, "input file does not exist"
        assert toPNG in [True, False], "option png is boolean"
        assert toPDF in [True, False], "option pdf is boolean"
        assert toEPS in [True, False], "option eps is boolean"

        # pf.debug(isinstance(toPNG, bool))
        pf.debug(toPDF)
        pf.debug(doc.format)

        # pf.debug(bitfield)
        # pf.debug(source)
        # pf.debug(vspace)
        # pf.debug(hspace)
        # pf.debug(lanes)
        # pf.debug(bits)
        # pf.debug(fontfamily)
        # pf.debug(fontsize)
        # pf.debug(fontweight)
        if os.path.exists("./" + dir_to) != 1:
            os.mkdir("./" + dir_to)

        _basename = "/".join([".",
                              dir_to,
                              str(self.counter)])
        _svg = ".".join([_basename, "svg"])
        # svg2pdf file.svg --output out.pdf
        # optional arguments:
        #   -h, --help            show this help message and exit
        #   -v, --version         Print version number and exit.
        #   -o PATH_PAT, --output PATH_PAT
        # $(RSVG) $<.svg --format=png --output=$@
        # $(RSVG) $<.svg --output $@

        toSVG = " ".join([self.bitfield,
                          "--input", source,
                          "--vspace", vspace,
                          "--hspace", hspace,
                          "--lanes", lanes,
                          "--bits", bits,
                          "--fontfamily", fontfamily,
                          "--fontsize", fontsize,
                          "--fontweight", fontweight,
                          ">", _svg
                          ])
        pf.debug(toSVG)
        pf.shell(toSVG)

        if(toPDF):
            output = [self.svg2pdf, _svg]
            if self.unix:
                output.append("--format=pdf")
            output.append("--output")
            output.append(".".join([_basename, "pdf"]))
            _svg2pdf = " ".join(output)
        else:
            _svg2pdf = "echo"

        if(toPNG):
            output = [self.svg2png, _svg]
            if self.unix:
                output.append("--format=png")
            output.append("--output")
            output.append(".".join([_basename, "png"]))
            _svg2png = " ".join(output)
        else:
            _svg2png = "echo"

        if(toEPS):
            output = [self.svg2pdf,
                      _svg,
                      "--format=eps"
                      "--output",
                      ".".join([_basename, "eps"])
                      ]
            _svg2eps = " ".join(output)
        else:
            _svg2eps = "echo"

        [pf.debug(command) for command in [_svg2pdf, _svg2png, _svg2eps]]
        [pf.shell(command) for command in [_svg2pdf, _svg2png, _svg2eps]]
        self.counter += 1
        return


def main(doc=None):
    bf = BitField()
    return pf.run_filter(pf.yaml_filter, tag='bitfield', function=bf.generate, doc=doc)


if __name__ == "__main__":
    main()
