import re
import unittest

from main import UsenetManager
from regexes import RegexRouter
from regexes.constants import REGEXES

class TestRegexRouter(unittest.TestCase):

    def setUp(self):
        self.group = UsenetManager.NewsGroup(*(None, ) * 4 + ('alt.binaries.tv', ))
        self.router = RegexRouter(self.group)


class TestRegexAltBinariesTv(unittest.TestCase):

    def setUp(self):
        self.group = UsenetManager.NewsGroup(*(None, ) * 4 + ('alt.binaries.tv', ))
        self.router = RegexRouter(self.group)

    def test_one(self):
        data = 'Friends - Season 3 [093/101] - "Friends Season 3.part092.rar" yEnc (008/112)'
        result = self.router.parse(data).groupdict()

        self.assertEqual(result['name'], 'Friends Season 3.part092.rar')
        self.assertEqual(result['parts'], '008/112')

    def test_two(self):
        data = 'Giuliana.And.Bill.s03e04.Picking.Up.the.Pieces [04/32] - "Giuliana.And.Bill.s03e04.Picking.Up.the.Pieces.part02.rar" yEnc (17/41)'
        result = self.router.parse(data).groupdict()

        self.assertEqual(result['name'], 'Giuliana.And.Bill.s03e04.Picking.Up.the.Pieces.part02.rar')
        self.assertEqual(result['parts'], '17/41')

    def test_three(self):
        data = 'Top.Gear.19x02.720p.HDTV.x264-FoV.part01.rar (No password required)  yEnc  [02/42] (005/201)'
        result = self.router.parse(data).groupdict()

        self.assertEqual(result['name'], 'Top.Gear.19x02.720p.HDTV.x264-FoV.part01.rar')
        self.assertEqual(result['parts'], '005/201')

    def test_four(self):
        data = 'Dream On S3 [05/58] - "dron s3.r03" yEnc (41/261)'
        result = self.router.parse(data).groupdict()

        self.assertEqual(result['name'], 'dron s3.r03')
        self.assertEqual(result['parts'], '41/261')




if __name__ == '__main__':
    unittest.main()
