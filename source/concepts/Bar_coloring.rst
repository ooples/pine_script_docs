.. _PageBarColoring:

Bar coloring
============

The `barcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_barcolor>`__ function lets you color chart bars.
It is the only Pine function that will work, whether your script is running in a pane or in overlay mode (``overlay = true``).

The function signature is::

    barcolor(color, offset, editable, show_last, title) → void

The coloring can be conditional because its ``color`` parameter accepts "series color" arguments.

The following script renders *inside* and *outside* bars in different colors::

    //@version=5
    indicator("barcolor example", overlay = true)
    isUp = close > open
    isDown = close <= open
    isOutsideUp = high > high[1] and low < low[1] and isUp
    isOutsideDown = high > high[1] and low < low[1] and isDown
    isInside = high < high[1] and low > low[1]
    barcolor(isInside ? color.yellow : isOutsideUp ? color.aqua : isOutsideDown ? color.purple : na)

.. image:: images/BarColoring-1.png

Note that:

- The `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ value leaves bars as is.
- In the `barcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_barcolor>`__ call,
  we use embedded `?: <https://www.tradingview.com/pine-script-reference/v5/#op_{question}{colon}>`__
  ternary operator expressions to select the color.


