.. _PageNextSteps:

Next steps
==========



"indicator" vs "strategy"
-------------------------
Pine strategies are used to run backtests. In addition to normal script calculations, they also contain ``strategy.*()`` calls to send buy and sell orders to the broker emulator, which can then simulate their execution. See :doc:`/essential/Strategies`.

Pine indicator, as the one in the previous example, also contain calculations, but cannot be used in backtesting. Because they do not make use of the broker emulator, they use less resources and will run faster.

Both strategies and studies can run in either overlay or pane mode, and plot information in that space. Both can also generate alert events. See :doc:`/essential/Alerts`.



Execution model of Pine scripts
-------------------------------

A Pine script is **not** like many normal programs that execute once and then stop. In the Pine runtime environment, a script runs in the equivalent of an invisible loop where it is executed once on each historical bar. When execution reaches the last, real-time bar, the script executes once every time a price or volume change is detected, then one final time when the real-time bar closes and becomes a historical bar.

By default, Pine *strategies* only execute once at the close of real-time bars, but they can also be instructed to execute on each price change, as *indicators* do. See :doc:`/language/Execution_model`.


Series
------
The main data type used in Pine scripts is called a *series*. It is a continuous list of values that stretches back in time from the current bar and where one value exists for each bar. While this structure may remind many of an array, a Pine series is totally different and thinking in terms of arrays will be detrimental to understanding this key Pine concept. You can read about series :ref:`here <PageTypeSystem_TimeSeries>` and get more information on how to use them :ref:`here <history_referencing_operator>`.


Understanding scripts
---------------------
If you intend to write Pine scripts of any reasonable complexity, a good comprehension of both the Pine execution model and series is essential in understanding how Pine scripts work. If you have never worked with data organized in series before, you will need practice in putting them to work for you. When you familiarize yourself with Pine’s fundamental concepts, you will discover that by combining the use of series with our built-in functions designed to efficiently process series information, much can be accomplished in very few lines of Pine code.


Pine Editor
-----------

The Pine Editor is where you will be working on your scripts. To open it, click on the *Pine Editor* tab at the bottom of your TradingView chart. This will open up the editor's window. We will create our first working Pine script. Start by bringing up the “Open” dropdown menu at the top right of the editor and choose *New blank indicator*. Then copy the previous example script, select all code already in the editor and replace it with the example script. Click *Save*, choose a name and then click *Add to Chart*. The MACD indicator will appear in a separate *Pane* under the chart.

From here, you can change the script’s code. For example, change the last line’s ``color.orange`` for ``color.fuchsia``. When you save the script, the change will be reflected in the indicator’s pane. Your first Pine script is running!


Where to go from here?
----------------------

This documentation contains numerous examples of code used to illustrate how functions, variables and operators are used in Pine. By going through it, you will be able to both learn the foundations of Pine and study the example scripts.

The fastest way to learn a programming language is to read about key concepts and try them out with real code. As we’ve just done, copy this documentation’s examples in the Editor and play with them. Explore! You won’t break anything.

You will also find examples of Pine scripts in the Editor’s "Open/New default built-in script" menu, and in TradingView's extensive Public Library of `scripts <https://www.tradingview.com/scripts/>`__ which contains more than 100,000 Pine scripts, many of which are open-source. Enjoy, and welcome to Pine!
