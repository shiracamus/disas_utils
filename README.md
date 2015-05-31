# disas_utils
Utilities for the objdump's disassemble outputs.

sample

```console
$ objdump -d -j .rodata /bin/ls | python dis2str.py

/bin/ls:     file format elf64-x86-64


Disassembly of section .rodata:

0000000000411820 <.rodata>:
  411820:       01 00 02 00             
  411824:       30 30 00                "00"
  411827:       6c 73 2e 63 00          "ls.c"
  41182c:       73 6f 72 74 5f 74 79 70 "sort_type != sort_version"
  411834:       65 20 21 3d 20 73 6f 72 
  41183c:       74 5f 76 65 72 73 69 6f 
  411844:       6e 00                   
  411846:       20 25 6c 75 00          " %lu"
  41184b:       25 2a 6c 75 20 00       "%*lu "
  411851:       3f 00                   "?"
  411853:       74 61 72 67 65 74 00    "target"
  41185a:       25 62 00                "%b"
  41185d:       25 73 20 25 2a 73 20 00 "%s %*s "
  411865:       20 20 00                "  "
  411868:       25 2a 73 2c 20 25 2a 73 "%*s, %*s "
  411870:       20 00                   
  411872:       20 2d 3e 20 00          " -> "
  411877:       63 61 6e 6e 6f 74 20 61 "cannot access %s"
  41187f:       63 63 65 73 73 20 25 73 
  411887:       00                      
  411888:       75 6e 6c 61 62 65 6c 65 "unlabeled"
  411890:       64 00                   
```

```console
$ objdump -D -Mintel /bin/ls > ls.dis
$ vi ls.dis
変換したい範囲の先頭行で ma
変換したい範囲の採集行で mb
:'a,'b!python dis2str.py
```
