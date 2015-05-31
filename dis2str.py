#!/usr/bin/env python
# -*- cording:utf-8 -*-

import sys

HEXA_PER_LINE = 8

# Whitespace characters are '\n', '\r', '\t', '\b', '\v', '\f'.
WHITESPACE = {ord(eval("'\\"+c+"'")):'\\'+c for c in 'nrtbvf'}

def printable(code):
    return 0x20 <= code < 0x7f or (code in WHITESPACE)

def code2str(code):
    if code in WHITESPACE:
        return WHITESPACE[code]
    if printable(code):
        return chr(code)
    else:
        return '\\x%02x' % code

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
        line = line[:-1] + '\t' + comment
        yield line
        addr += HEXA_PER_LINE
        comment = ''

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

    def show(self):
        while len(self.data) > 0:
            size = strlen(self.data)
            if size > 0:
                # string data
                if self.data[-1] == 0:
                        comment = '"' + data2str(self.data[:size]) + '"'
                        size += 1  # skip the string terminator '\0'
                else:
                        comment = "'" + data2str(self.data[:size]) + "'"
            else:
                # binary data
                size = binlen(self.data)
                comment = ''
            print '\n'.join(dump(self.addr, self.addr_width, self.data[:size], comment))
            self.addr += size
            self.data = self.data[size:]
        self.__init__()

if __name__ == '__main__':
    disas = Disas()
    for line in sys.stdin:
        try:
            disas.append(line)
        except ValueError:
            if disas.data:
                if printable(disas.data[-1]):
                    disas.data += [0]
                disas.show()
            print line.rstrip()
    disas.show()
