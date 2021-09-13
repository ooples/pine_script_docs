.. _PageFirstIndicator:

First indicator
===============

Let's look at the implementation of a
`MACD <https://www.tradingview.com/support/solutions/43000502344-macd-moving-average-convergence-divergence/>`__ indicator in Pine:

.. code-block:: pine
    :linenos:

    //@version=5
    indicator("MACD")
    fast = 12
    slow = 26
    fastMA = ta.ema(close, fast)
    slowMA = ta.ema(close, slow)
    macd = fastMA - slowMA
    signal = ta.sma(macd, 9)
    plot(macd, color = color.blue)
    plot(signal, color = color.orange)


Line 1: ``//@version=5``
    This is a comment containing a compiler directive that tells the compiler the script will use version 5 of Pine.
Line 2: ``indicator("MACD")``
    Defines the name of the script that will appear on the chart as "MACD".
Line 3: ``fast = 12``
    Defines a ``fast`` integer variable which will be the length of the fast EMA.
Line 4: ``slow = 26``
    Defines a ``slow`` integer variable which will be the length of the slow EMA.
Line 5: ``fastMA = ta.ema(close, fast)``
    Defines the variable ``fastMA``, containing the result of the
    EMA calculation (Exponential Moving Average) with a length equal
    to ``fast`` (12), on the ``close`` series, i.e., the closing price of bars.
Line 6: ``slowMA = ta.ema(close, slow)``
    Defines the variable ``slowMA``, containing the result of the
    EMA calculation with a length equal to ``slow`` (26), from ``close``.
Line 7: ``macd = fastMA - slowMA``
    Defines the variable ``macd`` as the difference between the two EMAs.
Line 8: ``signal = ta.sma(macd, 9)``
    Defines the variable ``signal`` as a smoothed value of
    ``macd`` using the SMA algorithm (Simple Moving Average) with
    a length of 9.
Line 9: ``plot(macd, color = color.blue)``
    Calls the ``plot`` function to output the variable ``macd`` using a blue line.
Line 10: ``plot(signal, color = color.orange)``
    Calls the ``plot`` function to output the variable ``signal`` using an orange line.

After adding the "MACD" script to the chart you will see the following:

.. image:: images/Macd_pine.png

Pine contains a variety of built-in functions for the most popular
algorithms (
`ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__ for an `SMA <https://www.tradingview.com/support/solutions/43000502589-moving-average/>`__,
`ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__ for an `EMA <https://www.tradingview.com/support/solutions/43000592270-exponential-moving-average/>`__,
`ta.wma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}wma>`__ for an `WMA <https://www.tradingview.com/support/solutions/43000594680-weighted-moving-average/>`__, etc.).
You can also define your custom functions. You will find a
description of all available built-in functions
`here <https://www.tradingview.com/pine-script-reference/v5/>`__.



