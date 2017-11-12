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
                    self.doc = doc
                    self.counter -= 1
                    # pf.debug("inline_listingtable.action()")
                    # pf.debug(subelem)
                    fn = subelem.url
                    # pf.debug(fn)
                    basename = os.path.basename(fn)
                    label = basename.lower().replace(".", "_").replace("/", "_") + str(self.counter)

                    options = subelem.attributes
                    # pf.debug(options)
                    file_type = options.get('type', 'plain')
                    # pf.debug(file_type)

                    types = [file_type, 'numberLines']

                    file_title = basename
                    if self.doc.format in ["latex"]:
                        file_title = basename.replace("_", "\textunderscore")

                    header_caption = pf.Para(pf.Str("Listing:"), pf.Space(), pf.Str("%s" % (file_title)))

                    with open(fn, 'r', encoding='utf-8') as f:
                        raw = f.read()
                        # data = self.validatejson(data)
                    read = pf.CodeBlock(raw, classes=types, identifier="lst:%s" %
                                        (label), attributes={"numbers": "left"})

                    pf.debug("inline listingtable of", fn)
                    ret.append(header_caption)
                    ret.append(read)
            return ret


def main(doc=None):
    lt = inline_listingtable()
    return pf.run_filter(lt.action, doc=doc)


if __name__ == '__main__':
    main()
