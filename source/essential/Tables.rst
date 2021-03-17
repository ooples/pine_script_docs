Tables
======

.. contents:: :local:
    :depth: 3



Introduction
------------

Tables are objects that can be used to position information in specific locations of the indicator's visual space, 
regardless of the chart bars being viewed or the zoom factor used. Contrary to all other plots or objects drawn in Pine, 
tables are not anchored to specific bars; they *float* in the indicator's space, whether in overlay or pane mode, in studies or strategies. 

Tables contain cells arranged in columns and rows. A table is created using ``table.new()``. A table is represented by a table id which acts as a pointer to the table, 
just like label, line, or array ids do. The content of cells and their individual properties are specified using a ``table.cell()`` call for each cell. 
Some attributes of a previously created table or cell can be changed using ``table.set_*()`` or ``table.cell_set_*()`` setter functions.

A table is positioned in an indicator's space by anchoring it to one of nine references: the four corners or a midpoint between two of them. 
Tables are positioned by expanding the table from its anchor, so a table anchored to the ``middle_right`` reference will be drawn by expanding up, 
down and left from that anchor.

Two modes are available to determine the width/height of table cells. 
An automatic mode calculates the width/height of cells in a column/row using the widest/highest text in them. 
An explicit mode allows programmers to define the width/height of cells using a percentage of the indicator's available x/y space.

Multiple tables can be used in one script. Each one can be manipulated separately using its own id. 
Limits on memory use are determined by the quantity of cells in all tables used in a script—not by the number of tables.



Creating a table
----------------


Populating a table
------------------


Tips
----

Tables should be created using the `var` keyword so they are created only once, when the script executes on the dataset's first bar. 
This is not only more efficient, but it also avoids frequent issues with handling tables that are re-created on each bar.

While table construction code can be executed on any bar the script is executing on, 
it will usually be more efficient to restrict its execution to the dataset's last bar by enclosing the code in a block following an `if barstate.islast` statement.

Keep in mind that even when script users scroll back in the chart's history, they are always looking at the table as it was drawn on the dataset's last bar. 
As the position of tables is unaffected by the chart  bars visible at any given time, the state of tables is also not a function of visible chart bars, 
so table calculations will not revert to their state on past bars when those bars become visible as a user scrolls his chart back in time. 
Pine scripts have no visibility on which bars are visible on the chart at any given time.


————————————————————————————————————————————————————————————————


TradingView alerts run 24x7 on our servers and do not require users to be logged in to execute. Alerts are created from the charts user interface (*UI*). 
You will find all the information necessary to understand how alerts work and how to create them from the charts UI in the 
Help Center's `About TradingView alerts <https://www.tradingview.com/?solution=43000520149>`__ page.

Some of the alert types available on TradingView (*generic alerts*, *drawing alerts* and *script alerts* on order fill events) are created from symbols or 
scripts loaded on the chart and do not require specific coding in Pine scripts. Any user can create these types of alerts from the charts UI.

Other types of alerts 
(*script alerts* triggering on *alert() function calls*, and *alertcondition() alerts*) 
require specific Pine code to be present in a script to create an *alert event* before script users can create alerts from them using the charts UI. 
Additionally, while script users can create *script alerts* triggering on *order fill events* from the charts UI on any strategy loaded on their chart, 
Pine coders can specify explicit order fill alert messages in their script for each type of order filled by the broker emulator. 

This page covers the different ways Pine programmers can code their scripts to create alert events 
from which script users will in turn be able to create alerts from the charts UI. 
We will cover:

- How to use the `alert() <https://www.tradingview.com/pine-script-reference/v4/#fun_alert>`__ function to *alert() function calls* 
  in studies or strategies, which can then be included in *script alerts* created from the charts UI.
- How to add custom alert messages to be included in *script alerts* triggering on the *order fill events* of strategies.
- How to use the `alertcondition() <https://www.tradingview.com/pine-script-reference/v4/#fun_alertcondition>`__ function to generate, 
  in studies only, *alertcondition() events* which can then be used to create *alertcondition() alerts* from the charts UI.

Keep in mind that:

- No alert-related Pine code can create a running alert in the charts UI; 
  it merely creates alert events which can then be used by script users to create running alerts from the charts UI.
- Alerts only trigger in the realtime bar. The operational scope of Pine code dealing with any type of alert is therefore restricted to realtime bars only.
- When an alert is created in the charts UI, TradingView saves a mirror image of the script and its inputs, along with the chart's main symbol and timeframe 
  to run the alert on its servers. Subsequent changes to your script's inputs or the chart will thus not affect running alerts previously created from them. 
  If you want any changes to your context to be reflected in a running alert's behavior, 
  you will need to delete the alert and create a new one in the new context.

