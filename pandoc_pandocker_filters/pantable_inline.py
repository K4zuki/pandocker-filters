#!/usr/bin/env python3

import csv
import panflute as pf
from attrdict import AttrDict
from pantable import pantable
import yaml


def get_tf(arg):
    if isinstance(arg, bool):
        return arg
    elif isinstance(arg, str):
        return True if arg.upper() in ["TRUE", "YES"] else False


class pantable_inline(object):
    def action(self, elem, doc):
        if isinstance(elem, (pf.Para)) and len(elem.content) == 1:
            for subelem in elem.content:
                if isinstance(subelem, pf.Link) and "table" in subelem.classes:
                    # options = {
                    #     "caption": string,
                    #     "alignment": string,
                    #     "width": list of float,
                    #     "table-width": float,
                    #     "header": bool,
                    #     "markdown": bool,
                    #     "include": string,
                    # }
                    options = subelem.attributes
                    idn = subelem.identifier
                    caption = subelem.content
                    fn = subelem.url

                    if options.get("width") is not None:
                        options["width"] = yaml.load(options.get("width"))
                    options["header"] = get_tf(options.get("header", True))
                    options["markdown"] = get_tf(options.get("markdown", False))
                    options["include"] = fn

                    pf.debug("[inline] inline pantable of", fn)

                    table = pantable.convert2table(options, None)
                    if not caption:
                        caption = [pf.Str(fn)]
                    if idn:
                        caption = [*caption, pf.Space(), pf.Str("{{#{}}}".format(idn))]
                    table.caption = caption
                    # pf.debug(table.caption)
                    return table


def main(doc=None):
    pti = pantable_inline()
    return pf.run_filter(pti.action, doc=doc)


if __name__ == "__main__":
    main()
