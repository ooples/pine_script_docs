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

Programmers interested in accessing data from multiple timeframes will need to become familiar with how
timeframes are expressed in Pine, and how to use them.

**Timeframe strings** come into play in different contexts:

- They must be used in `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
  when requesting data from another symbol and/or timeframe.
  See the page on :ref:`Other timeframes and data <PageOtherTimeframesAndData>` to explore the use of
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.
- They can be used as an argument to `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ and
  `time_close() <https://www.tradingview.com/pine-script-reference/v5/#fun_time_close>`__
  functions, to return the time of a higher timeframe bar. 
  This, in turn, can be used to detect changes in higher timeframes from the chart's timeframe
  without using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.
  See the :ref:`Testing for changes in higher timeframes <PageTime_TestingForChangesInHigherTimeframes>` section to see how to do this.
- The `input.timeframe() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}session>`__ function
  provides a way to allow script users to define a timeframe through a script's "Inputs" tab
  (see the :ref:`Timeframe input <PageInputs_TimeframeInput>` section for more information).
- The `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__
  declaration statement has an optional ``timeframe`` parameter that can be used to provide
  multi-timeframe capabilities to simple scripts without using
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.
- Many built-in variables provide information on the timeframe used by the chart the script is running on.
  See the :ref:`Chart timeframe <PageChartInformation_ChartTimeframe>` section for more information on them,
  including `timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__
  which returns a string in Pine's timeframe specification format.



Timeframe string specifications
-------------------------------

Timeframe strings follow these rules:

- They are composed of the multiplier and the timeframe unit, e.g., "1S", "30" (30 minutes), "1D" (one day), "3M" (three months).
- The unit is represented by a single letter, with no letter used for minutes: "S" for seconds, "D" for days, "W" for weeks and "M" for months.
- When no multiplier is used, 1 is assumed: "S" is equivalent to "1S", "D" to "1D, etc. If only "1" is used, it is interpreted as "1min",
  since no unit letter identifier is used for minutes.
- There is no "hour" unit; "1H" is **not** valid. The correct format for one hour is "60" (remember no unit letter is specified for minutes).
- The valid multipliers vary for each timeframe unit:

    - For seconds, only the discrete 1, 5, 15 and 30 multipliers are valid.
    - For minutes, 1 to 1440.
    - For days, 1 to 365.
    - For weeks, 1 to 52.
    - For months, 1 to 12.



Comparing timeframes
--------------------

It can be useful to compare different timeframe strings to determine,
for example, if the timeframe used on the chart is lower than the higher timeframes used in the script,
as using timeframes lower than the chart is usually not a good idea.
See the :ref:`Requesting data of a lower timeframe <PageOtherTimeframesAndData_RequestingDataOfALowerTimeframe>` section
for more information on the subject.

Converting timeframe strings to a representation in fractional minutes provides a way to compare them
using a universal unit. This script uses the ``tfInMinutes()`` function to convert a timeframe into float minutes::

    //@version=5
    indicator("", "", true)
    string tfInput = input.timeframe("")
    
    tfInMinutes(simple string tf = "") => 
        float chartTf =
          timeframe.multiplier * (
          timeframe.isseconds ? 1. / 60             :
          timeframe.isminutes ? 1.                  :
          timeframe.isdaily   ? 60. * 24            :
          timeframe.isweekly  ? 60. * 24 * 7        :
          timeframe.ismonthly ? 60. * 24 * 30.4375  : na)
        float result = tf == "" ? chartTf : request.security(syminfo.tickerid, tf, chartTf)
    
    float chartTFInMinutes = tfInMinutes()
    float inputTFInMinutes = tfInMinutes(tfInput)
    
    printTable(txt) => var table t = table.new(position.middle_right, 1, 1), table.cell(t, 0, 0, txt, bgcolor = color.yellow)
    printTable(
      "Chart TF: "    + str.tostring(chartTFInMinutes, "#.##### minutes") +
      "\n`tfInput`: " + str.tostring(inputTFInMinutes, "#.##### minutes"))
    
    if chartTFInMinutes > inputTFInMinutes
        runtime.error("The chart's timeframe nust not be higher than the input's timeframe.")
    
Note that:

- We define the single parameter of our ``tfInMinutes()`` function using ``simple string tf = ""``.
  This allows the compiler to restrict its argument to the "simple string" form-type,
  which ensures it will work as an argument for the ``timeframe`` parameter in our
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call.
  It also says that if no argument is supplied for our ``tf`` parameter, an empty string will be used as its default value.
  This will cause the function's logic to return the chart's timeframe in minutes.
- We use two calls to ``tfInMinutes()`` in the initialization of the ``chartTFInMinutes`` and ``inputTFInMinutes`` variables.
  In the first instance we do not supply an argument for its ``tf`` parameter, so the function returns the chart's timeframe in minutes.
  In the second call we supply the timeframe selected by the script's user through the call to
  `input.timeframe() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}session>`__.
  Note that the ``tfInMinutes()`` function produces a "series float" value, 
  which entails its result cannot be transformed in a tiemframe string for use with
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__,
  as its ``timeframe`` parameter requires a "simple string".
  See the page on Pine's :ref:`Type system <PageTypeSystem>` for more information on Pine forms and types.
- Then we validate the timeframes to ensure that the input timeframe is equal to or higher than the chart's timeframe.
  If it is not, we generate a runtime error.
- We finally print the two timeframe values converted to minutes.
