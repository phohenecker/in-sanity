in-sanity
=========


Even though it is sometimes considered to be "unpythonic", there are situations where we have to sanitize the value of a
function parameter in one way or the other.
A common example is the implementation of complicated mathematical models, e.g., for machine learning.
In a case like this, making assumptions about an arg explicit (by means of a sanity check) can often help to prevent
bugs that are hard to find otherwise. 

However, sanitizing parameters is tedious, and, on top of that, often inflates our code unnecessarily.
Therefore, to alleviate this sometimes necessary chore, the package `insanity` implements various common sanity checks
for function arguments, which allow for checking types as well as values of parameters concisely.


Installation
------------

This package can be installed from PyPI:
```
pip install insanity
```


Available Sanity Checks
-----------------------

The package `insanity` provides four basic sanity checks, which cover most of the commonly performed examinations.
All of the according check functions have a few things in common:
- The first two positional args, called `arg_name` and `arg_value`, expect the name of the arg that is being sanitized
  as well as the actual value that has been handed for it. 
- Check functions do not provide any return values, but rather signal a failed sanity check by raising either a
  `TypeError` or a `ValueError`. 
- Every check function accepts an optional keyword arg `error_msg`, which allows for specifying an error message that is
  passed to any error that is raised instead of the standard message. 


### Type Checks

The most basic among all sanity checks concerns the type of a provided arg, which is implemented by
[`insanity.sanitize_type`](src/main/python/insanity/sanity_checks.py#L352).
To use this function, we simply have to specify the type(s) that the sanitized arg may have:
```python
insanity.sanitize_type("some_arg", some_arg, int)
insanity.sanitize_type("some_arg", some_arg, [int, float])  # multiple types allowed
```
If we need to sanitize optional args that are `None` by default, then we may use the keyword arg `none_allowed` to
indicate that `None` is an allowed value, which is not the case otherwise:
```python
insanity.sanitize_type("some_arg", some_arg, str, none_allowed=True)
```


### Checking for Exhaustive Values

Often times, an arg needs to have one out of a fixed number of possible values.
In this case, args can be sanitized by means of
[`insanity.sanitize_value`](src/main/python/insanity/sanity_checks.py#L458)
This function accepts a few optional parameters, but in the most common case, we simply provide the values that the
sanitized arg may have as an `Iterable`:
```python
# an arg that may be either 0 or 1, specified as str or int
insanity.sanitize_value("some_arg", some_arg, [0, 1, "0", "1"])
```
Alternatively, one may specify prohibited rather than admissible values.
This is possible by providing the keyword arg `complement`:
```python
# an arg that may have any value EXCEPT 0 and 1
insanity.sanitize_value("some_arg", some_arg, [0, 1], complement=True)
```
There are a few rare cases in which we need to make use of a different notion of equality than the one that is realized
by Python's standard equality operator `==`.
In any such situation, a custom operator for comparing values may be provided via the keyword arg `equality_fn`:
```python
def eq_mod_5(x: int, y: int) -> bool:
    """Computes whether two integers are equal modulo 5."""
    return (x - y) % 5 == 0

# an arg that needs to be divisible by 5
insanity.sanitize_value(
    "some_arg",
    some_arg,
    0,
    equality_fn=eq_mod_5,
    error_msg="The arg is not divisible by 5!"
)
```
Finally, notice that `sanitize_value` again accepts the optional keyword arg `none_allowed` for indicating that the 
sanitized arg may be `None` (in addition the the specified admissible values).


### Checking Ranges

When we work with numbers, then we frequently have to ensure that args are within a certain range.
To that end, we can use
[`insanity.sanitize_range`](src/main/python/insanity/sanity_checks.py#L245),
which offers the self-explanatory keyword args `minimum`, `maximum`, `min_inclusive`, and `max_inclusive` for specifying
admissible intervals of values:
```python
# an arg that has to be in the half-closed interval [0, 1)
insanity.sanitize_range("some_arg", some_arg, minimum=0, maximum=1, min_inclusive=True, max_inclusive=False)
```
Just like `sanitize_value`, `sanitize_range` accepts the keyword arg `complement` for indicating that the described
range is prohibited rather than admissible.



### Sanitizing Iterables

The last of the provided sanity checks is for `Iterable`s, and is provided by
[`insanity.sanitize_iterable`](src/main/python/insanity/sanity_checks.py#L67)
This function accepts the following optional keyword args:
- `elements_type`: the type(s) that the elements may have,
- `target_length`: defines the exact length that the `Iterable` has to have,
- `min_length`: the minimum length of the `Iterable`,
- `max_length`: the maximum length of the `Iterable`,
- `none_allowed`: indicates whether the sanitized arg may be `None`, and
- `none_elements_allowed`: indicates whether the elements of the `Iterable` may be `None`.

Here is an example that demonstrates the use of this function:
```python
# an arg that needs to be an iterable that contains 10 to 20 numbers
insanity.sanitize_iterable(
    "some_arg",
    some_arg,
    elements_type=[int, float],
    min_length=10,
    max_length=20
)
```
To perform more comprehensive checks of the elements of an `Iterable`, `sanitize_iterable` provides the keyword arg
`element_check_fn`, which expects a function that, if provided, is applied to every element contained.
Any such custom check function should, like the ones provided by this package, raise an appropriate error if a
performed sanity check fails.
Notice that custom checks may be used in addition to those provided by `sanitized_iterable`.
Furthermore, the module `insanity.iterable_check_functions` provides two functions that may be provided via
`element_check_fn`, and that resemble the eponymous checks that are described above:
[`sanitize_range_fn`](src/main/python/insanity/iterable_check_functions.py#L46) and
[`sanitize_value_fn`](src/main/python/insanity/iterable_check_functions.py#L121).
