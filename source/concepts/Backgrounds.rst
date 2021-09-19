.. _PageBackgrounds:

Backgrounds
===========

.. contents:: :local:
    :depth: 2


The `bgcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_bgcolor>`__
function changes the color of the script's background. If the script is running in ``overlay = true`` mode, then it will color the chart's background.

The function's signature is::

    bgcolor(color, offset, editable, show_last, title) → void

Its ``color`` parameter allows a "series color" to be used for its argument,
so it can be dynamically calculated in an expression.
If the correct transparency is not part of the color to be used, 
it can be be generated using the `color.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_color{dot}new>`__ function.

Here is a script that colors the background of trading sessions (try it on
30min EURUSD, for example)::

    //@version=5
    indicator("Session backgrounds", overlay = true)
    
    // Default color constants using tranparency of 25.
    BLUE_COLOR   = #0050FF40
    PURPLE_COLOR = #0000FF40
    PINK_COLOR   = #5000FF40
    NO_COLOR     = color(na)
    
    // Allow user to change the colors.
    preMarketColor  = input.color(BLUE_COLOR, "Pre-market")
    regSessionColor = input.color(PURPLE_COLOR, "Pre-market")
    postMarketColor = input.color(PINK_COLOR, "Pre-market")
    
    // Function returns `true` when the bar's time is 
    timeInRange(tf, session) => 
        time(tf, session) != 0
    
    // Function prints a message at the bottom-right of the chart.
    f_print(_text) => 
        var table _t = table.new(position.bottom_right, 1, 1)
        table.cell(_t, 0, 0, _text, bgcolor = color.yellow)
    
    var chartIs30MinOrLess = timeframe.isseconds or (timeframe.isintraday and timeframe.multiplier <=30)
    sessionColor = if chartIs30MinOrLess
        switch
            timeInRange(timeframe.period, "0400-0930") => preMarketColor
            timeInRange(timeframe.period, "0930-1600") => regSessionColor
            timeInRange(timeframe.period, "1600-2000") => postMarketColor
            => NO_COLOR
    else
        f_print("No background is displayed.\nChart timeframe must be <= 30min.")
        NO_COLOR
    
    bgcolor(sessionColor)

.. image:: images/Backgrounds-Sessions.png


See the :ref:`Colors <PageColors>` page for more examples of backgrounds.
