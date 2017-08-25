in-sanity
=========

Even though it is sometimes considered to be "unpythonic", there are situations where we have to sanitize the value of a
function parameter in some way or the other. A common example is the implementation of complicated mathematical models,
e.g., for machine learning. In a case like this, making assumptions about an arg explicit (by means of a sanity check)
can often help to prevent bugs that are hard to find otherwise. 

However, sanitizing parameters is, quite frankly, a pain in the ass, and, on top of that, often inflates our code
unnecessarily. Therefore, to alleviate this sometimes necessary evil, this package implements various common sanity
checks for function arguments, which allow for checking types as well as values of parameters concisely.

The package `insanity` provides four basic sanity checks, which cover most of the commonly performed examinations:

- checking types: [`insanity.sanitize_type`](https://github.com/phohenecker/in-sanity/blob/master/src/main/python/insanity/sanity_checks.py#L352)
- checking values: [`insanity.sanitize_value`](https://github.com/phohenecker/in-sanity/blob/master/src/main/python/insanity/sanity_checks.py#L458)
- checking ranges of numeric values: [`insanity.sanitize_range`](https://github.com/phohenecker/in-sanity/blob/master/src/main/python/insanity/sanity_checks.py#L245)
- checking the elements of an `Iterable`: [`insanity.sanitize_iterable`](https://github.com/phohenecker/in-sanity/blob/master/src/main/python/insanity/sanity_checks.py#L67)
