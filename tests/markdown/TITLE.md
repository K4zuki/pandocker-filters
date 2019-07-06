```{.aafigure #fig:block-aafigure}
# input: data/bitfields/bit.yaml
caption: _**block aafigure sample**_
png: True
pdf: True
---
A   B
 AA   BB
 AA   BB

  ---- |         ___  ~~~|
       | --  ___|        |    ===
                         ~~~
/-------\\
| "foo" |
+-------+
| "bar" |
\\-------/
                                     +
      |  -  +   |  -  +   |  -  +   /               -
     /  /  /   /  /  /   /  /  /   /     --     |/| /    +
    |  |  |   +  +  +   -  -  -   /     /  \\        -   \\|/  |\\
                                 +     +    +          +-+-+ | +
    |  |  |   +  +  +   -  -  -   \\     \\  /        -   /|\\  |/
     \\  \\  \\   \\  \\  \\   \\  \\  \\   \\     --     |\\| \\    +
      |  -  +   |  -  +   |  -  +   \\               -
                                     +

    --->   | | | | | |
    ---<   | | | | | |
    ---o   ^ V v o O #
    ---O
    ---#
```

[inline aafigure sample](data/aafigure.txt){.aafigure png=True pdf=True eps=True}

<!--
```{.bitfield #fig:block-bitfield}
# input: data/bitfields/bit.yaml
caption: _**block bitfield sample**_
png: True
pdf: True
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
-->

ref to [@fig:block-bitfield]

[**inline bitfield sample**](data/bitfields/bit.json){.bitfield png=True pdf=True eps=True #fig:inline-bitfield}

ref to [@fig:inline-bitfield]

[**inline _hyperlink_ bitfield sample**](data/bitfields/bit.yaml){.bitfield png=True pdf=True eps=True #fig:inline-hyper-bitfield}

ref to [@fig:inline-hyper-bitfield]

<!--
```{.listingtable #lst:block-listingtable}
source: data/bitfields/bit.yaml
class: csv
tex: True
---
```
ref to [@lst:block-listingtable]
-->

[](data/waves/wave.yaml){.listingtable type=plain #lst:inline-listingtable}

ref to [@lst:inline-listingtable]


[inline wavedrom sample](data/waves/wave.yaml){.wavedrom png=True pdf=True}

[返却パケット](data/waves/commandSandP_wo_ret.yaml){.wavedrom}

[_8bit_ スレーブアドレス0x80に4バイト書込む コマンドパケット例](data/waves/commandSandP_wo.yaml){.wavedrom}

[該当するI^2^Cバスの動き](data/waves/commandSandP_wo_bus.yaml){.wavedrom}

[other inline wavedrom sample](data/waves/anotherwave.yaml){.wavedrom png=True pdf=True}

[another inline wavedrom sample](data/waves/wave.yaml){.wavedrom png=True pdf=True}

[inline wavedrom rotation sample 45degree ](data/waves/commandSandP_wo_bus.yaml){.wavedrom png=True pdf=True .rotate angle=45}

[inline wavedrom rotation sample 30degree](data/waves/wave.yaml){.wavedrom png=True pdf=True .rotate angle=30}

[inline bitfield rotation sample -30degree](data/bitfields/bit.yaml){.bitfield png=True pdf=True .rotate angle=-30}

<!--
```{.bitfield .rotate angle=-45}
# input: data/bitfields/bit.yaml
caption: _**block bitfield rotation sample -45degree**_
png: True
pdf: True
bits: 32
lanes: 2
---
[
    { "name": "IPO",   "bits": 8, "attr": "RO" },
    {                  "bits": 7 },
    { "name": "BRK",   "bits": 5, "attr": "RW" },
    { "name": "CPK",   "bits": 1 },
    { "name": "Clear", "bits": 3 },
    {                  "bits": 8 }
]
```
-->

[inline pantable sample](data/items.csv){.table #tbl:table markdown=True
                                         subset_from=[1,1] subset_to=[5,5]}

ref to [@tbl:table]
