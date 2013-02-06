import re
import unittest

from regexes.constants import ALT_BINARIES_TV

class TestRegexAltBinariesTv(unittest.TestCase):

    def setUp(self):
       self.patterns = [re.compile(regex) for regex in ALT_BINARIES_TV ]

    def get_info(self, data):
       for pattern in self.patterns:
           result = pattern.search(data)
           if result:
               return result

       return None

    def test_one(self):
        pattern = re.compile('\"(?P<name>.*\.rar)\".*\((?P<parts>\\d{1,3}\\/\\d{1,3})\)')
        data = 'Friends - Season 3 [093/101] - "Friends Season 3.part092.rar" yEnc (008/112)'
        result = self.get_info(data).groupdict()

        self.assertEqual(result['name'], 'Friends Season 3.part092.rar')
        self.assertEqual(result['parts'], '008/112')

    def test_two(self):
        pattern = re.compile('\"(?P<name>.*\.rar)\".*\((?P<parts>\\d{1,3}\\/\\d{1,3})\)')
        data = 'Giuliana.And.Bill.s03e04.Picking.Up.the.Pieces [04/32] - "Giuliana.And.Bill.s03e04.Picking.Up.the.Pieces.part02.rar" yEnc (17/41)'

        result = self.get_info(data).groupdict()
        self.assertEqual(result['name'], 'Giuliana.And.Bill.s03e04.Picking.Up.the.Pieces.part02.rar')
        self.assertEqual(result['parts'], '17/41')

    def test_three(self):
        pattern = re.compile('(?P<name>.*\.rar).*\((?P<parts>\\d{1,3}\\/\\d{1,3})\)')
        data = 'Top.Gear.19x02.720p.HDTV.x264-FoV.part01.rar (No password required)  yEnc  [02/42] (005/201)'
        result = pattern.search(data).groupdict()
        self.assertEqual(result['name'], 'Top.Gear.19x02.720p.HDTV.x264-FoV.part01.rar')
        self.assertEqual(result['parts'], '005/201')


if __name__ == '__main__':
    unittest.main()
