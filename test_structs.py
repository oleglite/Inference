#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Oleg Beloglazov'

import unittest
from structs import Fact, Term, Rule

class TestFact(unittest.TestCase):

    def setUp(self):
        self.facts = [
            Fact('A', ['a']),
            Fact('A', ['a', 'b', 'c']),
            Fact('A', ['a', 'b', 'a']),
            Fact('B', ['a', 'b', 'a'])
        ]

    def test_fits(self):
        term = Term('A', ['X', 'Y', 'Z'])
        self.assertEqual(
            [f.fits(term) for f in self.facts],
            [False, True, True, False]
        )

        term = Term('A', ['X', 'Y', 'X'])
        self.assertEqual(
            [f.fits(term) for f in self.facts],
            [False, False, True, False]
        )

class TestTerm(unittest.TestCase):

    def setUp(self):
        pass

    def test_equivalent(self):
        term = Term('A', ['X', 'Y', 'X'])
        tests = [
            {}, ['X', 'Y', 'X'],
            {'X':'N'}, ['N', 'Y', 'N'],
            {'Y':'N'}, ['X', 'N', 'X'],
            {'Z':'N'}, ['X', 'Y', 'X'],
            {'X':'N', 'Y':'M'}, ['N', 'M', 'N'],
            {'X':'Y', 'Y':'X'}, ['Y', 'X', 'Y']
        ]

        for i in xrange(0, len(tests), 2):
            self.assertEqual(term.equivalent(tests[i]).params, Term('A', tests[i + 1]).params)



class TestRule(unittest.TestCase):

    def setUp(self):
        self.rules = [
            Rule(Term('A', ['X']), [Term('B', ['X'])]),
            Rule(Term('A', ['X', 'Y']), [Term('B', ['X', 'Z']), Term('C', ['Y', 'Z'])]),
            Rule(Term('A', ['X', 'Y']), [Term('A', ['X', 'Z']), Term('C', ['Y', 'Z', 'V'])])
        ]


if __name__ == "__main__":
    unittest.main()
