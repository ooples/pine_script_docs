.. _PagePlots:

Plots
=====

.. contents:: :local:
    :depth: 2



Introduction
------------

The `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ 
function can be used to plot different styles of lines, histograms, areas, columns (like volume columns), fills, circles or crosses.
It has the following signature:

.. code-block:: text

    plot(series, title, color, linewidth, style, trackprice, histbase, offset, join, editable, show_last, display) → plot

This script showcases a few different uses of `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__
in an overlay script:

.. image:: images/Plots-Introduction-01.png

::
    //@version=5
    indicator("`plot()`", "", true)
    plot(high, "Blue `high` line")
    plot(math.avg(close, open), "Crosses in body center", close > open ? color.lime : color.purple, 6, plot.style_cross)
    plot(math.min(open, close), "Navy step line on body low point", color.navy, 3, plot.style_stepline)
    plot(low, "Gray dot on `low`", color.gray, 3, plot.style_circles)
    
    color VIOLET = #AA00FF
    color GOLD   = #CCCC00
    ma = ta.alma(hl2, 40, 0.85, 6)
    var almaColor = color.silver
    almaColor := ma > ma[2] ? GOLD : ma < ma[2]  ? VIOLET : almaColor
    plot(ma, "Two-color ALMA", almaColor, 2)

Note that:

- The first `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ call plots a 1-pixel blue line across the bar highs.
- The secong plots crosses at the mid-point of bodies. The crosses are colored lime when the bar is up and purple when it is down.
  The argument used for ``linewidth`` is ``6`` but it is not a pixel value; just a relative size.
- The third call plots a 3-pixel wide step line following the low point of bodies.
- The fourth call plot a gray circle at the bars' `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__.
- The last plot requires more setup. We first define our bull/bear colors, 
  we then calculate an `Arnaud Legoux Moving Average <https://www.tradingview.com/u/?solution=43000594683>`__.
  Then we make our color calculations. We initialize our color variable on bar zero only, using `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__.
  We initialize it to `color.silver <https://www.tradingview.com/pine-script-reference/v5/#var_color{dot}silver>`__, 
  so on the dataset's first bars, until one of our conditions causes the color to change, the line will be silver.
  The conditions that change the color of the line require it to be higher/lower than its value two bars ago.
  This makes for less noisy color transitions than if we merely looked for a higher/lower value than the previous one.

This script shows other uses of `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ in a pane::

    //@version=5
    indicator("Volume change", format = format.volume)
    
    color GREEN         = #008000
    color GREEN_LIGHT   = color.new(GREEN, 50)
    color GREEN_LIGHTER = color.new(GREEN, 85)
    color PINK          = #FF0080
    color PINK_LIGHT    = color.new(PINK, 50)
    color PINK_LIGHTER  = color.new(PINK, 90)
    
    bool  barUp = ta.rising(close, 1)
    bool  barDn = ta.falling(close, 1)
    float volumeChange = ta.change(volume)
    
    volumeColor = barUp ? GREEN_LIGHTER : barDn ? PINK_LIGHTER : color.gray
    plot(volume, "Volume columns", volumeColor, style = plot.style_columns)
    
    volumeChangeColor = barUp ? volumeChange > 0 ? GREEN : GREEN_LIGHT : volumeChange > 0 ? PINK : PINK_LIGHT
    plot(volumeChange, "Volume change columns", volumeChangeColor, 12, plot.style_histogram)
    
    plot(0, "Zero line", color.gray)

.. image:: images/Plots-Introduction-02.png

Note that:

- We are plotting normal `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__ 
  values as wide columns above the zero line 
  (see the ``style = plot.style_columns`` in our `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ call).
- Before plotting the columns we calculate our ``volumeColor`` by using the values of the ``barUp`` and ``barDn`` boolean variables.
  They become respectively ``true`` when the current bar's `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ 
  is higher/lower than the previous one. Note that the "Volume" built-in does not use the same condition; it identifies an up bar with ``close > open``.
  We use the ``GREEN_LIGHTER`` and ``PINK_LIGHTER`` colors for the volume columns.
- Because the first plot plots columns, we do not use the ``linewidth`` parameter, as it has no effect on columns.
- Our script's second plot is the **change** in volume, which we have calculated earlier using ``ta.change(volume)``.
  This value is plotted as a histogram, for which the ``linewidth`` parameter controls the width of the column.
  We make this width ``12`` so that histogram elements are thinner than the columns of the first plot.
  Positive/negative ``volumeChange`` values plot above/below the zero line; no manipulation is required to achieve this effect.
- Before plotting the histogram of ``volumeChange`` values, we calculate its color value, which can be one of four different colors.
  We use the bright ``GREEN`` or ``PINK`` colors when the bar is up/down AND the volume has increased since the last bar (``volumeChange > 0``).
  Because ``volumeChange`` is positive in this case, the histogram's element will be plotted above the zero line.
  We use the bright ``GREEN_LIGHT`` or ``PINK_LIGHT`` colors when the bar is up/down AND the volume has NOT increased since the last bar.
  Because ``volumeChange`` is negative in this case, the histogram's element will be plotted below the zero line.
- Finally, we plot a zero line. We could just as well have used ``hline(0)`` there.
- We use ``format = format.volume`` in our `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__ call
  so that large values displayed for this script are abbreviated like those of the built-in "Volume" indicator.

`plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ 
calls must always be placed in a line's first position, which entails they are always in the script's global scope.
They cannot be placed in user-defined functions or structures like `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__,
`for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__, etc. 
Calls to `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ **can**, however, 
be designed to plot conditionally in two ways, which we cover in the :ref:`Conditional plots <PagePlots_ConditionalPlots>`
section of this page.

A script can only plot in its own visual space, whether it is in a pane or on the chart as an overlay.
Scripts running in a pane can only :ref:`color bars <PageBarColoring>` in the chart area.

The parameters of `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ are:

``series``
   It is the only mandatory parameter. Its argument must be of "series int/float" type.
   Note that because the auto-casting rules in Pine convert in the int 🠆 float 🠆 bool direction,
   a "bool" type variable cannot be used as is; it must be converted to an "int" or a "float" for use as an argument.
   For example, if ``newDay`` is of "bool" type, 
   then ``newDay ? 1 : 0`` can be used to plot 1 when the variable is ``true``, and zero when it is ``false``.

``title``
   Requires a "const string" argument, so it must be known at compile time.
   The string appears:

   - In the script's scale when the "Chart settings/Scales/Indicator Name Label" field is checked.
   - In the Data Window.
   - In the "Settings/Style" tab.
   - In the dropdown of `input.source() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}source>`__ fields.
   - In the "Condition" field of the "Create Alert" dialog box, when the script is selected.
   - As the column header when exporting chart data to a CSV file.

``color``
   Accepts "series color", so can be calculated on the fly, bar by bar.
   Plotting with `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__
   as the color, or any color with a transparency of 100, is one way to hide plots when they are not needed.

``linewidth``
   Is the plotted element's size, but it does not apply to all styles. When a line is plotted, the unit is pixels.
   It has no impact when ``plot.style_columns`` is used.

``style``
   XXX

``trackprice``
   XXX

``histbase``
   XXX

``offset``
   XXX

``join``
   XXX

``editable``
   XXX

``show_last``
   XXX

``display``
   XXX


While the function is usually used to plot values that vary with time, such as in::

    plot(close)

it can also be used to plot horizontal levels, e.g.::

    plot(125.2)



Plot styles
-----------

Lines
^^^^^



.. _PagePlots_ConditionalPlots:

Conditional plots
-----------------

The value of the ``color`` parameter can be defined in different ways.
If it is a color constant, for example ``color.red``, then the whole line will be plotted using a *red* color::

    plot(close, color = color.red)

.. image:: images/Plot-01.png
The value of ``color`` can also be an expression of a *series*
type of color values. This series of colors will be used to
color the rendered line. For example::

    plotColor = close >= open ? color.lime : color.red
    plot(close, color = plotColor)

.. image:: images/Plot-02.png


Fills
-----




Offsets
-------

The ``offset`` parameter specifies the shift used when the line is plotted
(negative values shift in the past, positive values shift into the future.
For example::

    //@version=5
    indicator("", "", true)
    plot(close, color = color.red, offset = -5)
    plot(close, color = color.lime, offset = 5)

.. image:: images/Plots-Offsets-01.png

As can be seen in the screenshot, the *red* series has been shifted to the
left (since the argument's value is negative), while the *green*
series has been shifted to the right (its value is positive).

..
   Note that the ``offset`` parameter requires a "simple int" argument,
   which means it cannot change during the script's execution.



Limitations
-----------

Each script is limited to a maximum plot count of 64.
All ``plot*()`` calls and `alertcondition() <https://www.tradingview.com/pine-script-reference/v5/#func_alertcondition>`__ calls
count in the plot count of a script. Some types of calls count for more than one in the total plot count.

`plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ 
calls count for one in the total plot count if they use a "const color" argument for the ``color`` parameter, 
which means it is known at compile time, e.g.::

    plot(close, color = color.green)

When they use another form, such as any one of these, they will count for two in the total plot count::

    plot(close, color = syminfo.mintick > 0.0001 ? color.green : color.red) //🠆 "simple color"
    plot(close, color = input.color(color.purple)) //🠆 "input color"
    plot(close, color = close > open ? color.green : color.red) //🠆 "series color"
    plot(close, color = color.new(color.silver, close > open ? 40 : 0)) //🠆 "series color"



Scale
-----

Not all values can be plotted everywhere. 
Your script's visual space is always bound by upper and lower limits that are dynamically adjusted with the values plotted.
An `RSI <https://www.tradingview.com/u/?solution=43000502338>`__ indicator will plot values between 0 and 100, 
which is why it is usually displayed in a distinct *pane* — or area — above or below the chart.
If `RSI <https://www.tradingview.com/u/?solution=43000502338>`__ values were plotted as an overlay on the chart, 
the effect would be to distort the symbol's normal price scale, 
unless it just hapenned to be close to `RSI <https://www.tradingview.com/u/?solution=43000502338>`__'s 0 to 100 range.
This shows an `RSI <https://www.tradingview.com/u/?solution=43000502338>`__ signal line and a centerline at the 50 level, 
with the script running in a separate pane::

    //@version=5
    indicator("RSI")
    myRSI = ta.rsi(close, 20)
    bullColor = color.from_gradient(myRSI, 50, 80, color.new(color.lime, 70), color.new(color.lime, 0))
    bearColor = color.from_gradient(myRSI, 20, 50, color.new(color.red,   0), color.new(color.red, 70))
    myRSIColor = myRSI > 50 ? bullColor : bearColor
    plot(myRSI, "RSI", myRSIColor, 3)
    hline(50)

.. image:: images/Plots-Scale-01.png

Note that the *y* axis of our script's visual space is automatically sized using the range of values plotted, i.e., 
the values of `RSI <https://www.tradingview.com/u/?solution=43000502338>`__. 
See the page on :ref:`Colors <PageColors>` for more information on the 
`color.from_gradient() <https://www.tradingview.com/pine-script-reference/v5/#fun_color{dot}from_gradient>`__ function used in the script.

If we try to plot the symbol's 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ 
values in the same space by adding the following line to our script::

    plot(close)

This is what happens:

.. image:: images/Plots-Scale-02.png

The chart is on the BTCUSD symbol, whose `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
prices are around 40000 during this period. Plotting values in the 40000 range makes our `RSI <https://www.tradingview.com/u/?solution=43000502338>`__ plots in the 0 to 100 range indiscernible.
The same distorted plots would occur if we placed the `RSI <https://www.tradingview.com/u/?solution=43000502338>`__ indicator on the chart as an overlay.



Merging two indicators
^^^^^^^^^^^^^^^^^^^^^^^

If you are planning to merge two signals in one, first consider the scale of each.
It is impossible, for example, to correctly plot an 
`RSI <https://www.tradingview.com/u/?solution=43000502338>`__ and 
a `MACD <https://www.tradingview.com/u/?solution=43000502344>`__ 
in the same script's visual space because `RSI <https://www.tradingview.com/u/?solution=43000502338>`__
has a fixed range (0 to 100) while `MACD <https://www.tradingview.com/u/?solution=43000502344>`__ doesn't, as it plots moving averages calculated on price.

If both your indicators used fixed ranges, you can shift the values of one of them so they do not overlap.
We could, for example, plot both `RSI <https://www.tradingview.com/u/?solution=43000502338>`__ (0 to 100)
and the `True Strength Indicator (TSI) <https://www.tradingview.com/u/?solution=43000592290>`__ (-100 to +100) by displacing one of them.
Our strategy here will be to compress and shift the `TSI <https://www.tradingview.com/u/?solution=43000592290>`__ values
so they plot over `RSI <https://www.tradingview.com/u/?solution=43000502338>`__::

    //@version=5
    indicator("RSI and TSI")
    myRSI = ta.rsi(close, 20)
    bullColor = color.from_gradient(myRSI, 50, 80, color.new(color.lime, 70), color.new(color.lime, 0))
    bearColor = color.from_gradient(myRSI, 20, 50, color.new(color.red,   0), color.new(color.red, 70))
    myRSIColor = myRSI > 50 ? bullColor : bearColor
    plot(myRSI, "RSI", myRSIColor, 3)
    hline(100)
    hline(50)
    hline(0)
    
    // 1. Compress TSI's range from -100/100 to -50/50.
    // 2. Shift it higher by 150, so its -50 min value becomes 100.
    myTSI = 150 + (100 * ta.tsi(close, 13, 25) / 2)
    plot(myTSI, "TSI", color.blue, 2)
    plot(ta.ema(myTSI, 13), "TSI EMA", #FF006E)
    hline(200)
    hline(150)

.. image:: images/Plots-Scale-03.png

Note that:

- We have added levels using `hline <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__
  to situate both signals.
- In order for both signal lines to oscillate on the same range of 100,
  we divide the `TSI <https://www.tradingview.com/u/?solution=43000592290>`__ value by 2 because it has a 200 range (-100 to +100).
  We then shift this value up by 150 so it oscillates between 100 and 200, making 150 its centerline.
- The manipulations we make here are typical of the compromises required to bring two indicators
  with different scales in the same visual space, even when their values, contrary to 
  `MACD <https://www.tradingview.com/u/?solution=43000502344>`__, are bounded in a fixed range.