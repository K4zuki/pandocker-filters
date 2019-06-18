#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" pandoc-listingtable
Panflute filter to parse Any text in fenced YAML code blocks
http://scorreia.com/software/panflute/guide.html#yaml-code-blocks

block shape looks like this:

```listingtable
source: <relative path to file to include>
class: source file type
tex: True if rendering in tex mode; exclusive with docx
docx: True if rendering in docx mode; exclusive with tex
---
```

applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)

"""

import io
import csv
import panflute as pf
import codecs
import os

"""
    _type = type

    _label = _basename.lower().replace(".", "_")
    _label = _label.replace("/", "_")
    anchor = "" if not isDocx else 'TC "[@lst:%s] %s" `\l` 6\n\n' % (_label, _basename)

    _file_title = _basename if not isTex else _basename.replace("_", "\\\\\\_")

    _list = ["Listing: %s %s" % (_file_title, anchor),
             "```{#lst:%s %s}" % (_label, _type),
             "```"]

+--------------------------------------------------------------------------------+
|Listing: table.csv                                                              |
|```{#lst:table_csv .csv}                                                        |
|```                                                                             |
+--------------------------------------------------------------------------------+

```{.csv .numberLines numbers="left"}
this,is,a table,"multi\
line\
title"
to,show,an,example
of,table,markdown,"importer\
of\
multiline"
```

Table(TableRow(
TableCell(Para(Str(Listing: ) Space Str(table.csv))
CodeBlock(
identifier='lst:table_csv', classes=['csv'])))
alignment=['AlignDefault'], width=[1], rows=1, cols=1)
"""


class ListingTable(object):

    def __init__(self):
        self.counter = 0

    def action(self, options, data, element, doc):
        self.doc = doc
        self.counter += 1
        # We'll only run this for CodeBlock elements of class "listingtable"

        fn = options.get("source")
        idn = element.identifier
        caption = options.get("caption", "")
        if len(caption):
            caption = pf.convert_text(caption)[0].content
        pf.debug("listingtable of", fn)
        ret = self.listingtable(filename=fn, idn=idn, caption=caption, options=options)
        return ret

    def listingtable(self, filename, idn, caption, options):
        if self.doc.format in ["latex"]:
            for c in caption:
                if isinstance(c, (pf.Str)):
                    c.text = c.text.replace("_", r"\textunderscore ")
                    # pf.debug(c.text)
        basename = os.path.basename(filename)  # /path/to/file.txt -> file.txt
        file_type = options.get("type", "plain")
        types = [file_type, "numberLines"]
        startFrom = options.get("startFrom", "1")
        numbers = options.get("numbers", "left")
        attr = {"startFrom": startFrom, "numbers": numbers}
        linefrom = options.get("from")
        lineto = options.get("to")
        linefrom = None if not linefrom else (int(linefrom) - 1)
        lineto = None if not lineto else (int(lineto))

        if self.doc.format in ["latex"]:
            file_title = basename.replace("_", r"\textunderscore")
        else:
            file_title = basename

        temp_caption = [pf.Str("%s" % (file_title))]
        caption = temp_caption if not len(caption) else caption

        with open(filename, "r", encoding="utf-8") as f:
            lines = list(f)
        if (not linefrom) and (not lineto):
            raw = "".join(lines)
        elif linefrom and (not lineto):
            raw = "".join(lines[linefrom:])
        elif not linefrom and lineto:
            raw = "".join(lines[:lineto])
        else:
            raw = "".join(lines[linefrom:lineto])

        # pf.debug(linefrom, lineto, raw)
        label = basename.lower().replace(".", "_").replace("/", "_") + str(self.counter)
        idn = idn if idn else "lst:{label:s}".format(label=label)

        read = pf.CodeBlock(raw, classes=types, identifier=idn, attributes=attr)

        ret = [pf.Para(pf.Str("Listing:"), pf.Space(), *caption), read]
        return ret


def main(doc=None):
    lt = ListingTable()
    return pf.run_filter(pf.yaml_filter, tag="listingtable", function=lt.action, doc=doc)


if __name__ == "__main__":
    main()
