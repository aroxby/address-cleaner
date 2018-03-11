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
            '123 mAin st new york ny 10001':
                '123 Main St, New York Ny, 10001',
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
            '123 1st avenue Apt #1 New York, NY 10001':
                '123 1st Avenue, Apt #1, New York Ny, 10001',
            '10-20 my street city state 12345':
                '10-20 My Street, City State, 12345',
            '123 main st building 4 new york ny 10001':
                '123 Main St, Building 4, New York Ny, 10001',
            '345 Staint john\'s rd City State, 12345':
                '345 Staint John\'s Rd, City State, 12345',
            # Still fails because 'st' is not saint not street
            # '345 St john\'s rd City State, 12345':
            #     '345 St John\'s Rd, City State, 12345',
            'PO. box 1234 city state 12345':
                'P.O. Box 1234, City State, 12345',
            'P O box 1234 city state 12345':
                'P.O. Box 1234, City State, 12345',
        }
        for data, expected in cases.items():
            actual = clean(data)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
