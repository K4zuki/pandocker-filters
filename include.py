#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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


def fenced_action(options, data, element, doc):
    # We'll only run this for CodeBlock elements of class 'listingtable'

    # pf.debug(doc.get_metadata('include', 'no hoge'))
    # pf.debug(element.parent)
    # pf.debug(element.index)
    # pf.debug(element.parent.content)

    # pf.debug(element.parent)
    # pf.debug(element.prev)
    # pf.debug(element)
    # pf.debug(element.next)

    fn = options.get('source')
    basename = os.path.basename(fn)
    isTex = options.get('tex', False)
    isDocx = options.get('isDocx', False)
    file_type = options.get('class', 'plain')
    types = [file_type, 'numberLines']
    # pf.debug(file_type, types)
    for doctype in [isTex, isDocx]:
        if not isinstance(doctype, bool):
            if isinstance(doctype, str):
                doctype = doctype.upper()
                if doctype in ['TRUE', 'YES']:
                    doctype = True
                else:
                    doctype = False
            else:
                doctype = False

    if isTex and isDocx:
        pass
    else:
        with codecs.open(fn, 'r', 'utf-8') as f:
            # pf.debug("codecs.open()")
            raw = f.read()
        # pf.debug(raw)

        label = basename.lower().replace(".", "_").replace("/", "_")
        anchor = "" if not isDocx else 'TC "[@lst:%s] %s" `\l` 6\n\n' % (label, basename)
        file_title = basename if not isTex else basename.replace("_", "\\\\\\_")
        # pf.debug(label, anchor, file_title)

        # header_caption = pf.Str("Listing: %s %s" % (file_title, anchor))
        header_block = pf.CodeBlock("", identifier="lst:%s" % (label), classes=["%s" % (file_type)])
        header_caption = [pf.Str("Listing:"), pf.Space(), pf.Str("%s" % (file_title))]
        # pf.debug(header_caption)

        # header = pf.Para(*header_block)
        read = pf.CodeBlock(raw, classes=types, attributes={"numbers": "left"})

        cell = pf.TableCell(pf.Para(*header_caption), header_block)
        # pf.debug(cell)
        row = [pf.TableRow(cell)]
        # pf.debug(row)
        table = pf.Table(*row, alignment=['AlignDefault'], width=[1])
        # element.container.insert(element.index + 1, read)
        # element.container.insert(element.index + 1, table)
        # element.container.pop(element.index)

        # return []
        return [table, read]


def main(doc=None):
    return pf.run_filter(pf.yaml_filter, tag='listingtable', function=fenced_action,
                         doc=doc)


if __name__ == '__main__':
    main()
