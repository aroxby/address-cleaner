#!/usr/bin/env python
"""
Tests for address parsing
"""

import unittest
from main import clean


class TestClean(unittest.TestCase):
    """
    Tests clean method
    """
    def test_parse(self):
        cases = {
            '123 mAin st, apt 3b new york ny 10001':
                '123 Main St, Apt 3B, New York Ny, 10001',
            '123 main st apt 3B new, york ny 10001-1234':
                '123 Main St, Apt 3B, New York Ny, 10001-1234',
            '123 main st 2nd floOr new york ny, 10001':
                '123 Main St, 2nd Floor, New York Ny, 10001',
            '123 main st 1st floor new york ny 10001':
                '123 Main St, 1st Floor, New York Ny, 10001',
            '123 main st floor 5 new york ny 10001':
                '123 Main St, Floor 5, New York Ny, 10001',
        }
        for data, expected in cases.items():
            actual = clean(data)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
