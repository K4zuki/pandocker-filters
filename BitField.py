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
# import subprocess
from collections import OrderedDict


class BitField(object):

    def __init__(self):
        self.bitfield = pf.shell("which bitfield").decode('utf-8').strip()
        # self.bitfield = "./bitfield/bin/bitfield.js"
        self.counter = 0
        self.unix = True if (os.name) != "nt" else False
        self.pdfconvert = None
        self.pngconvert = None
        self.epsconvert = None
        if self.unix:
            self.pdfconvert = pf.shell("which rsvg-convert").decode('utf-8').strip()
            self.pngconvert = self.pdfconvert
            self.epsconvert = self.pdfconvert
        else:
            self.pdfconvert = "'" + str(pf.shell("which svg2pdf").decode('utf-8').strip()) + "'"
            self.pngconvert = "'" + str(pf.shell("which svg2png").decode('utf-8').strip()) + "'"
            pf.debug("non-UNIX OS!")
        self.defaultdir_to = "svg"
        self.svg = ""
        self.png = ""
        self.pdf = ""
        self.eps = ""

    def svg2png(self):
        output = [self.pngconvert, self.svg]
        self.png = ".".join([str(self.basename), "png"])
        if self.unix:
            output.append("--format=png")
        output.append("--output")
        output.append(png)
        pf.debug(" ".join(output))
        pf.shell(" ".join(output))

    def svg2pdf(self):
        output = [self.pdfconvert, self.svg]
        self.pdf = ".".join([str(self.basename), "pdf"])
        if self.unix:
            output.append("--format=pdf")
        output.append("--output")
        output.append(pdf)
        pf.debug(" ".join(output))
        pf.shell(" ".join(output))

    def svg2eps(self):
        self.eps = ".".join([self.basename, "eps"])
        output = [self.epsconvert,
                  self.svg,
                  "--format=eps",
                  "--output",
                  eps
                  ]
        pf.debug(" ".join(output))
        pf.shell(" ".join(output))

    def generate(self, options, data, element, doc):
        # pf.debug("generate()")
        source = options.get('input')

        vspace = str(options.get('lane-height', 80))
        hspace = str(options.get('lane-width', 640))
        lanes = str(options.get('lanes', 1))
        bits = str(options.get('bits', 8))

        fontfamily = '"' + options.get('fontfamily', 'source code pro') + '"'
        fontsize = str(options.get('fontsize', 16))
        fontweight = options.get('fontweight', "normal")

        caption = options.get('caption', "Untitled")
        dir_to = options.get('directory', self.defaultdir_to)

        attr = options.get('attr', {})
        title = options.get('title', "fig:")
        label = options.get('label', os.path.splitext(os.path.basename(source))[0])

        toPNG = options.get('png', True)
        toEPS = options.get('eps', False) if self.unix else False
        toPDF = True if doc.format in ["latex"] else options.get('pdf', False)

        assert source is not None, "mandatory option 'input' is not set"
        assert os.path.exists(source) == 1, "input file does not exist"
        assert isinstance(toPNG, bool), "option png is boolean"
        assert isinstance(toPDF, bool), "option pdf is boolean"
        assert isinstance(toEPS, bool), "option eps is boolean"

        # pf.debug(isinstance(toPNG, bool))
        # pf.debug(toPDF)
        # pf.debug(doc.format)
        # pf.debug(bitfield)
        # pf.debug(source)
        # pf.debug(vspace)
        # pf.debug(hspace)
        # pf.debug(lanes)
        # pf.debug(bits)
        # pf.debug(fontfamily)
        # pf.debug(fontsize)
        # pf.debug(fontweight)
        if os.path.exists(dir_to) != 1:
            os.mkdir(dir_to)

        self.basename = "/".join([dir_to,
                                  str(self.counter)])
        self.svg = ".".join([self.basename, "svg"])
        self.counter += 1

        toSVG = [self.bitfield,
                 "--input", source,
                 "--vspace", vspace,
                 "--hspace", hspace,
                 "--lanes", lanes,
                 "--bits", bits,
                 "--fontfamily", fontfamily,
                 "--fontsize", fontsize,
                 "--fontweight", fontweight,
                 ]
        pf.debug(" ".join(toSVG))
        with open(self.svg, 'w') as file:
            file.write(pf.shell(" ".join(toSVG)).decode('utf-8'))

        if(toPDF):
            self.svg2pdf()

        if(toPNG):
            self.svg2png()

        if(toEPS):
            self.svg2eps()

        if not attr:
            attr = OrderedDict({})

        caption = pf.convert_text(caption)
        title = pf.convert_text(title)
        title = title[0]
        title_text = pf.stringify(title).strip()

        if doc.format in ["latex"]:
            linkto = self.pdf
        elif doc.format in ["html", "html5"]:
            linkto = self.svg
        else:
            linkto = self.png

        linkto = os.path.abspath(linkto).replace('\\', '/')
        caption = caption[0]
        caption = caption.content

        # pf.debug(caption)
        # pf.debug(linkto)
        # pf.debug(title_text)
        # pf.debug(label)
        # pf.debug(attr)
        img = pf.Image(*caption, url=linkto, title=title_text, attributes=attr)
        # pf.debug(img)
        ans = pf.Para(img)
        # pf.debug(ans)

        return ans


def main(doc=None):
    bf = BitField()
    return pf.run_filter(pf.yaml_filter, tag='bitfield', function=bf.generate, doc=doc)


if __name__ == "__main__":
    main()
