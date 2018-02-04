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

applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

import os
import panflute as pf
from collections import OrderedDict
import json
import yaml
import hashlib
import datetime
from shutil import which
import subprocess
from attrdict import AttrDict
from bitfieldpy.bitfieldpy import BitField as BFP


class BitField(object):

    def __init__(self):

        self.unix = True if (os.name) != "nt" else False
        self.counter = 0
        self.pdfconvert = None
        self.pngconvert = None
        self.epsconvert = None
        if self.unix:
            # pf.debug(which("rsvg-convert"))
            self.pdfconvert = which("rsvg-convert")
            self.pngconvert = self.pdfconvert
            self.epsconvert = self.pdfconvert
        else:
            svg2png = which("svg2png")
            svg2pdf = which("svg2pdf")
            self.pdfconvert = "bash \'" + str(svg2pdf.replace("/c", "C:").replace(" ", "\ ")) + "\'"
            self.pngconvert = "bash \'" + str(svg2png.replace("/c", "C:").replace(" ", "\ ")) + "\'"
            pf.debug("non-UNIX OS!")
        self.defaultdir_to = "svg"
        self.svg = ""
        self.png = ""
        self.pdf = ""
        self.eps = ""
        self.doc = ""

    def json2svg(self):

        args = AttrDict({
            "input": self.source,
            "vspace": int(self.vspace),
            "hspace": int(self.hspace),
            "lanes": int(self.lanes),
            "bits": int(self.bits),
            "font_family": self.fontfamily,
            "font_size": self.fontsize,
            "font_weight": self.fontweight,
            "svg": self.svg
        })
        bfp = BFP(args)
        bfp.render()

    def svg2image(self):
        if(self.toPDF):
            self.svg2pdf()

        if(self.toPNG):
            self.svg2png()

        if(self.toEPS):
            self.svg2eps()

        if self.doc.format in ["latex"]:
            linkto = self.pdf
        elif self.doc.format in ["html", "html5"]:
            linkto = self.svg
        else:
            linkto = self.png

        self.linkto = os.path.abspath(linkto).replace("\\", "/")

    def svg2png(self):
        output = [self.pngconvert, self.svg]
        self.png = ".".join([str(self.basename), "png"])
        if self.unix:
            output.append("--format=png")
        output.append("--output")
        output.append(self.png)
        # pf.debug(" ".join(output))
        if not os.path.exists(self.png):
            subprocess.call(" ".join(output), shell=True)
        else:
            pf.debug("bypass conversion as output exists:", self.png)

    def svg2pdf(self):
        output = [self.pdfconvert, self.svg]
        self.pdf = ".".join([str(self.basename), "pdf"])
        if self.unix:
            output.append("--format=pdf")
        output.append("--output")
        output.append(self.pdf)
        # pf.debug(" ".join(output))
        if not os.path.exists(self.pdf):
            subprocess.call(" ".join(output), shell=True)
        else:
            pf.debug("bypass conversion as output exists:", self.pdf)

    def svg2eps(self):
        self.eps = ".".join([self.basename, "eps"])
        output = [self.epsconvert,
                  self.svg,
                  "--format=eps",
                  "--output",
                  self.eps
                  ]
        # pf.debug(" ".join(output))
        if not os.path.exists(self.eps):
            # renderPS.drawToFile(drawing, self.eps)
            pf.shell(" ".join(output))
        else:
            pf.debug("bypass conversion as output exists:", self.eps)

    def validatejson(self, data=""):
        ext = ""
        try:
            j = json.loads(data)
        except ValueError:
            # pf.debug("data is not json")
            try:
                data = json.dumps(yaml.load(data), indent=4)
            except ValueError:
                # pf.debug("data is not json nor yaml")
                raise
        return data

    def get_options(self, options, data, element, doc):
        self.doc = doc

        # pf.debug("get_options()")
        self.source = options.get("input")

        self.vspace = str(options.get("lane-height", 80))
        self.hspace = str(options.get("lane-width", 640))
        self.lanes = str(options.get("lanes", 1))
        self.bits = str(options.get("bits", 8))

        self.fontfamily = options.get("fontfamily", "source code pro")
        self.fontsize = str(options.get("fontsize", 16))
        self.fontweight = options.get("fontweight", "normal")

        self.caption = options.get("caption", "Untitled")
        self.dir_to = options.get("directory", self.defaultdir_to)

        if os.path.exists(self.dir_to) != 1:
            os.mkdir(self.dir_to)

        if not self.source and data is not None:
            # pf.debug("not source and data is not None")
            data = self.validatejson(data)
        else:  # source and data is "dont care"
            data = self.validatejson(open(self.source, "r", encoding="utf-8").read())

        self.counter = hashlib.sha1(data.encode("utf-8")).hexdigest()[:8]
        self.basename = "/".join([self.dir_to,
                                  str(self.counter)])

        self.source = ".".join([self.basename, "json"])
        open(self.source, "w", encoding="utf-8").write(data)

        self.attr = options.get("attr", {})
        self.title = options.get("title", "fig:")
        self.identifier = element.identifier
        self.label = options.get("label", os.path.splitext(os.path.basename(self.source))[0])

        self.toPNG = bool(options.get("png", True))
        self.toEPS = bool(options.get("eps", False))
        self.toPDF = True if doc.format in ["latex"] else bool(options.get("pdf", False))

        self.svg = ".".join([self.basename, "svg"])

        # pf.debug(isinstance(self.toPNG, bool))
        # pf.debug(self.toPDF)
        # pf.debug(doc.format)
        # pf.debug(self.bitfield)
        # pf.debug(self.source)
        # pf.debug(self.vspace)
        # pf.debug(self.hspace)
        # pf.debug(self.lanes)
        # pf.debug(self.bits)
        # pf.debug(self.fontfamily)
        # pf.debug(self.fontsize)
        # pf.debug(self.fontweight)

    def generate(self, options, data, element, doc):
        # pf.debug("generate()")

        self.get_options(options, data, element, doc)

        assert self.source is not None, "mandatory option input is not set"
        assert os.path.exists(self.source) == 1, "input file does not exist"
        assert isinstance(self.toPNG, bool), "option png is boolean"
        assert isinstance(self.toPDF, bool), "option pdf is boolean"
        assert isinstance(self.toEPS, bool), "option eps is boolean"

        self.json2svg()
        self.svg2image()

        if not self.attr:
            attr = OrderedDict({})

        caption = pf.convert_text(self.caption)
        title = pf.convert_text(self.title)
        title = title[0]
        title_text = pf.stringify(title).strip()

        caption = caption[0]
        caption = caption.content

        # pf.debug(caption)
        # pf.debug(linkto)
        # pf.debug(title_text)
        # pf.debug(label)
        # pf.debug(attr)
        pf.debug("generate bitfield from", self.linkto)
        # img = pf.Image(*caption, url=self.linkto, identifier=elem.identifier, title="fig:", attributes=attr)
        element.classes.remove("bitfield")
        img = pf.Image(*caption, classes=element.classes, url=self.linkto,
                       identifier=element.identifier, title="fig:", attributes=element.attributes)
        # pf.debug(img)
        ans = pf.Para(img)
        # pf.debug(ans)

        return ans


def main(doc=None):
    bf = BitField()
    return pf.run_filter(pf.yaml_filter, tag="bitfield", function=bf.generate, doc=doc)


if __name__ == "__main__":
    main()
