# -*- coding: utf-8 -*-

"""This module defines functions that may be handed to :func:`insanity.sanity_checks.sanitize_iterable` in order to
sanitize the elements of an `Iterable`.
"""


import collections
import numbers
import operator
import typing

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
__date__ = "Aug 24, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


def sanitize_value_fn(
        arg_name: str,
        target_value,
        complement: bool=False,
        expand_target: bool=True,
        none_allowed: bool=True,
        error_msg: str=None,
        equality_fn=operator.eq
) -> typing.Callable[[typing.Any], None]:
    """Retrieves a function that replicates :func:`insanity.sanity_checks.sanitize_value` with all of its args
    except ``arg_value`` predefined to the given parameters.

    Args:
        The parameters resemble exactly those eponymous parameters of :func:`insanity.sanity_checks.sanitize_value`.

    Returns:
        The created function.
    """
    # //////// Sanitize Args -------------------------------------------------------------------------------------------

    san.sanitize_type("arg_name", arg_name, str)
    san.sanitize_type("complement", complement, bool)
    san.sanitize_type("expand_target", expand_target, bool)
    san.sanitize_type("none_allowed", none_allowed, bool)
    san.sanitize_type("error_msg", error_msg, str, none_allowed=True)

    # //////// Perform Requested Sanity Check --------------------------------------------------------------------------

    # create error message
    if error_msg is None:
        if not expand_target or not isinstance(target_value, collections.Iterable):
            error_msg = (
                    "The elements of <{arg_name}> have to be %s {target_value}, but {arg_value} was encountered!"
            ) % ("different from" if complement else "equal to")
        else:
            error_msg = (
                    "The elements of <{arg_name}> have to be %s {target_value}, but {arg_value} was encountered!"
            ) % ("distinct from" if complement else "any of")

    # create check function
    return lambda x: san.sanitize_value(
            arg_name,
            x,
            target_value,
            complement=complement,
            expand_target=expand_target,
            none_allowed=none_allowed,
            error_msg=error_msg,
            equality_fn=equality_fn
    )
