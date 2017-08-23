# -*- coding: utf-8 -*-

"""This module contains various functions that implement common sanity checks for function arguments."""


import collections
import operator
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


def sanitize_value(
        arg_name: str,
        arg_value,
        target_value,
        complement: bool=False,
        expand_target: bool=True,
        none_allowed: bool=True,
        error_msg: str=None,
        equality_fn=operator.eq
):
    """Examines whether the value of an arg is among specified admissible values.

    Args:
        arg_name (str): The name of the parameter being sanitized.
        arg_value: The value that is subject of investigation.
        target_value: A target value or an ``Iterable`` of values that ``arg_value`` may have.
        complement (bool, optional): If ``True``, then ``target_value`` is interpreted as a specification of
            prohibited rather than admissible values.
        expand_target (bool, optional): If ``True``, then any target_value that is an ``Iterable`` is interpreted as a
            collection of multiple admissible target values. If ``False``, however, then ``target_value`` itself is
            considered as the one and only possible target, irrespective of whether it is an ``Iterable`` or not.
        none_allowed (bool, optional): Indicates whether ``arg_value`` may be ``None``.
        error_msg (str, optional): An optional error message that is provided if an error is raised.
        equality_fn (optional): The function that is used to check for equality.

    Raises:
        ValueError: If the value of ``arg_value`` is not admissible.
    """
    # //////// Sanitize Args -------------------------------------------------------------------------------------------

    sanitize_type("arg_name", arg_name, str)
    sanitize_type("complement", complement, bool)
    sanitize_type("expand_target", expand_target, bool)
    sanitize_type("none_allowed", none_allowed, bool)
    sanitize_type("error_msg", error_msg, str, none_allowed=True)

    # //////// Perform Requested Sanity Check --------------------------------------------------------------------------

    # check if arg_value is acceptably None
    if none_allowed and arg_value is None:
        return

    # //////// CASE 1: target_value is not expanded

    if not expand_target or not isinstance(target_value, collections.Iterable):
        if (
                (complement and equality_fn(arg_value, target_value)) or
                (not complement and not equality_fn(arg_value, target_value))
        ):
            # create error message
            if error_msg is None:
                error_msg = "The parameter <{arg_name}> has to be {} {target_value}, but is {arg_value}!"
            error_msg = error_msg.format(
                    "different from" if complement else "equal to",
                    arg_name=arg_name,
                    arg_value=arg_value,
                    target_value=target_value
            )

            # raise an error to signal inadmissible value
            raise ValueError(error_msg)

    # //////// CASE 2: target_value is expanded

    else:
        # create error message
        if error_msg is None:
            error_msg = "The parameter <{arg_name}> has to be {} {target_value}, but is {arg_value}!"
        error_msg = error_msg.format(
                "distinct from" if complement else "any of",
                arg_name=arg_name,
                arg_value=arg_value,
                target_value=("[" + ", ".join([str(t) for t in target_value]) + "]")
        )

        # run through all possible/prohibited values, and perform necessary checks
        for t in target_value:
            if equality_fn(arg_value, t):
                if complement:
                    raise ValueError(error_msg)
                else:
                    return

        # if complement is False => arg_value is not among the possible target values
        if not complement:
            raise ValueError(error_msg)
