.. image:: /images/Pine_Script_logo.svg
   :alt: Pine Script™ logo
   :target: https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html
   :align: right
   :width: 100
   :height: 100


.. _PageFunctionsFaq:



Functions FAQ
=============


.. contents:: :local:
    :depth: 3


Can I use a variable length in functions?
-----------------------------------------



How can I calculate values depending on variable lengths that reset on a condition?
-----------------------------------------------------------------------------------



Why do some functions and built-ins evaluate incorrectly in if or ternary (?) blocks?
-------------------------------------------------------------------------------------



How can I round a number to x increments?
-----------------------------------------

::

    //@version=5
    indicator("Round fraction example")
    incrementAmt = input.float(0.75, "Increment", step = 0.01)

    roundToIncrement(value, increment) =>
        // Kudos to @veryevilone for the idea.
        math.round(value / increment) * increment

    plot(roundToIncrement(close, incrementAmt))



How can I control the number of decimals used in displaying my script’s values?
-------------------------------------------------------------------------------

Rounding behavior in displayed values is controlled by a combination of your script’s ``precision =`` and ``format =`` arguments in its 
`indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__ or 
`strategy() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__ declaration statement. 
Make sure to consult the `Pine Script™ User Manual <https://www.tradingview.com/pine-script-docs/en/v5/language/Script_structure.html#declaration-statement>`__ on the subject. 
The default will use the precision of the price scale. To increase it, you will need to specify a ``precision =`` argument greater than that of the price scale.



How can I control the precision of values used in my calculations?
------------------------------------------------------------------

You can use the ``math.round(number, precision)`` form of `math.round() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}round>`__ to round values. 
You can also round values to tick precision using our function from this entry.



How can I round down the number of decimals of a value?
-------------------------------------------------------

This function allows you to truncate the number of decimal places of a float value. ``roundDown(1.218, 2)`` will return “1.21”, and ``roundDown(-1.218, 2)`` will return “-1.22”:

::

    roundDown(number, decimals) =>
    (math.floor(number * math.pow(10, decimals))) / math.pow(10, decimals)

Thanks to `Daveatt <https://www.tradingview.com/u/Daveatt/#published-scripts>`__ for the function.



How can I round to ticks?
-------------------------

Use `math.round_to_mintick() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}round_to_mintick>`__. 
If you need to round a string representation of a number, use ``str.tostring(x, format.mintick)``.



How can I abbreviate large values?
----------------------------------

To abbreviate large values like `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__ (e.g., 1,222,333.0 ► “1.222M”), you can:

 - Use ``format = format.volume`` in `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__ or 
 `strategy() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__. This affects all values displayed by the script.
 - Use ``str.tostring(value, format.volume)`` to abbreviate specific values.
 - Use a function such as this ``abbreviateValue(value, precision)``, which allows you to specify a custom precision, abbreviates up to trillions, 
 and provides subtle spacing between the value and the letter denoting the magnitude:

::

    //@version=5
    indicator("Value abbreviation example")
    // ————— Function to format large values.
    abbreviateValue(value, precision) =>  // Thx Alex P.!
        // float value : value to format.
        // string precision : format suffix for precision ("" for none, ".00" for two digits, etc.)
        float digitsAmt = math.log10(math.abs(value))
        string formatPrecision = "#" + precision
        string result = if digitsAmt > 12
            str.tostring(value / 1e12, formatPrecision + "  T")
        else if digitsAmt > 9
            str.tostring(value / 1e9, formatPrecision + "  B")
        else if digitsAmt > 6
            str.tostring(value / 1e6, formatPrecision + "  M")
        else if digitsAmt > 3
            str.tostring(value / 1e3, formatPrecision + "  K")
        else
            str.tostring(value, "#" + formatPrecision)
        result

    print(formattedString) =>
        var table t = table.new(position.middle_right, 1, 1)
        table.cell(t, 0, 0, formattedString, bgcolor = color.yellow)
    print(abbreviateValue(volume, ".00"))



How can I calculate using pips?
-------------------------------

Use this function to return the correct pip value for Forex symbols:

::

    getForexPips() => syminfo.mintick * (syminfo.type == "forex" ? 10 : 1)



How do I calculate averages?
----------------------------

 - If the values you need to average are in distinct variables, you can use `math.avg() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}avg>`__.
 - If you need the average between a single bar’s prices, see `hl2 <https://www.tradingview.com/pine-script-reference/v5/#var_hl2>`__, 
 `hlc3 <https://www.tradingview.com/pine-script-reference/v5/#var_hlc3>`__, `hlcc4 <https://www.tradingview.com/pine-script-reference/v5/#var_hlcc4>`__, 
 or `ohlc4 <https://www.tradingview.com/pine-script-reference/v5/#var_ohlc4>`__.
 - To average the last n values in a series, you can use `ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__.
 - You can also use an array to build a custom set of values and then use `array.avg() <https://www.tradingview.com/pine-script-reference/v5/#fun_array{dot}avg>`__ to average them. 
 See the `Pine Script™ User Manual Arrays page <https://www.tradingview.com/pine-script-docs/en/v5/language/Arrays.html>`__ for more information.
 - Finally, you can use a matrix to build a custom set of values and then use `matrix.avg() <https://www.tradingview.com/pine-script-reference/v5/#fun_matrix{dot}avg>`__ 
 to average them. See `this blog post introducing the new matrix feature <https://www.tradingview.com/blog/en/matrices-come-to-pine-script-30693/>`__ for more information.



How can I calculate an average only when a certain condition is true?
---------------------------------------------------------------------

`This script <https://www.tradingview.com/script/9l0ZpuQU-ConditionalAverages/>`__ shows how to calculate conditional averages using many different methods.



How can I generate a random number?
-----------------------------------

Use the `math.random() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}random>`__ function.



How can I evaluate a filter I am planning to use?
-------------------------------------------------



.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/