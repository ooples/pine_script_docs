.. _PageRepainting:

Repainting
==========

.. contents:: :local:
    :depth: 2



Introduction
------------

We define repainting as: **script behavior causing historical vs realtime calculations or plots to behave differently**.

Repainting behavior is widespread and can be caused by many factors. 
Following our definition, our estimate is that more than 95% of indicators in existence repaint. 
Widely used indicators like MACD and RSI, for example, repaint because they show one fixed value on historical bars,
yet when running in realtime they will produce results that constantly fluctuate until the realtime bar closes. 
They thus behave differently on historical and realtime bars. This does not make them less useful, nor prevent knowledgeable traders from using them.

**Repainting is not inherently good or bad.**



For script users
^^^^^^^^^^^^^^^^

You can very well decide to use repainting indicators if you understand how they behave and they suit your trading methodology.
Don't be one of those newcomers to trading who slap "repaint" sentences on published scripts as if it discredits them.
Doing so only reveals your incomprehension of the subject.

The question "Does it repaint?" means nothing, and consequently cannot be answered. 
Why? Because it needs to be qualified. Instead, one could ask:

- Do the entry/exit markers your indicator displays repaint (or: Do you wait for the realtime bar to close before displaying your entry/exit markers)?
- Do alerts wait for the end of the realtime bar before triggering?
- Do the higher timeframe plots repaint (which means they won't plot the same way on realtime bars as they do on historical bars)?
- Does your script plot in the past (as most pivot or zigzag scripts will do)?
- Does your strategy use ``calc_on_every_tick = true``?
- Will your indicator display in realtime the same way it does on historical bars?
- Are you fetching future information with your `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ calls?

What's important is that you understand how the tools you use work, 
and if their behavior is compatible with your objectives, repainting or not.
As you will learn if you read this page, repainting is a complex matter. 
It has many faces and many causes. Even if you don't program in Pine,
this page will help you understand the array of causes that can lead to repainting,
and hopefully enable more meaningful discussions with script authors.



For Pine coders
^^^^^^^^^^^^^^^

As we discussed in the previous section, not all types of repainting behavior must necessarily be avoided at all costs.
We hope this page helps you better understand the dynamics at play, so that you can make better design decisions concerning your trading tools.
This page's content should help you avoid making the most common coding mistakes that lead to repainting or misleading plots.

Whatever your design decisions are, if you publish your script, you should explain them to traders so they can understand how you script behaves.

Let's explore some of the causes of repainting, and discuss solutions when they exist.
We will survey three broad categories of repainting causes:

- Historical vs realtime calculations
- Plotting in the past
- Dataset variations



Historical vs realtime calculations
-----------------------------------



Fluid data values
^^^^^^^^^^^^^^^^^

Historical data does not include records of intrabar movements of price; only
`open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__,
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values (OHLC).

Conversely, on realtime bars (bars running when the instrument's market is open), the
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values are not fixed;
they can changes values many times before the realtime bar closes and its HLC values are fixed. They are *fluid*.
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

We can chieve this in many ways. This method adds a ``and barstate.isconfirmed`` 
condition to our cross detections, which requires the script to be executing on the bar's last iteration, 
when it closes and prices are confirmed. It is a simple way to avoid repainting::

    //@version=5
    indicator("Repainting", "", true)
    ma = ta.ema(close, 5)
    xUp = ta.crossover(close, ma) and barstate.isconfirmed
    xDn = ta.crossunder(close, ma) and barstate.isconfirmed
    plot(ma, "MA", color.black, 2)
    bgcolor(xUp ? color.new(color.lime, 80) : xDn ? color.new(color.fuchsia, 80) : na)

This uses the crosses detected on the previous bar::

    //@version=5
    indicator("Repainting", "", true)
    ma = ta.ema(close, 5)
    xUp = ta.crossover(close, ma)[1]
    xDn = ta.crossunder(close, ma)[1]
    plot(ma, "MA", color.black, 2)
    bgcolor(xUp ? color.new(color.lime, 80) : xDn ? color.new(color.fuchsia, 80) : na)

This uses only confirmed `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
and EMA values for its calculations::

    //@version=5
    indicator("Repainting", "", true)
    ma = ta.ema(close[1], 5)
    xUp = ta.crossover(close[1], ma)
    xDn = ta.crossunder(close[1], ma)
    plot(ma, "MA", color.black, 2)
    bgcolor(xUp ? color.new(color.lime, 80) : xDn ? color.new(color.fuchsia, 80) : na)

This detects crosses between the realtime bar's `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__
and the value of the EMA from the previous bars. Notice that the EMA is calculated using 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__, 
so it repaints. We must ensure we use a confirmed value to detect crosses, thus ``ma[1]``
in the cross detection logic::

    //@version=5
    indicator("Repainting", "", true)
    ma = ta.ema(close, 5)
    xUp = ta.crossover(open, ma[1])
    xDn = ta.crossunder(open, ma[1])
    plot(ma, "MA", color.black, 2)
    bgcolor(xUp ? color.new(color.lime, 80) : xDn ? color.new(color.fuchsia, 80) : na)

**Notice that all these methods have one thing in common: while they prevent repainting, 
they will also trigger signals later than repainting scripts. 
This is an inevitable compromise if one wants to avoid repainting.
You just can't have your cake and eat it too.**



Repainting \`request.security()\` calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data fetched with `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
will differ on historical and realtime bars if the function is not used in the correct manner.
Repainting `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
calls will produce historical data and plots that cannot be replicated in realtime.
Let's look at a script showing the difference between repainting and non-repainting
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ calls::

    //@version=5
    indicator("Repainting vs non-repainting `request.security()`", "", true)
    var BLACK_MEDIUM = color.new(color.black, 50)
    var ORANGE_LIGHT = color.new(color.orange, 80)
    
    tfInput = input.timeframe("1")
    
    repaintingClose = request.security(syminfo.tickerid, tfInput, close)
    plot(repaintingClose, "Repainting close", BLACK_MEDIUM, 8)
    
    indexHighTF = barstate.isrealtime ? 1 : 0
    indexCurrTF = barstate.isrealtime ? 0 : 1
    nonRepaintingClose = request.security(syminfo.tickerid, tfInput, close[indexHighTF])[indexCurrTF]
    plot(nonRepaintingClose, "Non-repainting close", color.fuchsia, 3)
    
    if ta.change(time(tfInput))
        label.new(bar_index, na, "↻", yloc = yloc.abovebar, style = label.style_none, textcolor = color.black, size = size.large)
    bgcolor(barstate.isrealtime ? ORANGE_LIGHT : na)

This is what its output looks like on a 5sec chart that has been running the script for a few minutes:

.. image:: images/Repainting-RepaintingRequestSecurityCalls-01.png

Note that:

- The orange background identifies the realtime bar, and elapsed realtime bars.
- A black curved arrow indicates when a new higher timeframe comes in.
- The thick gray line shows the repainting `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call
  used to initialize ``repaintingClose``.
- The fuchsia line shows the non-repainting `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call
  used to initialize ``nonRepaintingClose``.
- The behavior of the repainting line is completely different on historical bars and in realtime. On historical bars,
  it shows the new value of a completed timeframe on the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
  of the bar where it completes. It then stays stable until another timeframe completes. The problem is that in realtime,
  it follows the current `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ price,
  so it moves all the time and changes on each bar.
- The behavior of the non-repainting, fuchsia line, in contrast, behaves exactly the same way on historical bars and in realtime.
  It updates on the bar following the completion of the higher timeframe, and doesn't move until the bar after another higher timeframe completes.
  Thus, it is more reliable. Note that while new higher timeframe data comes in at the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
  of historical bars, it will be available on the `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__
  of the same bar in realtime.

This script shows a ``nonRepaintingSecurity()`` function that can be used to do the same as our non-repainting code in the previous example::

    //@version=5
    indicator("Non-repainting `nonRepaintingSecurity()`", "", true)
    
    tfInput = input.timeframe("1")
    
    nonRepaintingSecurity(sym, tf, src) =>
        request.security(sym, tf, close[barstate.isrealtime ? 1 : 0])[barstate.isrealtime ? 0 : 1]
    
    nonRepaintingClose = nonRepaintingSecurity(syminfo.tickerid, "1", close)
    plot(nonRepaintingClose, "Non-repainting close", color.fuchsia, 3)

Another way that can be used to produce non-repainting higher timeframe data is this,
which use an offset of ``[1]`` on the series, and ``lookahead``::

    request.security(sym, tf, close[1], lookahead = barmerge.lookahead_on)

While it will produce the same non-repainting behavior as ``nonRepaintingSecurity()`` in realtime,
it has the disadvantage of showing the higher timeframe values one bar earlier on historical bars.
This may look better, but the problem is that it does not reflect its behavior in realtime.
While the method used in ``nonRepaintingSecurity()`` is more complex, we find it more reliable.



Using \`request.security()\` at lower timeframes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some scripts use `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
to request data from a timeframe **lower** than the chart's timeframe.
This works on historical bars but will not work in realtime.



Future leak with \`request.security()\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
is used with ``lookahead = barmerge.lookahead_on`` to fetch prices without offsetting the series by ``[1]``,
it will return data from the future on historical bars, which is dangerously misleading.

While historical bars will magically display future prices before they should be known,
no lookahead is possible in realtime because the future there is unknown, as it should, so no future bars exist.

This is an example::

    //@version=5
    indicator("Future leak", "", true)
    futureHigh = request.security(syminfo.tickerid, "D", high, lookahead = barmerge.lookahead_on)
    plot(futureHigh)

.. image:: images/Repainting-FutureLeakWithRequestSecurity-01.png

Note how the higher timeframe line is showing the timeframe's `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__
value before it occurs. The solution is to use the function like we do in our ``nonRepaintingSecurity()`` shown earlier.



\`varip\`
^^^^^^^^^

Scripts using the `varip <https://www.tradingview.com/pine-script-reference/v5/#op_varip>`__ 
declaration mode for variables (see our section on :ref:`varip  <PageVariableDeclarations_Varip>` for more information)
save information across realtime updates, which cannot be reproduced on historical bars where only OHLC information is available.
Such scripts may be useful in realtime, including to generate alerts,
but their logic cannot be backtested, nor can their plots on historical bars reflect calculations that will be done in realtime.



Bar state built-ins
^^^^^^^^^^^^^^^^^^^

Scripts using :ref:`bar states <PageBarStates>` may or may not repaint.
As we have seen in the previous section, using `barstate.isconfirmed <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isconfirmed>`__
is actually one way to **avoid** repainting that **will** reproduce on historical bars, which are always "confirmed".
Uses of other bar states such as `barstate.isnew <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isnew>`__,
however, will lead to repainting. The reason is that on historical bars, 
`barstate.isnew <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isnew>`__ is ``true`` on the bar's
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__, yet in realtime, it is ``true`` on the bar's
`open <https://www.tradingview.com/pine-script-reference/v5/#open>`__. 
Using the other bar state variables will usually cause some type of behavioral discrepancy between historical and realtime bars.



Strategies
^^^^^^^^^^

Strategies using ``calc_on_every_tick = true`` cannot 


A strategy with parameter ``calc_on_every_tick = false`` may also be
   prone to repainting, but to a lesser degree.


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



Plotting in the past
--------------------

If a script takes 5 bars to detect a pivot, then in the realtime bar, 
pivots can only be detected 5 bars after they occur.
Historical bars 



Dataset variations
------------------



Starting points
^^^^^^^^^^^^^^^

Scripts begin executing on the chart's first historical bar, and then execute on each bar sequentially, 
as is explained in this manual's page on Pine's :ref:`execution model <PageExecutionModel>`.
If the first bar changes, then the script will often not calculate the same way it did when the dataset began at a different point in time.

The following factors have an impact on the quantity of bars you can see on your charts:

- The type of account you hold
- The historical data available from the data supplier
- The alignment requirements of the dataset, which determine its *starting point*

These are the account-specific bar limits:
	
- 20000 historical bars for the Premium plan.
- 10000 historical bars for Pro and Pro+ plans.
- 5000 historical bars for other plans.

Starting points are determined using the following rules, which depend on the chart's timeframe:

- **1 - 14 minutes**: aligns to the beginning of a week.
- **15 - 29 minutes**: aligns to the beginning of a month.
- **30 minutes and higher**: aligns to the beginning of a year.

As time goes by, the combinations of these factors cause your chart's history to start at different points in time.
This often has an impact on your scripts calculations, because calculations changes in early bars can ripple through all the other bars in the dataset. 
Using functions like `ta.valuewhen() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}valuewhen>`__,
`ta.barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}barssince>`__ or
`ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__, for example,
will yield results that vary with early history.



Revision of historical data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Historical and realtime bars are built using two different data feeds supplied by exchanges/brokers: historical data, and realtime data.
When realtime bars elapse, exchanges/brokers sometimes make what are usually small adjustments to bar prices, which are then written to their historical data.
When the chart is refreshed or the script is re-executed on those elapsed realtime bars,
they will then be built and calculated using the historical data, which will contain those usually small price revisions, if any have been made.

Historical data may also be revised for other reasons, e.g., for stock splits.
