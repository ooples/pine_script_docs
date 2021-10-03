.. _PageChartInformation:

Chart information
=================

.. contents:: :local:
    :depth: 2


Introduction
------------

The way scripts can obtain information about the chart and symbol they are currently running on 
is through a subset of Pine's :ref:`built-in variables <PageBuiltInFunctions_BuiltInVariables>`.
The ones we cover here allow scripts to access information relating to:

- The chart's prices and volume
- The chart's symbol
- The chart's timeframe
- The session (or time period) the symbol trades on



Prices and volume
-----------------

The Pine built-ins for OHLCV values are:

- `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__: the bar's opening price.
- `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__: the bar's highest price,
  or the highest price reached during the realtime bar's elapsed time.
- `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__: the bar's lowest price,
  or the lowest price reached during the realtime bar's elapsed time.
- `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__: the bar's closing price,
  or the current price in the realtime bar.
- `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__: the volume traded during the bar,
  or the volume traded during the realtime bar's elapsed time.

Other values are available through:

- `hl2 <https://www.tradingview.com/pine-script-reference/v5/#var_hl2>`__: 
  the average of the bar's `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ and
  `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ values.
- `hlc3 <https://www.tradingview.com/pine-script-reference/v5/#var_hlc3>`__:
  the average of the bar's `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
  `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
  `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values.
- `ohlc4 <https://www.tradingview.com/pine-script-reference/v5/#var_ohlc4>`__:
  the average of the bar's `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__, 
  `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__,
  `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ and
  `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values.

On historical bars, the values for the above variables do not move because only OHLCV information
is available on them. When running on historical bars, scripts execute on the bars'
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__, 
when all the bar's information is known and cannot change during the script's execution on the bar.

Realtime bars are another story altogether. 
When indicators (or strategies using ``calc_on_every_tick = true``) run in realtime,
the values of the above variables (except `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__)
will vary during the script's execution, because they represent their **current** value on incomplete realtime bar.
This may lead to one form of :ref:`repainting <PageRepainting>`.
See the page on Pine's :ref:`execution model <PageExecutionModel>` for more details.

The `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ :ref:`history-referencing operator <PageOperators_HistoryReferencingOperator>` 
can be used to refer to past values of the built-in variables, e.g., ``close[1]`` refers to the 
value of `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ on the previous bar,
relative to the particular bar the script is executing on.



Symbol information
------------------




Chart timeframe
---------------




Symbol Session
--------------

