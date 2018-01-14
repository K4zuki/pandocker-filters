```{.bitfield #fig:block-bitfield}
# input: data/bitfields/bit.yaml
caption: _**block bitfield sample**_
png: True
pdf: True
eps: True
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

ref to [@fig:block-bitfield]

![**inline bitfield sample**](data/bitfields/bit.yaml){.bitfield png=True pdf=True eps=True #fig:inline-bitfield}

ref to [@fig:inline-bitfield]

```{.listingtable #lst:block-listingtable}
source: data/bitfields/bit.yaml
class: csv
tex: True
---
```
ref to [@lst:block-listingtable]

[](data/waves/wave.yaml){.listingtable type=plain #lst:inline-listingtable}

ref to [@lst:inline-listingtable]

![inline wavedrom sample by image link](data/waves/wave.yaml){.wavedrom png=True pdf=True eps=True}

[inline wavedrom sample by hyperlink](data/waves/wave.yaml){.wavedrom png=True pdf=True eps=True}

[other inline wavedrom sample by hyperlink](data/waves/anotherwave.yaml){.wavedrom png=True pdf=True eps=True}

[another inline wavedrom sample by hyperlink](data/waves/wave.yaml){.wavedrom png=True pdf=True eps=True}

[inline wavedrom rotation sample 45degree by hyperlink](data/waves/wave.yaml){.wavedrom png=True pdf=True eps=True .rotate angle=45}

![inline wavedrom rotation sample 30degree](data/waves/wave.yaml){.wavedrom png=True pdf=True eps=True .rotate angle=30}

![inline bitfield rotation sample -30degree](data/bitfields/bit.yaml){.bitfield png=True pdf=True eps=True .rotate angle=-30}

```{.bitfield .rotate angle=-45}
# input: data/bitfields/bit.yaml
caption: _**block bitfield rotation sample -45degree**_
png: True
pdf: True
eps: True
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
