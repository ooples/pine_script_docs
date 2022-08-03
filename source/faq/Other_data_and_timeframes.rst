.. image:: /images/Pine_Script_logo.svg
   :alt: Pine Script™ logo
   :target: https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html
   :align: right
   :width: 100
   :height: 100


.. _PageOtherTimeframesFaq:


Other timeframes (MTF) FAQ
==========================


.. contents:: :local:
    :depth: 3


How can I convert the current resolution into a numeric format?
---------------------------------------------------------------

Use the ``resInMinutes()`` function from the PineCoders MTF Selection Framework to convert the chart’s current resolution into minutes of type float. 
From there you will be able to manipulate it using the other PineCoders MTF functions.

::

    //@version=5
    indicator("Current res in float minutes", "", true)

    // ————— Converts current chart timeframe into a float minutes value.
    resInMinutes() =>
        result = timeframe.multiplier * (timeframe.isseconds ? 1. / 60 : timeframe.isminutes ? 1. : timeframe.isdaily ? 60. * 24 : timeframe.isweekly ? 60. * 24 * 7 : timeframe.ismonthly ? 60. * 24 * 30.4375 : na)

    htfLabel(txt, y, lblColor, offsetLabels) =>
        t = int(time + resInMinutes() * offsetLabels * 60000)
        var lbl = label.new(t, y, txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large)
        if barstate.islast
            label.set_xy(lbl, t, y)
            label.set_text(lbl, txt)
            label.set_textcolor(lbl, lblColor)

    // ————— Plot label.
    htfLabel(str.tostring(resInMinutes(), "Current res in minutes (float): #.0000"), ta.sma(high + 3 * ta.tr, 10)[1], color.gray, 3)



How can I convert a resolution in float minutes into a string usable with security()?
-------------------------------------------------------------------------------------

Use the ``resFromMinutes()`` function from the PineCoders MTF Selection Framework.

::

    //@version=5
    indicator("Target res in string from float minutes", "", true)
    res = input.float(1440., "Minutes in target resolution (<= 0.0167 [1 sec.])", minval = 0.0167)
    repaint = input(false, "Repainting")

    // ————— Converts current "timeframe.multiplier" plus the TF into minutes of type float.
    resToMinutes() =>
        result = timeframe.multiplier * (timeframe.isseconds ? 1. / 60. : timeframe.isminutes ? 1. : timeframe.isdaily ? 1440. : timeframe.isweekly ? 10080. : timeframe.ismonthly ? 43800. : na)

    // Converts a resolution expressed in minutes into a string usable by "security()"
    resFromMinutes(minutes) =>
        minutes <= 0.0167 ? "1S" : 
        minutes <= 0.0834 ? "5S" : 
        minutes <= 0.2500 ? "15S" : 
        minutes <= 0.5000 ? "30S" : 
        minutes <= 1440 ? str.tostring(math.round(minutes)) : 
        minutes <= 43800 ? str.tostring(math.round(math.min(minutes / 1440, 365))) + "D" : 
        str.tostring(math.round(math.min(minutes / 43800, 12))) + "M"

    htfLabel(txt, y, lblColor, offsetLabels) =>
        t = int(time + resToMinutes() * offsetLabels * 60000)
        var lbl = label.new(t, y, txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large)
        if barstate.islast
            label.set_xy(lbl, t, y)
            label.set_text(lbl, txt)
            label.set_textcolor(lbl, lblColor)

    // ————— Convert target res in minutes from input into string.
    targetResInString = resFromMinutes(res)
    // ————— Fetch target resolution"s open in repainting/no-repainting mode.
    // This technique has the advantage of using only one "security()" to achieve a repainting/no-repainting choice.
    idx = repaint ? 1 : 0
    indexHighTf = barstate.isrealtime ? 1 - idx : 0
    indexCurrTf = barstate.isrealtime ? 0 : 1 - idx
    targetResOpen = request.security(syminfo.tickerid, targetResInString, open[indexHighTf])[indexCurrTf]

    // ————— Plot target res open.
    plot(targetResOpen)
    // ————— Plot label.
    htfLabel(str.format("\nTarget res (string): {0}", targetResInString), ta.sma(high + 3 * ta.tr, 10)[1], color.gray, 3)



How do I define a higher interval that is a multiple of the current one?
------------------------------------------------------------------------

Use the ``multipleOfRes()`` function from the PineCoders MTF Selection Framework.

::

    //@version=5
    //@author=LucF, for PineCoders
    indicator("Multiple of current TF")

    resMult = input.int(4, minval=1)

    // Returns a multiple of current TF as a string usable with "security()".
    multipleOfRes(res, mult) =>
        // res:  current resolution in minutes, in the fractional format supplied by f_resInMinutes() companion function.
        // mult: Multiple of current TF to be calculated.
        // Convert current float TF in minutes to target string TF in "timeframe.period" format.
        targetResInMin = res * math.max(mult, 1)
        // Find best string to express the resolution.
        targetResInMin <= 0.083 ? "5S" : 
        targetResInMin <= 0.251 ? "15S" : 
        targetResInMin <= 0.501 ? "30S" : 
        targetResInMin <= 1440 ? str.tostring(math.round(targetResInMin)) : 
        targetResInMin <= 43800 ? str.tostring(math.round(math.min(targetResInMin / 1440, 365))) + "D" : 
        str.tostring(math.round(math.min(targetResInMin / 43800, 12))) + "M"

    // ————— Converts current "timeframe.multiplier" plus the TF into minutes of type float.
    resInMinutes() =>
        resInMinutes = timeframe.multiplier * (timeframe.isseconds ? 1. / 60. : timeframe.isminutes ? 1. : timeframe.isdaily ? 1440. : timeframe.isweekly ? 10080. : timeframe.ismonthly ? 43800. : na)

    htfLabel(txt, y, lblColor, offsetLabels) =>
        t = int(time + resInMinutes() * offsetLabels * 60000)
        var lbl = label.new(t, y, txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large)
        if barstate.islast
            label.set_xy(lbl, t, y)
            label.set_text(lbl, txt)
            label.set_textcolor(lbl, lblColor)

    // Get multiple of current resolution.
    targetRes = multipleOfRes(resInMinutes(), resMult)
    // Create local rsi.
    myRsi = ta.rsi(close, 14)
    plot(myRsi, color = color.new(color.silver, 0))
    // No repainting HTF rsi.
    myRsiHtf1 = request.security(syminfo.tickerid, targetRes, myRsi[1], lookahead = barmerge.lookahead_on)
    plot(myRsiHtf1, color = color.new(color.green, 0))
    // Repainting HTF rsi
    myRsiHtf2 = request.security(syminfo.tickerid, targetRes, myRsi)
    plot(myRsiHtf2, color = color.new(color.red, 0))

    // ————— Plot label.
    htfLabel(str.format("\nTarget res (string): {0}", targetRes), ta.sma(myRsiHtf1, 10)[1], color.gray, 3)



Is it possible to use security() on lower timeframes than the chart’s current timeframe?
----------------------------------------------------------------------------------------

Yes it is possible, but only by using the `request.security_lower_tf() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security_lower_tf>`__ function. 



Why do HTF plots appear smoothed when using the resolution parameter with an indicator() script?
------------------------------------------------------------------------------------------------

Because gaps are used. See `this answer <https://www.tradingview.com/chart/TLT/gfhcvho3-How-to-Use-Multi-Timeframe-Analysis-and-What-It-Means/#tc4114362>`__ 
to a question on TradingView’s 
`How to Use Multi-Timeframe Analysis and What It Means <https://www.tradingview.com/chart/TLT/gfhcvho3-How-to-Use-Multi-Timeframe-Analysis-and-What-It-Means/>`__ 
publication for more details.



Why do intraday OHLCV values not correspond to values retrieved with security() at daily timeframes and higher?
---------------------------------------------------------------------------------------------------------------

Some exchanges/brokers provide distinct data feeds for intraday and daily charts, and the data from both feeds will sometimes differ.



How can I fetch the ATR value from a higher timeframe?
------------------------------------------------------

This will display a non-repainting ATR value formatted with the symbol’s tick precision and using the timeframe specified in the inputs:

::

    //@version=5
    indicator("ATR", "", true)
    string tf = input.timeframe("", "Timeframe")
    security(sym, res, src, rep) =>
        request.security(sym, res, src[not rep and barstate.isrealtime ? 1 : 0])[rep or barstate.isrealtime ? 0 : 1]
    print(txt) =>
        var lbl = label.new(bar_index, na, txt, xloc.bar_index, yloc.price, color(na), label.style_none, color.gray, size.large, text.align_left)
        label.set_xy(lbl, bar_index, ta.highest(10)[1])
        label.set_text(lbl, txt)
    tickFormat() =>
        result = str.tostring(syminfo.mintick)
        result := str.replace_all(result, "25", "00")
        result := str.replace_all(result, "5", "0")
        result := str.replace_all(result, "1", "0")

    float myAtr = ta.atr(20)
    float atrHtf = security(syminfo.tickerid, tf, myAtr, false)
    print(str.tostring(atrHtf, tickFormat()))



How can I plot a moving average only when the chart’s timeframe is 1D or higher?
--------------------------------------------------------------------------------

We use ``chartTfIntoMinutes() >= 1440`` in here to test if the chart’s timeframe is ``1D`` (1440 minutes) or greater. 
Our ``chartTfIntoMinutes()`` converts the chart’s timeframe into minutes:

::

    //@version=5
    indicator("", "", true)
    ma = ta.sma(close, 200)
    // ————— Converts current chart timeframe into a float minutes value.
    chartTfIntoMinutes() =>
        float result = timeframe.multiplier * (timeframe.isseconds ? 1. / 60 : timeframe.isminutes ? 1. : timeframe.isdaily ? 60. * 24 : timeframe.isweekly ? 60. * 24 * 7 : timeframe.ismonthly ? 60. * 24 * 30.4375 : na)

    // Detect if chart TF is >= 1D
    var bool plotMa = chartTfInMinutes() >= 1440
    plot(plotMa ? ma : na)



How can I plot a moving average calculated using the 1H timeframe on any chart?
-------------------------------------------------------------------------------

Here we plot the ``MA200`` calculated at the ``1H`` timeframe, but only when the chart’s timeframe is lower or equal to ``1H``, 
otherwise it doesn’t make sense to calculate a moving average on a lower timeframe than the chart’s:

::

    //@version=5
    indicator("", "", true)
    ma = ta.sma(close, 200)
    // ————— Converts current chart timeframe into a float minutes value.
    chartTfInMinutes() =>
        float result = timeframe.multiplier * (timeframe.isseconds ? 1. / 60 : timeframe.isminutes ? 1. : timeframe.isdaily ? 60. * 24 : timeframe.isweekly ? 60. * 24 * 7 : timeframe.ismonthly ? 60. * 24 * 30.4375 : na)
        result

    // ————— Provides non-repainting access to `request.security()`.
    nonRepaintSecurity(sym, res, src, rep) =>
        request.security(sym, res, src[not rep and barstate.isrealtime ? 1 : 0])[rep or barstate.isrealtime ? 0 : 1]

    // ————— Prints a message in the lower-right of the chart.
    print(txt) =>
        var table t = table.new(position.bottom_right, 1, 1)
        table.cell(t, 0, 0, txt, bgcolor = color.red)

    // Detect is chart"s timeframe is <= 60 minutes because we don"t plot the MA then.
    var bool plotMa = chartTfInMinutes() <= 60
    if not plotMa
        print("The MA is not displayed when the chart\"s timeframe is > 60 minutes.")

    ma1H = nonRepaintSecurity(syminfo.tickerid, "60", ma, false)
    plot(plotMa ? ma1H : na)

If you are OK with your script doing only that, this is a simpler method of achieving more or less the same result, without the bells and whistles of the previous example:

::

    //@version=5
    indicator("", "", true, timeframe = "60")
    ma = ta.sma(close, 200)
    plot(ma)




.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/