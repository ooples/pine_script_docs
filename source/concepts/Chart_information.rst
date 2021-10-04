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
  or the **current price** in the realtime bar.
- `volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__: the volume traded during the bar,
  or the volume traded during the realtime bar's elapsed time.
  The unit of volume information varies with the instrument. 
  It is in shares for stocks, in lots for forex, in contracts for futures, in the base currency for crypto, etc.

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

On historical bars, the values of the above variables do not vary during the bar because only OHLCV information
is available on them. When running on historical bars, scripts execute on the bar's
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__, 
when all the bar's information is known and cannot change during the script's execution on the bar.

Realtime bars are another story altogether. 
When indicators (or strategies using ``calc_on_every_tick = true``) run in realtime,
the values of the above variables (except `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__)
will vary between successive iterations of the script on the realtime bar, 
because they represent their **current** value at one point in time during the progress of the realtime bar.
This may lead to one form of :ref:`repainting <PageRepainting>`.
See the page on Pine's :ref:`execution model <PageExecutionModel>` for more details.

The `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ :ref:`history-referencing operator <PageOperators_HistoryReferencingOperator>` 
can be used to refer to past values of the built-in variables, e.g., ``close[1]`` refers to the 
value of `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ on the previous bar,
relative to the particular bar the script is executing on.



Symbol information
------------------

Built-in variables in the ``syminfo`` namespace provide scripts with information on the symbol of the chart
the script is running on. This information changes every time a script user changes the chart's symbol.
The script then re-executes on all the chart's bars using the new values of the built-in variables:

- `syminfo.basecurrency <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}basecurrency>`__:
  the traded currency: "BTC" in "BTCUSD", or "EUR" in "EURUSD".
- `syminfo.currency <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}currency>`__:
  the quote currency: "USD" in "BTCUSD", or "CAD" in "USDCAD".
- `syminfo.description <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}description>`__:
  
- `syminfo.mintick <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}mintick>`__:
  
- `syminfo.pointvalue <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}pointvalue>`__:
  
- `syminfo.prefix <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}prefix>`__:
  
- `syminfo.root <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}root>`__:
  
- `syminfo.session <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}session>`__:
  
- `syminfo.ticker <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}ticker>`__:
  
- `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__:
  
- `syminfo.timezone <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}timezone>`__:
  
- `syminfo.type <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}type>`__:
  
This script will display the values of those built-in variables on the chart::

    //@version=5
    indicator("`syminfo.*` built-ins", "", true)
    printTable(txtLeft, txtRight) => 
        var table t = table.new(position.middle_right, 2, 1)
        table.cell(t, 0, 0, txtLeft, bgcolor = color.yellow, text_halign = text.align_right)
        table.cell(t, 1, 0, txtRight, bgcolor = color.yellow, text_halign = text.align_left)
    
    nl = "\n"
    left =
      "syminfo.basecurrency: "  + nl +
      "syminfo.currency: "      + nl +
      "syminfo.description: "   + nl +
      "syminfo.mintick: "       + nl +
      "syminfo.pointvalue: "    + nl +
      "syminfo.prefix: "        + nl +
      "syminfo.root: "          + nl +
      "syminfo.session: "       + nl +
      "syminfo.ticker: "        + nl +
      "syminfo.tickerid: "      + nl +
      "syminfo.timezone: "      + nl +
      "syminfo.type: "
    
    right =
      syminfo.basecurrency  + nl +
      syminfo.currency      + nl +
      syminfo.description   + nl +
      str.tostring(syminfo.mintick)       + nl +
      str.tostring(syminfo.pointvalue)    + nl +
      syminfo.prefix        + nl +
      syminfo.root          + nl +
      syminfo.session       + nl +
      syminfo.ticker        + nl +
      syminfo.tickerid      + nl +
      syminfo.timezone      + nl +
      syminfo.type
    
    printTable(left, right)



Chart timeframe
---------------




Symbol Session
--------------

