.. _PageLoops:

Loops
=====



.. _PageLoops_ForStatement:

\`for\`
-------

The ``for`` statement allows to execute a number of instructions repeatedly:

.. code-block:: text

    <var_declarationX> = for <i> = <from> to <to> by <step>
        <var_decl0>
        <var_decl1>
        ...
        continue
        ...
        break
        ...
        <var_declN>
        <return_expression>

where:

-  ``i`` --- a loop counter variable.
-  ``from`` --- start value of the counter.
-  ``to`` --- end value of the counter. When the counter becomes greater
   than ``to`` (or less than ``to`` in the case where ``from > to``) the
   loop is stopped.
-  ``step`` --- loop step. Optional. Default is 1. If
   ``from`` is greater than ``to``, the loop step will automatically change direction; no need to use a negative step.
-  ``var_decl0``, ... ``var_declN``, ``return_expression`` --- body of the loop. It
   must be indented by 4 spaces [#tabs]_.
-  ``return_expression`` --- returning value. When a loop is finished or
   broken, the returning value is assigned to ``var_declarationX``.
-  ``continue`` --- a keyword. Can only be used in loops. It jumps to the loop's
   next iteration.
-  ``break`` --- a keyword. Can be used only in loops. It exits the loop.

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




\`while\`
---------
