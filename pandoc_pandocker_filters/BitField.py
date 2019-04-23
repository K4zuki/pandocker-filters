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

applies MIT License (c) 2017-2019 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

import os
import panflute as pf
from collections import OrderedDict
import json
import yaml
import hashlib
from shutil import which
import subprocess
import wavedrom.bitfield as bitfield


class BitField(object):
    defaultdir_to = "svg"
    svg_filename = ""
    png_filename = ""
    pdf_filename = ""
    eps_filename = ""
    doc = ""
    counter = 0
    pdfconvert = None
    pngconvert = None
    epsconvert = None

    def __init__(self):

        self.unix = True if (os.name) != "nt" else False
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

    def json2svg(self):

        with open(self.source, "r") as f:
            output = bitfield.BitField().render(json.loads(f.read()), self.options)
            output.saveas(self.svg_filename)

    def render_images(self):
        if (self.convert_to_pdf):
            self.render_pdf()

        if (self.convert_to_png):
            self.render_png()

        if (self.convert_to_eps):
            self.render_eps()

        if self.doc.format in ["latex"]:
            linkto = self.pdf_filename
        elif self.doc.format in ["html", "html5"]:
            linkto = self.svg_filename
        else:
            linkto = self.png_filename

        self.linkto = os.path.abspath(linkto).replace("\\", "/")

    def render_png(self):
        command_stack = [self.pngconvert, self.svg_filename]
        self.png_filename = ".".join([str(self.basename), "png"])
        if self.unix:
            command_stack.append("--format=png")
        command_stack.append("--output")
        command_stack.append(self.png_filename)
        # pf.debug(" ".join(output))
        if not os.path.exists(self.png_filename):
            subprocess.call(" ".join(command_stack), shell=True)
        else:
            pf.debug("bypass conversion as output exists:", self.png_filename)

    def render_pdf(self):
        command_stack = [self.pdfconvert, self.svg_filename]
        self.pdf_filename = ".".join([str(self.basename), "pdf"])
        if self.unix:
            command_stack.append("--format=pdf")
        command_stack.append("--output")
        command_stack.append(self.pdf_filename)
        # pf.debug(" ".join(output))
        if not os.path.exists(self.pdf_filename):
            subprocess.call(" ".join(command_stack), shell=True)
        else:
            pf.debug("bypass conversion as output exists:", self.pdf_filename)

    def render_eps(self):
        self.eps_filename = ".".join([self.basename, "eps"])
        command_stack = [self.epsconvert,
                         self.svg_filename,
                         "--format=eps",
                         "--output",
                         self.eps_filename
                         ]
        # pf.debug(" ".join(output))
        if not os.path.exists(self.eps_filename):
            # renderPS.drawToFile(drawing, self.eps)
            pf.shell(" ".join(command_stack))
        else:
            pf.debug("bypass conversion as output exists:", self.eps_filename)

    def validatejson(self, data=""):
        """ Test source string whether genuine JSON or YAML
        If `data` is JSON format string, return as-is; if YAML format, convert to JSON and return

        :param string data: source string under validation
        :return data: JSON format string
        """

        try:
            j = json.loads(data)
        except ValueError:
            # pf.debug("data is not json")
            try:
                data = json.dumps(yaml.load(data, Loader=yaml.SafeLoader), indent=4)
            except ValueError:
                # pf.debug("data is not json nor yaml")
                raise
        return data

    def get_options(self, options, data, element, doc):
        self.doc = doc

        # pf.debug("get_options()")
        self.source = options.get("input")
        self.options = bitfield.Options(
            vspace=int(options.get("lane-height", 80)),
            hspace=int(options.get("lane-width", 640)),
            lanes=int(options.get("lanes", 1)),
            bits=int(options.get("bits", 8)),
            fontfamily=options.get("fontfamily", "source code pro"),
            fontsize=int(options.get("fontsize", 16)),
            fontweight=options.get("fontweight", "normal")
        )

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

        self.convert_to_png = bool(options.get("png", True))
        self.convert_to_eps = bool(options.get("eps", False))
        self.convert_to_pdf = True if doc.format in ["latex"] else bool(options.get("pdf", False))

        self.svg_filename = ".".join([self.basename, "svg"])

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
        assert isinstance(self.convert_to_png, bool), "option png is boolean"
        assert isinstance(self.convert_to_pdf, bool), "option pdf is boolean"
        assert isinstance(self.convert_to_eps, bool), "option eps is boolean"

        self.json2svg()
        self.render_images()

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
