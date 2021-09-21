.. _PageRepainting:

Repainting
==========

We define repainting as: **script behavior where it will not calculate or plot the same way on historical bars and in realtime**.

Historical data does not include records of intra-bar movements of price; only
`open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__,
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values (OHLC).

Conversely, on realtime bars (bars running when the instrument's market is open), the
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values are not fixed;
they can changes values many times before the realtime bar closes and its HLC values are fixed.
This leads to a script sometimes working differently on historical data and in real time, 
where only the `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__ price will not change during the bar.

Any script using values like 
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ 
in realtime is subject to producing calculations that may not be repeatable on historical bars — thus repaint.

Let's look at this simple script. It detect crosses of the
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ value
(in the realtime bar, this corresponds to the current price of the instrument) 
over and under an `EMA <https://www.tradingview.com/u/?solution=43000592270#>`__::

    //@version=5
    indicator("Repainting", "", true)
    ma = ta.ema(close, 5)
    xUp = ta.crossover(close, ma)
    xDn = ta.crossunder(close, ma)
    plot(ma, "MA", color.black, 2)
    bgcolor(xUp ? color.new(color.lime, 80) : xDn ? color.new(color.fuchsia, 80) : na)

.. image:: images/Repainting-01.png

Note that:

- The script uses `bgcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_bgcolor>`__
  to color the background green when `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
  crosses over the EMA, and red on crosses under the EMA.
- The screen snapshot shows the script in realtime on a 30sec chart.
  A cross over the EMA has been detected, thus the background of the realtime bar is green.
- The problem here is that nothing guarantees this condition will hold true until the
  end of the realtime bar. The arrow points to the timer showing that 21 seconds remain in the realtime bar,
  and anything could happen until then.
- We are witnessing a repainting script.
  
To prevent this repainting, we must rewrite our script so that it does not use values that fluctuate
during the realtime bar. This will require using values from a bar that has elapsed
(typically the preceding bar), or the `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__
price, which does not vary in realtime.

We can chieve this in many ways. This uses the crosses detected on the previous bar.
It is the simplest way to avoid repainting::

    //@version=5
    indicator("Repainting", "", true)
    ma = ta.ema(close, 5)
    xUp = ta.crossover(close, ma)[1]
    xDn = ta.crossunder(close, ma)[1]
    plot(ma, "MA", color.black, 2)
    bgcolor(xUp ? color.new(color.lime, 80) : xDn ? color.new(color.fuchsia, 80) : na)

This uses only confirmed `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
values for its calculations::

    //@version=5
    indicator("Repainting", "", true)
    ma = ta.ema(close[1], 5)
    xUp = ta.crossover(close[1], ma)
    xDn = ta.crossunder(close[1], ma)
    plot(ma, "MA", color.black, 2)
    bgcolor(xUp ? color.new(color.lime, 80) : xDn ? color.new(color.fuchsia, 80) : na)

This uses the `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__

Here, we use the values of the the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_{question}{colon}>`__
history-referencing operator to use 

one form of repainting, 
Whereas these scrpits will produce only one result on historical bars because they calculate at their bar's close,
in realtime, such scripts are constantly recalculating values once they are running in realtime.
They can thus produce 

Other values will typically move many times before the realtime bar's final
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values are fixed, after the realtime bar closes.

If we add a script on a chart,
wait until it calculates on a number of realtime bars and then reload the page,
we will sometimes see a script's plots change slightly. This behavior is one of a few
different types of behaviors commonly referred to as *indicator repainting*.

Not all indicators are subject to the types of repainting we discuss here.
In most cases it depends on whether or not certain functions or language
constructs are used in the code.

Please note that this repainting effect
is **not** a bug; it is the result of the inherent differences between historic
bars and realtime bar information on TradingView.

Repainting is possible in the following cases:

#. Strategies using ``calc_on_every_tick = true``.
   A strategy with parameter ``calc_on_every_tick = false`` may also be
   prone to repainting, but to a lesser degree.

#. Using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
   to request data from a timeframe *higher* than the timeframe of the chart's main symbol::

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
   to request data from a timeframe **lower** than the timeframe of chart's main symbol
   (more on the subject :ref:`here <PageOtherTimeframesAndData_RequestingDataOfALowerTimeframe>`).
   When using lower timeframes in realtime, using ``lookahead = barmerge.lookahead_off`` will produce repainting.
   It is less probalbe with ``lookahead = barmerge.lookahead_on``,
   but may still occur when 1 and 5 minute updates outrun each other.

#. All scripts with calculations depending on a *starting point*.
   At the beginning of the dataset, intraday data gets aligned to the beginning of the week, month or
   year, depending on the timeframe. Due to this, the results produced by
   scripts can differ from time to time because they start on different bars.
   These are cases where scripts will be relying on a starting point:

   * When they use `ta.valuewhen() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}valuewhen>`__,
     `ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__ or
     `ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__
     functions (due to peculiarities in their algorithm).
   * Any backtesting strategy, regardless of the argument used for ``calc_on_every_tick``.

   There is a dependency between the timeframe and the alignment of a starting point:

   * 1 - 14 minutes: aligns to the beginning of a week.
   * 15 - 29 minutes: aligns to the beginning of a month.
   * from 30 minutes and higher: aligns to the beginning of a year.

   The following limitations of history lengths are taken into account when
   processing the data:
	
   * 20000 historical bars for the Premium plan.
   * 10000 historical bars for Pro and Pro+ plans.
   * 5000 historical bars for other plans.

#. Changes in historical data, for example, due to a *split*.

#. Presence of the following variables in the script often leads to repainting:

   * `barstate.isconfirmed <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isconfirmed>`__,
     `barstate.isfirst <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isfirst>`__,
     `barstate.ishistory <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}ishistory>`__,
     `barstate.islast <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}islast>`__,
     `barstate.isnew <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isnew>`__,
     `barstate.isrealtime <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isrealtime>`__
   * `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__
   * `bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__

#. When scripts use `varip <https://www.tradingview.com/pine-script-reference/v5/#op_varip>`__ variables
   to make calculations that can only be done in realtime (:ref:`more on varip here <PageVariableDeclarations_Varip>`).


Other types of repainting
-------------------------

Other types of behavior referred to as *repainting* include:

- Plotting with a negative offset on past bars.
- Values recalculating differently on historical bars vs elapsed realtime bars.
  This can be caused by the fact that exchanges/brokers will sometimes make what are usually small adjustments
  to bar prices when generating the historical data prices for newly elapsed realtime bars.
- Using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
  without the proper adjustments to ensure that it does not return higher timeframe data that fluctuates on realtime bars,
  due to the fact that the current higher timeframe has not completed. 
  See the Pinecoders `security() revisited <https://www.tradingview.com/script/00jFIl5w-security-revisited-PineCoders/>`__
  publication for more information.
