.. _PagePlots:

Plots
=====

.. contents:: :local:
    :depth: 2



Introduction
------------

The `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ 
function can be used to plot lines of different styles, histograms, areas, columns (like volume columns), circles or crosses.
It has the following signature:

.. code-block:: text

    plot(series, title, color, linewidth, style, trackprice, histbase, offset, join, editable, show_last, display) → plot

While the function is usually used to plot values that vary with time, such as in::

    plot(close)

it can also be used to plot horizontal levels, e.g.::

    plot(125.2)

Its parameters are:

``series``
   It is the only mandatory parameter. Its argument must be of "series int/float" type.

``title``
   XXX

``color``
   XXX

``linewidth``
   XXX

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


Plot styles
-----------



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


Offsets
-------

The ``offset`` parameter specifies the shift used when the line is plotted
(negative values shift to the left while positive values shift to
the right). For example::

    //@version=5
    indicator("My Script 12", overlay = true)
    plot(close, color = color.red, offset = -5)
    plot(close, color = color.lime, offset = 5)

.. image:: images/Plot-03.png


As can be seen in the screenshot, the *red* series has been shifted to the
left (since the argument's value is negative), while the *green*
series has been shifted to the right (its value is positive).


Scale
-----

Not all values can be plotted everywhere. 
Your scripts visual space is always bound by upper and lower limits that are dynamically adjusted with the values plotted.
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