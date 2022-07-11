#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import collections
import unittest

from insanity import sanity_checks as san


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2017 Patrick Hohenecker\n"
        "\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n"
        "\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n"
        "\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
)
__license__ = "MIT License"
__version__ = "2017.1"
__date__ = "Aug 13, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class SanityChecksTest(unittest.TestCase):
    """This class implements the tests for the module ``insanity.sanity_checks``."""

    @staticmethod
    def eq_mod_2(x: int, y: int) -> bool:
        """Computes whether two integers are equal modulo 2."""
        return (x - y) % 2 == 0

    @staticmethod
    def eq_mod_2_check(x, y):
        if not SanityChecksTest.eq_mod_2(x, y):
            raise ValueError("{} != {} mod 2".format(x, y))

    # noinspection PyTypeChecker
    def test_fully_qualified_name(self):
        # CHECK: providing an arg that is not a type causes a TypeError
        with self.assertRaises(TypeError):
            san._fully_qualified_name("not-a-type")

        # CHECK: legal invocations return fully qualified type names
        self.assertEqual(san._fully_qualified_name(str), "builtins.str")
        self.assertEqual(san._fully_qualified_name(type), "builtins.type")
        self.assertEqual(san._fully_qualified_name(collections.abc.Iterable), "collections.abc.Iterable")

    # noinspection PyTypeChecker
    def test_sanitize_iterable(self):
        # CHECK: invoking the function with an arg of an illegal type causes a TypeError
        with self.assertRaises(TypeError):
            san.sanitize_iterable(0, ["some_value"], elements_type=str)
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", 0, elements_type=str)
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], elements_type=0)
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], target_length="0")
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], min_length="0")
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], max_length="0")
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], elements_type=str, none_elements_allowed=0)
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], error_msg=0)

        # CHECK: invoking the function with incompatible args causes a ValueError/TypeError
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", [0, 1, 2])
        with self.assertRaises(ValueError):
            san.sanitize_iterable("some_arg", [0, 1, 2], target_length=3, min_length=2, max_length=4)
        with self.assertRaises(ValueError):
            san.sanitize_iterable("some_arg", [0, 1, 2], min_length=5, max_length=4)

        # CHECK: providing a list with elements of illegal type causes a TypeError
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], elements_type=int)
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value"], elements_type=[int, float])
        with self.assertRaises(TypeError):
            san.sanitize_iterable("some_arg", ["some_value", None], elements_type=int, none_elements_allowed=False)

        # CHECK: providing a list of illegal length causes a ValueError
        with self.assertRaises(ValueError):
            san.sanitize_iterable("some_arg", [0, 1, 2], target_length=2)
        with self.assertRaises(ValueError):
            san.sanitize_iterable("some_arg", [0, 1, 2], target_length=4)
        with self.assertRaises(ValueError):
            san.sanitize_iterable("some_arg", [0, 1, 2], min_length=4)
        with self.assertRaises(ValueError):
            san.sanitize_iterable("some_arg", [0, 1, 2], max_length=2)

        # CHECK: providing a list that is illegal w.r.t. to a custom sanity check causes a ValueError
        with self.assertRaises(ValueError):
            san.sanitize_iterable("some_arg", [0, 1, 2], element_check_fn=(lambda x: self.eq_mod_2_check(x, 0)))

        # CHECK: providing a list with legal elements causes no error
        san.sanitize_iterable("some_arg", [0, 1, 2], elements_type=int, max_length=3)
        san.sanitize_iterable("some_arg", [0, None, 2], elements_type=int, max_length=3, none_elements_allowed=True)
        san.sanitize_iterable("some_arg", [0, 1, "2"], elements_type=[int, str], min_length=2, max_length=4)
        san.sanitize_iterable("some_arg", None, elements_type=int, none_allowed=True)
        san.sanitize_iterable("some_arg", [0, 2, 4], element_check_fn=(lambda x: self.eq_mod_2_check(x, 0)))

    # noinspection PyTypeChecker
    def test_sanitize_range(self):
        # CHECK: invoking the function with an illegal type causes a TypeError
        with self.assertRaises(TypeError):
            san.sanitize_range(0, 1, minimum=0)
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", "0", minimum=0)
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", 1, minimum="0")
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", 1, maximum="0")
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", 1, minimum=0, error_msg=0)
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", 1, minimum=0, min_inclusive=0)
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", 1, minimum=0, max_inclusive=0)
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", 1, minimum=0, complement=0)

        # CHECK: leaving both minimum and maximum unspecified causes a TypeError
        with self.assertRaises(TypeError):
            san.sanitize_range("some_arg", 1)

        # CHECK: providing a minimum > maximum causes a ValueError
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 1, minimum=2, maximum=1)

        # CHECK: providing an out-of-range value causes a ValueError
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", -1, minimum=0, maximum=2, min_inclusive=True, complement=False)
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 0, minimum=0, maximum=2, min_inclusive=False, complement=False)
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 3, minimum=0, maximum=2, max_inclusive=True, complement=False)
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 2, minimum=0, maximum=2, max_inclusive=False, complement=False)
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 0, minimum=0, maximum=2, min_inclusive=True, complement=True)
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 1, minimum=0, maximum=2, min_inclusive=True, complement=True)
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 2, minimum=0, maximum=2, max_inclusive=True, complement=True)
        with self.assertRaises(ValueError):
            san.sanitize_range("some_arg", 1, minimum=0, maximum=2, max_inclusive=False, complement=True)

        # CHECK: providing an in-range value causes no error
        san.sanitize_range("some_arg", 0, minimum=0, maximum=2, min_inclusive=True)
        san.sanitize_range("some_arg", 1, minimum=0, maximum=2, min_inclusive=False)
        san.sanitize_range("some_arg", 2, minimum=0, maximum=2, max_inclusive=True)
        san.sanitize_range("some_arg", 1, minimum=0, maximum=2, max_inclusive=False)

    # noinspection PyTypeChecker
    def test_sanitize_type(self):
        # CHECK: invoking the function with an arg of an illegal type causes a TypeError
        with self.assertRaises(TypeError):
            san.sanitize_type(0, "some_value", str)
        with self.assertRaises(TypeError):
            san.sanitize_type("some_arg", "some_value", 0)
        with self.assertRaises(TypeError):
            san.sanitize_type("some_arg", "some_value", str, error_msg=0)
        with self.assertRaises(TypeError):
            san.sanitize_type("some_arg", "some_value", str, none_allowed=0)

        # CHECK: perform sanity check for an illegal arg_value
        with self.assertRaises(TypeError):
            san.sanitize_type("some_arg", "some_value", int)
        with self.assertRaises(TypeError):
            san.sanitize_type("some_arg", "some_value", [int, float])
        with self.assertRaises(TypeError):
            san.sanitize_type("some_arg", None, int, none_allowed=False)

        # CHECK: perform sanity check for an admissible arg_value
        san.sanitize_type("some_arg", "some_value", str)
        san.sanitize_type("some_arg", "some_value", [int, str])
        san.sanitize_type("some_arg", None, str, none_allowed=True)

    # noinspection PyTypeChecker
    def test_sanitize_value(self):
        # CHECK: invoking the function with an arg of an illegal type causes a TypeError
        with self.assertRaises(TypeError):
            san.sanitize_value(0, "some_value", "some_target_value")
        with self.assertRaises(TypeError):
            san.sanitize_value("some_arg", "some_value", "some_target_value", complement=0)
        with self.assertRaises(TypeError):
            san.sanitize_value("some_arg", "some_value", "some_target_value", expand_target=0)
        with self.assertRaises(TypeError):
            san.sanitize_value("some_arg", "some_value", "some_target_value", error_msg=0)

        # CHECK: sanity check for an illegal arg_value causes a ValueError
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", 0, 1)
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", 0, 0, complement=True)
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", 0, [1, 2])
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", 0, [0, 1], complement=True)
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", 0, [0, 1], expand_target=False)
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", [0, 1], [0, 1])
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", None, [0, 1], none_allowed=False)

        # CHECK: sanity check with an alternative equality function works as expected
        san.sanitize_value("some_arg", 3, 1, equality_fn=self.eq_mod_2)
        with self.assertRaises(ValueError):
            san.sanitize_value("some_arg", 3, 0, equality_fn=self.eq_mod_2)

        # CHECK: sanity check for an admissible arg_value causes no errors
        san.sanitize_value("some_arg", 0, 0)
        san.sanitize_value("some_arg", 0, [0, 1])
        san.sanitize_value("some_arg", 0, 1, complement=True)
        san.sanitize_value("some_arg", 0, [1, 2], complement=True)
        san.sanitize_value("some_arg", [0, 1], [0, 1], expand_target=False)
        san.sanitize_value("some_arg", None, [0, 1], none_allowed=True)


if __name__ == "__main__":
    unittest.main()
