Built-in Functions
==================

.. contents:: :local:
    :depth: 3


Introduction
------------

Pine comes with hundreds of built-in functions. Those in the same family share the same namespace, which is a prefix to the function's name. 
The `ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__ function, for example, is in the ``ta`` namespace, 
which stands for "technical analysis".

Many functions are used for the result(s) they return. These are a few examples:

- Math-related functions in the ``math`` namespace: 
  `math.abs() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}abs>`__,
  `math.log() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}log>`__,
  `math.max() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}max>`__,
  `math.random() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}random>`__,
  `math.round_to_mintick() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}round_to_mintick>`__, etc.
- Technical indicators in the ``ta`` namespace:
  `ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__,
  `ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__,
  `ta.macd() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}macd>`__,
  `ta.rsi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}rsi>`__,
  `ta.supertrend() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}supertrend>`__, etc.
- Support functions often used to calculate technical indicators in the ``ta`` namespace:
  `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__,
  `ta.crossover() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}crossover>`__,
  `ta.highest() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}highest>`__, etc.
- Functions to request data from other symbols or timeframes in the ``request`` namespace:
  `request.dividends() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}dividends>`__,
  `request.earnings() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}earnings>`__,
  `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__,
  `request.quandl() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}quandl>`__,
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__,
  `request.splits() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}splits>`__.
- Functions to manipulate strings in the ``str`` namespace:
  `str.format <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}format>`__,
  `str.length <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}length>`__,
  `str.tonumber <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}tonumber>`__,
  `str.tostring <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}tostring>`__, etc.
- Functions used to define the input values that script users can modify in the script's "Settings/Inputs" tab, in the ``input`` namespace:
  `input() <https://www.tradingview.com/pine-script-reference/v5/#fun_input>`__,
  `input.color() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}color>`__,
  `input.int() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}int>`__,
  `input.session() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}session>`__,
  `input.symbol() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}symbol>`__, etc.
- Functions used to manipulate colors in the ``color`` namespace:
  `color.from_gradient() <https://www.tradingview.com/pine-script-reference/v5/#fun_color{dot}from_gradient>`__,
  `color.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_color{dot}rgb>`__,
  `color.rgb() <https://www.tradingview.com/pine-script-reference/v5/#fun_color{dot}new>`__, etc.

Some functions do not return a result but are used for their side effect, which means they do something, even if they don't return a result:

- Functions used as a declaration statement defining one of three types of Pine scripts, and its properties. Each script must begin with a call to one of these functions:
  `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__,
  `strategy() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__ or 
  `library() <https://www.tradingview.com/pine-script-reference/v5/#fun_library>`__.
- Plotting or coloring functions:
  `bgcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_bgcolor>`__,
  `plotbar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotbar>`__,
  `plotcandle() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotcandle>`__,
  `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__,
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__,
  `fill() <https://www.tradingview.com/pine-script-reference/v5/#fun_fill>`__,
- Strategy functions placing orders in the ``strategy`` namespace:
  `strategy.cancel() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy{dot}cancel>`__,
  `strategy.close() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy{dot}close>`__,
  `strategy.entry() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy{dot}entry>`__,
  `strategy.exit() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy{dot}exit>`__,
  `strategy.order() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy{dot}order>`__, etc.
- Functions to generate alert events:
  `alert() <https://www.tradingview.com/pine-script-reference/v5/#fun_alert>`__ and
  `alertcondition() <https://www.tradingview.com/pine-script-reference/v5/#fun_alertcondition>`__.

Other functions return a result which is not always used. Sometimes we call them only for their side effect:
`hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__,
`plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__,
`array.pop() <https://www.tradingview.com/pine-script-reference/v5/#fun_array{dot}pop>`__,
`label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__, etc.


Using built-in functions
------------------------

All Pine built-ins are defined in the Pine Reference Manual. You can click on any of the function names listed here to go to its entry in the Reference Manual, 
which documents the function's signature, i.e., the list of *parameters* it accepts and the form-type of the value(s) it returns 
(a function can return more than one result). The Reference Manual entry will also list, for each parameter:

- Its name.
- The form-type of the value it requires (we use *argument* to name the values passed to a function when calling it).
- If the parameter is required or not.

All built-in functions have one or more parameters defined in their signature. Not all parameters are required for every function.

Let's look at the `ta.vwma <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}vwma>`__, 
which returns the volume-weighted moving average of a source value. Its signature (or definition) is::

    ta.vwma(source, length) → series float

This tells us it expects two arguments when it is called, one for the ``source`` parameter, and one for the ``length`` parameter (both are required in this case).
This is a call to the function in a line of code that assigns the result to a variable called ``myVwma``::

    myVwma = ta.vwma(close, 20)

Note that:

- We use the built-in variable `close <https://www.tradingview.com/pine-script-reference/v5/#>`__ as the argument for the ``source`` parameter.
- We use 20 as the argument for the ``length`` parameter.

We can also use the parameter names when calling the function. Parameter names are called *keyword arguments* when used in a function call::

    myVwma = ta.vwma(source = close, length = 20)

You can change the position of arguments when using keyword arguments, but only if you use them for all your arguments. 
When calling functions with many parameters such as `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__
you can also forego keyword arguments for the first arguments as long as you don't skip any, but if you skip some, 
you must then use keyword arguments so the Pine compiler can figure out which parameter they correspond to, e.g.::

    indicator("Example", "Ex", true, max_bars_back = 100)

Mixing things up this way is not allowed::

    indicator(precision = 3, "Example") // Compilation error!
    
When calling Pine built-ins, it is critical to ensure that the arguments you use are of the form and type required, which will vary for each parameter. 
To learn how to do this, one needs to understand Pine's :ref:`<PageTypeSytem>.



Execution of Pine functions and historical context inside function blocks
-------------------------------------------------------------------------

The history of series variables used inside Pine functions is created through each successive call to the function. If the function is not called on each bar the script runs on, this will result in disparities between the historic values of series inside vs outside the function's local block. Hence, series referenced inside and outside the function using the same index value will not refer to the same point in history if the function is not called on each bar.

Let's look at this example script where the ``f`` and ``f2`` functions are called every second bar::

   //@version=5
   indicator("My Script", overlay = true)

   // Returns the value of "a" the last time the function was called 2 bars ago.
   f(a) => a[1]
   // Returns the value of last bar's "close", as expected.
   f2() => close[1]

   oneBarInTwo = bar_index % 2 == 0
   plot(oneBarInTwo ? f(close) : na, color = color.maroon, linewidth = 6, style = plot.style_cross)
   plot(oneBarInTwo ? f2() : na, color = color.lime, linewidth = 6, style = plot.style_circles)
   plot(close[2], color = color.maroon)
   plot(close[1], color = color.lime)

.. image:: images/Function_historical_context_1.png

As can be seen with the resulting plots, ``a[1]`` returns the previous value of a in the function's context, so the last time ``f`` was called two bars ago — not the close of the previous bar, as ``close[1]`` does in ``f2``. This results in ``a[1]`` in the function block referring to a different past value than ``close[1]`` even though they use the same index of 1.

Why this behavior?
^^^^^^^^^^^^^^^^^^

This behavior is required because forcing execution of functions on each bar would lead to unexpected results, as would be the case for a ``label.new`` function call inside an if branch, which must not execute unless the if condition requires it.

On the other hand, this behavior leads to unexpected results with certain built-in functions which require being executed each bar to correctly calculate their results. Such functions will not return expected results if they are placed in contexts where they are not executed every bar, such as if branches.

The solution in these cases is to take those function calls outside their context so they can be executed on every bar.

In this script, ``ta.barssince`` is not called on every bar because it is inside a ternary operator's conditional branch::

   //@version=5
   indicator("Barssince", overlay = false)
   res = close > close[1] ? ta.barssince(close < close[1]) : -1
   plot(res, style = plot.style_histogram, color=res >= 0 ? color.red : color.blue)

This leads to incorrect results because ``ta.barssince`` is not executed on every bar:

.. image:: images/Function_historical_context_2.png

The solution is to take the barssince call outside the conditional branch to force its execution on every bar::

   //@version=5
   indicator("Barssince", overlay = false)
   b = ta.barssince(close < close[1])
   res = close > close[1] ? b : -1
   plot(res, style = plot.style_histogram, color = res >= 0 ? color.red : color.blue)

Using this technique we get the expected output:

.. image:: images/Function_historical_context_3.png

Exceptions
^^^^^^^^^^

Not all built-in functions need to be executed every bar. These are the functions which do not require it, and so do not need special treatment::

   dayofmonth, dayofweek, hour, linebreak, math.abs, math.acos, math.asin, math.atan, math.ceil,
   math.cos, math.exp, math.floor, math.log, math.log10, math.max, math.min, math.pow, math.round,
   math.sign, math.sin, math.sqrt, math.tan, minute, month, na, nz, second, str.tostring,
   ticker.heikinashi, ticker.kagi, ticker.new, ticker.renko, time, timestamp, weekofyear, year

.. note:: Functions called from within a ``for`` loop use the same context in each of the loop's iterations. In the example below, each ``ta.lowest`` call on the same bar uses the value that was passed to it (i.e., ``bar_index``), so function calls used in loops do not require special treatment.

::

   //@version=5
   indicator("My Script")
   va = 0.0
   for i = 1 to 2 by 1
       if (i + bar_index) % 2 == 0
           va := ta.lowest(bar_index, 10)  // same context on each call
   plot(va)
