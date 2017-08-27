#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pandoc filter using panflute
"""

import io
import csv
import panflute as pf
import codecs
# import pypandoc


def prepare(doc):
    pass


def action(elem, doc):
    # pf.debug("action()")
    if isinstance(elem, pf.Image):
        pf.debug(elem.attributes)
        pf.debug(elem.parent)
        pf.debug(elem.prev)
        pf.debug(elem.next)

    return None


def finalize(doc):
    pass


def main(doc=None):
    return pf.run_filter(action,
                         prepare=prepare,
                         finalize=finalize,
                         doc=doc)


if __name__ == '__main__':
    main()
