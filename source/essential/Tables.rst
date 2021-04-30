Tables
======

.. contents:: :local:
    :depth: 3



Introduction
------------

Tables are objects that can be used to position information in specific and fixed locations in a script's visual space. 
Contrary to all other plots or objects drawn in Pine, 
tables are not anchored to specific bars; they *float* in a script's space, whether in overlay or pane mode, in studies or strategies,
independently of the chart bars being viewed or the zoom factor used. 

Tables contain cells arranged in columns and rows, much like a spreadsheet. 
A table's structure and key attributes are defined using `table.new() <https://www.tradingview.com/pine-script-reference/v4/#fun_table{dot}new>`__, 
which returns a table id that acts like a pointer to the table, just like label, line, or array ids do.
The `table.new() <https://www.tradingview.com/pine-script-reference/v4/#fun_table{dot}new>`__ call will create the table but does not display it.
Once created, the table must be populated using one 
`table.cell() <https://www.tradingview.com/pine-script-reference/v4/#fun_table{dot}cell>`__ call for each cell. 
Table cells can contain text, or not.

Some attributes of a previously created table or cell can be changed using ``table.set_*()`` or ``table.cell_set_*()`` setter functions.

A table is positioned in an indicator's space by anchoring it to one of nine references: the four corners or a midpoint between two of them. 
Tables are positioned by expanding the table from its anchor, so a table anchored to the ``middle_right`` reference will be drawn by expanding up, 
down and left from that anchor.

Two modes are available to determine the width/height of table cells:

- An automatic mode calculates the width/height of cells in a column/row using the widest/highest text in them. 
- An explicit mode allows programmers to define the width/height of cells using a percentage of the indicator's available x/y space.

Multiple tables can be used in one script, each one identified by its own id.
Limits on the quantity of cells in all tables are determined by the total number of cells used in one script.

Displayed table contents always represent the last state of the table, as it was drawn on the script's last execution.
Contrary to values displayed in the Data Window or in indicator values, 
variable contents displayed in tables will not change as the user moves his cursor over specific chart bars.
For this reason, it is strongly recommended to restrict execution of all ``table.*()`` calls to either the first or last bars of the dataset
by systematically using `var <https://www.tradingview.com/pine-script-reference/v4/#op_var>`__ to declare tables and by enclosing 
all other calls inside an `if <https://www.tradingview.com/pine-script-reference/v4/#op_if>`__ `barstate.islast <https://www.tradingview.com/pine-script-reference/v4/#var_barstate{dot}islast>`__ block.

Keep in mind that even when script users scroll back in the chart's history, they are always looking at the table as it was drawn on the dataset's last bar. 
As the position of tables is unaffected by the specific chart bars visible at any given time, the state of tables is also not a function of visible chart bars. 
Table calculations will not revert to their state on past bars when those bars become visible as a user scrolls his chart back in time. 
Pine scripts have no visibility on which bars are visible on the chart at any given time.

Tables should be created using the `var` keyword so they are created only once, when the script executes on the dataset's first bar. 
This is not only more efficient, but it also avoids frequent issues with handling tables that are re-created on each bar.

While table construction code can be executed on any bar the script is executing on, 
it will usually be more efficient to restrict its execution to the dataset's last bar by enclosing the code in a block following an `if barstate.islast` statement.



Creating tables
---------------

Placing a single value in a constant position
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's place the value of ATR in the upper-right corner of the chart::

    //@version=4
    study("ATR", "", true)
    // We use `var` to only initialize the table on the first bar.
    var table atrDisplay = table.new(position.top_right, 1, 1)
    // We call `atr()` outside the `if` block so it executes on each bar.
    myAtr = atr(14)
    if barstate.islast
        // We only populate the table on the last bar.
        table.cell(atrDisplay, 0, 0, tostring(myAtr))

Note how we:

- We enclose 

Let's improve the usability and aesthethics of our script::

    //@version=4
    study("ATR", "", true)
    i_atrP = input(14,  "ATR period", minval = 1, tooltip = "Using a period of 1 yields True Range.")

    // ————— Produces a string format usable with `tostring()` to restrict precision to ticks. Note that `tostring()` will also round the value.
    f_tickFormat() =>
        _s = tostring(syminfo.mintick)
        _s := str.replace_all(_s, "25", "00")
        _s := str.replace_all(_s, "5",  "0")
        _s := str.replace_all(_s, "1",  "0")

    var table atrDisplay = table.new(position.top_right, 1, 1, bgcolor = color.gray, frame_width = 2, frame_color = color.black)
    myAtr = atr(i_atrP)
    if barstate.islast
        table.cell(atrDisplay, 0, 0, tostring(myAtr, f_tickFormat()), text_color = color.white)

We used `table.new() <https://www.tradingview.com/pine-script-reference/v4/#fun_table{dot}new>`__
to define a background color, a frame color and its width. 
When populating the cell with `table.cell() <https://www.tradingview.com/pine-script-reference/v4/#fun_table{dot}cell>`__
we set the text to display in white. Finally, we used the `f_tickFormat()` function to restrict the precision of ATR to the chart's tick precision.




Tips
----

