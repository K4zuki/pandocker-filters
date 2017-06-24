#!/usr/bin/env python

"""
modifying https://github.com/sergiocorreia/panflute-filters/filters/figure.py
to rotate given image by desired angle
"""

# ---------------------------
# Imports
# ---------------------------

import os
from string import Template

import panflute as pf
from PIL import Image

# ---------------------------
# Functions
# ---------------------------


def prepare(doc):
    pass


def finalize(doc):
    pass


def rotate(filename="", angle=0):

    with Image.open(filename) as img:
        path, ext = os.path.splitext(filename)
        if(angle == 0):
            pass
        elif(angle == 90):
            tmp = img.transpose(Image.ROTATE_90)
            filename = "%s_r+090%s" % (path, ext)
        elif(angle == 180 or angle == -180):
            tmp = img.transpose(Image.ROTATE_180)
            filename = "%s_r180%s" % (path, ext)
        elif(angle == 270 or angle == -90):
            tmp = img.transpose(Image.ROTATE_270)
            filename = "%s_r-090%s" % (path, ext)
        else:
            angle = angle % 360
            if(angle < 0):
                angle = 360 - abs(angle)
            # print angle
            tmp = img.rotate(angle, expand=True)
            filename = "%s_r%+03d%s" % (path, angle, ext)
        if not os.path.exists(filename):
            tmp.save(filename)

        # pf.debug("rotate()", angle, filename)
    return filename


def figure(options, data, element, doc):

    # Get options
    fn = os.path.abspath(options['source']).replace('\\', '/')
    title = options.get('title', '')
    caption = options.get('caption', '')
    label = options.get('label', os.path.splitext(os.path.basename(fn))[0])
    notes = data
    angle = options.get('angle', 0)

    fn = rotate(fn, angle)
    title = pf.convert_text(title)
    caption = pf.convert_text(caption)
    assert len(title) == 1, title

    title = title[0]
    title_text = pf.stringify(title).strip()

    caption = caption[0]
    caption = caption.content

    # pf.debug(title)

    # notes = pf.Div(*pf.convert_text(notes), classes=['note'])
    img = pf.Image(*caption, url=fn, title=title_text, identifier=label, attributes={})
    # ans = pf.Div(pf.Plain(img), pf.Plain(pf.LineBreak), notes, classes=['figure'])
    ans = pf.Para(img)
    return ans


def main(doc=None):
    return pf.run_filter(pf.yaml_filter, tag='rotate', function=figure,
                         doc=doc)


# ---------------------------
# Main
# ---------------------------

if __name__ == "__main__":
    main()
