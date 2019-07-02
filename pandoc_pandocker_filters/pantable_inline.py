#!/usr/bin/env python3

import os
import panflute as pf
from pantable import pantable
import yaml
import csv


def get_tf(arg):
    if isinstance(arg, bool):
        return arg
    elif isinstance(arg, str):
        return True if arg.upper() in ["TRUE", "YES"] else False


def get_coord(xy):
    if xy is not None:
        # pf.debug(xy)
        if xy == -1:
            return None
        else:
            xy += 1
            return xy


BEGIN = (0, 0)
END = (None, None)


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
                    #     "subset_from": list[column(x), row(y)] x >= 1, y >= 1
                    #     "subset_to": list[column(x), row(y)] x >= 1, y >= 1
                    # }
                    options = subelem.attributes
                    idn = subelem.identifier
                    caption = subelem.content
                    fn = subelem.url

                    if options.get("width") is not None:
                        options["width"] = yaml.load(options.get("width"), Loader=yaml.SafeLoader)
                    options["header"] = get_tf(options.get("header", True))
                    options["markdown"] = get_tf(options.get("markdown", False))
                    options["include"] = fn
                    if options.get("subset_from") is not None:
                        subset_from = tuple(yaml.load(options.get("subset_from"), Loader=yaml.SafeLoader))
                        # pf.debug(subset_from)
                    else:
                        subset_from = BEGIN
                    if options.get("subset_to") is not None:
                        subset_to = tuple(yaml.load(options.get("subset_to"), Loader=yaml.SafeLoader))
                        # pf.debug(subset_to)
                    else:
                        subset_to = END
                    if subset_from != BEGIN or subset_to != END:
                        basedir, _ = os.path.split(os.path.abspath(fn))
                        subset = os.path.join(basedir, "_subset.csv")
                        y1, x1 = subset_from
                        y2, x2 = subset_to
                        if y1 == 0:
                            y1 = 1
                        y2 = get_coord(y2)

                        if x1 == 0:
                            x1 = 1
                        x2 = get_coord(x2)
                        pf.debug(x1, y1, x2, y2)

                        with open(fn, "r") as f:
                            reader = list(csv.reader(f))
                            with open(subset, "w") as wf:
                                writer = csv.writer(wf)
                                for item in reader[y1 - 1:y2]:
                                    writer.writerow(item[x1 - 1:x2])
                        options["include"] = subset

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
