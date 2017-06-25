---
include: [.,include]
---

## とあるテキスト(source.md)[^16]

```rotate
source: images/front-image.png
angle: 0
# caption: "*Awsome* image title"
attr:
  width: 20%
  height: 50%
---
```

***
![ **caption** ]( images/front-image.png ){width=50% }

<!-- ![ caption ]( ../images/front-image.png ){width=30% } -->

***

`import hoge`{.python}

***

<#include "another.md">
<#include "yet_another.md">

[^16]: ほげ

<!-- `````table
---
alignment: L
caption: "hello.c"
header: true
markdown: true
table-width: 1.0
# width:
---
hello.c
"~~~{.c}
#include <stdio.h>

void main(void){
  printf("Hello, World\n");
}
~~~
"
````` -->
