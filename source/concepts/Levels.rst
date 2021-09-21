.. _PageLevels:

Levels
======

.. contents:: :local:
    :depth: 2


\`hline()\` levels
------------------

Levels are lines plotted using the 
`hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__ function.
It is designed to plot straigth, horizontal levels using a color that does not change on different bars.

The function has the following signature:

.. code-block:: text

    hline(price, title, color, linestyle, linewidth, editable) → hline

`hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__
has a few constraints when compared to 
`plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__:

- Its ``price`` parameter requires an "input int/float" argument,
  which means that "series float" values such as `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
  or dynamically-calculated values cannot be used.
- Its ``color`` parameter requires an "input int" argument,
  which precludes the use of dynamic colors, i.e., colors calculated on each bar — or "series color" values.
- Three different line styles are supported through the ``linestyle`` parameter:
  ``hline.style_solid``, ``hline.style_dotted`` and ``hline.style_dashed``.

Let's see `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__
in action in the "True Strength Index" indicator::

    //@version=5
    indicator("TSI")
    myTSI = 100 * ta.tsi(close, 25, 13)
    
    hline( 50, "+50",  color.lime)
    hline( 25, "+25",  color.green)
    hline(  0, "Zero", color.gray, linestyle = hline.style_dotted)
    hline(-25, "-25",  color.maroon)
    hline(-50, "-50",  color.red)
    
    plot(myTSI)

.. image:: images/Levels-HlineLevels-01.png

.. image:: images/Levels-HlineLevels-02.png

Note that:

- We display 5 levels, each of a different color.
- We use a different line style for the zero centerline.
- We choose colors that will work well on both light and dark themes.
- The usual range for the indicator's values is +100 to -100.
  Since the `ta.tsi() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}tsi>`__
  built-in returns values in the +1 to -1 range, we make the adjustment in our code.



Fills between levels
--------------------

The space between two levels plotted with `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__
can be colored using `fill() <https://www.tradingview.com/pine-script-reference/v5/#fun_fill>`__.
Keep in mind that **both** plots must have been plotted with
`hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__.



