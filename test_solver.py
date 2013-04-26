#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Oleg Beloglazov'

import unittest
from solver import *


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.dicts = [
            {1:'a'},
            {1:'a', 2:'b'},
            {1:'a', 2:'a', 3:'c'},
            {2:'b', 3:'c'},
            {1:'a', 2:'b', 3:'c'},
        ]

    def test_hard_union(self):
        dicts = self.dicts

        self.assertEqual(
            hard_union(dicts[0], dicts[1]),
            {1:'a', 2:'b'}
        )

        self.assertEqual(
            hard_union(dicts[0], dicts[2]),
            {1:'a', 2:'a', 3:'c'}
        )

        self.assertEqual(
            hard_union(dicts[1], dicts[2]),
            None
        )

        self.assertEqual(
            hard_union(dicts[1], dicts[3]),
            {1:'a', 2:'b', 3:'c'}
        )

    def test_multi_hard_union(self):
        dicts1 = [
            {1:0, 2:0, 3:0},
            {2:1, 3:1}
        ]

        dicts2 = [
            {2:0, 4:1},
            {3:1}
        ]

        res = [
            {1:0, 2:0, 3:0, 4:1},
            {2:1, 3:1}
        ]

        self.assertEqual(multi_hard_union(dicts1, dicts2), res)


if __name__ == "__main__":
    unittest.main()
