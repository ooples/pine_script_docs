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



