.. _PageInputs:

Inputs
======

.. contents:: :local:
    :depth: 2


Introduction
------------

Script inputs are the means by which Pine scripts can receive user inputs,
which allows Pine programmers to write more flexible scripts because their behavior can adapt to user preferences.

The following script plots a 20-period `simple moving average (SMA) <https://www.tradingview.com/u/?solution=43000502589>`__
using ``ta.sma(close, 20)``. While it is simple to write, it is not very flexible because that specific MA is all it will ever plot::

    //@version=5
    indicator("MA", "", true)
    plot(ta.sma(close, 20))

If instead we write our script this way, it becomes much more flexible because its users will be able to select
the source and the length they want to use for the MA's calculation::

    //@version=5
    indicator("MA", "", true)
    sourceInput = input(close, "Source")
    lengthInput = input(20, "Length")
    plot(ta.sma(sourceInput, lengthInput))


Inputs can only be accessed when a script is running on the chart.
Script users access them through the script's "Settings" dialog box, 
which can be reached different ways, by:

- Double-clicking on the name of an on-chart indicator
- Right-clicking on the script's name and choosing the "Settings" item from the dropdown menu
- Choosing the "Settings" item from the "More" menu icon (three dots) that appears when one hovers over the indicator's name on the chart
- Double-clicking on the indicator's name from the Data Window (fourth icon down to the right of the chart)

The "Settings" dialog box always contains the "Style" and "Visibility" tabs,
which allow users to specify their preferences about the script's visuals
and the chart timeframes where it should be visible.

When a script contains calls to ``input.*()`` functions, an "Inputs" tab appears in the "Settings" dialog box.

.. image:: images/Inputs-Introduction-1.png

In the flow of a script's execution, inputs are processed when the script is already on a chart 
and user changes values in the "Inputs" tab. 
These changes trigger a re-execution of the script on all the chart bars,
so when a user changes an input value, your script recalculates using that new value.



Input functions
---------------

The following input functions are available:

- `input() <https://www.tradingview.com/pine-script-reference/v5/#fun_input>`__
- `input.int() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}int>`__
- `input.float() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}float>`__
- `input.bool() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}bool>`__
- `input.color() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}color>`__
- `input.string() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}string>`__
- `input.price() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}price>`__
- `input.source() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}source>`__
- `input.session() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}session>`__
- `input.symbol() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}symbol>`__
- `input.time() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}time>`__
- `input.timeframe() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}timeframe>`__

`input() <https://www.tradingview.com/pine-script-reference/v5/#fun_input>`__ is a simple, 
generic function that supports the fundamental Pine types: "int", "float", "bool", "color" and "string" types.
It also support "source" inputs, which are price-related values such as
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__,
`hl2 <https://www.tradingview.com/pine-script-reference/v5/#hl2>`__, and
`hlc3 <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__,
or which can be used to receive the output value of another script.

A specific input *widget* is created in the "Inputs" tab for each type of input.

Input function definitions typically contain many parameters,
which allow you to control the default value of inputs, its limits, 
and the way it is organized in the "Inputs" tab.

All values returned by ``input.*()`` functions except "source" ones are of the "input" form
(see the section on :ref:`forms <PageTypeSystem_Forms>` form more information).



Simple inputs
-------------

The `input() <https://www.tradingview.com/pine-script-reference/v5/#fun_input>`__
function and other ``input.*()`` functions (``input.int()``, ``input.string()``, etc) make it possible for script users to modify selected
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



Organization of inputs
----------------------

