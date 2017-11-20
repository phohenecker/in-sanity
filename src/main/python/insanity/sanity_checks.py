# -*- coding: utf-8 -*-

"""This module contains various functions that implement common sanity checks for function arguments."""


import collections
import numbers
import operator
import typing


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


# noinspection PyTypeChecker
def sanitize_iterable(
        arg_name: str,
        arg_value: collections.Iterable,
        elements_type: typing.Union[type, typing.Iterable[type]]=None,
        target_length: int=None,
        min_length: int=None,
        max_length: int=None,
        none_allowed: bool=False,
        none_elements_allowed: bool=False,
        element_check_fn: typing.Callable[[typing.Any], typing.Any]=None,
        error_msg: str=None
) -> None:
    """Sanitizes an ``Iterable`` as well as its elements.

    For more advanced sanity checks of an ``Iterable``'s elements, ``element_check_fn`` accepts an arbitrary callable
    that will be passed every element of ``arg_value``, and can thus be used to implement any kind of check. It is also
    possible to use ``element_check_fn`` together with any of the built-in sanity checks, which will be executed first.
    This way is it possible, e.g., to sanitize the type of the elements before any custom sanity checks are performed.

    Args:
        arg_name (str): The name of the parameter being sanitized.
        arg_value (collections.Iterable): The ``Iterable`` that is subject of investigation.
        elements_type (type or collections.Iterable[type], optional): A target type or an ``Iterable`` of types that
            the elements of ``arg_value`` may have.
        target_length (int, optional): The target length that ``arg_value`` is supposed to have. This option cannot be
            combined with ``min_length`` or ``max_length``.
        min_length (int, optional): The minimum length that ``arg_value`` is supposed to have.
        max_length (int, optional): The maximum length that ``arg_value`` is supposed to have.
        none_allowed (bool, optional): Indicates whether ``arg_value`` may be ``None``.
        none_elements_allowed (bool, optional): Indicates whether elements of ``arg_value`` may be ``None``.
        element_check_fn (optional): A callable that implements a custom sanity check. If provided, then it will be
            applied to every element of ``arg_value``.
        error_msg (str, optional): An optional error message that is provided if an error is raised.

    Raises:
        ValueError: If ``arg_value`` is not admissible.
        TypeError: If ``arg_value`` is not an ``Iterable`` or if not at least one of ``elements_type``,
            ``target_length``, ``min_length``, ``max_length``, and ``element_check_fn`` is provided.
    """
    # //////// Sanitize Args -------------------------------------------------------------------------------------------

    sanitize_type("arg_name", arg_name, str)
    sanitize_type("none_allowed", none_allowed, bool)
    sanitize_type("arg_value", arg_value, collections.Iterable, none_allowed=none_allowed)

    if elements_type is not None:
        if isinstance(elements_type, collections.Iterable):
            for t in elements_type:
                sanitize_type(
                        "elements_type",
                        t,
                        type,
                        error_msg=(
                                "The parameter <{arg_name}> has to be a type or an Iterable of types, "
                                "but contains an element of type {arg_value_type}!"
                        )
                )
        elif not isinstance(elements_type, type):
            raise TypeError(
                    "The parameter <elements_type> has to be a type or an Iterable of types, but is of type {}!".format(
                            type(elements_type).__name__
                    )
            )

    sanitize_type("target_length", target_length, int, none_allowed=True)
    if target_length is not None:
        sanitize_range("target_length", target_length, minimum=0)
    sanitize_type("min_length", min_length, int, none_allowed=True)
    if min_length is not None:
        sanitize_range("min_length", min_length, minimum=0)
    sanitize_type("max_length", max_length, int, none_allowed=True)
    if max_length is not None:
        sanitize_range("max_length", max_length, minimum=0)
    sanitize_type("none_elements_allowed", none_elements_allowed, bool)
    sanitize_type("error_msg", error_msg, str, none_allowed=True)

    if element_check_fn is not None and not callable(element_check_fn):
        raise TypeError("The parameter <element_check_fn> has to be callable!")

    if (
            elements_type is None and
            target_length is None and
            min_length is None and
            max_length is None and
            element_check_fn is None
    ):
        raise TypeError(
                "At least one of the parameters <elements_type>, <target_length>, <min_length>, <max_length>, "
                "and <element_check_fn> has to be specified!"
        )

    if (
            arg_value is not None and
            (target_length is not None or min_length is not None or max_length is not None) and
            not isinstance(arg_value, collections.Sized)
    ):
        raise TypeError(
                (
                        "The parameter <arg_value> has to be an instance of collections.abc.Sized in order to "
                        "perform length checks!"
                )
        )

    if target_length is not None and (min_length is not None or max_length is not None):
        raise ValueError(
                "If <target_length> is specified, then neither <min_length> nor <max_length> must be provided."
        )

    # //////// Perform Requested Sanity Check --------------------------------------------------------------------------

    # check if arg_value is acceptably None
    if arg_value is None:
        return

    # create error messages
    if error_msg is None:
        none_err = "The elements of <{arg_name}> must not be None!"
        if isinstance(elements_type, collections.Iterable):
            type_err_msg = \
                    "The types of the elements of <{arg_name}> have to be any of " + \
                    "[" + ", ".join([t.__name__ for t in elements_type]) + "], " + \
                    "but {arg_value_type} was encountered!"
        else:
            type_err_msg = (
                    "The type of the elements of <{arg_name}> has to be {target_type}, "
                    "but {arg_value_type} was encountered!"
            )
        len_err_msg = "The parameter <{arg_name}> has to be of length {target_value}, but has {arg_value} elements!"
        len_range = (
                ">= {min} and <= {max}"
                if min_length is not None and max_length is not None else
                (">= {min}" if min_length is not None else "<= {max}")
        ).format(
                min=min_length,
                max=max_length
        )
        range_err_msg = "The length of parameter <{arg_name}> has to be " + len_range + ", but is {arg_value}!"
    else:
        none_err = error_msg
        type_err_msg = error_msg
        len_err_msg = error_msg
        range_err_msg = error_msg

    # check if arg_value contains illegal None-elements
    if not none_elements_allowed and any([e is None for e in arg_value]):
        raise TypeError(none_err.format(arg_name=arg_name))

    # run through all elements of arg_value and check their types
    if elements_type is not None:
        for e in arg_value:
            sanitize_type(arg_name, e, elements_type, none_allowed=none_elements_allowed, error_msg=type_err_msg)

    # check length of arg_value
    if target_length is not None:
        sanitize_value(arg_name, len(arg_value), target_length, error_msg=len_err_msg)
    if min_length is not None or max_length is not None:
        sanitize_range(
                arg_name,
                len(arg_value),
                minimum=min_length,
                maximum=max_length,
                min_inclusive=True,
                max_inclusive=True,
                error_msg=range_err_msg
        )

    # run custom sanity checks (if element_check_fn is provided)
    if element_check_fn is not None:
        try:
            for e in arg_value:
                if e is not None:
                    element_check_fn(e)
        except Exception as ex:
            if error_msg is None:
                error_msg = "The parameter <{arg_name}> contains illegal elements: {}"
            raise ValueError(error_msg.format(str(ex), arg_name=arg_name))


def sanitize_range(
        arg_name: str,
        arg_value: numbers.Number,
        minimum: numbers.Number=None,
        maximum: numbers.Number=None,
        min_inclusive: bool=True,
        max_inclusive: bool=True,
        complement: bool=False,
        error_msg: str=None
) -> None:
    """Examines whether the value of a numerical arg is within a certain range.

    Args:
        arg_name (str): The name of the parameter being sanitized.
        arg_value (numbers.Number): The value that is subject of investigation.
        minimum (numbers.Number, optional): The minimum value that ``arg_value`` may have.
        maximum (numbers.Number, optional): The maximum value that ``arg_value`` may have.
        min_inclusive (bool, optional): Indicates whether ``minimum`` is an admissible value.
        max_inclusive (bool, optional): Indicates whether ``maximum` is an admissible value.
        complement (bool, optional): If ``True``, then values of the specified range are interpreted as prohibited
            rather than admissible.
        error_msg (str, optional): An optional error message that is provided if an error is raised.

    Raises:
        ValueError: If ``arg_value`` is out-of-range.`
        TypeError: If ``arg_value`` is not a number or if not at least one of ``minimum`` and ``maximum`` is provided.
    """
    # //////// Sanitize Args -------------------------------------------------------------------------------------------

    sanitize_type("arg_name", arg_name, str)
    sanitize_type("arg_value", arg_value, numbers.Number)
    sanitize_type("minimum", minimum, numbers.Number, none_allowed=True)
    sanitize_type("maximum", maximum, numbers.Number, none_allowed=True)
    sanitize_type("min_inclusive", min_inclusive, bool)
    sanitize_type("max_inclusive", max_inclusive, bool)
    sanitize_type("complement", complement, bool)
    sanitize_type("error_msg", error_msg, str, none_allowed=True)

    if minimum is None and maximum is None:
        raise TypeError("At least one of the parameters <minimum> and <maximum> has to be provided!")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError(
                "The parameter <minimum> must not be greater than <maximum>, but {} > {}!".format(
                        minimum,
                        maximum
                )
        )

    # if only one boundary is provided, then we can simply exchange min-max in order to handle complement checks
    if complement:
        if minimum is None:
            minimum = maximum
            maximum = None
            min_inclusive = not max_inclusive
            complement = False
        elif maximum is None:
            maximum = minimum
            minimum = None
            max_inclusive = not min_inclusive
            complement = False

    # //////// Perform Requested Sanity Check --------------------------------------------------------------------------

    # create error message
    if complement:
        min_sym = "<" if min_inclusive else "<="
        max_sym = ">" if max_inclusive else ">="
    else:
        min_sym = ">=" if min_inclusive else ">"
        max_sym = "<=" if max_inclusive else "<"
    if error_msg is None:
        if minimum is None:
            error_msg = "The parameter <{arg_name}> has to be {max_sym} {maximum}, but is {arg_value}!"
        elif maximum is None:
            error_msg = "The parameter <{arg_name}> has to be {min_sym} {minimum}, but is {arg_value}!"
        else:
            error_msg = \
                    "The parameter <{arg_name}> has to be {min_sym} {minimum} " + \
                    ("or " if complement else "and ") + \
                    "{max_sym} {maximum}, " + \
                    "but is {arg_value}!"
    error_msg = error_msg.format(
            arg_name=arg_name,
            arg_value=arg_value,
            minimum=minimum,
            maximum=maximum,
            min_sym=min_sym,
            max_sym=max_sym
    )

    # check value and raise ValueError if it is out-of-range
    out_of_range = (
            (
                    minimum is not None and
                    ((min_inclusive and arg_value < minimum) or (not min_inclusive and arg_value <= minimum))
            ) or
            (
                    maximum is not None and
                    ((max_inclusive and arg_value > maximum) or (not max_inclusive and arg_value >= maximum))
            )
    )
    if complement:
        out_of_range = not out_of_range
    if out_of_range:
        raise ValueError(error_msg)


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
