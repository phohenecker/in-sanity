# -*- coding: utf-8 -*-

"""This module contains various functions that implement common sanity checks for function arguments."""


import collections
import typing


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
__date__ = "Aug 16, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


def _fully_qualified_name(t: type) -> str:
    """Retrieves the fully qualified name of the provided type.

    Args:
        t (type): The type whose fully qualified name shall be retrieved.

    Returns:
        str: The fully qualified name of ``t``.

    Raises:
        TypeError: If ``t`` is not an instance of ``type``.
    """
    if not isinstance(t, type):
        raise TypeError(
                "The parameter <t> has to be a type, but is an instance of {}!".format(_fully_qualified_name(type(t)))
        )

    prefix = ""
    if hasattr(t, "__module__"):
        prefix = t.__module__ + "."

    return prefix + t.__name__


def sanitize_type(
        arg_name: str,
        arg_value,
        target_type: typing.Union[type, typing.Iterable[type]],
        none_allowed: bool=False,
        error_msg: str=None
) -> None:
    """Sanitizes the type of an arg.

    Args:
        arg_name (str): The name of the parameter being sanitized.
        arg_value: The value that is subject of investigation.
        target_type (type or collections.Iterable[type]): A target type or an ``Iterable`` of types that ``arg_value``
            may have.
        none_allowed (bool, optional): Indicates whether ``arg_value`` is allowed to be ``None``.
        error_msg (str, optional): An optional error message that is provided if an error is raised.

    Raises:
        TypeError: If the provided argument is not of the required type.
    """
    # //////// Sanitize Args -------------------------------------------------------------------------------------------

    if not isinstance(arg_name, str):
        raise TypeError(
                "The parameter <arg_name> has to be of type str, has type {}!".format(
                        _fully_qualified_name(type(arg_name))
                )
        )
    if isinstance(target_type, collections.Iterable):
        for t in target_type:
            if not isinstance(t, type):
                raise TypeError(
                        (
                                "The parameter <target_type> has to be a type or a list of types, "
                                "but is a list that contains an element of type {}!"
                        ).format(_fully_qualified_name(type(t)))
                )
    elif not isinstance(target_type, type):
        raise TypeError(
                "The parameter <target_type> has to be a type or a list of types, but is of type {}!".format(
                        _fully_qualified_name(type(target_type))
                )
        )
    if not isinstance(none_allowed, bool):
        raise TypeError(
                "The parameter <none_allowed> has to be of type bool, but has type {}!".format(
                            _fully_qualified_name(type(none_allowed))
                )
        )
    if error_msg is not None and not isinstance(error_msg, str):
        raise TypeError(
                "If provided, parameter <error_msg> has to be of type str, but has type {}!".format(
                        _fully_qualified_name(type(error_msg))
                )
        )

    # //////// Perform Requested Sanity Check --------------------------------------------------------------------------

    # check if arg_value is acceptably None
    if arg_value is None and none_allowed:
        return

    # //////// CASE 1: target_type is a type, not an Iterable

    if isinstance(target_type, type):

        # check type of arg_value
        if not isinstance(arg_value, target_type):

            # create error message (if not provided)
            if error_msg is None:
                error_msg = "The parameter <{arg_name}> has to be of type {target_type}, but has type {arg_value_type}!"
            error_msg = error_msg.format(
                    arg_name=arg_name,
                    target_type=_fully_qualified_name(target_type),
                    arg_value_type=_fully_qualified_name(type(arg_value))
            )

            # raise an error to signal incorrect type
            raise TypeError(error_msg)

    # //////// CASE 2: target_type is an Iterable of types

    else:

        # run through all possible types, and return if a valid type is found
        for t in target_type:
            if isinstance(arg_value, t):
                return

        # create error message (if not provided)
        if error_msg is None:
            error_msg = (
                    "The type of parameter <{arg_name}> has to be any of {target_type}, "
                    "but it has type {arg_value_type}!"
            )
        error_msg = error_msg.format(
                arg_name=arg_name,
                target_type="[" + ", ".join([_fully_qualified_name(t) for t in target_type]) + "]",
                arg_value_type=_fully_qualified_name(type(arg_value))
        )

        # raise an error to signal incorrect type
        raise TypeError(error_msg)
