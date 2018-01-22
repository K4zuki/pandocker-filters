# pandocker-filters

# What is this Repository for?
Yet another Pandoc filter package for Pandoc document converter, using
panflute library

# Install

`pip install git+https://github.com/K4zuki/pandocker-filters.git`

or

`pip install pandoc-pandocker-filters`

# Syntax
Base syntax is panflute's yaml-codeblock syntax.
Some of "-inline" filters use standard hyperlink syntax with options(and with limitation).

Note: **It used to have Image link syntax(`![caption](url){.filter}`) but now obsolete.**

~~~~~markdown
```listingtable
caption: Sample ListingTable
include: pandoc_pandocker_filters/ListingTable.py
---
```
<!-- inline syntax requires blank lines before and after statement -->
[Sample ListingTable-inline](pandoc_pandocker_filters/ListingTable.py){.listingtable}
<!-- inline syntax requires blank lines before and after statement -->
~~~~~

## pandocker-bitfield(-inline)
Renders "bitfield" image from YAML or JSON.

The filter calls bitfield randerer internally. It requires bitfield npm/nodeJS module.


### syntax
~~~~~markdown
```bitfield
caption: Sample BitField(use external file)
include: data/bit.yaml
---
```

```bitfield
caption: Sample BitField
---
# list from LSB
# bits: bit width
# attr: information RO/WO/RW etc.
# name: name of bitfield
- bits: 5
- bits: 1
  attr: RW
  name: IPO
- bits: 1
  attr: RW
  name: BRK
- bits: 1
  name: CPK
```

<!-- inline syntax requires blank lines before and after statement -->
[Sample BitField-inline](data/bit.yaml){.bitfield}
<!-- inline syntax requires blank lines before and after statement -->
~~~~~
### options

Table: BitField filter options

|  Parameters   | Optional |     Default     |      Purpose       |
|---------------|----------|-----------------|--------------------|
| `input`       | N        |                 | Source file name   |
| `png`         | Y        | **True**        | PNG output flag    |
| `eps`         | Y        | False           | EPS output flag    |
| `pdf`         | Y        | False           | PDF output flag    |
| `lane-height` | Y        | 80              | height (px/lane)   |
| `lane-width`  | Y        | 640             | width (px/lane)    |
| `lanes`       | Y        | 1               | number of lane     |
| `bits`        | Y        | 8               | Total bit width    |
| `fontfamily`  | Y        | source code pro | Font family name   |
| `fontsize`    | Y        | 16              | Font size          |
| `fontweight`  | Y        | normal          | Font weight        |
| `caption`     | Y        | Untitled(*)     | Caption            |
| `directory`   | Y        | `./svg`         | Output directory   |
| `attr`        | Y        |                 | additional options |

(**\***): Valid for yaml style syntax. URL link style uses link caption.

## pandocker-wavedrom-inline
The filter calls wavedrom randerer internally. requires wavedrom-cli and phantomJS npm modules

### syntax
~~~~~markdown
<!-- inline syntax requires blank lines before and after statement -->
[Sample WaveDrom-inline](data/wave.yaml){.wavedrom}
<!-- inline syntax requires blank lines before and after statement -->
~~~~~

### options

| Parameters | optional | default value |     purpose     |
|------------|----------|---------------|-----------------|
| `png`      | Y        | **True**      | PNG output flag |
| `eps`      | Y        | False         | EPS output flag |
| `pdf`      | Y        | False         | PDF output flag |

## pandocker-listingtable(-inline)
The filter includes a text file as codeblock. Default caption is filename itself.

### syntax

~~~~~markdown

```listingtable
source: data/table.csv
class: csv
tex: True
---
```

[](data/table.csv){.listingtable type=plain}

~~~~~
### options

Table: ListingTable options

| Parameters | Optional | default value |               purpose               |
|------------|----------|---------------|-------------------------------------|
| source     | N        |               | relative path to source file        |
| type       | N        | plain         | file type(python,cpp,markdown etc.) |
| from       | Y        | 1             | crop lines from                     |
| to         | Y        | (end of file) | crop lines to                       |

## pandocker-rotateimage(-inline)
rotates an image. positive number for CW, negative is CCW direction.
Can co-operate with `bitfield-inline`/`wavedrom-inline` filters

### syntax

`````markdown
[inline wavedrom rotation sample 30degree](data/waves/wave.yaml){.wavedrom .rotate angle=30}

[inline bitfield rotation sample -30degree](data/bitfields/bit.yaml){.bitfield .rotate angle=-30}
`````

### options

| Parameters | Optional | default value |           purpose            |
|------------|----------|---------------|------------------------------|
| angle      | N        |               | relative path to source file |

# References

- wavedrom: <http://wavedrom.com>
- bitfield: <https://github.com/drom/bitfield>
- aafigure: <https://github.com/aafigure/aafigure>

# License

MIT License (c) 2017-2018 Kazuki Yamamoto(k.yamamoto.08136891@gmail.com)
