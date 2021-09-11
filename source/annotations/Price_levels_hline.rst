Price levels, hline
-------------------

The `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__
annotation function renders a horizontal line at a given level. For example::

    //@version=5
    indicator("Chaikin Oscillator", "Chaikin Osc")
    shortInput = input.int(3, minval = 1)
    longInput = input.int(10, minval = 1)
    osc = ta.ema(ta.accdist, shortInput) - ta.ema(ta.accdist, longInput)
    plot(osc, color = color.red)
    hline(0, "Zero", color.gray, hline.style_dashed)

.. image:: images/Price_levels_hline_1.png


A *number* must be the first argument of ``hline``. Values of *series* form
are forbidden. It's possible to create a few horizontal lines with the
help of ``hline`` and fill the background between them with a
translucent color using `fill() <https://www.tradingview.com/pine-script-reference/v5/#fun_fill>`__.
