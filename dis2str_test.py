import unittest
from dis2str import *

class TestDis2Str(unittest.TestCase):

    def test_printable(self):
        for code in 0x20, 0x7e:
            self.assertTrue(printable(code))
        for c in '\n\r\t\b\v\f !09AZ~':
            self.assertTrue(printable(ord(c)))
        for code in -1, 0, 0x1f, 0x7f, 0x80, 0xff, 0x100, 0xff:
            self.assertFalse(printable(code))

    def test_code2str(self):
        for c,s in { 'a':'a', '\n':'\\n', chr(0):'\\x00', chr(0xff):'\\xff' }.items():
            self.assertTrue(code2str(ord(c)) == s)

    def test_hexa2data(self):
        self.assertTrue(data2str(hexa2data('61')) == 'a')
        self.assertTrue(data2str(hexa2data('61\tcomment')) == 'a')
        self.assertTrue(data2str(hexa2data('61 \tcomment')) == 'a')
        self.assertTrue(data2str(hexa2data('61  comment')) == 'a')
        self.assertTrue(data2str(hexa2data("61'comment")) == 'a')
        self.assertTrue(data2str(hexa2data("61 'comment")) == 'a')
        self.assertTrue(data2str(hexa2data('61"comment')) == 'a')
        self.assertTrue(data2str(hexa2data('61 "comment')) == 'a')
        self.assertTrue(data2str(hexa2data('61#comment')) == 'a')
        self.assertTrue(data2str(hexa2data('61 #comment')) == 'a')
        self.assertTrue(data2str(hexa2data('61//comment')) == 'a')
        self.assertTrue(data2str(hexa2data('61 //comment')) == 'a')
        self.assertTrue(data2str(hexa2data('61 62')) == 'ab')
        self.assertTrue(data2str(hexa2data('61 62 00')) == 'ab\\x00')
        self.assertTrue(data2str(hexa2data('61 0a 09')) == 'a\\n\\t')
        self.assertTrue(data2str(hexa2data('00 08 09\tcomment')) == '\\x00\\b\\t')
        self.assertTrue(data2str(hexa2data('61 62 09 \tcomment')) == 'ab\\t')
        self.assertTrue(data2str(hexa2data('61 62 09  comment')) == 'ab\\t')

    def test_parse(self):
        self.assertTrue(data2str(parse('09 61 62 63 \tcomment')[1]) == '\\tabc')
        self.assertTrue(data2str(parse('09 61 62 63\tcomment')[1]) == '\\tabc')
        self.assertTrue(data2str(parse('09 61 62 63\tcomment')[1]) == '\\tabc')
        self.assertTrue(data2str(parse('61 62 08 63 \tcomment')[1]) == 'ab\\bc')
        self.assertTrue(data2str(parse('61 62 08 63 \tcomment')[1]) == 'ab\\bc')
        self.assertTrue(data2str(parse('411824:	30 30                	xor    BYTE PTR [rax],dh')[1]) == '00')
        self.assertTrue(data2str(parse('     +:	30 30                	"00"')[1]) == '00') # oldstyle

    def test_strlen(self):
        self.assertTrue(strlen(hexa2data('00')) == 0)
        self.assertTrue(strlen(hexa2data('61')) == 1)
        self.assertTrue(strlen(hexa2data('61 62 08 63')) == 4)
        self.assertTrue(strlen(hexa2data('61 62 00 63')) == 2)

    def test_binlen(self):
        self.assertTrue(binlen(hexa2data('61')) == 0)
        self.assertTrue(binlen(hexa2data('00')) == 1)
        self.assertTrue(binlen(hexa2data('00 61')) == 1)
        self.assertTrue(binlen(hexa2data('00 01')) == 2)
        self.assertTrue(binlen(hexa2data('00 01 62 03')) == 2)

if __name__ == '__main__':
    unittest.main()
