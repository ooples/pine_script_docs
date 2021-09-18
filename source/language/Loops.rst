.. _PageLoops:

Loops
=====

.. contents:: :local:
    :depth: 2



.. _PageLoops_For:

\`for\`
-------

The `for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__ 
structure allows the repetitive execution of statements. Its syntax is::

    [[<declaration_mode>] [<type>] <identifier> = ]for <identifier> = <expression> to <expression>[ by <expression>]
        <local_block_loop>

where:

- Parts enclosed in square brackets (``[]``) can appear zero or one time, and those enclosed in curly braces (``{}``) can appear zero or more times.
- <declaration_mode> is the variable's :ref:`declaration mode <PageVariableDeclarations_DeclarationModes>`
- <type> is optional, as in almost all Pine variable declarations (see :ref:`types <PageTypeSystem_Types>`)
- <identifier> is a variable's :ref:`name <PageIdentifiers>`
- <expression> can be a literal, a variable, an expression or a function call.
- <local_block_loop> consists of zero or more statements followed by a return value, which can be a tuple of values.
  It must be indented by four spaces or a tab. It can contain the ``break`` statement to exit the loop, 
  or the ``continue`` statement to exit the current iteration and continue on with the next.
- The value assigned to the variable is the return value of the <local_block_loop>, or 
  `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ if no local block is executed.
- The identifier in ``for <identifier>`` is the loop's counter *initial value*.
- The expression in ``= <expression>`` is the *start value* of the counter.
- The expression in ``to <expression>`` is the *end value* of the counter. **It is only evaluated upon entry in the loop**.
- The expression in ``by <expression>`` is optional.
  It is the step by which the loop counter is increased or decreased on each iteration of the loop.
  Its default value is 1 when ``start value < end value``. It is -1 when ``start value > end value``.
  The step (+1 or -1) used as the default is determined by the start and end values.

This example uses a `for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__ 
statement to look back a user-defined amount of bars to determine how many bars have a 
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ that is higher or lower than the 
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ of the last bar on the chart. 
A `for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__ loop is necessary here, 
since the script only has access to the reference value on the chart's last bar. 
Pine's runtime cannot, here, be used to calculate on the fly, as the script is executing bar to bar::

    //@version=5
    indicator("`for` loop")
    lookbackInput = input.int(50, "Lookback in bars", minval = 1, maxval = 4999)
    higherBars = 0
    lowerBars = 0
    if barstate.islast
        var label lbl = label.new(na, na, "", style = label.style_label_left)
        for i = 1 to lookbackInput
            if high[i] > high
                higherBars += 1
            else if high[i] < high
                lowerBars += 1
        label.set_xy(lbl, bar_index, high)
        label.set_text(lbl, str.tostring(higherBars, "# higher bars\n") + str.tostring(lowerBars, "# lower bars"))




.. _PageLoops_For:

\`while\`
---------

::

    <while_structure>
        while <expression>
            <local_block_loop>
