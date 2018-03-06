import unittest
import re
import regexputil
from decimal import Decimal


class TestMoneyRegexp(unittest.TestCase):
    def test1(self):
        match = re.fullmatch(regexputil.money_regexp, "2 tysiące nowych polskich zł")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '2')
        self.assertEqual(match.group('integer'), '2')
        self.assertIsNone(match.group('decimal'))
        self.assertEqual(match.group('multiplier'), 'tysiące')
        self.assertEqual(match.group('thousand'), 'tysiące')
        self.assertIsNone(match.group('million'))
        self.assertIsNone(match.group('billion'))

    def test2(self):
        match = re.fullmatch(regexputil.money_regexp, "500 000 PLN")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '500 000')
        self.assertEqual(match.group('integer'), '500 000')
        self.assertIsNone(match.group('decimal'))
        self.assertIsNone(match.group('multiplier'))
        self.assertIsNone(match.group('thousand'))
        self.assertIsNone(match.group('million'))
        self.assertIsNone(match.group('billion'))

    def test3(self):
        match = re.fullmatch(regexputil.money_regexp, "2 mld starych polskich złotych")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '2')
        self.assertEqual(match.group('integer'), '2')
        self.assertIsNone(match.group('decimal'))
        self.assertEqual(match.group('multiplier'), 'mld')
        self.assertIsNone(match.group('thousand'))
        self.assertIsNone(match.group('million'))
        self.assertEqual(match.group('billion'), 'mld')

    def test4(self):
        match = re.fullmatch(regexputil.money_regexp, "1 tysiąc nowych polskich zł")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '1')
        self.assertEqual(match.group('integer'), '1')
        self.assertIsNone(match.group('decimal'))
        self.assertEqual(match.group('multiplier'), 'tysiąc')
        self.assertEqual(match.group('thousand'), 'tysiąc')
        self.assertIsNone(match.group('million'))
        self.assertIsNone(match.group('billion'))

    def test5(self):
        match = re.fullmatch(regexputil.money_regexp, "45,67 zł")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '45,67')
        self.assertEqual(match.group('integer'), '45')
        self.assertEqual(match.group('decimal'), '67')
        self.assertIsNone(match.group('multiplier'))
        self.assertIsNone(match.group('thousand'))
        self.assertIsNone(match.group('million'))
        self.assertIsNone(match.group('billion'))

    def test6(self):
        match = re.fullmatch(regexputil.money_regexp, "10.500,23 złotych")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '10.500,23')
        self.assertEqual(match.group('integer'), '10.500')
        self.assertEqual(match.group('decimal'), '23')
        self.assertIsNone(match.group('multiplier'))
        self.assertIsNone(match.group('thousand'))
        self.assertIsNone(match.group('million'))
        self.assertIsNone(match.group('billion'))

    def test7(self):
        match = re.fullmatch(regexputil.money_regexp, "5 tys. polskich złotych")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number'), '5')
        self.assertEqual(match.group('integer'), '5')
        self.assertIsNone(match.group('decimal'))
        self.assertEqual(match.group('multiplier'), 'tys.')
        self.assertEqual(match.group('thousand'), 'tys')
        self.assertIsNone(match.group('million'))
        self.assertIsNone(match.group('billion'))

    def test8(self):
        match = re.fullmatch(regexputil.money_regexp, "5 tys. zl")
        self.assertIsNone(match)


class TestEvaluate(unittest.TestCase):
    def test1(self):
        match = re.fullmatch(regexputil.money_regexp, "2 tysiące nowych polskich zł")
        self.assertEqual(regexputil.evaluate(match), 2000)

    def test2(self):
        match = re.fullmatch(regexputil.money_regexp, "500 000 PLN")
        self.assertEqual(regexputil.evaluate(match), 500000)

    def test3(self):
        match = re.fullmatch(regexputil.money_regexp, "2 mld starych polskich złotych")
        self.assertEqual(regexputil.evaluate(match), 2000000000)

    def test4(self):
        match = re.fullmatch(regexputil.money_regexp, "1 tysiąc nowych polskich zł")
        self.assertEqual(regexputil.evaluate(match), 1000)

    def test5(self):
        match = re.fullmatch(regexputil.money_regexp, "45,67 zł")
        self.assertEqual(regexputil.evaluate(match), Decimal('45.67'))

    def test6(self):
        match = re.fullmatch(regexputil.money_regexp, "10.500,23 złotych")
        self.assertEqual(regexputil.evaluate(match), Decimal('10500.23'))

    def test7(self):
        match = re.fullmatch(regexputil.money_regexp, "5 tys. polskich złotych")
        self.assertEqual(regexputil.evaluate(match), 5000)


class TestSzkodaRegexp(unittest.TestCase):
    def test1(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkoda")

    def test2(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkody")

    def test3(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkody")

    def test4(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkód")

    def test5(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkodzie")

    def test6(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkodom")

    def test7(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkodę")

    def test8(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkodą")

    def test9(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkodami")

    def test10(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkodach")

    def test11(self):
        self.assertIsNotNone(regexputil.szkoda_regexp, "szkodo")


if __name__ == "__main__":
    unittest.main()
