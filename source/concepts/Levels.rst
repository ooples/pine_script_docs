.. _PageLevels:

Levels
======

.. contents:: :local:
    :depth: 2


\`hline()\` levels
------------------

Levels are lines plotted using the 
`hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__ function.


The function has the following signature:

.. code-block:: text

    hline(price, title, color, linestyle, linewidth, editable) → hline

The function has a few constraints when compared to 
`plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__:

- Its ``price`` parameter requires an "input int/float" argument,
  which means that "series float" values such as `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
  or variables calculated dynamically cannot be used.


Let's see `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__
in action in the True Strength Index indicator::

    //@version=5
    indicator("TSI")
    myTSI = 100 * ta.tsi(close, 25, 13)
    
    hline( 50, "+50",  color.lime)
    hline( 25, "+25",  color.green)
    hline(  0, "Zero", color.gray, linestyle = hline.style_dotted)
    hline(-25, "-25",  color.maroon)
    hline(-50, "-50",  color.red)
    
    plot(myTSI)

Note that:

- We display 5 levels, each of a different color.
- We use a different line style for the zero centerline.
- We choose colors that will work well on both light and dark themes.
- The usual range for the indicator's values is +100 to -100.
  Since the `ta.tsi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}tsi>`__
  built-in returns values in the +1 to -1 range, we make the adjustment in our code.



Price levels with \`hline()\`
-----------------------------

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



Fills between levels
--------------------

The space between two levels plotted with `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__
can be colored using `fill() <https://www.tradingview.com/pine-script-reference/v5/#fun_fill>`__.
Keep in mind that **both** plots must have been plotted with
`hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__.



