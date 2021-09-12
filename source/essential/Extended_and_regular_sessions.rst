..    include:: <isonum.txt>

Extended and regular sessions
=============================

On TradingView you can access extended hours sessions by
*right-clicking* on a chart and choosing *Settings* |rarr|
*Symbol* |rarr| *Extended Hours (Intraday only)*.
There are two types of sessions: *regular* (excluding pre- and post-market
data) and *extended* (including pre- and post-market data).
Pine scripts may request additional session data using the
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function.

The ``request.security`` function can be called with a symbol name
(*"EXCHANGE_PREFIX:TICKER"*, e.g., "BATS:AAPL") as its first argument.
Used this way, the ``request.security`` function will return data for the regular session. For example::

    //@version=5
    indicator("Example 1: Regular Session Data")
    cc = request.security("BATS:AAPL", timeframe.period, close, barmerge.gaps_on)
    plot(cc, style = plot.style_linebr)

.. image:: images/Pine-_Regular_Session_Data.png

If you want the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call to return extended session data, you
must first use the `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__ function
to build `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call's first argument::

    //@version=5
    indicator("Example 2: Extended Session Data")
    t = ticker.new("BATS", "AAPL", session.extended)
    cc = request.security(t, timeframe.period, close, barmerge.gaps_on)
    plot(cc, style=plot.style_linebr)

.. image:: images/Pine_Extended_Session_Data.png


Notice that the previous chart's gaps in the script's plot are now filled. Also keep in mind
that the background coloring on the chart is not produced by our example scripts;
it is due to the chart's settings showing extended hours.

The first argument of the `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__ 
function is an exchange prefix ("BATS") and the
second argument is a ticker ("AAPL"). The third argument specifies the type
of the session (``session.extended`` or ``session.regular``). So *Example 1*
could be rewritten as::

    //@version=5
    indicator("Example 3: Regular Session Data using `ticker.new()`")
    t = ticker.new("BATS", "AAPL", session.regular)
    cc = request.security("BATS:AAPL", timeframe.period, close, barmerge.gaps_on)
    plot(cc, style=plot.style_linebr)

If you want to request the same session specification used for the chart's main
symbol, omit the third argument; it is optional. Or, if you want your code to
explicitly declare your intention, use the ``syminfo.session``
built-in variable as the third argument to the `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__ 
function, as it holds the session type of the chart's main symbol::

    //@version=5
    indicator("Example 4: Same as Main Symbol Session Type Data")
    t = ticker.new("BATS", "AAPL", syminfo.session)
    cc = request.security(t, timeframe.period, close, barmerge.gaps_on)
    plot(cc, style=plot.style_linebr)
