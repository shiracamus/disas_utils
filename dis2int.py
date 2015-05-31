#!/usr/bin/env python
# -*- cording:utf-8 -*-

# Author: @shiracamus

import sys
import struct

HEXA_PER_LINE = 8

# Whitespace characters are '\n', '\r', '\t', '\b', '\v', '\f'.
WHITESPACE = {ord(eval("'\\"+c+"'")):'\\'+c for c in 'nrtbvf'}

def printable(code):
    return 0x20 <= code < 0x7f or (code in WHITESPACE)

def code2str(code):
    if code in WHITESPACE:
        #return WHITESPACE[code]
        return '.'
    if printable(code):
        return chr(code)
    else:
        return '.'

def hexa2data(hexa):
    hexa = hexa.strip()
    for separator in '\t','  ','"',"'",'#','//':
        if separator in hexa:
            hexa = hexa.split(separator, 1)[0]
    return [int(x, 16) for x in hexa.split()]

def parse(line):
    addr, hexa = 0, line.strip()
    if ':' in hexa:
        addr, hexa = line.split(':', 1)
        addr = 0 if addr.strip() == '+' else int(addr, 16)
    return addr, hexa2data(hexa)

def data2str(data):
    return ''.join(map(code2str, data))
 
def strlen(data):
    for size in xrange(len(data)):
        if not printable(data[size]): return size
    return len(data)
 
def binlen(data):
    for size in xrange(len(data)):
        if printable(data[size]): return size
    return len(data)

def dump(addr, addr_width, data, comment = None):
    for offset in xrange(0, len(data), HEXA_PER_LINE):
        line = '%*x:\t' % (addr_width, addr)
        for i in xrange(offset, offset + HEXA_PER_LINE):
            if i < len(data):
                line += '%02x ' % data[i]
            else:
                line += '   '
        if comment:
            line += '\t' + comment
            comment = None
        yield line
        addr += HEXA_PER_LINE
        comment = ''

BYTES_PER_LINE = 4
PADDING = '\0'*BYTES_PER_LINE

def unpack(format, data):
    return struct.unpack(format, (''.join(map(chr, data))+PADDING)[:BYTES_PER_LINE])[0]

def data2int(data):
    return unpack('<i', data)

def data2uint(data):
    return unpack('<I', data)

class Disas:
    def __init__(self):
        self.addr = 0
        self.addr_width = 8
        self.data = [] 

    def append(self, line):
        addr, data = parse(line)
        if not self.addr:
            self.addr = addr
            self.addr_width = line.index(':')
	self.data += data

    def show_int(self):
        addr = self.addr
        addr_width = self.addr_width
        for i in range(0, len(self.data), BYTES_PER_LINE):
            data = self.data[i:i+BYTES_PER_LINE]
            comment = "# %-6s, 0x%08x, %d" % ('"'+data2str(data)+'"', data2uint(data), data2int(data))
            for line in dump(addr, addr_width, data, comment):
                print line
            addr += BYTES_PER_LINE
        self.__init__()

if __name__ == '__main__':
    disas = Disas()
    for line in sys.stdin:
        try:
            disas.append(line)
        except ValueError:
            disas.show_int()
            print line.rstrip()
    disas.show_int()
