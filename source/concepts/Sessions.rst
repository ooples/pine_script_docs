.. _PageSessions:

..    include:: <isonum.txt>

Sessions
========



Introduction
------------

Sessions information is usable in two different ways in Pine:

1. **Session strings** containing from-to start times and day information can be used in functions
   such as `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ and
   `time_close() <https://www.tradingview.com/pine-script-reference/v5/#fun_time_close>`__
   to detect when bars are in a particular time period, on specific days.
2. When fetching data with `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
   you can choose to return data from *regular* sessions only, or from *extended* sessions also.
   In this case, the definition of **regular and extended sessions** is that of the exchange.
   It is part of the instrument's properties — not user-defined as in point #1.
   This notion of *regular* and *extended* sessions is the same one used in the chart's interface,
   in the "Chart Settings/Symbol/Session" field, for example. 
   Note that not all user accounts on TradingView have access to extended session information.

Here, we cover both methods of using session information in Pine.



Session strings
---------------



Session string specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Session strings must have a specific format.
Their syntax is:

.. code-block:: text

    <time_period>:<days>

where:

- <time_period> use times of "hhmm" format, with "hh" in 24-hour format, so ``1700`` for 5PM.
  The time periods are in the "hhmm-hhmm" format, and multiple time periods can be separated by a comma.
- <days> is a set of digits from 1 to 7 that specifies on which days the session is valid.
  1 is Sunday, 7 is Saturday. 
  
.. note:: **The default days is**: ``1234567``, which is different in Pine v5 than in earlier version,
   which use the ``23456`` default days. For v5 code to reproduce the behavior from previous versions,
   it should explicitly mention the days required, as in ``0930-1700:23456``.


These are examples of trade session specifications:

0000-0000
   A monday to friday 24-hour session beginning at midnight.

0900-1600,1700-2000
   A session that begins at 9:00, breaks from 16:00 to 17:00 and continues until 20:00.
   Applies to every day of the week.

2000-1630:1234567
   An overnight session that begins at 20:00 and ends at
   16:30 the next day.

0930-1700:146
   A session that begins at 9:30 and
   ends at 17:00 on Sundays (1), Wednesdays (4) and Fridays (6) (other days
   of the week are days off).

24x7
   A complete 24-hour session beginning at 00:00 every day.

0000-0000:1234567
   Same as "24x7".

0000-0000:23456
   Same as previous example, but only Monday to Friday.

1700-1700:23456
   An *overnight session*. Monday session starts
   Sunday at 17:00 and ends Monday at 17:00. Applies to Monday through Friday.

1000-1001:26
   A weird session that lasts only one minute on
   Mondays (2) and one minute on Fridays (6).



Using session strings 
^^^^^^^^^^^^^^^^^^^^^

Session specification used for the `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ function's
second argument does not need to correspond to the symbol's real trade
session. Hypothetical session specifications can be used to highlight
other bars of a data series.

Pine provides an overloaded version of the `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ function which does not require
custom session specification. This version of the function uses the
regular session of a symbol. For example, it is possible to
highlight the beginning of each half-hour bar on a minute chart in
the following way::

    //@version=5
    indicator("new 30 min bar")
    isNewBar(tf) =>
        nz(ta.change(time(tf)) > 0, true)
    plot(isNewBar("30") ? 1 : 0)

.. image:: images/Chart_time_2.png


Here, we use `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__
with a ``session`` argument to display the market's opening
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ and 
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ on an intraday chart::

    //@version=5
    indicator("Opening high/low", overlay = true)
    
    highTFInput = input.timeframe("D")
    sessSpecInput = input.session("0930-1600")
    
    isNewBar(res, sess) =>
        t = time(res, sess)
        na(t[1]) and not na(t) or t[1] < t
    
    var float hi = na
    var float lo = na
    if isNewBar(highTFInput, sessSpecInput)
        hi := high
        lo := low
    
    plot(lo, "lo", color.red, 3, plot.style_circles)
    plot(hi, "hi", color.lime, 3, plot.style_circles)

.. image:: images/Chart_time_3.png



Regular and extended sessions
-----------------------------

On TradingView you can access extended hours sessions by
*right-clicking* on a chart and choosing *Settings* |rarr|
*Symbol* |rarr| *Extended Hours (Intraday only)*.
There are two types of sessions: *regular* (excluding pre- and post-market
data) and *extended* (including pre- and post-market data).
Pine scripts may request additional session data using the
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function.

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
function can be called with a symbol name in the ``"EXCHANGE_PREFIX:TICKER"`` format (e.g., "NASDAQ:AAPL") as its first argument.
Used this way, the function will return data for the regular session. For example::

    //@version=5
    indicator("Example 1: Regular Session Data")
    cc = request.security("NASDAQ:AAPL", timeframe.period, close, barmerge.gaps_on)
    plot(cc, style = plot.style_linebr)

.. image:: images/Pine-_Regular_Session_Data.png

If you want the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call to return extended session data, you
must first use the `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__ function
to build `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call's first argument::

    //@version=5
    indicator("Example 2: Extended Session Data")
    t = ticker.new("NASDAQ", "AAPL", session.extended)
    cc = request.security(t, timeframe.period, close, barmerge.gaps_on)
    plot(cc, style=plot.style_linebr)

.. image:: images/Pine_Extended_Session_Data.png


Notice that the previous chart's gaps in the script's plot are now filled. Also keep in mind
that the background coloring on the chart is not produced by our example scripts;
it is due to the chart's settings showing extended hours.

The first argument of the `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__ 
function is an exchange prefix ("NASDAQ") and the
second argument is a ticker ("AAPL"). The third argument specifies the type
of the session (``session.extended`` or ``session.regular``). So *Example 1*
could be rewritten as::

    //@version=5
    indicator("Example 3: Regular Session Data using `ticker.new()`")
    t = ticker.new("NASDAQ", "AAPL", session.regular)
    cc = request.security("NASDAQ:AAPL", timeframe.period, close, barmerge.gaps_on)
    plot(cc, style=plot.style_linebr)

If you want to request the same session specification used for the chart's main
symbol, omit the third argument; it is optional. Or, if you want your code to
explicitly declare your intention, use the ``syminfo.session``
built-in variable as the third argument to the `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__ 
function, as it holds the session type of the chart's main symbol::

    //@version=5
    indicator("Example 4: Same as Main Symbol Session Type Data")
    t = ticker.new("NASDAQ", "AAPL", syminfo.session)
    cc = request.security(t, timeframe.period, close, barmerge.gaps_on)
    plot(cc, style=plot.style_linebr)
