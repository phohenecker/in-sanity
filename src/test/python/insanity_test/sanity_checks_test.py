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


if __name__ == "__main__":
    unittest.main()
