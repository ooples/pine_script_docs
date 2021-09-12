Indicator repainting
====================

Historical data does not include records of intra-bar movements of price;
only open, high, low and close (OHLC). This leads to a script sometimes
working differently on historical data and in real-time, where only the open price
is known and where price will typically move many times before the
real-time bar's final high, low and close values are
set after the real-time bar closes.

If we add a script on a chart,
wait until it calculates on a number of real-time bars and then reload the page,
we will sometimes see a script's plots change slightly. This behavior is one of a few
different types of behaviors commonly referred to as *indicator repainting*. It is the
type of repainting we are concerned with here and which we will refer to when using *repainting*.
It is due to the fact that when certain features are used in scripts, they will
calculate differently on historical and real-time bars.

Other types of behavior rightly or wrongly referred to as *repainting* include plotting with a
negative offset on past bars and using otherwise unavailable future information received through
malformed calls to the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function, which can introduce
data not available in real-time into script calculations.

Not all indicators are subject to the type of repainting we discuss here.
In most cases it depends on whether or not certain functions or language
constructs are used in the code. Please note that this repainting effect
is **not** a bug; it is the result of the inherent differences between historic
bars and real-time bar information on TradingView.

We can see repainting in the following cases:

#. Strategies using ``calc_on_every_tick=true``.
   A strategy with parameter ``calc_on_every_tick = false`` may also be
   prone to repainting, but to a lesser degree.

#. Using ``request.security`` for requesting data from a resolution *higher* than the resolution of the chart's main symbol::

    // Add this study on 1 minute chart
    //@version=5
    indicator("My Script")
    c = request.security(syminfo.tickerid, "5", close)
    plot(close)
    plot(c, color = color.red)

   This study will calculate differently on real-time and
   historical data, regardless of ``lookahead`` parameter's value (see
   :ref:`understanding_lookahead`).

#. Using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
   to request data from a timeframe *lower* than the timeframe of chart's main symbol
   (more information :ref:`here <requesting_data_of_a_lower_timeframe>`).
   If ``lookahead=barmerge.lookahead_off``, repainting will occur. When ``lookahead=barmerge.lookahead_on``,
   repainting is less probable. It may still happen when 1 and 5 minute updates
   outrun each other.

#. All scripts which calculations depending on a *starting point*.
   Intraday data gets aligned to the beginning of the week, month or
   year, depending on the resolution. Due to this, the results produced by
   such scripts can differ from time to time. These are cases where
   scripts will be relying on a starting point:

   * when they use `ta.valuewhen() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}valuewhen>`__,
     `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__ or
     `ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__
     functions (due to peculiarities in their algorithm).
   * any backtesting strategy (regardless of how the ``calc_on_every_tick`` parameter is defined).

   There is a dependency between the resolution and the alignment of a starting point:

   * 1--14 minutes --- aligns to the beginning of a week.
   * 15--29 minutes --- aligns to the beginning of a month.
   * from 30 minutes and higher --- aligns to the beginning of a year.

   The following limitations of history lengths are taken into account when
   processing the data:
	
   * 20000 historical bars for the Premium plan.
   * 10000 historical bars for Pro and Pro+ plans.
   * 5000 historical bars for other plans.

#. Changes in historical data, for example, due to a *split*.

#. Presence of the following variables in the script usually leads to repainting:

   * `barstate.isconfirmed <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isconfirmed>`__,
     `barstate.isfirst <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isfirst>`__,
     `barstate.ishistory <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}ishistory>`__,
     `barstate.islast <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}islast>`__,
     `barstate.isnew <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isnew>`__,
     `barstate.isrealtime <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isrealtime>`__;
   * `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__;
   * `bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__.


