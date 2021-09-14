.. _PageNextSteps:

Next steps
==========

.. contents:: :local:
    :depth: 3

In this page, we explore a bit more of the Pine landscape. We give brief explanations of some fundamental concepts that will be useful to go further than your :ref:`<PageFirstSteps>` and your :ref:`<PageFirstIndicator>`.


Getting around the Pine documentation
-------------------------------------

While reading code from published scripts is no doubt useful, spending time in our documentation will be necessary to attain any degree of proficiency in Pine.
Our two main sources of documentation on Pine are:

- This `Pine User Manual <https://www.tradingview.com/pine-script-docs/en/v5/index.html>`__
- Our `Pine Reference Manual <https://www.tradingview.com/pine-script-reference/v5/>`__

There are five different versions of Pine, so be sure that the documentation you are reading is that of the Pine version you are using.

See 



"indicators" vs "strategies"
----------------------------

Pine :ref:`<PageStrategies>` are used to backtest on historical data and forward test on open markets. 
In addition to indicator calculations, they contain ``strategy.*()`` calls to send trade orders to Pine's broker emulator, which can then simulate their execution.
Strategies display backtest results in the "Strategy Tester" tab at the bottom of the chart, next to the "Pine Editor" tab.

Pine indicators also contain calculations, but cannot be used in backtesting. 
Because they do not make use of the broker emulator, they use less resources and will run faster.
It is thus advantageous to use indicators whenever you can.

Both indicators and strategies can run in either overlay mode (over the chart's bars) or pane mode (in a separate section below or over the chart). Both can also plot information in their respective space, and both can generate :ref:`alert events <PageAlerts>`.

Strategies differ from indicators in how the execute. The  :ref:`<PageStrategies>` page explains how.


How scripts run on charts
------------------------

A Pine script is **not** like many normal programs that execute once and then stop. In the Pine runtime environment, a script runs in the equivalent of an invisible loop where it is executed once on each historical bar. When execution reaches the last, real-time bar, the script executes once every time a price or volume change is detected, then one final time when the real-time bar closes and becomes a historical bar.

By default, Pine *strategies* only execute once at the close of real-time bars, but they can also be instructed to execute on each price change, as *indicators* do. See :doc:`/language/Execution_model`.


Time series
-----------

The main data type used in Pine scripts is called a *series*. It is a continuous list of values that stretches back in time from the current bar and where one value exists for each bar. While this structure may remind many of an array, a Pine series is totally different and thinking in terms of arrays will be detrimental to understanding this key Pine concept. You can read about series :ref:`here <PageTypeSystem_TimeSeries>` and get more information on how to use them :ref:`here <history_referencing_operator>`.


Understanding scripts
---------------------

If you intend to write Pine scripts of any reasonable complexity, a good comprehension of both the Pine execution model and series is essential in understanding how Pine scripts work. If you have never worked with data organized in series before, you will need practice to put them to work for you. When you familiarize yourself with Pine’s fundamental concepts, you will discover that by combining the use of series with our built-in functions designed to efficiently process series information, much can be accomplished in very few lines of Pine code.


Publishing scripts
------------------



Where to go from here?
----------------------

This documentation contains numerous examples of code used to illustrate how functions, variables and operators are used in Pine. By going through it, you will be able to both learn the foundations of Pine and study the example scripts.

The fastest way to learn a programming language is to read about key concepts and try them out with real code. As we’ve just done, copy this documentation’s examples in the Editor and play with them. Explore! You won’t break anything.

You will also find examples of Pine scripts in the Editor’s "Open/New default built-in script" menu, and in TradingView's extensive Public Library of `scripts <https://www.tradingview.com/scripts/>`__ which contains more than 100,000 Pine scripts, many of which are open-source. Enjoy, and welcome to Pine!
