.. _PageTextAndShapes:

Text and shapes
===============

.. contents:: :local:
    :depth: 2


Introduction
------------

You may display text using four different ways with Pine:


- `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__
- `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__
- Labels created with `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__
- Tables created with `table.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_table{dot}new>`__

Which one you to use depends on your needs:

- Tables can display text in various relative positions on charts that will not move as users scroll of zoom the chart horizontally.
  Their content is not tethered to bars. In contrast, text displayed with 
  `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__, 
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ or
  `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__ is always tethered to a specific bar,
  so it will move with the bar's position on the chart.
  See the page on :ref:`Tables <PageTables>` for more information on them.
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
  require a "const string" argument, it cannot contain values such as prices that can only be known on the bar.
- To include "series" values in text displayed using `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__,
  they will first need to be converted to strings using 
  `str.tostring() <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}tostring>`__.
- Characters displayed by all these functions can be Unicode characters, which may include Unicode symbols.
- The concatenation operator for strings in Pine is ``+``. It is used to join string components into one string, e.g.,
  ``msg = "Chart symbol: " + syminfo.tickerid``, 
  where `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__
  is a Pine built-in variable that returns the chart's exchange and symbol information in string format.



\`plotchar()\`
--------------



\`plotshape()\`
---------------



Labels
------


Starting with Pine v4, indicators and strategies can
create *drawing objects* on the chart. Three types of
drawings are currently supported: "label", "line" and "box".
You will find one instance of each on the following chart:

.. image:: images/label_and_line_drawings.png

.. note:: On TradingView charts, a complete set of *Drawing Tools*
  allows users to create and modify drawings using mouse actions. While they may look similar to
  drawing objects created with Pine code, they are essentially different entities.
  Drawing objects created using Pine code cannot be modified with mouse actions, 
  and hand-drawn drawings from the chart user interface are not visible from Pine scripts.

The line, label, and box drawings in Pine allow you to create indicators with more sophisticated
visual components, e.g., pivot points, support/resistance levels,
zig zag lines, labels containing dynamic text, etc.

In contrast to indicator plots (plots are created with functions 
`plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__, 
`plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ and 
`plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__), 
drawing objects can be created on historical bars as well as in the future, where no bars exist yet.



Creating drawings
^^^^^^^^^^^^^^^^^

Pine drawing objects are created with the `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`_ , 
`line.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_line{dot}new>`__ and 
`box.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_box{dot}new>`__ functions.
While each function has many parameters, only the coordinates are mandatory.
This is an example of code used to create a label on every bar::

    //@version=5
    indicator("My Script", overlay = true)
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



Modifying drawings
^^^^^^^^^^^^^^^^^^

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
| Label style name               | Label                                           | Label with text                                 |
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

