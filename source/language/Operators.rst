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

In order to fully understand how expressions are calculated in Pine, a good understanding of Pine *forms* and *types* is required. 
The :ref:`<PageTypeSystem_Forms>` page explains them.



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

Comparison operations are binary. The result is determined by the type
of the operands. If at least one of these operands has a *series* type, then
the type of the result will also be *series* (a series of logical
values). If both operands have a numerical type, then the result will be
of the logical type *bool*.



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

All logical operators can operate with *bool* operands, numerical
operands, or *series* type operands. As is the case with arithmetic and comparison
operators, if at least one of the operands is of *series*
type, then the result will also be of *series* type. In all other cases
the type of the result will be the logical type *bool*.

The operator ``not`` is unary. When applied to a ``true``
operand the result will be ``false``, and vice versa.

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

.. _ternary_operator:

\`?:\` ternary operator
-----------------------

The `?: ternary operator <https://www.tradingview.com/pine-script-reference/v5/#op_{question}{colon}>`__
evaluates if the first expression is (condition) and returns the value of either
the second operand (if the condition is ``true``) or of the third
operand (if the condition is ``false``). Syntax is::

    condition ? valueWhenConditionIsTrue : valueWhenConditionIsFalse

If ``condition`` is ``true`` then the ternary operator will return ``result1``,
otherwise it will return ``result2``.

A combination of conditional operators can build
constructs similar to *switch* statements. For
example::

    timeframe.isintraday ? color.red : timeframe.isdaily ? color.green : timeframe.ismonthly ? color.blue : na

The example is calculated from left to right.
First, the ``timeframe.isintraday`` condition is calculated; if it is ``true`` then
``color.red`` will be the result. If it is ``false`` then ``timeframe.isdaily`` is calculated,
if this is ``true``, then ``color.green`` will be the result. If it is
``false``, then ``timeframe.ismonthly`` is calculated. If it is ``true``, then ``color.blue``
will be the result, otherwise ``na`` will be the result.

Note that the two result values are expressions — not local blocks, so they will not affect the limit of 500 local blocks per scope.



.. _PageOperators_HistoryReferencingOperator:

\`[ ]\` History-referencing operator
------------------------------------

It is possible to refer to the historical values of any variable of the
*series* type with the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ operator. 
*Historical* values are variable values for the previous bars.

Most data in Pine is stored in series (somewhat like arrays, but with a dynamic index).
Let’s see how the index is dynamic, and why series are also very different from arrays.
In Pine, the ``close`` variable, or ``close[0]`` which is equivalent,
holds the price at the close of the current bar.
If your code is now executing on the **third** bar of the dataset,
``close`` will contain the price at the close of that bar,
``close[1]`` will contain the price at the close of the preceding bar (the second),
and ``close[2]``, the first. ``close[3]`` will return ``na`` because no bar exists
in that position, and thus its value is *not available*.

When the same code is executed on the next bar, the **fourth** in the dataset,
``close`` will now contain the closing price of that bar, and the same ``close[1]``
used in your code will now refer to the close of the third bar.
The close of the first bar in the dataset will now be ``close[3]``
and this time ``close[4]`` will return ``na``.

In the Pine runtime environment, as your code is executed once for each historical bar in the dataset,
starting from the left of the chart, Pine is adding a new element in the series at index 0
and pushing the pre-existing elements in the series one index further away.
Arrays, in comparison, are usually static in size and their content or indexing structure
is not modified by the runtime environment. Pine series are thus very different from arrays and
share familiarity with them mostly through their indexing syntax.

At the realtime, ``close`` variable 
represents the current price and will only contain the actual closing price of the
realtime bar the last time the script is executed on that bar, and from then on,
when it is referred to using the history-referencing operator.

Pine has a variable that keeps track of the bar count: ``bar_index``.
On the first bar, ``bar_index`` is equal to 0 and it increases by 1 at each new bar,
so at the last bar, ``bar_index`` is equal to the number of bars in the dataset minus one.

There is another important consideration to keep in mind when using the ``[]`` operator in
Pine. We have seen cases when a history reference may return the ``na``
value. ``na`` represents a value which is not a number and
using it in any math expression will produce a result that is also ``na`` (similar
to `NaN <https://en.wikipedia.org/wiki/NaN>`__).
Such cases often happen during the script's calculations in the
early bars of the dataset, but can also occur in later bars under certain conditions.
If your Pine code does not explicitly provide for handling these special cases,
they can introduce invalid results in your script's calculations
which can ripple through all the way to the realtime bar.
The `na <https://www.tradingview.com/pine-script-reference/v5/#fun_na>`__ and
`nz <https://www.tradingview.com/pine-script-reference/v5/#fun_nz>`__ functions
are designed to allow for handling such cases.

**Note 1**. Almost all built-in functions in Pine's standard library
return a *series* result. It is therefore
possible to apply the ``[]`` operator directly to function calls, as is done here:

::

    ta.sma(close, 10)[1]

**Note 2**. Despite the fact that the ``[]`` operator returns a result
of *series* type, it is prohibited to apply this operator to the same
operand over and over again. Here is an example of incorrect use
which will generate a compilation error:

::

    close[1][2] // Error: incorrect use of [] operator

In some situations, the user may want to shift the series to the left.
Negative arguments for the operator ``[]`` are prohibited. This can be
accomplished using the ``offset`` parameter in the ``plot`` annotation, which
supports both positive and negative values. Note though that it is a
visual shift., i.e., it will be applied after all calculations.
Further details on ``plot`` and its parameters can be found
`here <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__.



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

