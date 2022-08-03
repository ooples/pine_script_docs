.. image:: /images/Pine_Script_logo.svg
   :alt: Pine Script™ logo
   :target: https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html
   :align: right
   :width: 100
   :height: 100


.. _PageStrategiesFaq:


Strategies FAQ
==============


.. contents:: :local:
    :depth: 3



Why are my orders executed on the bar following my triggers?
------------------------------------------------------------

TradingView backtesting evaluates conditions at the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ of historical bars. 
When a condition triggers, the associated order is executed at the `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__ of the next bar, 
unless ``process_orders_on_close = true`` in the `strategy() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__ declaration statement, 
in which case the broker emulator will try to execute orders at the bar’s `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__.

In the real-time bar, orders may be executed on the tick (price change) following detection of a condition. While this may seem appealing, 
it is important to realize that if you use ``calc_on_every_tick = true`` in the `strategy() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__ 
declaration statement to make your strategy work this way, you are going to be running a different strategy than the one you tested on historical bars. 
See the `Strategies <https://www.tradingview.com/pine-script-docs/en/v5/concepts/Strategies.html>`__ page of the Pine Script™ User Manual for more information.



How do I implement date range filtering in strategies?
------------------------------------------------------

This code allows coders to restrict specific calculations in a script to user-selected from/to dates. 
If you need to also filter on specific times, use `How To Set Backtest Time Ranges <https://www.tradingview.com/script/xAEG4ZJG-How-To-Set-Backtest-Time-Ranges>`__ by 
`allanster <https://www.tradingview.com/u/allanster/#published-scripts>`__.

::

    //@version=5
    indicator("Date filtering example", "", true)
    useDateFilter = input(false, "═════ Date Range Filtering ═════")
    startYear = input.int(1900, "Start Year", minval=1900)
    startMonth = input.int(1, "Start Month", minval=1, maxval=12)
    startDay = input.int(1, "Start Day", minval=1, maxval=31)
    endYear = input.int(2999, "End Year", minval=1900)
    endMonth = input.int(1, "End Month", minval=1, maxval=12)
    endDay = input.int(1, "End Day", minval=1, maxval=31)

    startDate = timestamp(startYear, startMonth, startDay, 00, 00)
    endDate = timestamp(endYear, endMonth, endDay, 23, 59)
    tradeDateIsAllowed() =>
        not useDateFilter or time >= startDate and time <= endDate

    enterLong = tradeDateIsAllowed() and ta.crossover(ta.rsi(close, 14), 50)

    plotchar(enterLong, "enterLong", "▲", location.belowbar, color.new(color.lime, 0), size=size.tiny)

Note that with this code snippet, date filtering can quickly be enabled/disabled using a checkbox. 
This way, traders don’t have to reset dates when filtering is no longer needed; they can simply uncheck the box.



Why is backtesting on Heikin Ashi and other non-standard charts not recommended?
--------------------------------------------------------------------------------

Because non-standard chart types use non-standard prices which produce non-standard results. 
See our `Backtesting on Non-Standard Charts: Caution! - PineCoders FAQ <>`__ strategy script and its description for a more complete explanation.

The TradingView Help Center also has a `good article <https://www.tradingview.com/support/solutions/43000481029>`__ on the subject.



How can I save the entry price in a strategy?
---------------------------------------------

Here are two ways you can go about it:

::

    //@version=5
    // Mod of original code at https://www.tradingview.com/script/bHTnipgY-HOWTO-Plot-Entry-Price/
    strategy('Plot Entry Price', '', true)

    longCondition = ta.crossover(ta.sma(close, 14), ta.sma(close, 28))
    if longCondition
        strategy.entry('My Long Entry Id', strategy.long)
    shortCondition = ta.crossunder(ta.sma(close, 14), ta.sma(close, 28))
    if shortCondition
        strategy.entry('My Short Entry Id', strategy.short)

    // ————— Method 1: wait until bar following order and use its open.
    var float entryPrice = na
    if longCondition[1] or shortCondition[1]
        entryPrice := open
        entryPrice
    plot(entryPrice, 'Method 1', color.new(color.orange, 0), 3, plot.style_circles)

    // ————— Method 2: use built-in variable.
    plot(strategy.position_avg_price, 'Method 2', color.new(color.gray, 0), 1, plot.style_circles)



Can my strategy place orders with TradingView brokers?
------------------------------------------------------

Not directly from the TradingView platform, as can be done manually; only manual orders can be placed with brokers integrated in TradingView. 
It is, however, possible for Pine scripts to place orders in markets for automated trading, including through some of the brokers integrated in TradingView, 
but to reach them you will need to use a third party execution engine to relay orders. See our next entry on the subject.



Can my Pine strategy or study place automated orders in markets?
----------------------------------------------------------------



Can I connect my strategies to my paper trading account?
--------------------------------------------------------



How can I implement a time delay between orders?
------------------------------------------------

We can do this by saving the time when trades occur, and then determining the time delay since the last order execution. 
The broker emulator doesn’t notify a script when an order is executed, so we will detect their execution by monitoring changes in the 
`strategy.position_size <https://www.tradingview.com/pine-script-reference/v5/#var_strategy{dot}position_size>`__ built-in variable.
Here, we set up the script to allow the user to turn the delay on and off, and to set the duration of the delay. 
The ``tfInMinutes()`` and ``timeFrom(from, qty, units)`` are lifted from our `Time Offset Calculation Framework <>`__:

::

    //@version=5
    strategy("Strat with time delay", overlay = true)

    timeUnitsQty = -input.int(20, "Quantity", inline="Delay", minval=0, tooltip="Use 0 for no delay")
    timeUnitType = input.string("minutes", "", inline="Delay", options=["seconds", "minutes", "hours", "days", "months", "years"])

    // ————— Converts current chart timeframe into a float minutes value.
    tfInMinutes() =>
        tfInMinutes = timeframe.multiplier * (timeframe.isseconds ? 1. / 60 : timeframe.isminutes ? 1. : timeframe.isdaily ? 60. * 24 : timeframe.isweekly ? 60. * 24 * 7 : timeframe.ismonthly ? 60. * 24 * 30.4375 : na)

    // ————— Calculates a +/- time offset in variable units from the current bar"s time or from the current time.
    // WARNING:
    //      This functions does not solve the challenge of taking into account irregular gaps between bars when calculating time offsets.
    //      Optimal behavior occurs when there are no missing bars at the chart resolution between the current bar and the calculated time for the offset.
    //      Holidays, no-trade periods or other irregularities causing missing bars will produce unpredictable results.
    timeFrom(from, qty, units) =>
        // from  : starting time from where the offset is calculated: "bar" to start from the bar"s starting time, "close" to start from the bar"s closing time, "now" to start from the current time.
        // qty   : the +/- qty of _units of offset required. A "series float" can be used but it will be cast to a "series int".
        // units : string containing one of the seven allowed time units: "chart" (chart"s resolution), "seconds", "minutes", "hours", "days", "months", "years".
        int timeFrom = na
        // Remove any "s" letter in the _units argument, so we don"t need to compare singular and plural unit names.
        unit = str.replace_all(units, "s", "")
        // Determine if we will calculate offset from the bar"s time or from current time.
        t = from == "bar" ? time : from == "close" ? time_close : timenow
        // Calculate time at offset.
        if units == "chart"
            // Offset in chart res multiples.
            timeFrom := int(t + tfInMinutes() * 60 * 1000 * qty)
        else
            // Add the required qty of time units to the from starting time.
            y = year(t) + (unit == "year" ? int(qty) : 0)
            m = month(t) + (unit == "month" ? int(qty) : 0)
            d = dayofmonth(t) + (unit == "day" ? int(qty) : 0)
            h = hour(t) + (unit == "hour" ? int(qty) : 0)
            min = minute(t) + (unit == "minute" ? int(qty) : 0)
            s = second(t) + (unit == "econd" ? int(qty) : 0)
            // Return the resulting time in ms Unix time format.
            timeFrom := timestamp(y, m, d, h, min, s)

    // Entry conditions.
    ma = ta.sma(close, 100)
    goLong = close > ma
    goShort = close < ma

    // Time delay filter
    var float lastTradeTime = na
    if nz(ta.change(strategy.position_size), time) != 0
        // An order has been executed; save the bar"s time.
        lastTradeTime := time
        lastTradeTime
    // If user has chosen to do so, wait `timeUnitsQty` `timeUnitType` between orders
    delayElapsed = timeFrom("bar", timeUnitsQty, timeUnitType) >= lastTradeTime

    if goLong and delayElapsed
        strategy.entry("Long", strategy.long, comment="Long")
    if goShort and delayElapsed
        strategy.entry("Short", strategy.short, comment="Short")

    plot(ma, "MA", goLong ? color.lime : color.red)
    plotchar(delayElapsed, "delayElapsed", "•", location.top, size=size.tiny)



How can I calculate custom statistics in a strategy?
----------------------------------------------------

When you issue orders in a strategy by using any of the ``strategy.*()`` function calls, you do the equivalent of sending an order to your broker/exchange. 
The broker emulator takes over the management of those orders and simulates their execution when the conditions in the orders are fulfilled. 
In order to detect the execution of those orders, you can use changes in the built-in variables such as 
`strategy.opentrades <https://www.tradingview.com/pine-script-reference/v5/#var_strategy{dot}opentrades>`__ and 
`strategy.closedtrades <https://www.tradingview.com/pine-script-reference/v5/#var_strategy{dot}closedtrades>`__.

This script demonstrates how to accomplish this. The first part calculates the usual conditions required to manage trade orders and issues those orders. 
The second part detects order fill events and calculates various statistics from them. The script also demonstrates how to calculate position sizes using a fixed 
percentage of the equity and the risk incurred when entering the trade, which is defined as the distance to the entry stop. 
The default strategy parameters also use commission. All strategies should account for some fees, either in the form of commission or in slippage 
(which can be used to simulate spreads), as nobody usually trades for free, and ignoring trading fees is a common mistake which can be costly:

::

    //@version=5
    strategy("Custom strat stats", "", true, initial_capital = 10000, commission_type = strategy.commission.percent, commission_value = 0.075, max_bars_back = 1000)

    float maxPctRisk = input.float(1.0, "Maximum %Risk On Equity Per Trade", minval = 0.0, maxval = 100.0, step = 0.25) / 100.0

    // ———————————————————— Strat calcs.
    // ————— Function rounding _price to tick precision.
    roundToTick(_price) =>
        math.round(_price / syminfo.mintick) * syminfo.mintick

    // ————— Entries on MA crosses when equity is not depleted.
    float c = roundToTick(close)
    float maF = roundToTick(ta.sma(hlc3, 10))
    float maS = roundToTick(ta.sma(hlc3, 60))
    bool enterLong = ta.crossover(maF, maS) and strategy.equity > 0
    bool enterShort = ta.crossunder(maF, maS) and strategy.equity > 0
    // ————— Exits on breach of hi/lo channel.
    float stopLong = ta.lowest(20)[1]
    float stopShort = ta.highest(20)[1]
    // ————— Position sizing.
    // Position size is calculated so the trade"s risk equals the user-selected max risk of equity allowed per trade.
    // This way, positions sizes throttle with equity variations, but always incur the same % risk on equity.
    // Note that we are estimating here. We do not yet know the actual fill price because the order will only be executed at the open of the next bar.
    float riskOnEntry = math.abs(c - (enterLong ? stopLong : enterShort ? stopShort : na))
    float positionSize = strategy.equity * maxPctRisk / riskOnEntry
    // ————— Orders to broker emulator.
    // Entries, which may include reversals. Don"t enter on first bars if no stop can be calculated yet.
    strategy.entry("Long", strategy.long, qty = positionSize, comment = "►Long", when = enterLong and not na(stopLong))
    strategy.entry("Short", strategy.short, qty = positionSize, comment = "►Short", when = enterShort and not na(stopShort))
    // Exits. Each successive call modifies the existing order, so the current stop value is always used.
    strategy.exit("◄Long", "Long", stop=stopLong)
    strategy.exit("◄Short", "Short", stop=stopShort)

    // ———————————————————— Custom stat calcs.
    // From this point on, we only rely on changes to `strategy.*` variables to detect the execution of orders.
    // ————— Detection of order fill events.
    bool tradeWasClosed = ta.change(strategy.closedtrades)
    bool tradeWasEntered = ta.change(strategy.opentrades) > 0 or strategy.opentrades > 0 and tradeWasClosed
    bool tradeIsActive = strategy.opentrades != 0
    // ————— Number of trades entered.
    float tradesEntered = ta.cum(tradeWasEntered ? 1 : 0)
    // ————— Percentage of bars we are in a trade.
    float barsInTradePct = 100 * ta.cum(tradeIsActive ? 1 : 0) / bar_index
    // ————— Avg position size.
    float avgPositionSize = ta.cum(nz(positionSize))[1] / tradesEntered
    // ————— Avg entry stop in %.
    float stopPct = riskOnEntry / c
    float avgEntryStopPct = 100 * ta.cum(nz(stopPct)) / tradesEntered
    // ————— Avg distance to stop during trades in %.
    var float[] distancesToStopInPctDuringTrade = array.new_float(0)
    var float[] distancesToStopInPct = array.new_float(0)
    float stop = strategy.position_size > 0 ? stopLong : strategy.position_size < 0 ? stopShort : na
    float distanceToStopInPct = 100 * math.abs(stop - c) / c
    // Keep track of distances to stop during trades.
    if tradeWasEntered
        // Start with an empty array for each trade.
        array.clear(distancesToStopInPctDuringTrade)
        // Add a new distance for each bar in the trade.
    else if tradeIsActive
        array.push(distancesToStopInPctDuringTrade, distanceToStopInPct)
        // At the end of a trade, save the avg distance for that trade in our global values for all trades.
    else if tradeWasClosed
        array.push(distancesToStopInPct, array.avg(distancesToStopInPctDuringTrade))
    // Avg distance for all trades.
    float avgDistancesToStop = array.avg(distancesToStopInPct)

    // ———————————————————— Plots
    // ————— Chart plots.
    plot(maF, "MA Fast")
    plot(maS, "MA Slow", color.new(color.silver, 0))
    plot(stop, "Stop", color.new(color.fuchsia, 0), 1, plot.style_circles)
    bgcolor(strategy.position_size > 0 ? color.new(color.teal, 95) : strategy.position_size < 0 ? color.new(color.maroon, 95) : na)
    // ————— Data Window plots.
    plotchar(na, "════════ Risk", "", location.top, size = size.tiny)
    plotchar(strategy.equity, "Equity", "", location.top, size = size.tiny)
    plotchar(strategy.equity * maxPctRisk, "Max value of equity to risk", "", location.top, size = size.tiny)
    plotchar(riskOnEntry, "Risk On Entry", "", location.top, size = size.tiny)
    plotchar(positionSize, "Position Size", "", location.top, size = size.tiny)
    plotchar(0, "════════ Stats", "", location.top, size = size.tiny)
    plotchar(tradesEntered, "tradesEntered", "", location.top, size = size.tiny)
    plotchar(barsInTradePct, "barsInTradePct", "", location.top, size = size.tiny)
    plotchar(avgPositionSize, "avgPositionSize", "", location.top, size = size.tiny)
    plotchar(avgEntryStopPct, "avgEntryStopPct", "", location.top, size = size.tiny)
    plotchar(avgDistancesToStop, "avgDistancesToStop", "", location.top, size = size.tiny)
    plotchar(na, "════════ Misc.", "", location.top, size = size.tiny)
    plotchar(strategy.opentrades, "strategy.opentrades", "", location.top, size = size.tiny)
    plotchar(strategy.closedtrades, "strategy.closedtrades", "", location.top, size = size.tiny)
    plotchar(strategy.position_size, "strategy.position_size", "", location.top, size = size.tiny)
    plotchar(positionSize, "positionSize", "", location.top, size = size.tiny)
    plotchar(positionSize * close, "Position\"s Value", "", location.top, size = size.tiny)
    plotchar(close, "Estimated entry Price", "", location.top, size = size.tiny)
    p = riskOnEntry / close
    plotchar(p, "p", "", location.top, size = size.tiny)
    plotchar(strategy.equity * maxPctRisk, "strategy.equity * i_maxPctRisk", "", location.top, size = size.tiny)
    r = positionSize * riskOnEntry
    plotchar(r, "r", "", location.top, size = size.tiny)
    plotchar(enterLong, "enterLong", "", location.top, size = size.tiny)
    plotchar(enterShort, "enterShort", "", location.top, size = size.tiny)
    plotchar(tradeWasClosed, "tradeWasClosed", "—", location.bottom, size = size.tiny)
    plotchar(tradeWasEntered, "tradeWasEntered", "+", location.top, size = size.tiny)



How can I backtest deeper into history?
---------------------------------------

The depth of history is measured in bars and not time. The quantity of bars on charts varies with your type of account:

 - 5K bars for Basic accounts.
 - 10K bars for Pro and Pro+ accounts.
 - 20K bars for Premium accounts.

At 20K bars on 1min charts, the depth measured in time will vary with the quantity of 1min bars in the dataset. 
24x7 markets with pretty much all 1min bars present will yield ~17 days of history. Less densely populated 1min charts like GOOGL will yield ~72 days.

You can use this script to test how deep your history reaches:

::

    //@version=5
    indicator("Days of history")
    var begin = time
    days = (time - begin) / (24 * 60 * 60 * 1000)
    plot(days)
    print(text) =>
        var lbl = label.new(bar_index, na, text, xloc.bar_index, yloc.price, color(na), label.style_label_up, color.gray, size.large, text.align_left)
        label.set_xy(lbl, bar_index, days)
        label.set_text(lbl, text)
        
    if barstate.islast
        print(str.tostring(days, "#.0 days\n") + str.tostring(bar_index + 1, "# bars"))



.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/