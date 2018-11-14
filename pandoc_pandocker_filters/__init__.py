import panflute as pf
from . import aafigure_inline
from . import bitfield_inline
from . import listingtable_inline
from . import rotateimage_inline
from . import wavedrom_inline


def main(doc=None):
    aaf = aafigure_inline.inline_aafigure()
    bf = bitfield_inline.inline_bitfield()
    lt = listingtable_inline.inline_listingtable()
    roi = rotateimage_inline.rotateimage_inline()
    wd = wavedrom_inline.wavedrom_inline()
    pf.run_filters([aaf.action, bf.action, lt.action, roi.action, wd.action], doc=doc)
    return doc


if __name__ == "__main__":
    main()
