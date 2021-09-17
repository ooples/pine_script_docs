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

Conditional structures can be embedded; you can use an 
`if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ or
`switch <https://www.tradingview.com/pine-script-reference/v5/#op_switch>`__
inside another one.

The local blocks in conditional structures must be indented by four spaces or a tab.



.. _PageConditionalStructures_If:

\`if\` structure
----------------



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
and no ``else`` clause exists, `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ is returned.

Using `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
structures for their side effects can be useful to manage the order flow in strategies, for example.
While the same functionality can often be achieved using the ``when`` parameter in 
``strategy.*()`` calls, code using `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
structures is easier to read::

    if (ta.crossover(source, lower))
        strategy.entry("BBandLE", strategy.long, stop=lower,
                       oca_name="BollingerBands",
                       oca_type=strategy.oca.cancel, comment="BBandLE")
    else
        strategy.cancel(id="BBandLE")



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

where:

- <declaration_mode> is the variable's :ref:`declaration mode <PageVariableDeclarations_DeclarationModes>`
- The type is optional, as in almost all Pine variable declarations (see :ref:`types <PageTypeSystem_Types>`)
- <identifier> is the variable's :ref:`name <PageIdentifiers>`
- The value assigned to the variable is the return value of the <local_block>, or 
  `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ if no local block is executed.

This is an example::

    //@version=5
    indicator("", "", true)
    string barState = if barstate.islastconfirmedhistory
        "islastconfirmedhistory"
    else if barstate.isnew
        "isnew"
    else if barstate.isrealtime
        "isrealtime"
    else
        "other"
    
    f_print(_text) => 
        var table _t = table.new(position.middle_right, 1, 1)
        table.cell(_t, 0, 0, _text, bgcolor = color.yellow)
    f_print(barState)

It is possible to omit the *else* block. In this case, if the ``condition``
is false, an *empty* value (``na``, ``false``, or ``""``) will be assigned to the
``var_declarationX`` variable.

This is an example showing how 
`na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__
is returned when no local block is executed. If ``close > open`` is ``false`` in here,
`na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ is returned::

    x = if close > open
        close



.. _PageConditionalStructures_Switch:

\`switch\` structure
--------------------



\`switch\` used for its side effects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



\`switch\` used to return a value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Matching local block type requirement
-------------------------------------

Whether an `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ 
structure is used for its side effects or to return a value, the value returned
by each of its local blocks must be of the same type, otherwise a compiler error will occur.

This code compiles fine because `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
and `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__ are both of "float" type::

    x = if close > open
        close
    else
        open

This code does not compile because the first local block returns a "float" and the second one, a "string" value::

    // Compilation error!
    x = if close > open
        close
    else
        "open"

While this makes perfect sense when using conditional structures to assign a value to a variable,
it can sometimes cause problems when conditional structures are used for their side effects.
To work around this limitation, you can force the type of the local block's unused return value, eg.::

    //@version=5
    indicator("", "", true)
    var closeLine = line.new(bar_index - 1, close, bar_index, close, extend = extend.right, width = 3)
    if barstate.islast
        if syminfo.type == "crypto"
            line.set_xy1(closeLine, bar_index - 1, close)
            line.set_xy2(closeLine, bar_index, close)
            int(na)
        else
            label.new(bar_index, high, "Not a crypto market")
            int(na)

Note that we make the return value of each local block ``int(na)``, 
which is the `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__
value cast to an integer using `int() <https://www.tradingview.com/pine-script-reference/v5/#fun_int>`__.
This way, they both return an "int", which is not assigned to any variable.
Without these additions to our code, it would not compile.