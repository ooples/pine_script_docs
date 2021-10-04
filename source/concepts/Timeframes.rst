.. _PageTimeframes:

Timeframes
==========

.. contents:: :local:
    :depth: 2



Introduction
------------

The *timeframe* of a chart is sometimes also referred to as its *interval* or *resolution*.
It is the unit of time represented by one bar on the chart.
All standard chart types use a timeframe: "Bars", "Candles", "Hollow Candles", "Line", "Area" and "Baseline".
One non-standard chart type also uses timeframes: "Heikin Ashi".

**Timeframe strings** come into play in a few different context in Pine scripts:

1. They can be used as an argument to `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ and
   `time_close() <https://www.tradingview.com/pine-script-reference/v5/#fun_time_close>`__
   functions, to return the time of a higher timeframe bar. 
   This, in turn, can be used to detect changes in higher timeframes from the chart's timeframe,
   without using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.
   See the :ref:`Testing for changes in higher timeframes <PageTime_TestingForChangesInHigherTimeframes>` section to see how to do this.
2. They must be used in `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
   when requesting data from another symbol or timeframe.
3. The `input.timeframe() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}session>`__ function
   provides a way to allow script users to define a timeframe through a script's "Inputs" tab
   (see the :ref:`Session input <PageInputs_SessionInput>` section for more information).
4. The `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__
   declaration statement has an optional ``timeframe`` parameter that can be used to provide
   multi-timeframe capabilities to simple scripts without using
   `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.
5. The `xxx <https://www.tradingview.com/pine-script-reference/v5/#>`__
In the following sections, we cover the use of timeframes in all these contexts.

Note that:

- Not all user accounts on TradingView have access to extended session information.
- There is no special "session" type in Pine. Session strings are of "string" type,
  but they must conform to the session string syntax.



Timeframe string specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Timeframe strings follow these rules:

- They are composed of the multiplier and the timeframe unit, e.g., "1S", "30" (30 minutes), "1D" (one day), "3M" (three months).
- The unit is represented by a single letter, with no letter used for minutes: "S" for seconds, "D" for days, "W" for weeks and "M" for months.
- When no multiplier is used, 1 is assumed: "S" is equivalent to "1S", "D" to "1D, etc. If only "1" is used, it is interpreted as "1min",
  since no unit letter identifier is used for minutes.
- There is no "hour" unit; "1H" is **not** valid. The correct format for one hour is "60" (remember no unit letter is specified for minutes).
- The valid multipliers vary for each timeframe unit:

    - For seconds, only the discrete 1, 5, 15 and 30 multipliers are valid.
    - For minutes, 1 to 1440 are valid multipliers.
    - For days, 1 to 365 are valid.
    - For weeks, 1 to 52 are valid.
    - For months, 1 to 12 are valid.



