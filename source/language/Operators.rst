.. _PageOperators:

Operators
=========

.. contents:: :local:
    :depth: 2


Introduction
------------

Some operators are used to build *expressions* returning a result:

- Arithmetic operators
- Comparison operators
- Logical operators
- The `?: <https://www.tradingview.com/pine-script-reference/v5/#op_{question}{colon}>`__ ternary operator
- The `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ history-referencing operator

Other operators are used to assign values to variables:

- ``=`` is used to assign a value to a variable, **but only when you declare the variable** (the first time you use it)
- ``:=`` is used to assign a value to a **previously declared variable**. The following operators can also be used in such a way: ``+=``, ``-=``, ``*=``, ``/=``, ``%=``

As is explained in the :ref:`<PageTypeSystem_Forms>` page, *forms* and *types* play a critical role in determining the type of results that expressions yield.
This, in turn, has an impact on how and with what functions you will be allowed to use those results. 
Expressions always return a form of the strongest one used in the expression, e.g., if you multiply an "input int" with a "series int", 
the expression will produce a "series int" result, which you will not be able to use as the argument to ``length`` in 
`ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__.

This script will produce a compilation error::

    //@version=5
    indicator("")
    lenInput = input.int(14, "Length")
    factor = year > 2020 ? 3 : 1
    adjustedLength = lenInput * factor
    ma = ta.ema(close, adjustedLength)  // Compilation error!
    plot(ma)

The compiler will complain: *Cannot call 'ta.ema' with argument 'length'='adjustedLength'. An argument of 'series int' type was used but a 'simple int' is expected;*.
This is happening because ``lenInput`` is an "input int" but ``factor`` is a "series int" (it can only be determined by looking at the value of 
`year <https://www.tradingview.com/pine-script-reference/v5/#var_year>`__ on each bar). 
The ``adjustedLength`` variable is thus assigned a "series int" value. 
Our problem is that the Reference Manual entry for `ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__ tells us that its ``length`` parameter requires values of "simple" form, which is a weaker form that "series", so a "series int" value is not allowed.

The solution to our conundrum requires:

- Using another moving average function that supports a "series int" length, such as `ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__, or
- Not using a calculation producing a "series int" value for our length.



Arithmetic operators
--------------------

There are five arithmetic operators in Pine Script:

+-------+------------------------------------+
| ``+`` | Addition                           |
+-------+------------------------------------+
| ``-`` | Subtraction                        |
+-------+------------------------------------+
| ``*`` | Multiplication                     |
+-------+------------------------------------+
| ``/`` | Division                           |
+-------+------------------------------------+
| ``%`` | Modulo (remainder after division)  |
+-------+------------------------------------+

The arithmetic operators above are all binary (means they need two *operands* — or values — to work on, like in ``1 + 2``). 
The ``+`` and ``-`` also serve as unary operators (means they work on one operand, like ``-1`` or ``+1``).

If both operands are numbers but at least one of these is of "float" type, the result will also be a "float". 
If both operands are of "int" type, the result will also be an "int".
If at least one operand is `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__, 
the result is also `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__.

The ``+`` operator also serves as the concatenation operator for strings. ``"EUR"+"USD"`` yields the ``"EURUSD"`` string.



Comparison operators
--------------------

There are six comparison operators in Pine Script:

+--------+---------------------------------+
| ``<``  | Less Than                       |
+--------+---------------------------------+
| ``<=`` | Less Than or Equal To           |
+--------+---------------------------------+
| ``!=`` | Not Equal                       |
+--------+---------------------------------+
| ``==`` | Equal                           |
+--------+---------------------------------+
| ``>``  | Greater Than                    |
+--------+---------------------------------+
| ``>=`` | Greater Than or Equal To        |
+--------+---------------------------------+

Comparison operations are binary. If both operands have a numerical value, the result will be of type *bool*, i.e., ``true``, ``false`` or 
`na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__.

Examples::

    1 > 2  // false
    1 != 1 // false
    close >= open  // Depends on values of `close` and `open`



Logical operators
-----------------

There are three logical operators in Pine Script:

+---------+---------------------------------+
| ``not`` | Negation                        |
+---------+---------------------------------+
| ``and`` | Logical Conjunction             |
+---------+---------------------------------+
| ``or``  | Logical Disjunction             |
+---------+---------------------------------+

The operator ``not`` is unary. When applied to a ``true``, operand the result will be ``false``, and vice versa.

``and`` operator truth table:

+---------+---------+-----------+
| a       | b       | a and b   |
+=========+=========+===========+
| true    | true    | true      |
+---------+---------+-----------+
| true    | false   | false     |
+---------+---------+-----------+
| false   | true    | false     |
+---------+---------+-----------+
| false   | false   | false     |
+---------+---------+-----------+

``or`` operator truth table:

+---------+---------+----------+
| a       | b       | a or b   |
+=========+=========+==========+
| true    | true    | true     |
+---------+---------+----------+
| true    | false   | true     |
+---------+---------+----------+
| false   | true    | true     |
+---------+---------+----------+
| false   | false   | false    |
+---------+---------+----------+



.. _PageOperators_TernaryOperator:

\`?:\` ternary operator
-----------------------

The `?: <https://www.tradingview.com/pine-script-reference/v5/#op_{question}{colon}>`__ ternary operator is used to create expressions of the form::

    condition ? valueWhenConditionIsTrue : valueWhenConditionIsFalse

The ternary operator returns a result that depends on the value of ``condition``. If it is ``true``,  then ``valueWhenConditionIsTrue`` is returned.
If ``condition`` is ``false`` or `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__,  then ``valueWhenConditionIsFalse`` is returned.

A combination of ternary expressions can be used to achieve the same effect as a 
`switch <https://www.tradingview.com/pine-script-reference/v5/#op_switch>`__ structure, e.g.::

    timeframe.isintraday ? color.red : timeframe.isdaily ? color.green : timeframe.ismonthly ? color.blue : na

The example is calculated from left to right:

- If `timeframe.isintraday <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}isintraday>`__ is ``true``,
  then ``color.red`` is returned. If it is ``false``, then `timeframe.isdaily <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}isdaily>`__ is evaluated.
- If `timeframe.isdaily <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}isdaily>`__ is ``true``, 
  then ``color.green`` is returned. If it is ``false``, 
  then `timeframe.ismonthly <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}ismonthly>`__ is evaluated. 
- If `timeframe.ismonthly <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}ismonthly>`__ is ``true``, 
  then ``color.blue`` is returned, otherwise `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ is returned.

Note that the return values on each side of the ``:`` are expressions — not local blocks, so they will not affect the limit of 500 local blocks per scope.



.. _PageOperators_HistoryReferencingOperator:

\`[ ]\` history-referencing operator
------------------------------------

It is possible to refer to past values of :ref:`time series <PageTimeSeries>` using the 
`[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ history-referencing operator. 
Past values are values a variable had on bars preceding the bar where the script is currently executing — the *current bar*.
See the :ref:`<PageExecutionModel>` page for more information about the way scripts are executed on bars.

The `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ operator is used after a variable, expression or function call.
The value used inside the square brackets of the operator is the offset in the past we want to refer to.
To refer to the value of the `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__ 
built-in variable two bars away from the current bar, one would use ``volume[2]``.

Because series grow dynamically, as the script moves on sucessive bars, the offset used with the operator will refer to different bars.
Let’s see how the offset is dynamic, and why series are also very different from arrays.
In Pine, the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ variable, or ``close[0]`` which is equivalent,
holds the price at the "close" of the current bar.
If your code is now executing on the **third** bar of the dataset (the set of all bars on your chart), ``close`` will contain the price at the close of that bar,
``close[1]`` will contain the price at the close of the preceding bar (the dataset's second bar),
and ``close[2]``, the first bar. ``close[3]`` will return `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ 
because no bar exists in that position, and thus its value is *not available*.

When the same code is executed on the next bar, the **fourth** in the dataset,
``close`` will now contain the closing price of that bar, and the same ``close[1]``
used in your code will now refer to the "close" of the third bar in the dataset.
The close of the first bar in the dataset will now be ``close[3]``, 
and this time ``close[4]`` will return `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__.

In the Pine runtime environment, as your code is executed once for each historical bar in the dataset,
starting from the left of the chart, Pine is adding a new element in the series at index 0
and pushing the pre-existing elements in the series one index further away.
Arrays, in comparison, can have constant or variable sizes, and their content or indexing structure
is not modified by the runtime environment. Pine series are thus very different from arrays and
only share familiarity with them through their indexing syntax.

When the market for the chart symbol is open and the script is executing on the chart's last bar, the *realtime bar*, 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ return the value of the current price. 
It will only contain the actual closing price of the realtime bar the last time the script is executed on that bar, when it closes.

Pine has a variable that contains the number of the bar the script is executing on: 
`bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__.
On the first bar, `bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__ 
is equal to 0 and it increases by 1 on each successive bar the script executes on.
On the last bar, `bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__ is equal to the number of bars in the dataset minus one.

There is another important consideration to keep in mind when using the ``[]`` operator in
Pine. We have seen cases when a history reference may return the `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__
value. `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ represents a value which is not a number and
using it in any math expression will produce a result that is also `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ (similar
to `NaN <https://en.wikipedia.org/wiki/NaN>`__).
Such cases often happen during the script's calculations in the
early bars of the dataset, but can also occur in later bars under certain conditions.
If your Pine code does not explicitly provide for handling these special cases,
they can introduce invalid results in your script's calculations
which can ripple through all the way to the realtime bar.
The `na <https://www.tradingview.com/pine-script-reference/v5/#fun_na>`__ and
`nz <https://www.tradingview.com/pine-script-reference/v5/#fun_nz>`__ functions
are designed to allow for handling such cases.


::

    ta.sma(close, 10)[1]

**Note 2**. Despite the fact that the ``[]`` operator returns a result
of *series* type, it is prohibited to apply this operator to the same
operand over and over again. Here is an example of incorrect use
which will generate a compilation error:


Note that the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ can only be used once on the same value. This is not allowed::

    close[1][2] // Error: incorrect use of [] operator



Operator precedence
-------------------

The order of calculations is determined by the operators' precedence.
Operators with greater precedence are calculated first. Below is a list
of operators sorted by decreasing precedence:

+------------+-------------------------------------+
| Precedence | Operator                            |
+============+=====================================+
| 9          | ``[]``                              |
+------------+-------------------------------------+
| 8          | unary ``+``, unary ``-``, ``not``   |
+------------+-------------------------------------+
| 7          | ``*``, ``%``                        |
+------------+-------------------------------------+
| 6          | ``+``, ``-``                        |
+------------+-------------------------------------+
| 5          | ``>``, ``<``, ``>=``, ``<=``        |
+------------+-------------------------------------+
| 4          | ``==``, ``!=``                      |
+------------+-------------------------------------+
| 3          | ``and``                             |
+------------+-------------------------------------+
| 2          | ``or``                              |
+------------+-------------------------------------+
| 1          | ``?:``                              |
+------------+-------------------------------------+

If in one expression there are several operators with the same precedence,
then they are calculated left to right.

If the expression must be calculated in a different order than precedence would dictate,
then parts of the expression can be grouped together with parentheses.



\`=\` assignement operator
-----------------------------------



\`:=\` reassignement operator
--------------------------------------

