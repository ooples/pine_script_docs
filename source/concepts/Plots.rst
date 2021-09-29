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
