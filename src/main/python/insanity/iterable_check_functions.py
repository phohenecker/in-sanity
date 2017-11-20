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


def sanitize_range_fn(
        arg_name: str,
        minimum: numbers.Number=None,
        maximum: numbers.Number=None,
        min_inclusive: bool=True,
        max_inclusive: bool=True,
        complement: bool=False,
        error_msg: str=None
) -> typing.Callable[[typing.Any], None]:
    """Retrieves a function that replicates :func:`insanity.sanity_checks.sanitize_range` with all of its args
    except ``arg_value`` predefined to the given parameters.

    Args:
        The parameters resemble exactly those eponymous parameters of :func:`insanity.sanity_checks.sanitize_range`.

    Returns:
        The created function.
    """
    # //////// Sanitize Args -------------------------------------------------------------------------------------------

    san.sanitize_type("arg_name", arg_name, str)
    san.sanitize_type("minimum", minimum, numbers.Number, none_allowed=True)
    san.sanitize_type("maximum", maximum, numbers.Number, none_allowed=True)
    san.sanitize_type("min_inclusive", min_inclusive, bool)
    san.sanitize_type("max_inclusive", max_inclusive, bool)
    san.sanitize_type("complement", complement, bool)
    san.sanitize_type("error_msg", error_msg, str, none_allowed=True)

    if minimum is None and maximum is None:
        raise TypeError("At least one of the parameters <minimum> and <maximum> has to be provided!")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError(
                "The parameter <minimum> must not be greater than <maximum>, but {} > {}!".format(
                        minimum,
                        maximum
                )
        )

    # //////// Create Check Function -----------------------------------------------------------------------------------

    # create error message
    if error_msg is None:
        if complement:
            min_sym = "<" if min_inclusive else "<="
            max_sym = ">" if max_inclusive else ">="
        else:
            min_sym = ">=" if min_inclusive else ">"
            max_sym = "<=" if max_inclusive else "<"
        if error_msg is None:
            if minimum is None:
                error_msg = \
                        "The elements of <{arg_name}> have to be " + max_sym + "{maximum}, but {arg_value} was found!"
            elif maximum is None:
                error_msg = \
                        "The elements of <{arg_name}> have to be " + min_sym + " {minimum}, but {arg_value} was found!"
            else:
                error_msg = \
                        "The elements in <{arg_name}> have to be " + min_sym + " {minimum} " + \
                        ("or " if complement else "and ") + \
                        max_sym + " {maximum}, " + \
                        "but {arg_value} was found!"

    # create check function
    return lambda x: san.sanitize_range(
            arg_name,
            x,
            minimum=minimum,
            maximum=maximum,
            min_inclusive=min_inclusive,
            max_inclusive=max_inclusive,
            complement=complement,
            error_msg=error_msg
    )


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
