#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pandoc filter using panflute
applies MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
"""

import io
import csv
import panflute as pf
import codecs
# import pypandoc


def prepare(doc):
    pass


def action(elem, doc):
    pf.debug("action()")
    if isinstance(elem, pf.Para):

        # pf.debug(elem)
        e = elem.walk(make_emph)
        # pf.debug(e)
        pf.debug(e.content)

        # return e.content
    # pf.debug("")


def make_emph(elem, doc):
    if isinstance(elem, pf.Code) and 'include' in elem.classes:
        pf.debug("\tmake_emph()")
        fn = elem.text
        with codecs.open(fn, 'r', 'utf-8') as f:
            raw = f.read()

            new_elems = pf.convert_text(raw)
            # i = (item.walk(make_emph, doc) for item in new_elems)
            # pf.debug(i)
            d = pf.Doc(*new_elems, format='md')
            e = d.walk(make_emph)
            pf.debug(e.content)
            return e.content
        # return new_elems
    pf.debug("")
    # return pf.Emph(elem)
    # data = pypandoc.convert_file(fn, 'json')
    # _doc = pf.load(io.StringIO(data))
    # _doc = pf.run_filter(action, prepare=prepare, doc=_doc)
    # return _doc


def finalize(doc):
    pass


def main(doc=None):
    return pf.run_filter(action,
                         prepare=prepare,
                         finalize=finalize,
                         doc=doc)


if __name__ == '__main__':
    main()
