.. _PageNonStandardChartsData:

Non-standard charts data
========================

.. contents:: :local:
    :depth: 2



Introduction
------------

These functions allow scripts to fetch information from non-standard
bars or chart types, regardless of the type of chart the script is running on.
They are:
`ticker.heikinashi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}heikinashi>`_,
`ticker.renko() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}renko>`_,
`ticker.linebreak() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}linebreak>`_,
`ticker.kagi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}kagi>`_ and 
`ticker.pointfigure() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}pointfigure>`_.
All of them work in the same manner; they create a special ticker identifier to be used as
the first argument in a `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function call.


\`ticker.heikinashi()\`
-----------------------

*Heikin-Ashi* means *average bar* in Japanese. 
The open/high/low/close values of Heikin-Ashi candlesticks are synthetic; they are not actual market prices.
They are calculated by averaging combinations of real OHLC values from the current and previous bar. 
The calculations used make Heikin-Ashi bars less noisy than normal candlesticks.
They can be useful to make visual assessments, but are unsuited to backtesting or automated trading, 
as orders execute on market prices — not Heikin-Ashi prices.

The `ticker.heikinashi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}heikinashi>`__
function creates a special ticker identifier for
requesting Heikin-Ashi data with the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function.

This script requests the close value of Heikin-Ashi bars and plots them on top of the normal candlesticks::

    //@version=5
    indicator("HA Close", "", true)
    haTicker = ticker.heikinashi(syminfo.tickerid)
    haClose = request.security(haTicker, timeframe.period, close)
    plot(haClose, "HA Close", color.black, 3)

.. image:: images/NonStandardCharts-TickerHeikinAshi-01.png

Note that:

- The close values for Heikin-Ashi bars plotted as the black line are very different from those of real candles using market prices. They act more like a moving average.
- The black line appears over the chart bars because we have selected "Visual Order/Bring to Front" from the script's "More" menu.

If you wanted to omit values for extended hours in the last example, 
an intermediary ticker without extended session information would need to be created first::

    //@version=5
    indicator("HA Close", "", true)
    regularSessionTicker = ticker.new(syminfo.prefix, syminfo.ticker, session.regular)
    haTicker = ticker.heikinashi(regularSessionTicker)
    haClose = request.security(haTicker, timeframe.period, close, gaps = barmerge.gaps_on)
    plot(haClose, "HA Close", color.black, 3, plot.style_linebr)

.. image:: images/NonStandardCharts-TickerHeikinAshi-02.png

Note that:

- We use the `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__ function first, 
  to create a ticker without extended session information.
- We use that ticker instead of `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__ in our 
  `ticker.heikinashi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}heikinashi>`__ call.
- In our `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call,
  we set the ``gaps`` parameter's value to ``barmerge.gaps_on``.
  This instructs the function not to use previous values to fill slots where data is absent.
  This makes it possible for it to return `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__
  values outside of regular sessions.
- To be able to see this on the chart, we also need to use a special ``plot.style_linebr`` style,
  which breaks the plots on `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ values.

This script plots Heikin-Ashi candles under the chart::

    //@version=5
    indicator("Heikin-Ashi candles")
    CANDLE_GREEN = #26A69A
    CANDLE_RED   = #EF5350
    
    haTicker = ticker.heikinashi(syminfo.tickerid)
    haO = request.security(haTicker, timeframe.period, open)
    haH = request.security(haTicker, timeframe.period, high)
    haL = request.security(haTicker, timeframe.period, low)
    haC = request.security(haTicker, timeframe.period, close)
    candleColor = haC >= haO ? CANDLE_GREEN : CANDLE_RED
    plotcandle(haO, haH, haL, haC, color = candleColor)

.. image:: images/NonStandardCharts-TickerHeikinAshi-03.png

You will find more information on `plotcandle() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotcandle>`__
and the related `plotbar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotbar>`__ functions in
the :ref:`Bar plotting <PageBarPlotting>` page.



\`ticker.renko()\`
------------------

*Renko* bars only plot price movements, without taking time or
volume into consideration. They are constructed from ticks and look like
bricks stacked in adjacent columns [#ticks]_. A new brick is drawn after the price
passes the top or bottom by a predetermined amount.

::

    //@version=5
    indicator("Example 7", overlay = true)
    renko_t = ticker.renko(syminfo.tickerid, "ATR", 10)
    renko_low = request.security(renko_t, timeframe.period, low)
    plot(renko_low)

.. image:: images/Pine_Renko.png

Please note that you cannot plot Renko bricks from Pine script exactly
as they look. You can only get a series of numbers similar to
OHLC values for Renko bars and use them in your algorithms.

For detailed information, see `ticker.renko() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}renko>`__.


\`ticker.linebreak()\`
----------------------

The *Line Break* chart type displays a series of vertical boxes that are based on
price changes [#ticks]_.

::

    //@version=5
    indicator("Example 8", overlay = true)
    lb_t = ticker.linebreak(syminfo.tickerid, 3)
    lb_close = request.security(lb_t, timeframe.period, close)
    plot(lb_close)

.. image:: images/Pine_Linebreak.png

Please note that you cannot plot Line Break boxes from Pine script
exactly as they look. You can only get a series of numbers similar to
OHLC values for Line Break charts and use them in your algorithms.

For detailed information, see `ticker.linebreak() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}linebreak>`__.


\`ticker.kagi()\`
-----------------

*Kagi* charts are made of a continuous line that changes directions.
The direction changes when the price changes [#ticks]_
beyond a predetermined amount.

::

    //@version=5
    indicator("Example 9", overlay = true)
    kagi_t = ticker.kagi(syminfo.tickerid, 1)
    kagi_close = request.security(kagi_t, timeframe.period, close)
    plot(kagi_close)

.. image:: images/Pine_Kagi.png

Please note that you cannot plot Kagi lines from Pine script exactly as
they look. You can only get a series of numbers similar to OHLC
values for Kagi charts and use them in your algorithms.

For detailed information, see `ticker.kagi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}kagi>`__.


\`ticker.pointfigure()\`
------------------------

*Point and Figure* (PnF) charts only plot price movements [#ticks]_, without
taking time into consideration. A column of X's is plotted as the price
rises, and O's are plotted when price drops.

Please note that you cannot plot PnF X's and O's from Pine script
exactly as they look. You can only get a series of numbers that are
similar to OHLC values for PnF charts and use them in your algorithms.
Every column of X's or O's is represented with four numbers. You may
think of them as synthetic OHLC PnF values.

::

    //@version=5
    indicator("Example 10", overlay = true)
    pnf_t = ticker.pointfigure(syminfo.tickerid, "hl", "ATR", 14, 3)
    pnf_open = request.security(pnf_t, timeframe.period, open, barmerge.gaps_on)
    pnf_close = request.security(pnf_t, timeframe.period, close, barmerge.gaps_on)
    plot(pnf_open, color=color.green, style=plot.style_linebr, linewidth=4)
    plot(pnf_close, color=color.red, style=plot.style_linebr, linewidth=4)

.. image:: images/Pine_Point_and_Figure.png

For detailed information, see `ticker.pointfigure() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}pointfigure>`__.


.. rubric:: Footnotes

.. [#ticks] On TradingView, Renko, Line Break, Kagi and PnF chart types are generated from OHLC values from a lower timeframe.
   These chart types thus represent only an approximation of what they would be like if they were generated from tick data.
