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

You can use a ``series int`` length (a length that varies from bar to bar) in the following Pine Script™ functions: 
`ta.alma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}alma>`__, `ta.bb() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}bb>`__, 
`ta.bbw() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}bbw>`__, `ta.cci() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}cci>`__, 
`ta.change() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}change>`__, `ta.cmo() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}cmo>`__, 
`ta.cog() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}cog>`__, `ta.correlation() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}correlation>`__, 
`ta.dev() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}dev>`__, `ta.falling() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}falling>`__, 
`ta.highest() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}highest>`__, `ta.highestbars() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}highestbars>`__, 
`ta.linreg() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}linreg>`__, `ta.lowest() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}lowest>`__, 
`ta.lowestbars() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}lowestbars>`__, `ta.mfi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}mfi>`__, 
`ta.mom() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}mom>`__, 
`ta.percentile_linear_interpolation() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}percentile_linear_interpolation>`__, 
`ta.percentile_nearest_rank() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}percentile_nearest_rank>`__, 
`ta.percentrank() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}percentrank>`__, 
`ta.rising() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}rising>`__, `ta.roc() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}roc>`__, 
`ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__, `ta.stdev() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}stdev>`__, 
`ta.stoch() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}stoch>`__, `math.sum() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}sum>`__, 
`ta.variance() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}variance>`__, `ta.vwma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}vwma>`__, 
`ta.wma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}wma>`__, and `ta.wpr() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}wpr>`__.



How can I calculate values depending on variable lengths that reset on a condition?
-----------------------------------------------------------------------------------

Such calculations typically use `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__ 
to determine the number of bars elapsed since a condition occurs. When using variable lengths, you must pay attention to the following:

 - `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__ returns zero on the bar where the condition is met. 
 Lengths, however, cannot be zero, so you need to ensure the length has a minimum value of one, which can be accomplished by using 
 `math.max() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}max>`__.
 - At the beginning of a dataset, until the condition is detected a first time, `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__ 
 returns na, which also cannot be used as a length, so you must protect your calculation against this, which can be done by using 
 `nz() <https://www.tradingview.com/pine-script-reference/v5/#fun_nz>`__.
 - The length must be an ``int``, so it is safer to cast the result of your length’s calculation to an ``int`` using 
 `int() <https://www.tradingview.com/pine-script-reference/v5/#fun_int>`__.
 - Finally, a `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__ value of 0 must translate to a variable length of 1, 
 and so on, so we must add 1 to the value returned by `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__.

Put together, these requirements yield code such as this example to calculate the lowest low since ``cond`` has occurred the last time:

::

    //@version=5
    indicator("Lowest low since condition", "", true)
    cond = ta.rising(close, 3)
    lookback = int(math.max(1, nz(ta.barssince(cond)) + 1))
    lowestSinceCondition = ta.lowest(lookback)
    plot(lowestSinceCondition)
    // Show when condition occurs.
    plotchar(cond, "cond", "•", location.top, size=size.tiny)
    // Display varying lookback period in Data Window.
    plotchar(lookback, "lookback", "", location.top, size=size.tiny)



Why do some functions and built-ins evaluate incorrectly in if or ternary (?) blocks?
-------------------------------------------------------------------------------------

Many functions/built-ins need to execute on every bar to return correct results. 
Think of a rolling average like `ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__ or a function like 
`ta.highest() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}highest>`__. If they miss values along the way, it’s easy to see how they won’t calculate properly.

To avoid problems, you need to be on the lookout for these conditions:

**Condition A**
A conditional expression that can only be evaluated with incoming, new bar information (i.e., using series variables like 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__). This excludes expressions using values of literal, const, input or simple forms 
because they do not change during the script’s execution, and so when you use them, the same block in the if statement is guaranteed to execute on every bar. 
`Read this <https://www.tradingview.com/pine-script-docs/en/v5/language/Type_system.html>`__ if you are not familiar with Pine Script™ forms and types.

**Condition B**
When condition A is met, and the if block(s) contain(s) functions or built-ins NOT in the list of exceptions, i.e., 
which require evaluation on every bar to return a correct result, then condition B is also met.

This is an example where an apparently inoffensive built-in like `ta.vwap <https://www.tradingview.com/pine-script-reference/v5/#var_ta{dot}vwap>`__ is used in a ternary. 
`ta.vwap <https://www.tradingview.com/pine-script-reference/v5/#var_ta{dot}vwap>`__ is not in the 
`list of exceptions <https://www.tradingview.com/pine-script-docs/en/v5/language/Execution_model.html#exceptions>`__, and so when condition A is realized, 
it will require evaluation prior to entry in the if block. You can flip between 3 modes: #1 where condition A is fulfilled and #2 and #3 where it is not. 
You will see how the unshielded value (``upVwap2`` in the thick line) will produce incorrect results when mode 1 is used.

.. image:: images/Faq-Functions-01.png

::

    //@version=5
    indicator("When to pre-evaluate functions/built-ins", "", true)
    CN1 = "1. Condition A is true because evaluation varies bar to bar"
    CN2 = "2. Condition A is false because `timeframe.multiplier` does not vary during the script\'s execution"
    CN3 = "3. Condition A is false because an input does not vary during the script\'s execution"
    useCond = input.string(CN1, "Test on conditional expression:", options=[CN1, CN2, CN3])
    p = 10

    // ————— Conditional expression 1: CAUTION!
    //       Can lead to execution of either `if` block because:
    //          uses *series* variables, so result changes bar to bar.
    //       (Condition A is fulfilled).
    cond1 = close > open
    // ————— Conditional expression 2: NO WORRIES
    //       Guarantees execution of same `if` block on every bar because:
    //          uses *simple* variable, so result does NOT change bar to bar
    //          because it is known before the script executes and does not change.
    //       (Condition A is NOT fulfilled).
    cond2 = timeframe.multiplier > 0
    // ————— Conditional expression 3: NO WORRIES
    //       Guarantees execution of same `if` block on every bar because:
    //          uses *input* variable, so result does NOT change bar to bar
    //          because it is known before the script execcutes and does not change.
    //       (Condition A is NOT fulfilled).
    cond3 = input(true)

    cond = useCond == CN1 ? cond1 : useCond == CN2 ? cond2 : cond3

    // Built-in used in "if" blocks that is not part of the exception list,
    // and so will require forced evaluation on every bar prior to entry in "if" statement.
    // (Condition B will be true when Condition A is also true)
    v = ta.vwap
    // Shielded against condition B because vwap is pre-evaluted.
    upVwap = math.sum(cond ? v : 0, p) / math.sum(cond ? 1 : 0, p)
    // NOT shielded against condition B because vwap is NOT pre-evaluted.
    upVwap2 = math.sum(cond ? ta.vwap : 0, p) / math.sum(cond ? 1 : 0, p)

    plot(upVwap, "upVwap", color.new(color.fuchsia, 0))
    plot(upVwap2, "upVwap2", color.new(color.fuchsia, 80), 8)
    bgcolor(upVwap != upVwap2 ? color.silver : na, transp=90)



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