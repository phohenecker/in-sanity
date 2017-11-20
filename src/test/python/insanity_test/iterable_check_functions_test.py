#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import insanity as ins

from insanity import iterable_check_functions as fn


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
__date__ = "Aug 24, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class IterableCheckFunctionsTest(unittest.TestCase):
    """This class implements the tests for the module ``insanity.iterable_check_functions``."""

    # noinspection PyTypeChecker
    def test_sanitize_range_fn(self):
        # CHECK: invoking the function with an illegal type causes a TypeError
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn(0, minimum=0)
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn("some_arg", minimum="0")
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn("some_arg", maximum="0")
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn("some_arg", minimum=0, error_msg=0)
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn("some_arg", minimum=0, min_inclusive=0)
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn("some_arg", minimum=0, max_inclusive=0)
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn("some_arg", minimum=0, complement=0)

        # CHECK: leaving both minimum and maximum unspecified causes a TypeError
        with self.assertRaises(TypeError):
            fn.sanitize_range_fn("some_arg")

        # CHECK: providing a minimum > maximum causes a ValueError
        with self.assertRaises(ValueError):
            fn.sanitize_range_fn("some_arg", minimum=2, maximum=1)

        # CHECK: providing an in-range value causes no error
        ins.sanitize_iterable(
                "some_arg",
                [0],
                element_check_fn=fn.sanitize_range_fn("some_arg", minimum=0, maximum=2, min_inclusive=True)
        )
        ins.sanitize_iterable(
                "some_arg",
                [1],
                element_check_fn=fn.sanitize_range_fn("some_arg", minimum=0, maximum=2, min_inclusive=False)
        )
        ins.sanitize_iterable(
                "some_arg",
                [2],
                element_check_fn=fn.sanitize_range_fn("some_arg", minimum=0, maximum=2, max_inclusive=True)
        )
        ins.sanitize_iterable(
                "some_arg",
                [1],
                element_check_fn=fn.sanitize_range_fn("some_arg", minimum=0, maximum=2, max_inclusive=False)
        )

    # noinspection PyTypeChecker
    def test_sanitize_value_fn(self):
        # CHECK: invoking the function with an arg of an illegal type causes a TypeError
        with self.assertRaises(TypeError):
            fn.sanitize_value_fn(0, "some_target_value")
        with self.assertRaises(TypeError):
            fn.sanitize_value_fn("some_arg", "some_target_value", complement=0)
        with self.assertRaises(TypeError):
            fn.sanitize_value_fn("some_arg", "some_target_value", expand_target=0)
        with self.assertRaises(TypeError):
            fn.sanitize_value_fn("some_arg",  "some_target_value", error_msg=0)

        # CHECK: sanity check for an admissible arg_value causes no errors
        ins.sanitize_iterable("some_arg", [0], element_check_fn=fn.sanitize_value_fn("some_arg", 0))
        ins.sanitize_iterable("some_arg", [0], element_check_fn=fn.sanitize_value_fn("some_arg", [0, 1]))
        ins.sanitize_iterable("some_arg", [0], element_check_fn=fn.sanitize_value_fn("some_arg", 1, complement=True))
        ins.sanitize_iterable(
                "some_arg", [0], element_check_fn=fn.sanitize_value_fn("some_arg", [1, 2], complement=True)
        )
        ins.sanitize_iterable(
                "some_arg", [[0, 1]], element_check_fn=fn.sanitize_value_fn("some_arg", [0, 1], expand_target=False)
        )


if __name__ == "__main__":
    unittest.main()
