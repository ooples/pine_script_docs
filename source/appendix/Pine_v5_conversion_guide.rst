

Pine version 5 migration guide
==============================

This document helps to migrate Pine Script code from ``@version=4`` to
``@version=5``.

Converter
---------

Pine Editor now comes with an utility to automatically convert v4 indicators and strategies to v5. To access it, open a script with ``//@version=4`` in it and select the ``Convert to v5`` option in the ``More`` dropdown menu:

PICTURE

Not all scripts can be automatically converted from v4 to v5. If you want to convert the script manually or if your indicator returns a compilation error after conversion, consult the guide below for more information.

Renamed functions and variables
-------------------------------
Many built-in functions and variables were renamed in v5 for clarity and consistency. Most changes simply add a namespace is the addition of the namespace: for example, the ``sma()`` function is now called ``ta.sma()`` in v5. As such, the new name can be easily found by entering the old name and checking the suggestion list:

PICTURE

The only two functions that were fully renamed are:

 * ``study()`` -> ``indicator()``
 * ``tickerid()`` -> ``ticker.new()``

The full list of renamed variables, should you need it, can be found here[link to the end of the page so that we don’t post a giant table in the middle of the text].

Renamed function arguments
--------------------------
Some 'historical' argument names for built-in functions have been changed because they were not descriptive enough. This has no bearing on most scripts, but if you used these arguments in their 'keyword' form, you’ll have to use a different keyword now. For example::

  // Valid in v4, not valid in v5:
  strv4 = tostring(x = close, y = "#.#")
  // Valid in v5:
  strv5 = str.tostring(value = close, format = "#.#") 

The full list of renamed function arguments can be found here[link to the end of the page so that we don’t post a giant table in the middle of the text].

Removed an ``rsi()`` overload
-----------------------------
Previously, the built-in ``rsi()`` function had two different overloads:
* ``rsi(series float, simple int)`` -> regular RSI calculation
* ``rsi(series float, series float)`` -> an overload used in the MFI indicator, did a calculation equivalent to ``100.0 - (100.0 / (1.0 + arg1 / arg2))``. 

Because of this, a single built-in function did two tasks with different expected results, and it was hard to distinguish which overload would be used at a glance. We’ve found a number of indicators misusing this and getting an incorrect calculation as a result. As such, the second overload has been removed to get rid of ambiguous behavior of the function. 

Now, the ``rsi()`` function can only take a simple integer as its second argument.
If you passed a float value to the second argument, you can replace the ``rsi()`` call with the following formula ``100.0 - (100.0 / (1.0 + arg1 / arg2))``. It is equivalent to the calculation that ``rsi(series float, series float)`` did.

If you passed a series integer value as the second argument, it only used to work in v4 because series integer was automatically cast to series float and used the second overload. Note that it did not give the result you would actually expect from the ``rsi(source, length)`` function. Also note that the original ``rsi()`` calculation takes previous bars into account, so a series length is not applicable there, which is why there is no overload for ``rsi(series float, series integer)`` and a varying length can no longer be passed to ``rsi()``.

If you passed an integer value of a non-series, nothing should change for you.

Reserved keywords
-----------------
A number of words have been reserved and are no longer valid as variable and function names: ``text``, ``ellipse``, ``polygon``, ``return``, ``class``, ``struct``, ``throw``, ``try``, ``catch``, ``is``, ``in``, ``range``, ``while``, ``do``. If your v4 indicator uses any of these words as a variable or a function name, rename them for the script to work in v5.

Removed iff() and offset()
--------------------------
The functions ``iff()`` and ``offset()`` have been removed. The code that uses the ``iff()`` function can be rewritten using the ternary operator::

    // iff(<condition>, <return if true>, <return if false>)
    // Valid in v4, not valid in v5
    barColorIff = iff(close >= open, color.green, color.red)
    // <condition> ? <return if true> : <return if false>
    // Valid in v4 and v5
    barColorTernary = close >= open ? color.green : color.red

The ``offset()`` function can in turn be replaced with the ``[]`` operator::

  // Valid in v4, not valid in v5
  prevClosev4 = offset(close, 1)
  // Valid in v4 and v5
  prevClosev5 = close[1]

Split ``input()`` into several functions
------------------------------------
The old ``input()`` function had too many different overloads, each one with its list of different arguments that can be possibly passed to it. For clarity, most of these overloads have now been split into separate functions. Each new function shares its name with an ``input.*`` constant from v4. The constants themselves have been removed.

For example, to convert an indicator with an input from v4 to v5, where you would use ``input(type = input.symbol)`` before, you should now use the ``input.symbol()`` function instead::

  // Valid in v4, not valid in v5
  aaplTicker = input("AAPL", type = input.symbol)
  // Valid in v5
  aaplTicker = input.symbol("AAPL")

The basic version of the function (that detects the type automatically based on the default value) still exists, but without most of its parameters::

  // Valid in v4 and v5
  // Even though "AAPL" is a valid ticker, the input is considered just a string because the type is not specified
  aaplString = input("AAPL", title = "String")

Some functions now require named constants instead of raw values
----------------------------------------------------------------
In v4, built-in constants were simply variables with pre-defined values of a specific type. For example, the ``barmerge.lookahead_on`` is simply a constant that passes true and has to specific ties to the ``lookahead`` argument of the ``security()`` function. We found this and many other similar cases to be a common source of confusion for users who passed incorrect constants to functions and got unexpected results.

In v5, function parameters that have constants dedicated to them can only use constants instead of raw values. Conversely, constants can no longer be used anywhere but in the parameters they are tied to. For example::

  // Not valid in v5: lookahead has a constant tied to it
  request.security(syminfo.tickerid, “1D”, close, lookahead = true)
  // Valid: using proper constant
  request.security(syminfo.tickerid, “1D”, close, lookahead = barmerge.lookahead_on)

  // Will compile in v4 because plot.style_columns is equal to 5
  // Won’t compile in v5
  a = 2 * plot.style_columns
  plot(a)

To convert your script from v4 to v5, make sure to replace all variables with constants where necessary.

The ``Transp`` argument has been removed
----------------------------------------
The ``transp=`` argument that was present in many plot functions in v4 interfered with the rgb functionality and has been removed. The ``color.new()`` function can be used to specify the transparency of any color instead.
TODO: write about functions with removed default `transp` values, e.g. fill()

Default session for time() and time_close() has been changed
------------------------------------------------------------
The default value for the ``session`` argument of the ``time()`` and ``time_close()`` functions has changed. In v4, when you pass a specific session time for any of the two functions mentioned above without specifying the days, the session automatically fills the days as ``23456``, i.e. Monday to Friday. In v5, we have changed this to auto-complete the session as ``1234567`` instead::

  // This line of code will behave differently in v4 and v5 on symbols that are traded on the weekends:
  t0 = time("1D", "1000-1200")
  // This line is equivalent to t0 in v4:
  t1 = time("1D", "1000-1200:23456")
  // This line is equivalent to t0 in v5:
  t2 = time("1D", "1000-1200:1234567")

To make sure that your script’s behavior in v5 is consistent with v4, add ``:12345`` to all ``time()`` and ``time_close()`` calls that specify the session without the days. For an example of how to convert ``time()`` from v4 to v5, see the code below::

  //@version=4
  study("Lunch Break", overlay=true)
  isLunch = time(timeframe.period, "1300-1400")
  bgcolor(isLunch ? color.green : na)

  //@version=5
  indicator('Lunch Break', overlay=true)
  isLunch = time(timeframe.period, '1300-1400:23456')
  bgcolor(isLunch ? color.new(color.green, 90) : na)

strategy.exit() now must do something
-------------------------------------
Gone are the days when the ``strategy.exit()`` function was allowed to loiter. Now it must actually have an effect on the strategy itself, and to do so, it should have at least one of the following parameters: ``profit``, ``limit``, ``loss``, ``stop``, or one of the following pairs: ``trail_offset`` and ``trail_price`` / ``trail_points``. 
In v4, it used to compile with a warning (although the function itself did not do anything in the code); now it is no longer valid code. If you are converting a script to v5 and get this error, feel free to comment it out or remove it altogether: it didn’t do anything in your code anyway.

Name changes

.. csv-table:: Table Title
   :file: Untitled spreadsheet - Sheet1.csv
   :widths: 30, 70
   :header-rows: 1
