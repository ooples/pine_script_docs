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
- `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__: the bar's highest price.
- `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__: the bar's lowest price.
- `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__: the bar's closing price,
  or the current price in the realtime bar.
- `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__: the volume traded during the bar.

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

On historical bars, 

Symbol information
------------------




Chart timeframe
---------------




Symbol Session
--------------

