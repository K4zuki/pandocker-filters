#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" listingtable-inline
inline ListingTable filter which copies pointed external file
with adding title which is expected to use pandoc-crossref
"""

import os
import panflute as pf
from ListingTable import ListingTable


class inline_listingtable(ListingTable):

    def __init__(self):
        super().__init__()

    def action(self, elem, doc):
        ret = []
        if isinstance(elem, pf.Para) and isinstance(elem.content[0], pf.Image):
            # if isinstance(elem, pf.Image):
            for subelem in elem.content:
                # subelem = elem.content[0]
                # pf.debug(isinstance(elem.content[0], pf.Image))
                if isinstance(subelem, pf.Image) and 'listingtable' in subelem.classes:
                    index = elem.content.index(subelem)
                    pf.debug(index)
                    self.doc = doc
                    self.counter -= 1
                    # pf.debug("inline_listingtable.action()")
                    # pf.debug(subelem)
                    fn = subelem.url
                    options = subelem.attributes
                    idn = subelem.identifier
                    caption = subelem.content
                    # pf.debug(fn)
                    # pf.debug(options)
                    # pf.debug(idn)
                    # pf.debug(len(caption))
                    basename = os.path.basename(fn)
                    label = basename.lower().replace(".", "_").replace("/", "_") + str(self.counter)
                    idn = idn if idn else "lst:{label:s}".format(label=label)

                    file_type = options.get('type', 'text')
                    # pf.debug(file_type)

                    types = [file_type, 'numberLines']

                    file_title = basename
                    if self.doc.format in ["latex"]:
                        file_title = basename.replace("_", "\textunderscore")
                    caption = [pf.Str("%s" % (file_title))] if not len(caption) else caption
                    header_caption = pf.Para(pf.Str("Listing:"), pf.Space(), *caption)

                    with open(fn, 'r', encoding='utf-8') as f:
                        raw = f.read()
                        # data = self.validatejson(data)
                    attr = {"numbers": "left"}
                    read = pf.CodeBlock(raw, classes=types, identifier=idn, attributes=attr)

                    pf.debug("inline listingtable of", fn)
                    ret.append(header_caption)
                    ret.append(read)
            return ret


def main(doc=None):
    lt = inline_listingtable()
    return pf.run_filter(lt.action, doc=doc)


if __name__ == '__main__':
    main()
