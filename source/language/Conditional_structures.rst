.. _PageConditionalStructures:

Conditional structures
======================

.. contents:: :local:
    :depth: 2


Introduction
------------

The conditional structures in Pine are `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ and
`switch <https://www.tradingview.com/pine-script-reference/v5/#op_switch>`__. They can be used:

- For their side effects, i.e., when they don't return a value but do things,
  like reassign values to variables or call functions.
- To return a value or a tuple which can then be assigned to one (or more, in the case of tuples) variable.



.. _PageConditionalStructures_If:

\`if\` structure
----------------

Whether an `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ 
structure is used for its side effects or to return a value, the value returned
by each of its local blocks must be of the same type, otherwise a compiler error will occur.



\`if\` used for its side effects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ 
structure used for its side effects has the following syntax::

    if <expression>
        <local_block>
    {else if <expression>
        <local_block>}
    [else
        <local_block>]

where:

- <expression> must be of "bool" type or be auto-castable to that type,
  which is only possible for "int" or "float" values (see the :ref:`Type system <PageTypeSystem_Types>` page).
- <local_block> consists of zero or more statements followed by a return value, which can be a tuple of values.
- There can be zero or more ``else if`` clauses.
- There can be zero or one ``else`` clause.

When the <expression> following the `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
evaluates to `true <https://www.tradingview.com/pine-script-reference/v5/#op_true>`__,
the first local block is executed, the `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
structure's execution ends, and the value(s) evaluated at the end of the local block are returned.

When the <expression> following the `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
evaluates to `false <https://www.tradingview.com/pine-script-reference/v5/#op_false>`__,
the successive ``else if`` clauses are evaluated, if there are any.
When the <expression> of one evaluates to `true <https://www.tradingview.com/pine-script-reference/v5/#op_true>`__,
its local block is executed, the `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
structure's execution ends, and the value(s) evaluated at the end of the local block are returned.

When no <expression> has evaluated to `true <https://www.tradingview.com/pine-script-reference/v5/#op_true>`__
and an ``else`` clause exists, its local block is executed, the `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
structure's execution ends, and the value(s) evaluated at the end of the local block are returned.

When no <expression> has evaluated to `true <https://www.tradingview.com/pine-script-reference/v5/#op_true>`__
and no ``else`` clause exists, `xxx <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ is returned.



\`if\` used to return a value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ 
structure used to return one or more values has the following syntax::

    [<declaration_mode>] [<type>] <identifier> = if <expression>
        <local_block>
    {else if <expression>
        <local_block>}
    [else
        <local_block>]

This is an example::

    //@version=5
    indicator("", "", true)
    string barState = if barstate.islastconfirmedhistory
        barState = "islastconfirmedhistory"
    else if barstate.isnew
        barState = "isnew"
    else if barstate.isrealtime
        barState = "isrealtime"
    else
        barState = "other"
    
    f_print(_text) => 
        var table _t = table.new(position.middle_right, 1, 1)
        table.cell(_t, 0, 0, _text, bgcolor = color.yellow)
    f_print(barState)

The type of the returning value of the ``if`` statement is determined by the type of
``return_expression_then`` and ``return_expression_else``. Their types
must match. It is not possible to return an integer value from the *then* block
if the *else* block returns a string value.

Example::

    // This code compiles
    x = if close > open
        close
    else
        open
    // This code doesn't compile
    x = if close > open
        close
    else
        "open"

It is possible to omit the *else* block. In this case, if the ``condition``
is false, an *empty* value (``na``, ``false``, or ``""``) will be assigned to the
``var_declarationX`` variable.

Example::

    x = if close > open
        close
    // If current close > current open, then x = close.
    // Otherwise the x = na.
    
It is possible to use either multiple *else if* blocks or none at all.

Example::

    x = if open > close
        5
    else if high > low
        close
    else
        open
        
The *then*, *else if* and *else* blocks are shifted by four spaces [#tabs]_. ``if`` statements can
be nested by adding four more spaces::

    x = if close > open
        b = if close > close[1]
            close
        else
            close[1]
        b
    else
        open

It is possible and quite frequent to ignore the resulting value of an ``if`` statement
(``var_declarationX =`` can be omited). This form is used when you need the
side effect of the expression, for example in ``strategy.*()`` calls:

::

    if (ta.crossover(source, lower))
        strategy.entry("BBandLE", strategy.long, stop=lower,
                       oca_name="BollingerBands",
                       oca_type=strategy.oca.cancel, comment="BBandLE")
    else
        strategy.cancel(id="BBandLE")



.. _PageConditionalStructures_Switch:

\`switch\` structure
--------------------



\`switch\` used for its side effects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



\`switch\` used to return a value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

