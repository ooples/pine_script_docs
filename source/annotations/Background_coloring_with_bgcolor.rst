
Background coloring with \`bgcolor()\`
--------------------------------------

The `bgcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_bgcolor>`__
function changes the color of the script's background. If the script is running in ``overlay = true`` mode, then it will color the chart's background.
The color used in `bgcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_bgcolor>`__ can be calculated in
an expression, and the `color.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_color{dot}new>`__ 
function can be used to specify the color's transparency.

Here is a script that colors the background of trading sessions (try it on
30min EURUSD, for example)::

    //@version=5
    indicator("bgcolor example", overlay = true)
    timeInRange(res, sess) => time(res, sess) != 0
    PREMARKET_COLOR  = #0050FF
    REGULAR_COLOR    = #0000FF
    POSTMARKET_COLOR = #5000FF
    NOTRADING_COLOR  = color(na)
    sessionColor = timeInRange("30", "0400-0930") ? PREMARKET_COLOR :
      timeInRange("30", "0930-1600") ? REGULAR_COLOR :
      timeInRange("30", "1600-2000") ? POSTMARKET_COLOR : NOTRADING_COLOR
    bgcolor(color.new(sessionColor, 75))

.. image:: images/Background_coloring_bgcolor_1.png






