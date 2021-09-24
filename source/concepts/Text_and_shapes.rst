.. _PageTextAndShapes:

Text and shapes
===============

.. contents:: :local:
    :depth: 2


Introduction
------------

You may display text or shapes using five different ways with Pine:


- `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__
- `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__
- `plotarrow() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__
- Labels created with `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__
- Tables created with `table.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_table{dot}new>`__
  (see :ref:`Tables <PageTables>`)

Which one to use depends on your needs:

- Tables can display text in various relative positions on charts that will not move as users scroll of zoom the chart horizontally.
  Their content is not tethered to bars. In contrast, text displayed with 
  `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__, 
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ or
  `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__ is always tethered to a specific bar,
  so it will move with the bar's position on the chart.
  See the page on :ref:`Tables <PageTables>` for more information on them.
- Three function include are able to display pre-defined shapes:
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__,
  `plotarrow() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__ and
  Labels created with `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__.
- `plotarrow() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__ cannot display text, only up or down arrows.
- `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ and
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ 
  can display non-dynamic (not of "series" form) text on any bar or all bars of the chart.
- `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__
  can only display one character while `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__
  can display strings, including line breaks.
- `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__
  can display a maximum of 500 labels on the chart. Its text **can** contain dynamic text, or "series strings".
  Line breaks are also supported in label text.
- While `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ and
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ 
  can display text at a fixed offset in the past or the future, which cannot change during the script's execution,
  each `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__ call
  can use a "series" offset that can be calculated on the fly.

These are a few things to keep in mind concerning Pine strings:

- Since the ``text`` parameter in both 
  `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ and
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ 
  require a "const string" argument, it cannot contain values such as prices that can only be known on the bar ("series string").
- To include "series" values in text displayed using `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__,
  they will first need to be converted to strings using 
  `str.tostring() <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}tostring>`__.
- The concatenation operator for strings in Pine is ``+``. It is used to join string components into one string, e.g.,
  ``msg = "Chart symbol: " + syminfo.tickerid`` 
  (where `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__
  is a Pine built-in variable that returns the chart's exchange and symbol information in string format).
- Characters displayed by all these functions can be Unicode characters, which may include Unicode symbols.
  See this `Exploring Unicode <https://www.tradingview.com/script/0rFQOCKf-Exploring-Unicode/>`__
  script to get an idea of what can be done with Unicode characters.
- The color or size of text can sometimes be controlled using function parameters,
  but no inline formatting (bold, italics, monospace, etc.) is possible.
- Text from Pine scripts always displays on the chart in the Trebuchet MS font, which is used in many TradingView texts,
  including this one.

This script displays text using the four methods available in Pine::

    //@version=5
    indicator("Four displays of text", overlay = true)
    plotchar(ta.rising(close, 5), "`plotchar()`", "🠅", location.belowbar, color.lime, size = size.small)
    plotshape(ta.falling(close, 5), "`plotchar()`", location = location.abovebar, color = na, text = "•`plotshape()•`\n🠇", textcolor = color.fuchsia, size = size.huge)
    
    if bar_index % 25 == 0
        label.new(bar_index, na, "•LABEL•\nHigh = " + str.tostring(high, format.mintick) + "\n🠇", yloc = yloc.abovebar, style = label.style_none, textcolor = color.black, size = size.normal)
    
    printTable(txt) => var table t = table.new(position.middle_right, 1, 1), table.cell(t, 0, 0, txt, bgcolor = color.yellow)
    printTable("•TABLE•\n" + str.tostring(bar_index + 1) + " bars\nin the dataset")

.. image:: images/TextAndShapes-Introduction-01.png

Note that:

- The method used to display each text string is shown with the text, except for the lime up arrows displayed using
  `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__, as it can only display one character.
- Label and table calls can be inserted in conditional structures to control when their are executed,
  whereas `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ and
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ cannot.
  Their conditional plotting must be controlled using their first argument, 
  which is a "series bool" whose ``true`` or ``false`` value determines when the text is displayed.
- Numeric values displayed in the table and labels is first converted to a string using
  `str.tostring() <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}tostring>`__.
- We use the ``+`` operator to concatenate string components.
- `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ is designed to display a shape
  with accompanying text. Its ``size`` parameter controls the size of the shape, not of the text.
  We use `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ for its ``color`` argument
  so that the shape is not visible.
- Contrary to other texts, the table text will not move as you scroll or scale the chart.
- Some text strings contain the 🠇 Unicode arrow (U+1F807).
- Some text strings contain the ``\n`` sequence that represents a new line.


\`plotchar()\`
--------------

This function is useful to display a single character on bars. It has the following syntax:

.. code-block:: text

    plotchar(series, title, char, location, color, offset, text, textcolor, editable, size, show_last, display) → void

See the `Reference Manual entry for plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__
for details on its parameters.

As explained in the :ref:`When the script's scale must be preserved <PageDebugging_WhenTheScriptsScaleMustBePreserved>` 
section of our page on :ref:`Debugging <PageDebugging>`,
the function can be used to display and inspect values in the Data Window or in the indicator values displayed to the right of the script's name on the chart::

    //@version=5
    indicator("", "", true)
    plotchar(bar_index, "Bar index", "", location.top)

.. image:: images/TextAndShapes-Plotchar-01.png

Note that:

- The cursor is on the chart's last bar.
- The value of `bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__
  on **that** bar is displayed in indicator values (1) and in the Data Window (2).
- We use ``location.top`` because the default ``location.abovebar`` will put the price into play in the script's scale,
  which will often interfere with other plots.

`plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__
also works well to identify specific points on the chart or to validate that conditions
are ``true`` when we expect them to be. This example displays an up arrow under bars where
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__,
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ and
`volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__
have all been rising for two bars::

    //@version=5
    indicator("", "", true)
    bool longSignal = ta.rising(close, 2) and ta.rising(high, 2) and (na(volume) or ta.rising(volume, 2))
    plotchar(longSignal, "Long", "▲", location.belowbar, color = na(volume) ? color.gray : color.blue, size = size.tiny)

.. image:: images/TextAndShapes-Plotchar-02.png

Note that:

- We use ``(na(volume) or ta.rising(volume, 2))`` so our script will work on symbols without 
  `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__ data.
  If we did not make provisions for when there is no `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__ data,
  which is what ``na(volume)`` does by being ``true`` when there is no volume, 
  the ``longSignal`` variable's value would never be ``true`` because ``ta.rising(volume, 2)`` yields ``false`` in those cases.
- We display the arrow in gray when there is no volume, to remind us that all three base conditions are not being met.
- Because `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__
  is now displaying a character on the chart, we use ``size = size.tiny`` to control its size.
- We have adapted the ``location`` argument to display the character under bars.

If you don't mind plotting only circles, you could also use `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__
to achieve a similar effect::

    //@version=5
    indicator("", "", true)
    longSignal = ta.rising(close, 2) and ta.rising(high, 2) and (na(volume) or ta.rising(volume, 2))
    plot(longSignal ? low - ta.tr : na, "Long", color.blue, 2, plot.style_circles)

This method has the inconvenience that, since there is no relative positioning mechanism with
`plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__
one must shift the circles down using something like 
`ta.tr <https://www.tradingview.com/pine-script-reference/v5/#var_ta{dot}tr>`__
(the bar's "True Range"):

.. image:: images/TextAndShapes-Plotchar-03.png



\`plotshape()\`
---------------

This function is useful to display pre-defined shapes and/or text on bars. It has the following syntax:

.. code-block:: text

    plotshape(series, title, style, location, color, offset, text, textcolor, editable, size, show_last, display) → void

See the `Reference Manual entry for plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__
for details on its parameters.

Let's use the function to achieve more or less the same result as with our second example of the previous section::

    //@version=5
    indicator("", "", true)
    longSignal = ta.rising(close, 2) and ta.rising(high, 2) and (na(volume) or ta.rising(volume, 2))
    plotshape(longSignal, "Long", shape.arrowup, location.belowbar)

Note that here, rather than using an arrow character, we are using the ``shape.arrowup`` argument
for the ``style`` parameter.

.. image:: images/TextAndShapes-Plotshape-01.png

It is possible to use different `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__
calls to superimpose text on bars. 
You will need to use ``\n`` followed by a special non-printing character that doesn’t get stripped out to preserve the newline's functionality. 
Here we’re using a Unicode Zero-width space (U+200E). While you don’t see it in the following code’s strings, it is there and can be copy/pasted. 
The special Unicode character needs to be the **last** one in the string for text going up, 
and the **first** one when you are plotting under the bar and text is going down::

    //@version=5
    indicator("Lift text", "", true)
    plotshape(true, "", shape.arrowup,   location.abovebar, color.green,  text="A")
    plotshape(true, "", shape.arrowup,   location.abovebar, color.lime,   text="B\n​")
    plotshape(true, "", shape.arrowdown, location.belowbar, color.red,    text="C")
    plotshape(true, "", shape.arrowdown, location.belowbar, color.maroon, text="​\nD")

.. image:: images/TextAndShapes-Plotshape-02.png

The available shapes you can use with the ``style`` parameter are:

+------------------------+--------------------------+--------------------------+-+------------------------+--------------------------+--------------------------+
| Argument               | Shape                    | With Text                | | Argument               | Shape                    | With Text                |
+========================+==========================+==========================+=+========================+==========================+==========================+
| ``shape.xcross``       | |Plotshape_xcross|       | |Xcross_with_text|       | | ``shape.arrowup``      | |Plotshape_arrowup|      | |Arrowup_with_text|      |
+------------------------+--------------------------+--------------------------+-+------------------------+--------------------------+--------------------------+
| ``shape.cross``        | |Plotshape_cross|        | |Cross_with_text|        | | ``shape.arrowdown``    | |Plotshape_arrowdown|    | |Arrowdown_with_text|    |
+------------------------+--------------------------+--------------------------+-+------------------------+--------------------------+--------------------------+
| ``shape.circle``       | |Plotshape_circle|       | |Circle_with_text|       | | ``shape.square``       | |Plotshape_square|       | |Square_with_text|       |
+------------------------+--------------------------+--------------------------+-+------------------------+--------------------------+--------------------------+
| ``shape.triangleup``   | |Plotshape_triangleup|   | |Triangleup_with_text|   | | ``shape.diamond``      | |Plotshape_diamond|      | |Diamond_with_text|      |
+------------------------+--------------------------+--------------------------+-+------------------------+--------------------------+--------------------------+
| ``shape.triangledown`` | |Plotshape_triangledown| | |Triangledown_with_text| | | ``shape.labelup``      | |Plotshape_labelup|      | |Labelup_with_text|      |
+------------------------+--------------------------+--------------------------+-+------------------------+--------------------------+--------------------------+
| ``shape.flag``         | |Plotshape_flag|         | |Flag_with_text|         | | ``shape.labeldown``    | |Plotshape_labeldown|    | |Labeldown_with_text|    |
+------------------------+--------------------------+--------------------------+-+------------------------+--------------------------+--------------------------+

.. |Plotshape_xcross| image:: images/TextAndShapes-Plotshape-Xcross.png
.. |Xcross_with_text| image:: images/TextAndShapes-Plotshape-Xcross_with_text.png
.. |Plotshape_cross| image:: images/TextAndShapes-Plotshape-Cross.png
.. |Cross_with_text| image:: images/TextAndShapes-Plotshape-Cross_with_text.png
.. |Plotshape_circle| image:: images/TextAndShapes-Plotshape-Circle.png
.. |Circle_with_text| image:: images/TextAndShapes-Plotshape-Circle_with_text.png
.. |Plotshape_triangleup| image:: images/TextAndShapes-Plotshape-Triangleup.png
.. |Triangleup_with_text| image:: images/TextAndShapes-Plotshape-Triangleup_with_text.png
.. |Plotshape_triangledown| image:: images/TextAndShapes-Plotshape-Triangledown.png
.. |Triangledown_with_text| image:: images/TextAndShapes-Plotshape-Triangledown_with_text.png
.. |Plotshape_flag| image:: images/TextAndShapes-Plotshape-Flag.png
.. |Flag_with_text| image:: images/TextAndShapes-Plotshape-Flag_with_text.png
.. |Plotshape_arrowup| image:: images/TextAndShapes-Plotshape-Arrowup.png
.. |Arrowup_with_text| image:: images/TextAndShapes-Plotshape-Arrowup_with_text.png
.. |Plotshape_arrowdown| image:: images/TextAndShapes-Plotshape-Arrowdown.png
.. |Arrowdown_with_text| image:: images/TextAndShapes-Plotshape-Arrowdown_with_text.png
.. |Plotshape_square| image:: images/TextAndShapes-Plotshape-Square.png
.. |Square_with_text| image:: images/TextAndShapes-Plotshape-Square_with_text.png
.. |Plotshape_diamond| image:: images/TextAndShapes-Plotshape-Diamond.png
.. |Diamond_with_text| image:: images/TextAndShapes-Plotshape-Diamond_with_text.png
.. |Plotshape_labelup| image:: images/TextAndShapes-Plotshape-Labelup.png
.. |Labelup_with_text| image:: images/TextAndShapes-Plotshape-Labelup_with_text.png
.. |Plotshape_labeldown| image:: images/TextAndShapes-Plotshape-Labeldown.png
.. |Labeldown_with_text| image:: images/TextAndShapes-Plotshape-Labeldown_with_text.png



\`plotarrow()\`
---------------

The `plotarrow <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__
function displays up or down arrows of variable length, 
based on the relative value of the series used in the function's first argument. 
It has the following syntax:

.. code-block:: text

    plotarrow(series, title, colorup, colordown, offset, minheight, maxheight, editable, show_last, display) → void

See the `Reference Manual entry for plotarrow() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__
for details on its parameters.

The ``series`` parameter in `plotarrow() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__
is not a "series bool" as in `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ and
`plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__; 
it is a "series int/float" and there's more to it than a simple ``true`` or ``false`` value determining when the arrows are plotted.
This is the logic governing how the argument supplied to ``series`` 
affects the behavior of `plotarrow() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__:

-  ``series > 0``: An up arrow is displayed, the length of which will be proportional to the
   relative value of the series on that bar in relation to other series values.
-  ``series < 0``: A down arrow is displayed, proportionally-sized using the same rules.
-  ``series == 0 or na(series)``: No arrow is displayed.

The maximum and minimum possible sizes for the arrows (in pixels) 
can be controlled using the ``minheight`` and ``maxheight`` parameters.

Here is a simple script illustrating how `plotarrow() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotarrow>`__ works::
	
    //@version=5
    indicator("", "", true)
    body = close - open
    plotarrow(body, colorup = color.teal, colordown = color.orange)

.. image:: images/TextAndShapes-Plotarrow-01.png

Note how the heigth of arrows is proportional to the relative size of the bar bodies.

You can use any series to plot the arrows. Here we use the value of the
"Chaikin Oscillator" to control the location and size of the arrows::

    //@version=5
    indicator("Chaikin Oscillator Arrows", overlay = true)
    fastLengthInput = input.int(3,  minval = 1)
    slowLengthInput = input.int(10, minval = 1)
    osc = ta.ema(ta.accdist, fastLengthInput) - ta.ema(ta.accdist, slowLengthInput)
    plotarrow(osc)

.. image:: images/TextAndShapes-Plotarrow-02.png

Note that we display the actual "Chaikin Oscillator" in a pane below the chart, 
so you can see what values are used to determine the position and size of the arrows.



Labels
------

Labels are only available in v4 and higher versions of Pine. They work very differently than 
`plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ and
`plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__.

Labels are objects, like :ref:`lines and boxes <PageLinesAndBoxes>` and are referred to using an ID of "label" type.
Many functions exist in the ``label`` namespace. They are used to create, modify and delete labels.

.. note:: On TradingView charts, a complete set of *Drawing Tools*
  allows users to create and modify drawings using mouse actions. While they may sometimes look similar to
  drawing objects created with Pine code, they are different entities.
  Drawing objects created using Pine code cannot be modified with mouse actions, 
  and hand-drawn drawings from the chart user interface are not visible from Pine scripts.

Labels are advantageous because:

- They allow "series" values to be converted to text and placed on charts.
  This means they are ideal to display values that cannot be known before time,
  such as price values, support and resistance levels, of any other values that your script calculates.
- Their positioning options are more flexible that those of the ``plot*()`` functions.
- They offer more display modes.
- Contrary to ``plot*()`` functions, label-handling functions can be inserted in conditional or loop structures,
  making it easier to control their behavior.
- You can add tooltips to labels.

One drawback to using labels is that you can only have a limited quantity of them on the chart.
The default is ~50 and you can use the ``max_labels_count`` parameter in your 
`indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__ or 
`indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__
declaration statement to specify up to 500. Labels, as other objects, 
are managed using a garbage collection mechanism which deletes the oldest ones on the chart
such that only the newest displayed labels are visible.



Label functions
^^^^^^^^^^^^^^^

Your toolbox of built-ins to manage labels includes:

- `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`_ to create labels
- ``label.set_*()`` functions to modify the properties of an existing label
- ``label.get_*()`` functions to read the properties of an existing label
- `label.delete() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}delete>`_ to delete labels
- The `label.all <https://www.tradingview.com/pine-script-reference/v5/#var_label{dot}all>`__ 
  array which always contains the IDs of all the visible labels on the chart. 
  The array's size will depend on the maximum label count for your script and how many of those you have drawn.
  ``aray.size(label.all)`` will return the array's size.



Creating labels
^^^^^^^^^^^^^^^

The `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`_
function creates a new label. It has the following signature:

.. code-block:: text

    label.new(x, y, text, xloc, yloc, color, style, textcolor, size, textalign, tooltip) → series label

This is how you can create labels in their simplest form::

    //@version=5
    indicator("", "", true)
    label.new(bar_index, high)

.. image:: images/minimal_label.png

The label is created with the parameters ``x = bar_index`` (the index of the current bar,
`bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__) and ``y = high`` (high price of the current bar).
When a new bar opens, a new label is created on it. Label objects created on previous bars stay on the chart
until the indicator deletes them with an explicit call of the `label.delete() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}delete>`__
function, or until the automatic garbage collection process removes them.

Here is a modified version of the same script that shows the values of the ``x`` and ``y`` coordinates used to create the labels::

    //@version=5
    indicator("My Script", overlay = true)
    label.new(bar_index, high, style = label.style_none,
              text = "x=" + str.tostring(bar_index) + "\ny=" + str.tostring(high))

.. image:: images/minimal_label_with_x_y_coordinates.png

In this example labels are shown without background coloring (because of parameter ``style = label.style_none``) but with
dynamically created text (``text = "x=" + str.tostring(bar_index) + "\ny=" + str.tostring(high)``) that prints label coordinates.

This is an example of code that creates line objects on a chart::

    //@version=5
    indicator("My Script", overlay = true)
    line.new(x1 = bar_index[1], y1 = low[1], x2 = bar_index, y2 = high)

.. image:: images/minimal_line.png

This is an example of code that creates box objects on a chart::

    //@version=5
    indicator("My Script", overlay = true)
    box.new(left = bar_index[1], top = low[1], right = bar_index, bottom = high)

.. image:: images/minimal_box.png



Calculation of drawings on bar updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Drawing objects are subject to both *commit* and *rollback* actions, which affect the behavior of a script when it executes
in the realtime bar. See the page on Pine's :ref:`Execution model <Page_ExecutionModel>`.

This script demonstrates the effect of rollback when running in the realtime bar::

    //@version=5
    indicator("My Script", overlay = true)
    label.new(bar_index, high)

While `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`_ 
creates a new label on every iteration of the script when price changes in the realtime bar,
the most recent label created in the script's previous iteration is also automatically deleted because of rollback before the next iteration. 
Only the last label created before the realtime bar's close will be committed, and will thus persist.

.. _drawings_coordinates:



Coordinates
^^^^^^^^^^^

Drawing objects are positioned on the chart according to *x* and *y* coordinates using a combination of 4 parameters: ``x``, ``y``, ``xloc`` and ``yloc``. The value of ``xloc`` determines whether ``x`` will hold a bar index or time value. When ``yloc = yloc.price``, ``y`` holds a price. ``y`` is ignored when ``yloc`` is set to `yloc.abovebar <https://www.tradingview.com/pine-script-reference/v5/#var_yloc{dot}abovebar>`__ or `yloc.belowbar <https://www.tradingview.com/pine-script-reference/v5/#var_yloc{dot}belowbar>`__.

If a drawing object uses `xloc.bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_xloc{dot}bar_index>`__, then
the x-coordinate is treated as an absolute bar index. The bar index of the current bar can be obtained from the built-in variable ``bar_index``. The bar index of previous bars is ``bar_index[1]``, ``bar_index[2]`` and so on. ``xloc.bar_index`` is the default value for x-location parameters of both label and line drawings.

If a drawing object uses `xloc.bar_time <https://www.tradingview.com/pine-script-reference/v5/#var_xloc{dot}bar_time>`__, then
the x-coordinate is treated as a UNIX time in milliseconds. The start time of the current bar can be obtained from the built-in variable ``time``.
The bar time of previous bars is ``time[1]``, ``time[2]`` and so on. Time can also be set to an absolute time point with the
`timestamp <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__ function.

Both modes make it possible to place a drawing object in the future, to the right of the current bar. For example::

    //@version=5
    indicator("My Script", overlay = true)
    dt = time - time[1]
    if barstate.islast
        label.new(time + 3*dt, close, xloc = xloc.bar_time)

.. image:: images/label_in_the_future.png

This code places a label object in the future. X-location logic works identically for label, line, and box drawings.

Example for ``xloc.bar_index``::

    //@version=5
    indicator("My Script", overlay = true)
    label.new(bar_index+100, high)

.. image:: images/label_in_the_future_2.png

In contrast, y-location logic is different for label and line or box drawings.
Pine's *line* and *box* drawings always use `yloc.price <https://www.tradingview.com/pine-script-reference/v5/#var_yloc{dot}price>`__,
so their y-coordinate is always treated as an absolute price value.

Label drawings have additional y-location values: `yloc.abovebar <https://www.tradingview.com/pine-script-reference/v5/#var_yloc{dot}abovebar>`__ and
`yloc.belowbar <https://www.tradingview.com/pine-script-reference/v5/#var_yloc{dot}belowbar>`__.
When they are used, the value of the ``y`` parameter is ignored and the drawing object is placed above or below the bar.



Modifying labels
^^^^^^^^^^^^^^^^

A drawing object can be modified after its creation. The 
`label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`_, 
`line.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_line{dot}new>`_, and 
`box.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_box{dot}new>`_ functions return
a reference to the created drawing object (of type "series label", "series line" and "series box" respectively).
This reference can then be used as the first argument to the ``label.set_*()``, ``line.set_*()``, or ``box.set_*()`` functions used to modify drawings.
For example::

    //@version=5
    indicator("My Script", overlay = true)
    l = label.new(bar_index, na)
    if close >= open
        label.set_text(l, "green")
        label.set_color(l, color.green)
        label.set_yloc(l, yloc.belowbar)
        label.set_style(l, label.style_label_up)
    else
        label.set_text(l, "red")
        label.set_color(l, color.red)
        label.set_yloc(l, yloc.abovebar)
        label.set_style(l, label.style_label_down)

.. image:: images/label_changing_example.png

This simple script first creates a label on the current bar and then it writes a reference to it in a variable ``l``.
Then, depending on whether the current bar is rising or falling (condition ``close >= open``), a number of label drawing properties are modified:
text, color, *y* coordinate location (``yloc``) and label style.

One may notice that ``na`` is passed as the ``y`` argument to the ``label.new`` function call. The reason for this is that
the example's label uses either ``yloc.belowbar`` or ``yloc.abovebar`` y-locations, which don't require a y value.
A finite value for ``y`` is needed only if a label uses ``yloc.price``.

The available *setter* functions for label drawings are:

    * `label.set_color() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_color>`__ --- changes color of label
    * `label.set_size() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_size>`__ --- changes size of label
    * `label.set_style() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_style>`__ --- changes :ref:`style of label <drawings_label_styles>`
    * `label.set_text() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_text>`__ --- changes text of label
    * `label.set_textcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_textcolor>`__ --- changes color of text
    * `label.set_x() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_x>`__ --- changes x-coordinate of label
    * `label.set_y() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_y>`__ --- changes y-coordinate of label
    * `label.set_xy() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_xy>`__ --- changes both x and y coordinates of label
    * `label.set_xloc() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_xloc>`__ --- changes x-location of label
    * `label.set_yloc() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_yloc>`__ --- changes y-location of label
    * `label.set_tooltip() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_tooltip>`__ --- changes tooltip of label


.. _drawings_label_styles:



Label styles
^^^^^^^^^^^^

Various styles can be applied to labels with either the `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__ or
`label.set_style() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}set_style>`__
function:

+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| Argument                       | Label                                           | Label with text                                 |
+================================+=================================================+=================================================+
| ``label.style_none``           |                                                 | |label_style_none_t|                            |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_xcross``         | |label_style_xcross|                            | |label_style_xcross_t|                          |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_cross``          | |label_style_cross|                             | |label_style_cross_t|                           |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_triangleup``     | |label_style_triangleup|                        | |label_style_triangleup_t|                      |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_triangledown``   | |label_style_triangledown|                      | |label_style_triangledown_t|                    |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_flag``           | |label_style_flag|                              | |label_style_flag_t|                            |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_circle``         | |label_style_circle|                            | |label_style_circle_t|                          |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_arrowup``        | |label_style_arrowup|                           | |label_style_arrowup_t|                         |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_arrowdown``      | |label_style_arrowdown|                         | |label_style_arrowdown_t|                       |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_label_up``       | |label_style_label_up|                          | |label_style_label_up_t|                        |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_label_down``     | |label_style_label_down|                        | |label_style_label_down_t|                      |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_square``         | |label_style_square|                            | |label_style_square_t|                          |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+
| ``label.style_diamond``        | |label_style_diamond|                           | |label_style_diamond_t|                         |
+--------------------------------+-------------------------------------------------+-------------------------------------------------+

.. |label_style_xcross| image:: images/label.style_xcross.png
.. |label_style_cross| image:: images/label.style_cross.png
.. |label_style_triangleup| image:: images/label.style_triangleup.png
.. |label_style_triangledown| image:: images/label.style_triangledown.png
.. |label_style_flag| image:: images/label.style_flag.png
.. |label_style_circle| image:: images/label.style_circle.png
.. |label_style_arrowup| image:: images/label.style_arrowup.png
.. |label_style_arrowdown| image:: images/label.style_arrowdown.png
.. |label_style_label_up| image:: images/label.style_labelup.png
.. |label_style_label_down| image:: images/label.style_labeldown.png
.. |label_style_square| image:: images/label.style_square.png
.. |label_style_diamond| image:: images/label.style_diamond.png

.. |label_style_none_t| image:: images/label.style_none_t.png
.. |label_style_xcross_t| image:: images/label.style_xcross_t.png
.. |label_style_cross_t| image:: images/label.style_cross_t.png
.. |label_style_triangleup_t| image:: images/label.style_triangleup_t.png
.. |label_style_triangledown_t| image:: images/label.style_triangledown_t.png
.. |label_style_flag_t| image:: images/label.style_flag_t.png
.. |label_style_circle_t| image:: images/label.style_circle_t.png
.. |label_style_arrowup_t| image:: images/label.style_arrowup_t.png
.. |label_style_arrowdown_t| image:: images/label.style_arrowdown_t.png
.. |label_style_label_up_t| image:: images/label.style_labelup_t.png
.. |label_style_label_down_t| image:: images/label.style_labeldown_t.png
.. |label_style_square_t| image:: images/label.style_square_t.png
.. |label_style_diamond_t| image:: images/label.style_diamond_t.png


.. _drawings_line_styles:



Deleting drawings
^^^^^^^^^^^^^^^^^

The `label.delete() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}delete>`_, `line.delete() <https://www.tradingview.com/pine-script-reference/v5/#fun_line{dot}delete>`__ and `box.delete() <https://www.tradingview.com/pine-script-reference/v5/#fun_box{dot}delete>`__
functions delete label, line, or box drawing objects from the chart.

Here is Pine code that keeps just one label drawing object on the current bar,
*deleting the old ones*::

    //@version=5
    indicator("Last Bar Close 1", overlay = true)

    c = close >= open ? color.lime : color.red
    l = label.new(bar_index, na,
      text = str.tostring(close), color = c,
      style = label.style_label_down, yloc = yloc.abovebar)

    label.delete(l[1])

.. image:: images/Last_Bar_Close_1.png

On every new bar update of the "Last Bar Close 1" indicator, a new label object is created and written to variable ``l``.
Variable ``l`` is of type *series label*, so the ``[]`` operator is used to get the previous bar's label object.
That previous label is then passed to the ``label.delete`` function to delete it.

Functions ``label.delete`` and ``line.delete`` do nothing if the ``na`` value is used as an id, which makes code like the following unnecessary::

    if not na(l[1])
        label.delete(l[1])

The previous script's behavior can be reproduced using another approach::

    //@version=5
    indicator("Last Bar Close 2", overlay = true)

    var label l = na
    label.delete(l)
    c = close >= open ? color.lime : color.red
    l := label.new(bar_index, na,
      text = str.tostring(close), color = c,
      style = label.style_label_down, yloc = yloc.abovebar)

When the study "Last Bar Close 2" gets a new bar update, variable ``l`` is still referencing the old label object created on the previous bar. This label is deleted with the ``label.delete(l)`` call. A new label is then created and its id saved to ``l``. Using this approach there is no need to use the ``[]`` operator.

Note the use of the :ref:`var keyword <variable_declaration>`. It creates variable ``l`` and initializes it with the ``na`` value only once. ``label.delete(l)`` would have no object to delete if it weren't for the fact that ``l`` is initialized only once.

There is yet another way to achieve the same objective as in the two previous scripts, this time by modifying the label rather than deleting it::

    //@version=5
    indicator("Last Bar Close 3", overlay = true)

    var label l = label.new(bar_index, na,
      style = label.style_label_down, yloc = yloc.abovebar)

    c = close >= open ? color.lime : color.red
    label.set_color(l, c)
    label.set_text(l, str.tostring(close))
    label.set_x(l, bar_index)

Once again, the use of new :ref:`var keyword <variable_declaration>` is essential. It is what allows the 
`label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`_ call to be
executed only once, on the very first historical bar.

