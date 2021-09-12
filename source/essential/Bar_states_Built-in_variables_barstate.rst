.. contents:: :local:
    :depth: 3

Bar states
==========

A set of built-in variables in the ``barstate`` namespace allow your script to detect different properties of the bar on which the script is currently exectuting. 
These states can be used to restrict the execution or the logic of your code to specific bars.

Bar state built-in variables
----------------------------

Note that while indicators and libraries run on all price or volume updates in real time, strategies not using ``calc_on_every_tick`` will not; they will only execute when the realtime bar closes. This will affect the detection of bar states in that type of script.


\`barstate.isfirst\`
^^^^^^^^^^^^^^^^^^^^

`barstate.isfirst <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isfirst>`__ 
is only ``true`` on the dataset's first bar, i.e., when `bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__ is zero.

It can be useful to initialize variables on the first bar only, e.g.::

    // Declare array and set its values on the first bar only.
    FILL_COLOR = color.green
    var fillColors = array.new_color(0)
    if barstate.isfirst
        // Initialize the array elements with progressively lighter shades of the fill color.
        array.push(fillColors, color.new(FILL_COLOR, 70))
        array.push(fillColors, color.new(FILL_COLOR, 75))
        array.push(fillColors, color.new(FILL_COLOR, 80))
        array.push(fillColors, color.new(FILL_COLOR, 85))
        array.push(fillColors, color.new(FILL_COLOR, 90))


\`barstate.islast\`
^^^^^^^^^^^^^^^^^^^

`barstate.islast <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}islast>`__ 
is ``true`` if the current bar is the last one on the chart, whether that bar is a realtime bar or not.

It is often used to restrict the execution of code to the chart's last bar, which is often useful when drawing lines, labels or tables.


\`barstate.ishistory\`
^^^^^^^^^^^^^^^^^^^^^^

`barstate.ishistory <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}ishistory>`__ 
is ``true`` on all historical bars. It can never be ``true`` on a bar when 
`barstate.isrealtime <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isrealtime>`__ is also ``true``, 
and it does not become ``true`` on a realtime bar's closing update, when 
`barstate.isconfirmed <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isconfirmed>`__ becomes ``true``. 
On closed markets, it can be ``true`` on the same bar where `barstate.islast <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}islast>`__ 
is also ``true``.


\`barstate.isrealtime\`
^^^^^^^^^^^^^^^^^^^^^^^

`barstate.isrealtime <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isrealtime>`__ 
is ``true`` if the current data update is a real-time bar update, ``false`` otherwise (thus it is historical). Note that every realtime bar is also the *last* one.


\`barstate.isnew\`
^^^^^^^^^^^^^^^^^^

`barstate.isnew <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isnew>`__ 
is ``true`` on all historical bars. On the realtime bar, it is only ``true`` on its first (opening) update.

It is useful to reset `varip <https://www.tradingview.com/pine-script-reference/v5/#op_varip>`__ variables when a new realtime bar comes in::

    //@version=5
    indicator("")
    updateNo() => 
        varip int updateNo = na
        if barstate.isnew
            updateNo := 1
        else
            updateNo += 1
    plot(updateNo())


\`barstate.isconfirmed\`
^^^^^^^^^^^^^^^^^^^^^^^^

`barstate.isconfirmed <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isconfirmed>`__ 
is ``true`` on all historical bars and on the last (closing) update of a realtime bar.

It can be useful to avoid repainting by requiring the realtime bar to be closed before a condition can become ``true``. 
We use it here to hold plotting of our RSI until the realtime bar closes and becomes an elapsed realtime bar. 
It will plot on historical bars because `barstate.isconfirmed <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}isconfirmed>`__ 
is always ``true`` on them::

    //@version=5
    indicator("")
    myRSI = ta.rsi(close, 20)
    plot(barstate.isconfirmed ? myRSI : na)


\`barstate.islastconfirmedhistory\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`barstate.islastconfirmedhistory <https://www.tradingview.com/pine-script-reference/v5/#var_barstate{dot}islastconfirmedhistory>`__ 
is ``true`` if the script is executing on the dataset's last bar when the market is closed, or on the bar immediately preceding the realtime bar if the market is open.

It can be used to detect the first realtime bar with ``barstate.islastconfirmedhistory[1]``, or to postpone server-intensive calculations until the last historical bar, which would otherwise be undetectable on open markets.


Example script
--------------

All historical bars are considered *new* bars. That is because of the fact that the script receives them in a sequential order
from the oldest to the newer ones. For bars that update in realtime, a bar
is considered new only at the opening tick of this bar.

Here is an example of a script using ``barstate.*`` variables::

    //@version=5
    indicator("Bar States", overlay = true)
    first = barstate.isfirst
    last = barstate.islast

    hist = barstate.ishistory
    rt = barstate.isrealtime

    new = barstate.isnew
    conf = barstate.isconfirmed

    t = new ? "new" : conf ? "conf" : "intra-bar"
    t := t + (hist ? "\nhist" : rt ? "\nrt" : "")
    t := t + (first ? "\nfirst" : last ? "\nlast" : "")
    label.new(bar_index, na, yloc=yloc.abovebar, text=t,
              color=hist ? color.green : color.red)

We begin by adding the "Bar States" study to a yearly chart and take a screenshot before any realtime update is received.
This shows the *first* and the *last* bars, and the fact that all bars are *new* ones:

.. image:: images/barstates_history_only.png

When a realtime update is received, the picture changes slightly. The current bar is no longer a historical bar, it has become a realtime bar. Additionally, it is neither *new* nor *confirmed*, which we indicate with the *intra-bar* text in the label.

.. image:: images/barstates_history_then_realtime.png

This is a screenshot of the same symbol at a *1 minute* timeframe, after a few realtime bars have elapsed.
The elapsed realtime bars show the *confirmed* state.

.. image:: images/barstates_history_then_more_realtime.png

.. rubric:: Footnotes

.. [#isconfirmed] Variable ``barstate.isconfirmed`` returns the state of current chart symbol data only.
   It does not take into account any secondary symbol data requested with the ``request.security`` function.
