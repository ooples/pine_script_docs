.. _PageInputs:

Inputs
======

.. contents:: :local:
    :depth: 2


Introduction
------------

Script inputs are the means by which Pine scripts can receive user inputs.
They can only be accessed when a script is running on the chart.
Script users access them through the script's "Settings" dialog box, 
which can be reached by:

- Double-clicking on the name of an on-chart indicator
- Right-clicking on the script's name and choosing the "Settings" item from the dropdown menu
- Choosing the "Settings" item from the "More" menu icon (three dots) that appears when one hovers over the indicator's name on the chart
- Double-clicking on the indicator's name from the Data Window (fourth icon down to the right of the chart)

The "Settings" dialog box always contains the "Style" and "Visibility" tabs,
which allow users to specify their preferences about the script's visuals
and the chart timeframes where it should be visible.

When a script contains calls to ``input.*()`` functions, an "Inputs" tab appears in the "Settings" dialog box:





Script inputs
-------------

The `input() <https://www.tradingview.com/pine-script-reference/v5/#fun_input>`__
annotation function and other ``input.*()`` functions (``input.int()``, ``input.string()``, etc) make it possible for script users to modify selected
values which the script can then use in its calculation or logic,
without the need to modify the script's code.

Specific widgets are supplied in the *Settings/Inputs* dialog box
for each type of input. A description of the value as well as minimum/maximum
values and a step increment can also be defined for many input types. The type of the variable can be explicitly defined using the relevant ``input.*()`` function, or a general purpose ``input()`` function can be used to automatically assign a type based on the default value. Only basic types (``int``, ``float``, ``bool``, ``string``, and ``color``) can be assigned that way.

Pine supports the following types of input:

-  input.bool(),
-  input.color(),
-  input.int(),
-  input.float(),
-  input.string(),
-  input.symbol(),
-  input.timeframe(),
-  input.session(),
-  input.source(),
-  input.time().

The following examples show how to create each type of input and what
its widget looks like.


Boolean input
^^^^^^^^^^^^^
::

    showOpenInput = input.bool(true, "On/Off")
    plot(showOpenInput ? open : na)

.. figure:: images/Inputs_of_indicator_1.png

Color input
^^^^^^^^^^^
::

    plotColorInput = input.color(color.red, "Color")
    plot(close, color = plotColorInput)

.. figure:: images/Inputs_of_indicator_8.png

Integer input
^^^^^^^^^^^^^
::

    offsetInput = input.int(7, "Offset", minval = -10, maxval = 10)
    plot(close[offsetInput])

.. figure:: images/Inputs_of_indicator_2.png


Float input
^^^^^^^^^^^
::

    angleInput = input.float(-0.5, "Angle", minval = -3.14, maxval = 3.14, step = 0.2)
    plot(sin(angleInput) > 0 ? close : open)

.. figure:: images/Inputs_of_indicator_3.png


Symbol and resolution inputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    symbolInput = input.symbol("SPY", "Symbol")
    tfInput = input.timeframe("60", "Timeframe")
    plot(close, color = color.red)
    plot(request.security(symbolInput, tfInput, close), color = color.green)

.. figure:: images/Inputs_of_indicator_4.png



The symbol input widget has a built-in *symbol search* which activates
automatically when the ticker's first characters are typed.


Session input
^^^^^^^^^^^^^
::

    sessionInput = input.session("24x7", "Session")
    plot(time(timeframe.period, sessionInput))

.. figure:: images/Inputs_of_indicator_5.png


Source input
^^^^^^^^^^^^^
::

    srcInput = input.source(close, "Source")
    ma = ta.sma(srcInput, 9)
    plot(ma)

.. figure:: images/Inputs_of_indicator_6.png


Time input
^^^^^^^^^^^^^
::

    dateInput = input.time(timestamp("20 Feb 2020 00:00 +0300"), "Date")
    plot(dateInput)

.. figure:: images/Inputs_of_indicator_9.png


options parameter
^^^^^^^^^^^^^^^^^
The ``options`` parameter is useful to provide users with a list
of constant values they can choose from using a dropdown menu.
::

    choiceInput = input.string("A", "Choice", options = ["A", "B"])
    plot(choiceInput == "A" ? close : choiceInput == "B" ? open : na)
	
.. figure:: images/Inputs_of_indicator_7.png


