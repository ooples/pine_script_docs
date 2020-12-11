Debugging
=========

.. contents:: :local:
    :depth: 2



Introduction
------------

TradingView's close integration between the Pine Editor and charts allows for efficient and interactive debugging of Pine code. 
Once a Pine programmer understands the most appropriate technique to debug each type of situation, he will be able to debug quickly and thoroughly. 
This page demonstrates the most useful techniques to debug Pine code.

If you are not yet familiar with Pine's execution model, it is important that you read the :doc:`/language/Execution_model` page of this User Manual 
so you understand how your debugging code will behave in the Pine environment.



The lay of the land
-------------------

Values plotted by Pine scripts can be displayed in four distinct places:

#. Next to the script's name (controlled by the *Indicator Values* checkbox in the *Chart settings/Status Line* tab).
#. In the script's pane, whether your script is an overlay on the chart or in a separate pane.
#. In the scale (only displays the last bar's value and is controlled by the *Indicator Last Value Label* in the *Chart settings/Scale* tab).
#. In the Data Window (which you can bring up using the fourth icon down to the right of your chart).

.. image:: images/Debugging-TheLayOfTheLand-1.png

Note the following in the preceding screenshot:

- The chart's cursor is on the dataset's first bar, where ``bar_index`` is zero. That value is reflected next to the indicator's name and in the Data Window. 
  **Moving your cursor on other bars would update those values so they always represent the value of the plot on that bar.** 
  This is a good way to inspect the value of a variable as the script's execution progresses from bar to bar.
- The ``title`` argument of our `plot() <https://www.tradingview.com/pine-script-reference/v4/#fun_plot>`__ call, "Bar Index", is used as the value's legend in the Data Window.
- The precision of the values displayed in the Data Window is dependent on the chart symbol's tick value. You can modify it in two ways:
 
  - By changing the value of the *Precision* field in the script's *Settings/Style* tab. You can obtain up to eight digits of precision using this method.

  - By using the ``precision`` parameter in your script's `study() <https://www.tradingview.com/pine-script-reference/v4/#fun_study>`__ or `strategy() <https://www.tradingview.com/pine-script-reference/v4/#fun_strategy>`__ declaration statement. This method allows specifying up to 16 digits precision.

- The `plot() <https://www.tradingview.com/pine-script-reference/v4/#fun_plot>`__ call in our script plots the value of ``bar_index`` in the indicator's pane, 
  which shows the increasing value of the variable.
- The scale of the script's pane is automatically sized to accommodate the smallest and largest values plotted by all ``plot()`` calls in the script.


Displaying numeric values
-------------------------

When the script's scale is unimportant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The script in the preceding screenshot used the simplest way to inspect numerical values: a ``plot()`` call, 
which plots a line corresponding to the variable's value in the script's display area. 
Our example script plotted the value of the `bar_index <https://www.tradingview.com/pine-script-reference/v4/#var_bar_index>`__ builtin variable, 
which contains the bar's number, a value beginning at zero on the dataset's first bar and increased by one on each 
subsequent bar. We used a ``plot()`` call to plot the variable to inspect because our script was not plotting anything else; 
we were not preoccupied with preserving the scale for other plots to continue to plot normally. This is the script we used::

    //@version=4
    study("Plot `bar_index`")
    plot(bar_index, "Bar Index")


When the script's scale must be preserved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Plotting values in the script's display area is not always possible. When we already have other plots going on and adding debugging plots of variables whose values fall outside the script's plotting boundaries would make the plots unreadable, another technique must be used to inspect values if we want to preserve the scale of the other plots.

Suppose we want to continue inspecting the value of ``bar_index``, but this time in a script where we are also plotting RSI::

    //@version=4
    study("Plot RSI and `bar_index`")
    r = rsi(close, 20)
    plot(r, "RSI", color.black)
    plot(bar_index, "Bar Index")

Running the script on a dataset containing a large number of bars yields the following display:

.. image:: images/Debugging-DisplayingNumericValues-1.png

where:

1. The RSI line in black is flat because it varies between zero and 100, but the indicator's pane is scaled to show the maximum value of ``bar_index``, which is ``25692.0000``.
2. The value of ``bar_index`` on the bar the cursor is on is displayed next to the indicator's name, and its blue plot in the script's pane is flat.
3. The ``25692.0000`` value of ``bar_index`` shown in the scale represents its value on the last bar, so the dataset contains 25693 bars.
4. The value of ``bar_index`` on the bar the cursor is on is also displayed in the Data Window, along with that bar's value for RSI just above it.

In order to preserve our plot of RSI while still being able to inspect the value or ``bar_index``, 
we will plot the variable using `plotchar() <https://www.tradingview.com/pine-script-reference/v4/#fun_plot>`__ like this::

    //@version=4
    study("Plot RSI and `bar_index`")
    r = rsi(close, 20)
    plot(r, "RSI", color.black)
    plotchar(bar_index, "Bar index", "", location.top)

.. image:: images/Debugging-DisplayingNumericValues-2.png

where:

- Because the value of ``bar_index`` is no longer being plotted in the script's pane, the pane's boundaries are now those of RSI, which displays normally.
- The value plotted using ``plotchar()`` is displayed next to the script's name and in the Data Window.
- We are not plotting a character with our ``plotchar()`` call, so the third argument is an empty string (``""``). 
  We are also specifying ``location.top`` as the ``location`` argument, so that we do not put the symbol's price in play in the calculation of the display area's boundaries.



Displaying strings
------------------

Pine labels must be used to display strings. Labels only appear in the script's display area; strings shown in labels will thus not appear in the Data Window or anywhere else.

Labels on each bar
^^^^^^^^^^^^^^^^^^

The following script demonstrates the simplest way to repetitively draw a label showing the symbol's name::

    //@version=4
    study("Simple label", "", true)
    label.new(bar_index, high, syminfo.ticker)

.. image:: images/Debugging-DisplayingStrings-1.png


Simple labels on last bar
^^^^^^^^^^^^^^^^^^^^^^^^^

As strings manipulated in Pine scripts often do not change bar to bar, the method most frequently used to visualize them is to draw a label on the dataset's last bar. 
Here, we use a function to create a more sophisticated label that only appears on the chart's last bar. Our ``f_print()`` function has only one parameter: the text string to be displayed::

    //@version=4
    study("f_print()", "", true)
    f_print(_text) =>
        // Create label on the first bar.
        var _label = label.new(bar_index, na, _text, xloc.bar_index, yloc.price, color(na), label.style_none, color.gray, size.large, text.align_left)
        // On next bars, update the label's x and y position, and the text it displays.
        label.set_xy(_label, bar_index, highest(10)[1])
        label.set_text(_label, _text)

    f_print("Multiplier = " + tostring(timeframe.multiplier) + "\nPeriod = " + timeframe.period + "\nHigh = " + tostring(high))
    f_print("Hello world!\n\n\n\n")

.. image:: images/Debugging-DisplayingStrings-2.png

Note the following in our last code example:

- We use the ``f_print()`` function to enclose the label-drawing code. While the function is called on each bar, 
  the label is only created on the dataset's first bar because of our use of the 
  `var <https://www.tradingview.com/pine-script-reference/v4/#op_var>`__ keyword when declaring the ``_label`` variable inside the function. After creating it, 
  we only update the label's *x* and *y* coordinates and its text on each successive bar. If we did not update those values, the label would remain on the dataset's first bar
  and would only display the text string's value on that bar. Lastly, note that we use ``highest(10)[1]`` to position the label vertically, 
  By using the highest high of the **previous** 10 bars, we prevent the label from moving during the realtime bar.

- We call the ``f_print()`` function twice to show that if you make multiple calls because it makes debugging multiple strings easier, 
  you can superimpose their text by using the correct amount of newlines (``\n``) to separate it.

- We use the `tostring() <https://www.tradingview.com/pine-script-reference/v4/#fun_tostring>`__ function to convert numeric values to a string for inclusion in the text to be displayed.

- You may need to change the *y* position where the label is drawn (``highest(10)[1]``) in certain conditions.

- We use AutoHotKey to speed coding up and have this line in our AHK script, which we use to bring up the ``f_print()`` function in our script when we need to debug strings.
  This is the AutoHotKey line that allows us to use CTRL-SHIT-P to insert the one-line version of the function in our code and create an empty call to the function, 
  ready to for you to type the string you want to debug::

    ^+p:: SendInput f_print(_text) => var _label = label.new(bar_index, na, _text, xloc.bar_index, yloc.price, {#}00000000, label.style_none, color.gray, size.large, text.align_left), label.set_xy(_label, bar_index, highest(10)[1]), label.set_text(_label, _text)`nf_print(){Left}

  AutoHotKey works only on Windows systems. Keyboard Maestro and others can be substituted on Apple systems.


More flexible labels on last bar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Debugging conditions
--------------------



Debugging from inside functions
-------------------------------



Debugging from inside 'for' loops
---------------------------------


