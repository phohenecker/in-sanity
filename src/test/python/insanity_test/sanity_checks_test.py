#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import collections
import unittest

from insanity import sanity_checks as san


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2017 Patrick Hohenecker"
        "\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy "
        "of this software and associated documentation files (the \"Software\"), to deal "
        "in the Software without restriction, including without limitation the rights "
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
        "copies of the Software, and to permit persons to whom the Software is "
        "furnished to do so, subject to the following conditions:"
        "\n\n"
        "The above copyright notice and this permission notice shall be included in all "
        "copies or substantial portions of the Software."
        "\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
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

    # noinspection PyTypeChecker
    def test_fully_qualified_name(self):
        # CHECK: providing an arg that is not a type causes a TypeError
        with self.assertRaises(TypeError):
            san._fully_qualified_name("not-a-type")

        # CHECK: legal invocations return fully qualified type names
        self.assertEqual(san._fully_qualified_name(str), "builtins.str")
        self.assertEqual(san._fully_qualified_name(type), "builtins.type")
        self.assertEqual(san._fully_qualified_name(collections.Iterable), "collections.abc.Iterable")

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
