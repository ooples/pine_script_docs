.. _PageBarPlotting:

Bar plotting
============

.. contents:: :local:
    :depth: 2



Plotting candles with \`plotcandle()\`
--------------------------------------

You can create your own custom candles with the `plotcandle() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotcandle>`__
built-in function. It's signature is::

    plotcandle(open, high, low, close, title, color, wickcolor, editable, show_last, bordercolor, display) → void


    //@version=5
    indicator("Example 1")
    plotbar(open, high, low, close)

.. image:: images/BarPlotting-Plotbar-1.png

*Example 1* simply replicates bars of the current symbol.
To color them green or red, we can use the following code::

    //@version=5
    indicator("Example 2")
    paletteColor = close >= open ? color.lime : color.red
    plotbar(open, high, low, close, color = paletteColor)

.. image:: images/Custom_ohlc_bars_and_candles_2.png

*Example 2* illustrates using the ``color`` argument, which can be given
constant values such as ``red``, ``lime``, ``"#FF9090"``, as well as expressions that
calculate colors conditionally at runtime (see the ``palette`` variable in the example above).

The ``plotcandle`` annotation function is similar to ``plotbar``, but it plots candles
instead of bars and has an optional argument: ``wickcolor``.

Both ``plotbar`` and ``plotcandle`` need four series as the arguments that will be
used for new bar/candle OHLC prices. If one of
the arguments for a bar has a ``na`` value, then the bar is not
plotted. Example::

    //@version=5
    indicator("Example 3")
    c = close > open ? na : close
    plotcandle(open, high, low, c)

.. image:: images/Custom_ohlc_bars_and_candles_3.png

You can build bars or candles using values other than the actual OHLC values.
For example you could calculate and plot *smoothed* candles using the following code::

    //@version=5
    indicator("Example 4")
    lenInput = input.int(9)
    smooth(source, length) =>
        ta.sma(source, length)
    o = smooth(open, lenInput)
    h = smooth(high, lenInput)
    l = smooth(low, lenInput)
    c = smooth(close, lenInput)
    plotcandle(o, h, l, c)

.. image:: images/Custom_ohlc_bars_and_candles_4.png

You may find it useful to plot OHLC values taken from a
higher timeframe. You can, for example, plot daily bars on a *60 minutes* chart::

    // NOTE: add this script on intraday chart
    //@version=5
    indicator("Example 5")
    higherTFInput = input.timeframe("D")
    isNewBar(res) =>
        nz(ta.change(time(res)) > 0, true)
    [o, h, l, c] = request.security(syminfo.tickerid, higherTFInput, [open, high, low, close])
    plotbar(isNewBar(higherTFInput) ? o : na, h, l, c, color=c >= o ? color.lime : color.red)

.. image:: images/Custom_ohlc_bars_and_candles_5.png

The ``plotbar`` and ``plotcandle`` annotation functions also have a ``title`` argument, so users can distinguish them in
the *Style* tab of the *Settings* dialog box.



Plotting bars with \`plotbar()\`
--------------------------------

Whereas `plotcandle() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotcandle>`__
creates candles, `plotbar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotbar>`__
creates conventional bars. It's signature is::

    plotbar(open, high, low, close, title, color, editable, show_last, display) → void

This plots simple bars using the habitual OHLC values in a separate pane::

    //@version=5
    indicator("Single-color bars")
    plotbar(open, high, low, close, "OHLC bars")

.. image:: images/ColoringAndPlottingBars-Plotbar-1.png

To color them green or red, we can use the following code::

    //@version=5
    indicator("Example 2")
    paletteColor = close >= open ? color.lime : color.red
    plotbar(open, high, low, close, color = paletteColor)

.. image:: images/BarPlotting-Plotbar-2.png

Note that:

- The ``color`` argument accepts constant values such as ``color.red``, ``color.lime``, ``"#FF9090"``, 
  as well as expressions that calculate colors at runtime, as is done with the ``paletteColor`` variable here.

The ``plotcandle`` annotation function is similar to ``plotbar``, but it plots candles
instead of bars and has an optional argument: ``wickcolor``.

Both ``plotbar`` and ``plotcandle`` need four series as the arguments that will be
used for new bar/candle OHLC prices. If one of
the arguments for a bar has a ``na`` value, then the bar is not
plotted. Example::

    //@version=5
    indicator("Example 3")
    c = close > open ? na : close
    plotcandle(open, high, low, c)

.. image:: images/Custom_ohlc_bars_and_candles_3.png

You can build bars or candles using values other than the actual OHLC values.
For example you could calculate and plot *smoothed* candles using the following code::

    //@version=5
    indicator("Example 4")
    lenInput = input.int(9)
    smooth(source, length) =>
        ta.sma(source, length)
    o = smooth(open, lenInput)
    h = smooth(high, lenInput)
    l = smooth(low, lenInput)
    c = smooth(close, lenInput)
    plotcandle(o, h, l, c)

.. image:: images/Custom_ohlc_bars_and_candles_4.png

You may find it useful to plot OHLC values taken from a
higher timeframe. You can, for example, plot daily bars on a *60 minutes* chart::

    // NOTE: add this script on intraday chart
    //@version=5
    indicator("Example 5")
    higherTFInput = input.timeframe("D")
    isNewBar(res) =>
        nz(ta.change(time(res)) > 0, true)
    [o, h, l, c] = request.security(syminfo.tickerid, higherTFInput, [open, high, low, close])
    plotbar(isNewBar(higherTFInput) ? o : na, h, l, c, color=c >= o ? color.lime : color.red)

.. image:: images/Custom_ohlc_bars_and_candles_5.png

The ``plotbar`` and ``plotcandle`` annotation functions also have a ``title`` argument, so users can distinguish them in
the *Style* tab of the *Settings* dialog box.
