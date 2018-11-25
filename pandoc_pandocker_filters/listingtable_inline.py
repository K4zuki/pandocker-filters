#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" listingtable-inline
inline ListingTable filter which copies pointed external file
with adding title which is expected to use pandoc-crossref
applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

import os
import panflute as pf
from pandoc_pandocker_filters.ListingTable import ListingTable


class inline_listingtable(ListingTable):

    def __init__(self):
        super().__init__()

    def action(self, elem, doc, **args):
        self.doc = doc
        if isinstance(elem, (pf.Para)) and len(elem.content) == 1:
            for subelem in elem.content:
                if isinstance(subelem, pf.Link) and "listingtable" in subelem.classes:
                    self.counter -= 1
                    fn = subelem.url
                    options = subelem.attributes
                    idn = subelem.identifier
                    caption = subelem.content
                    # pf.debug(caption)
                    pf.debug("[inline] inline listingtable of", fn)
                    elem = self.listingtable(filename=fn, idn=idn, caption=caption, options=options)
                    # return ret
                    # elem = self.listingtable(subelem)
        return elem


def main(doc=None):
    lt = inline_listingtable()
    return pf.run_filter(lt.action, doc=doc)


def listed(doc=None):
    inline = inline_listingtable()
    block = ListingTable()
    return pf.run_filters([inline.action, pf.yaml_filter], tag="listingtable", function=block.action, doc=doc)


if __name__ == "__main__":
    main()
