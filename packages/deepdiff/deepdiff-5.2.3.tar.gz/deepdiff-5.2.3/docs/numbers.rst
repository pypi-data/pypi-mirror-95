:doc:`/index`

Numbers
=======

When dealing with numbers, DeepDiff provides the following functionalities:

.. _significant_digits_label:

Significant Digits
------------------

significant_digits : int >= 0, default=None

significant_digits defines the number of digits AFTER the decimal point to be used in the comparison. However you can override that by setting the number_format_notation="e" which will make it mean the digits in scientific notation.

.. note::
    Setting significant_digits will affect ANY number comparison.

If ignore_numeric_type_changes is set to True and you have left significant_digits to the default of None, it gets automatically set to 55. The reason is that normally when numbers from 2 different types are compared, instead of comparing the values, we only report the type change. However when ignore_numeric_type_changes=True, in order compare numbers from different types to each other, we need to convert them all into strings. The significant_digits will be used to make sure we accurately convert all the numbers into strings in order to report the changes between them.

.. note::
    significant_digits by default uses "{:.Xf}".format(Your Number) behind the scene to compare numbers where X=significant_digits when the number_format_notation is left as the default of "f" meaning fixed point.

    As a side note, please pay attention that adding digits to your floating point can result in small differences in the results. For example:
    "{:.3f}".format(1.1135) = 1.113, but "{:.3f}".format(1.11351) = 1.114

    For Decimals, Python's format rounds 2.5 to 2 and 3.5 to 4 (to the closest even number)

.. note::
    To override what significant digits mean and switch it to scientific notation, use number_format_notation="e
    Behind the scene that switches DeepDiff to use "{:.Xe}".format(Your Number) where X=significant_digits.

**Examples:**

Approximate decimals comparison (Significant digits after the point):
    >>> t1 = Decimal('1.52')
    >>> t2 = Decimal('1.57')
    >>> DeepDiff(t1, t2, significant_digits=0)
    {}
    >>> DeepDiff(t1, t2, significant_digits=1)
    {'values_changed': {'root': {'new_value': Decimal('1.57'), 'old_value': Decimal('1.52')}}}

Approximate float comparison (Significant digits after the point):
    >>> t1 = [ 1.1129, 1.3359 ]
    >>> t2 = [ 1.113, 1.3362 ]
    >>> pprint(DeepDiff(t1, t2, significant_digits=3))
    {}
    >>> pprint(DeepDiff(t1, t2))
    {'values_changed': {'root[0]': {'new_value': 1.113, 'old_value': 1.1129},
                        'root[1]': {'new_value': 1.3362, 'old_value': 1.3359}}}
    >>> pprint(DeepDiff(1.23*10**20, 1.24*10**20, significant_digits=1))
    {'values_changed': {'root': {'new_value': 1.24e+20, 'old_value': 1.23e+20}}}


.. _number_format_notation_label:

Number Format Notation
----------------------

number_format_notation : string, default="f"
    number_format_notation is what defines the meaning of significant digits. The default value of "f" means the digits AFTER the decimal point. "f" stands for fixed point. The other option is "e" which stands for exponent notation or scientific notation.

**Examples:**

Approximate number comparison (significant_digits after the decimal point in scientific notation)
    >>> DeepDiff(1024, 1020, significant_digits=2, number_format_notation="f")  # default is "f"
    {'values_changed': {'root': {'new_value': 1020, 'old_value': 1024}}}
    >>> DeepDiff(1024, 1020, significant_digits=2, number_format_notation="e")
    {}

.. _number_to_string_func_label:

Number To String Function
-------------------------

number_to_string_func : function, default=None
    In many cases DeepDiff converts numbers to strings in order to compare them. For example when ignore_order=True, when significant digits parameter is defined or when the ignore_numeric_type_changes=True.
    In its simplest form, the number_to_string_func is "{:.Xf}".format(Your Number) where X is the significant digits and the number_format_notation is left as the default of "f" meaning fixed point.
    The number_to_string_func parameter gives the user the full control into overriding how numbers are converted to strings for comparison. The default function is defined in https://github.com/seperman/deepdiff/blob/master/deepdiff/helper.py and is called number_to_string. You can define your own custom function instead of the default one in the helper module.

Defining your own number_to_string_func
    Lets say you want the numbers comparison happen only for numbers above 100 for some reason.

    >>> from deepdiff import DeepDiff
    >>> from deepdiff.helper import number_to_string
    >>> def custom_number_to_string(number, *args, **kwargs):
    ...     number = 100 if number < 100 else number
    ...     return number_to_string(number, *args, **kwargs)
    ...
    >>> t1 = [10, 12, 100000]
    >>> t2 = [50, 63, 100021]
    >>> DeepDiff(t1, t2, significant_digits=3, number_format_notation="e")
    {'values_changed': {'root[0]': {'new_value': 50, 'old_value': 10}, 'root[1]': {'new_value': 63, 'old_value': 12}}}
    >>> 
    >>> DeepDiff(t1, t2, significant_digits=3, number_format_notation="e",
    ...          number_to_string_func=custom_number_to_string)
    {}


Ignore Numeric Type Changes
---------------------------

ignore_numeric_type_changes: Boolean, default = False
read more at :ref:`ignore_numeric_type_changes_label`

.. _ignore_nan_inequality_label:

Ignore Nan Inequality
---------------------

ignore_nan_inequality: Boolean, default = False
    Whether to ignore float('nan') inequality in Python. Note that this is a cPython "feature". Some versions of Pypy3 have nan==nan where in cPython nan!=nan

    >>> float('nan') == float('nan')
    False
    >>> DeepDiff(float('nan'), float('nan'))
    {'values_changed': {'root': {'new_value': nan, 'old_value': nan}}}
    >>> DeepDiff(float('nan'), float('nan'), ignore_nan_inequality=True)
    {}

.. _math_epsilon_label:

Math Epsilon
------------

math_epsilon: Decimal, default = None
    math_epsilon uses Python's built in Math.isclose. It defines a tolerance value which is passed to math.isclose(). Any numbers that are within the tolerance will not report as being different. Any numbers outside of that tolerance will show up as different.

    For example for some sensor data derived and computed values must lie in a certain range. It does not matter that they are off by e.g. 1e-5.

    To check against that the math core module provides the valuable isclose() function. It evaluates the being close of two numbers to each other, with reference to an epsilon (abs_tol). This is superior to the format function, as it evaluates the mathematical representation and not the string representation.

Example:
    >>> from decimal import Decimal
    >>> d1 = {"a": Decimal("7.175")}
    >>> d2 = {"a": Decimal("7.174")}
    >>> DeepDiff(d1, d2, math_epsilon=0.01)
    {}

.. note::
    math_epsilon cannot currently handle the hashing of values, which is done when :ref:`ignore_order_label` is True.


Performance Improvement of Numbers diffing
------------------------------------------

Take a look at :ref:`diffing_numbers_optimizations_label`

Back to :doc:`/index`
