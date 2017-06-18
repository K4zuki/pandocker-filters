#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Panflute filter to parse Any text in fenced YAML code blocks
http://scorreia.com/software/panflute/guide.html#yaml-code-blocks
"""

import io
import csv
import panflute as pf
import codecs


def fenced_action(options, data, element, doc):
    # We'll only run this for CodeBlock elements of class 'csv'
    pf.debug("")
    fn = options.get('path')
    with codecs.open(fn, 'r', 'utf-8') as f:
        pf.debug("fenced_action()")
        raw = f.read()
        # pf.debug(raw)

        new_elems = pf.convert_text(raw)
        pf.debug(new_elems)
        d = pf.Doc(*new_elems, format='md')
        pf.debug(d.content)
        e = pf.run_filter(pf.yaml_filter, tag='include', function=fenced_action,
                          doc=d)
        pf.debug(e.content)
        return new_elems


def main(doc=None):
    return pf.run_filter(pf.yaml_filter, tag='include', function=fenced_action,
                         doc=doc)


if __name__ == '__main__':
    main()
