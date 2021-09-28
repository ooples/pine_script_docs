.. _PagePlots:

Plots
=====

.. contents:: :local:
    :depth: 2



The `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ function
has one mandatory parameter: a value of "series int/float" type, which it displays
as a line. A basic call looks like this:

::

    plot(close)

Pine's automatic type conversions makes it possible to also use
any numeric value as an argument. For example:

::

    plot(125.2)

In this case, the value 125.2 will automatically be converted to a
series type value which will be the same number on every bar. The plot
will be represented as a horizontal line.

The `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__
function has many optional parameters, in particular those which set the line's display style: 
``style``, ``color``, ``linewidth``, and others.

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
