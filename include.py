#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Panflute filter to parse Any text in fenced YAML code blocks
http://scorreia.com/software/panflute/guide.html#yaml-code-blocks

block shape looks like this:

```{.include}
path: <relative path to file to include>
---
```

"""

import io
import csv
import panflute as pf
import codecs


def fenced_action(options, data, element, doc):
    # We'll only run this for CodeBlock elements of class 'include'
    # pf.debug("\nfenced_action() at %d" % (element.index))
    # pf.debug(element.parent.content.list)
    # element.parent.content.list.pop(element.index)
    # pf.debug(element.parent.content.list)
    # element.index = element.parent.content.list.index(element)
    fn = options.get('path')
    with codecs.open(fn, 'r', 'utf-8') as f:
        pf.debug("\tcodecs.open()")
        raw = f.read()
        # pf.debug(raw)

        new_elems = pf.convert_text(raw)
        # pf.debug(new_elems)
    d = pf.Doc(*new_elems, format='md')
    pf.debug(d.content.list)

    if element.parent.content:
        element.parent.content.list.pop(element.index)
        # e = pf.run_filter(pf.yaml_filter, tag='include', function=fenced_action, doc=d)
        # pf.debug(e.content)

        pf.debug(d.content.list)
        for _d in reversed(d.content.list):
            e = pf.yaml_filter(_d, doc=d, tag='include', function=fenced_action)
            element.parent.content.list.insert(_d, element.index)
            # pf.debug(_d)

        # return e.content


def main(doc=None):
    return pf.run_filter(pf.yaml_filter, tag='include', function=fenced_action,
                         doc=doc)


if __name__ == '__main__':
    main()

'''
source.md
    |- another.md
    |   `- yet_another.md
    `- yet_another.md
'''
