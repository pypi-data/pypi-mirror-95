import unittest

from kanjize import kanji2int, int2kanji, Number


class TestKanjize(unittest.TestCase):
    """
    test class of kanjize
    """

    def testkanji2int(self):
        self.assertEqual(1, kanji2int("一"))
        self.assertEqual(10, kanji2int("十"))
        self.assertEqual(11, kanji2int("十一"))
        self.assertEqual(111, kanji2int("百十一"))
        self.assertEqual(211, kanji2int("二百十一"))
        self.assertEqual(121, kanji2int("百二十一"))
        self.assertEqual(11, kanji2int("十一"))
        self.assertEqual(111, kanji2int("百十一"))
        self.assertEqual(211, kanji2int("二百十一"))
        self.assertEqual(121, kanji2int("百二十一"))
        self.assertEqual(1000, kanji2int("千"))
        self.assertEqual(1001, kanji2int("千一"))
        self.assertEqual(2025, kanji2int("二千二十五"))
        self.assertEqual(58076099, kanji2int("五千八百七万六千九十九"))

        # added 1.0.0
        self.assertEqual(10000000000000000000000000000000000000000000000000000, kanji2int("一恒河沙"))
        self.assertEqual(
            999999999999999999999999999999999999999999999999999999999999999999999999,
            kanji2int("九千九百九十九無量大数九千九百九十九不可思議九千九百九十九那由多九千九百九十九阿僧祇九千九百九十九恒河沙九千九百九十九極"
                      "九千九百九十九載九千九百九十九正九千九百九十九澗九千九百九十九溝九千九百九十九穣九千九百九十九𥝱九千九百九十九垓"
                      "九千九百九十九京九千九百九十九兆九千九百九十九億九千九百九十九万九千九百九十九")
        )

        self.assertEqual(1, kanji2int("1", style="mixed"))
        self.assertEqual(10, kanji2int("10", style="mixed"))
        self.assertEqual(11, kanji2int("11", style="mixed"))
        self.assertEqual(121, kanji2int("121", style="mixed"))
        self.assertEqual(1000, kanji2int("1千", style="mixed"))
        self.assertEqual(1001, kanji2int("1001", style="mixed"))
        self.assertEqual(2025, kanji2int("2025", style="mixed"))
        self.assertEqual(58076099, kanji2int("5807万6099", style="mixed"))
        self.assertEqual(223423542566000, kanji2int("223兆4235億4256万6千", style="mixed"))
        self.assertEqual(223400042566000, kanji2int("223兆4千億4256万6千", style="mixed"))
        self.assertEqual(50000000000000000000, kanji2int("5千京", style="mixed"))
        self.assertEqual(394385000048950000, kanji2int("39京4385兆4895万", style="mixed"))

        # added 0.2.1
        self.assertEqual(1001, kanji2int("千1", style="mixed"))
        self.assertEqual(2025, kanji2int("2千2十5", style="mixed"))
        self.assertEqual(4000000, kanji2int("4百万", style="mixed"))
        self.assertEqual(58076099, kanji2int("58百7万6千99", style="mixed"))
        self.assertEqual(223423542566000, kanji2int("2百23兆4千2百3十5億4256万6千", style="mixed"))
        self.assertEqual(223400042566000, kanji2int("223兆4千億4256万6千", style="mixed"))
        self.assertEqual(223400042566000, kanji2int("2234千億4256万6千", style="mixed"))
        self.assertEqual(50500000000000000000, kanji2int("5千5十京", style="mixed"))
        self.assertEqual(394385000048950000, kanji2int("39京4385兆4895万", style="mixed"))

        # added 1.0.0
        self.assertEqual(10000000000000000000000000000000000000000000000000000, kanji2int("1恒河沙", style="mixed"))
        self.assertEqual(
            999999999999999999999999999999999999999999999999999999999999999999999999,
            kanji2int("9999無量大数9999不可思議9999那由多9999阿僧祇"
                      "9999恒河沙9999極9999載9999正9999澗9999溝9999穣"
                      "9999𥝱9999垓9999京9999兆9999億9999万9999")
        )

    def testint2kanji(self):
        self.assertEqual(int2kanji(1), "一", "all")
        self.assertEqual(int2kanji(10), "十", "all")
        self.assertEqual(int2kanji(11), "十一", "all")
        self.assertEqual(int2kanji(111), "百十一", "all")
        self.assertEqual(int2kanji(211), "二百十一", "all")
        self.assertEqual(int2kanji(121), "百二十一", "all")
        self.assertEqual(int2kanji(11), "十一", "all")
        self.assertEqual(int2kanji(111), "百十一", "all")
        self.assertEqual(int2kanji(211), "二百十一")
        self.assertEqual(int2kanji(121), "百二十一")
        self.assertEqual(int2kanji(1000), "千")
        self.assertEqual(int2kanji(1001), "千一")
        self.assertEqual(int2kanji(2025), "二千二十五")
        self.assertEqual(int2kanji(58076099), "五千八百七万六千九十九")

        # added 1.0.0
        self.assertEqual(int2kanji(10000000000000000000000000000000000000000000000000000), "一恒河沙")
        self.assertEqual(
            int2kanji(999999999999999999999999999999999999999999999999999999999999999999999999),
            ("九千九百九十九無量大数九千九百九十九不可思議九千九百九十九那由多九千九百九十九阿僧祇九千九百九十九恒河沙九千九百九十九極"
             "九千九百九十九載九千九百九十九正九千九百九十九澗九千九百九十九溝九千九百九十九穣九千九百九十九𥝱九千九百九十九垓"
             "九千九百九十九京九千九百九十九兆九千九百九十九億九千九百九十九万九千九百九十九")
        )

        self.assertEqual("1", int2kanji(1, style="mixed"))
        self.assertEqual("10", int2kanji(10, style="mixed"))
        self.assertEqual("11", int2kanji(11, style="mixed"))
        self.assertEqual("121", int2kanji(121, style="mixed"))
        self.assertEqual("1千", int2kanji(1000, style="mixed"))
        self.assertEqual("1001", int2kanji(1001, style="mixed"))
        self.assertEqual("2025", int2kanji(2025, style="mixed"))
        self.assertEqual("5807万6099", int2kanji(58076099, style="mixed"))
        self.assertEqual("223兆4235億4256万6千", int2kanji(223423542566000, style="mixed"))
        self.assertEqual("5千京", int2kanji(50000000000000000000, style="mixed"))
        self.assertEqual("5000京", int2kanji(50000000000000000000, style="mixed", kanji_thousand=False))
        self.assertEqual("39京4385兆4895万", int2kanji(394385000048950000, style="mixed"))
        self.assertEqual("223兆4千億4256万6千", int2kanji(223400042566000, style="mixed"))
        self.assertEqual("223兆4000億4256万6000", int2kanji(223400042566000, style="mixed", kanji_thousand=False))

        # added 1.0.0
        self.assertEqual("1恒河沙", int2kanji(10000000000000000000000000000000000000000000000000000, style="mixed",
                                           kanji_thousand=False))
        self.assertEqual(
            "9999無量大数9999不可思議9999那由多9999阿僧祇9999恒河沙9999極9999載9999正9999澗9999溝9999穣9999𥝱9999垓9999京9999兆9999億9999万9999",
            int2kanji(999999999999999999999999999999999999999999999999999999999999999999999999, style='mixed')
        )

    def testnumber(self):
        self.assertEqual(12000, Number(276493734) - Number.from_kanji("2億7648万1734"))
        self.assertEqual(12734, Number(276493734) - Number.from_kanji("2億7648万1千"))
        self.assertEqual("2億7648万1734", (Number(276493734) - Number(12000)).to_kanji(style="mixed"))


if __name__ == "__main__":
    unittest.main()
