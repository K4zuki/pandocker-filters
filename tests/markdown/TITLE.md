```bitfield
# input: data/bitfields/bit.yaml
caption: _**block bitfield sample**_
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

![**inline bitfield sample**](data/bitfields/bit.yaml){.bitfield png=True pdf=True eps=True}

```listingtable
source: data/bitfields/bit.yaml
class: csv
tex: True
---
```

[](data/waves/wave.yaml){.listingtable type=plain}

![inline wavedrom sample](data/waves/wave.yaml){.wavedrom png=True pdf=True eps=True}

![inline wavedrom rotation sample 30degree](data/waves/wave.yaml){.wavedrom png=True pdf=True eps=True .rotate angle=30}

![inline bitfield rotation sample -30degree](data/bitfields/bit.yaml){.bitfield png=True pdf=True eps=True .rotate angle=-30}
