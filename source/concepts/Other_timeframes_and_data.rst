.. _PageOtherTimeframesAndData:

.. image:: /images/Pine_Script_logo_small.png
   :alt: Pine Script™
   :target: https://www.tradingview.com/pine-script-docs/en/v5/index.html
   :align: right
   :width: 50
   :height: 50

Other timeframes and data
=========================

.. contents:: :local:
    :depth: 3



Introduction
------------

The functions we present here all fetch data from other sources than the chart the script is running on.
That data can be:

- From other another symbol, timeframe or context, with `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.
- Financial data from `FactSet <https://www.factset.com/>`__, with `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__.
- Dividends, earnings and splits information from the exchange, with
  `request.dividends() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}dividends>`__,
  `request.earnings() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}earnings>`__ or
  `request.splits() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}splits>`__.
- Information from the `NASDAQ Data Link (formerly Quandl) <https://data.nasdaq.com/search>`__, 
  with `request.quandl() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}quandl>`__.

These are the signatures of the functions in the ``request`` namespace:

.. code-block:: text

    request.security(symbol, timeframe, expression, gaps, lookahead, ignore_invalid_symbol, currency) → series int/float/bool/color

    request.financial(symbol, financial_id, period, gaps, ignore_invalid_symbol, currency) → series float
    
    request.dividends(ticker, field, gaps, lookahead, ignore_invalid_symbol, currency) → series float
    request.earnings(ticker, field, gaps, lookahead, ignore_invalid_symbol, currency) → series float
    request.splits(ticker, field, gaps, lookahead, ignore_invalid_symbol, currency) → series float
    
    request.quandl(ticker, gaps, index, ignore_invalid_symbol, currency) → series float

Functions in the ``request.*()`` family have many different applications, and their use can be rather involved.
Accordingly, this page is quite lengthy.



.. _PageOtherTimeframesAndData_CommonCharacteristics:

Common characteristics
----------------------

Many of the functions in the ``request`` namespace share common properties and parameters.
Before exploring each function in detail, let's go over their common characteristics.



Use
^^^

While the ``request.*()`` functions return "series" results, which means their result can change on every bar,
their parameters require arguments of either "const" or "simple" form, 
wich entails they must be known at either compile time or when the script begins execution on bar zero.
This **also** entails that, except for the ``expression`` parameter in `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
which allows a "series" argument, the arguments of ``request.*()`` function calls cannot vary during the execution of a script, e.g.:

- The argument used for the ``symbol`` parameter in a `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
  call must be a "simple string". This means is can be determined through the script's inputs, but it cannot then change on the script's last bar, for example.
  The same goes for its ``timeframe`` parameter.
- All the other `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ parameters except ``expression``, i.e.,
  ``gaps``, ``lookahead``, ``ignore_invalid_symbol`` and ``currency``, require a "const" argument,
  which means it must be known at compile time and cannot be determined through inputs.
- ``request.*()`` functions cannot be used in local blocks of either conditional structures or loops, nor in library functions.
  They can be used in user-defined functions.

Think of ``request.*()`` function calls as requiring to be executable on bar zero and not varying during the script's execution on all bars.
You can make multiple calls in one script and choose which result you will use based on "series" criteria that may vary bar to bar,
but all the necessary calls whose results you will be selecting from will need to have been previously made by the script, available for picking among them.

Because of the fact that one cannot turn ``request.*()`` function calls on or off during the script's execution,
the only way to improve the performance of scripts using such functions is to minimize the number of different calls defined in the script.
While a maximum of 40 calls can be made in any given script, programmers should strive to minimize the quantity of calls,
as they have a sizable impact on script performance.



.. _PageOtherTimeframesAndData_Gaps:

\`gaps\`
^^^^^^^^

All the ``request.*()`` functions include the ``gaps`` parameter in their signature.
*Gaps* are `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ values
(see the :ref:`section on \`na\` <PageTypeSystem_NaValue>` if you are not familiar with it).

A script running on a 60min chart has access to prices such as `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
on each bar of the chart. When retrieving data from other contexts, however, new values for that data may not be coming in for each new bar on the chart.
When fetching daily data on our 60min chart, for example, new data will not be coming in on every chart bar. 
A choice must thus be made as to how the data from the outside context will be *merged* on chart bars.
That behavior is what the ``gaps`` parameter controls.

When functions do not return a value on each of the chart bars the calling script is running on,
one must determine if the function should return `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ values in those cases 
(`barmerge.gaps_on <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}gaps_on>`__),
or the latest non-`na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ value returned by the function
(`barmerge.gaps_off <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}gaps_off>`__).

In cases where no gaps are allowed, the last non-`na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ value
will repeat on chart bars until a new value comes in. This shows the diffence between using gaps or not:

.. image:: images/OtherTimeframesAndData-Gaps-01.png

::

    //@version=5
    indicator("gaps", "", true)
    noGaps = request.security(syminfo.tickerid, "1", close)
    withGaps = request.security(syminfo.tickerid, "1", close, gaps = barmerge.gaps_on)
    plot(noGaps, "noGaps", color.blue, 3, plot.style_linebr)
    plot(withGaps, "withGaps", color.fuchsia, 12, plot.style_linebr)
    bgcolor(barstate.isrealtime ? #00000020 : na)

Note that:

- We are requesting the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ value
  from the chart's symbol at the 1min timeframe, so we are viewing a 5sec chart to display higher timeframe values.
- We plot both our lines using the `plot.style_linebr <https://www.tradingview.com/pine-script-reference/v5/#var_plot{dot}style_linebr>`__ style
  because it does not bridge over `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ values,
  like the `plot.style_line <https://www.tradingview.com/pine-script-reference/v5/#var_plot{dot}style_line>`__ style would.
  This way we can distinguish between bars where a value is returned, and others where `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ is returned.
- The blue line plotting ``noGaps`` shows no gaps. We initialize ``noGaps`` using a `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
  call that does not specify a value for the ``gaps`` parameter, so the default
  `barmerge.gaps_off <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}gaps_off>`__ is used.
- The fuchsia line plotting ``withGaps`` shows gaps.
- New values for the higher timeframe come in at the same time, whether we use gaps or not.


\`ignore_invalid_symbol\`
^^^^^^^^^^^^^^^^^^^^^^^^^

All the ``request.*()`` functions include the ``ignore_invalid_symbol`` parameter in their signature.
The parameter's values can be ``true`` or ``false`` (the default).
It controls the behavior of functions when they are used with arguments that cannot produce valid results, e.g.:

- The symbol or ticker doesn't exist.
- There is no financial information available for a symbol used with 
  `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__, 
  (as is the case for crypto, forex or derivative instruments). 
  This will also be the case when information for the particular ``period`` requested is not available.

When the default ``ignore_invalid_symbol = false`` is used, a runtime error will be generated and the script will stop when no result can be returned.
When ``ignore_invalid_symbol = true`` is used, rather than throwing a runtime error, the function will return `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__.

This script demonstrates how to use ``ignore_invalid_symbol = true`` to handle invalid results when requesting
the shares outstanding for stocks. It will only display information on instruments where valid data can be obtained:

.. image:: images/OtherTimeframesAndData-IgnoreValidSymbol-01.png

::

    //@version=5
    indicator("", "", true)
    printTable(txt) => var table t = table.new(position.middle_right, 1, 1), table.cell(t, 0, 0, txt, bgcolor = color.yellow, text_size = size.huge)
    TSO = request.financial(syminfo.tickerid, "TOTAL_SHARES_OUTSTANDING", "FQ", ignore_invalid_symbol = true) 
    MarketCap = TSO * close
    if not na(MarketCap) and barstate.islast
        txt = "Market cap\n" + str.tostring(MarketCap, format.volume) + " " + syminfo.currency
        printTable(txt)

Note that:

- We use ``ignore_invalid_symbol = true`` in our 
  `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__ call.
  This will produce `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ results when the function cannot return a valid value.
- We use the ``TSO`` value to calculate the stock's ``MarketCap``.
- The ``not na(MarketCap)`` condition prevents us from displaying anything when ``TSO`` 
  — and thus ``MarketCap`` — is `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__.
- The ``barstate.islast`` condition ensures we only make a call to ``printTable(txt)`` on the chart's last bar.
  It would be inefficient to call it on each bar.
- We format the displayed string and assign its content to the ``txt`` variable.
  ``"Market cap\n"`` is our legend, with a newline character. 
  ``str.tostring(MarketCap, format.volume)`` converts the ``MarketCap`` "float" value to a string, formatting it like volume, by abbreviating large values.
  Adding ``syminfo.currency`` provides script users with the instrument's quote currency.
  In our example, Tencent is traded on HKEX, Hong Kong's stock exchange, so the currency is HKD, the Hong Kong dollar.
- We use a :ref:`table <PageTables>` to display our script's output. Our ``printTable()`` function declared just after our script's
  `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__ declaration statement handles the table code.



\`currency\`
^^^^^^^^^^^^

All the ``request.*()`` functions also include the ``currency`` parameter in their signature.
It allows conversion of the value returned by the function to another currency.
The currency being converted **from** is the symbol's quote currency, i.e., `syminfo.currency <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}currency>`__,
which is determined by the exchange it trades on.
The currency being converted **to** is the value used for the ``currency`` parameter, 
which can be any currency in the `ISO 4217 format <https://en.wikipedia.org/wiki/ISO_4217#Active_codes>`__,
or one of the currency built-ins in the ``currency.XXX`` format, such as `currency.JPY <https://www.tradingview.com/pine-script-reference/v5/#var_currency{dot}JPY>`__.

The conversion rates used are based on the FX_IDC pairs' daily rates of the previous day, relative to the bar where the calculation occurs.
When no instrument exists to determine a particular pair's conversion rate, a spread is used. For example, to convert ZAR to USD, 
the ``ZARUSD*USDHKD`` spread would be used, as there is no instrument providing a ``ZARUSD`` rate.

.. note:: Not all values returned by ``request.*()`` functions may be in currency, so it does not always make sense to convert them into another currency.
   When requesting financial information with `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__
   or `request.quandl() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}quandl>`__
   for example, many of the values are ratios, or expressed in other units than currency, such as ``PIOTROSKI_F_SCORE`` or ``NUMBER_OF_EMPLOYEES``.
   It is the programmer's responsibility to determine when currency conversion is applicable.



.. _PageOtherTimeframesAndData_Lookahead:

\`lookahead\`
^^^^^^^^^^^^^

The ``lookahead`` parameter controls whether future data is returned by the 
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__,
`request.dividends() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}dividends>`__,
`request.earnings() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}earnings>`__ and
`request.splits() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}splits>`__ functions.
In order to avoid *future leak*, or *lookahead bias*, which produces unrealistic results, **it should generally be avoided — or treated with extreme caution**.
``lookahead`` is only useful in special circumstances, when it doesn't compromise the integrity of your script's logic, e.g.:

- When used with an offset on the series (such as ``close[1]``), to produce non-repainting
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ calls.
- When retrieving the underlying, normal chart data from non-standard charts.
- When using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
  at intrabar timeframes, i.e., timeframes lower than the chart's.

The parameter only affects the script's behavior on historical bars, as there are no future bars to look forward to in realtime, where the future is unknown — as it should.

.. note:: Using ``lookahead = barmerge.lookahead_on`` when fetching price information, or calculations depending on prices, causes future leak,
   which means your script is using future information it should **not** have access to.
   Except in rare cases, this is a very bad idea. Using ``request.*()`` functions this way is misleading, and not allowed in script publications.
   It is considered a serious violation of `Script publishing rules <https://www.tradingview.com/house-rules/?solution=43000590599>`__, 
   so it is your responsability, if you publish scripts, to ensure you do not mislead users of your script by using future information on historical bars.
   While your plots on historical bars will look great because your script will magically acquire prescience (which will not reproduce in realtime, by the way),
   you will be misleading users of your scripts — and yourself.

The default value for ``lookahead`` is `barmerge.lookahead_off <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}lookahead_off>`__.
To enable it, use `barmerge.lookahead_on <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}lookahead_on>`__.

This example shows why using ``lookahead = barmerge.lookahead_on`` to fetch price information can be so dangerous.
We retrieve the 1min `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ from a 5sec chart
and show the difference in results between using 
`barmerge.lookahead_on <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}lookahead_on>`__ (bad, in red) and
`barmerge.lookahead_off <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}lookahead_off>`__ (good, in gray):

.. image:: images/OtherTimeframesAndData-Lookahead-01.png

::

    //@version=5
    indicator("lookahead", "", true)
    lookaheadOn  = request.security(syminfo.tickerid, '1', high, lookahead = barmerge.lookahead_on)
    lookaheadOff = request.security(syminfo.tickerid, '1', high, lookahead = barmerge.lookahead_off)
    plot(lookaheadOn,  "lookaheadOn", color.new(color.red, 60), 6)
    plot(lookaheadOff, "lookaheadOff",  color.gray, 2)
    bgcolor(barstate.isrealtime ? #00000020 : na)

Note that:

- The red line shows the result of using lookahead. The black line does not use it.
- On historical bars, the red line is showing the 1min highs before they actually occur (see #1 and #2, where it is most obvious).
- In realtime (the bars after #3 with the silver background), there is no difference between the plots because there are no futures bars to look into.

.. note:: In Pine Script™ v1 and v2, ``security()`` did not include a ``lookahead`` parameter, but it behaved as it does in later versions of Pine Script™
   with ``lookahead = barmerge.lookahead_on``, which means it was systematically using future data. 
   Scripts written with Pine Script™ v1 or v2 and using ``security()`` should therefore be treated with caution, unless they offset the series fetched, e.g., using ``close[1]``.



\`request.security()\`
----------------------

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
function is used to request data from other contexts than the chart's. Those different contexts may be:

- Other symbols
- Spreads
- Other timeframes (see the page on :ref:`Timeframes <PageTimeframes>` to timeframe specifications in Pine Script™)
- Other chart types (see the page on :ref:`Non-standard chart data <PageNonStandardChartsData>`)
- Other chart types or sessions, through ``ticker.*()`` functions
  (see this page's :ref:`Other contexts, with \`ticker.new()\` <PageOtherTimeframesAndData_OtherContextsWithTickerNew>` section)

The function's signature is:

.. code-block:: text

    request.security(symbol, timeframe, expression, gaps, lookahead, ignore_resolve_errors, currency) → series int/float/bool/color/string
    request.security(symbol, timeframe, expression, gaps, lookahead, ignore_resolve_errors, currency) → series int[]/float[]/bool[]/color[]/string[]

``symbol``
   This is the ticker identifier of the symbol whose information is to be fetched. It must be of "simple string" type and can be defined in multiple ways:

      - With a literal string containing either a simple ticker like ``"IBM"`` or ``"EURUSD"``, 
        or an exchange:symbol pair like ``"NYSE:IBM"`` or ``"OANDA:EURUSD"``.
        When an exchange is not provided, a default exchange will be used when it is possible.
        You will obtain more reliable results by specifying the exchange.
      - Using the `syminfo.ticker <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}ticker>`__ or
        `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__ built-in variables,
        which respectively return only the ticker or the exchange:ticker information of the chart's symbol.
        It is recommended to use `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__ 
        to avoid ambiguity. See the :ref:`Symbol information <PageChartInformation_SymbolInformation>` section for more information.
        Note that an empty string can also be supplied as a value, in which case the chart's symbol is used.
      - Spreads can also be used, e.g., ``"AAPL/BTCUSD"`` or ``"ETH/BTC"``. Note that spreads will not replay in "Replay mode".
      - A ticker identifier created using `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__,
        which provides access to data from non-standard charts, extended hours or other contexts
        (see the :ref:`Other contexts, with \`ticker.new()\` <PageOtherTimeframesAndData_OtherContextsWithTickerNew>` section of this page).

``timeframe``
   This is a "simple string" in :ref:`timeframe specifications <PageTimeframes>` format.
   The timeframe of the main chart's symbol is stored in the
   `timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__
   built-in variable.
   
``expression``
   This can be a "series int/float/bool/color" variable, expression, function call or tuple.
   It is the value that must be calculated in `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__'s
   context and returned to the script.
   For more details, see the :ref:`Information requested <PageOtherTimeframesAndData_InformationRequested>` section later in this page.

This script uses `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
to fetch the `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ and
`low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ values of a user-defined symbol and timeframe:

.. image:: images/OtherTimeframesAndData-RequestSecurity()-01.png

::

    //@version=5
    indicator("Symbol/TF")
    symbolInput = input.symbol("", "Symbol & timeframe", inline = "1")
    tfInput = input.timeframe("", "", inline = "1")
    
    [hi, lo] = request.security(symbolInput, tfInput, [high, low])
    
    plot(hi, "hi", color.lime, 3)
    plot(lo, "lo", color.fuchsia, 3)
    plotchar(ta.change(time(tfInput)), "ta.change(time(tfInput))", "•", location.top, size = size.tiny)
    plotchar(barstate.isrealtime, "barstate.isrealtime", "•", location.bottom, color.red, size = size.tiny)

Note that:

- As is revealed by the input values showing to the right of the script's name on the chart, we are viewing higher timeframe
  information from the same symbol as the chart's at 1min, but from the 5min timeframe.
- The lime line plots highs and the fuchsia line plots lows.
- We plot a blue dot when the higher timeframe change is detected by the script.
- On historical bars (those without a red dot at the bottom), new values come in on the higher timeframe's last chart bar.
  Point #1 shows the value for the 03:15 5min timeframe coming in at the close of the 03:19 bar 
  (keep in mind that scripts execute on the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ of historical bars).
- On realtime bars, the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ values
  fluctuate with incoming data from the higher timeframe. At point #2, a new higher timeframe begins at 03:30,
  so the `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ of that bar, which was fluctuating during the bar,
  becomes the current `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ value for the higher timeframe bar.
  That value, however, is uncertain because it could be superceded by any lower `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__
  coming in further realtime bars, until the close of the 03:34 bar. As it happens, none does, 
  so the fuchsia line stays the same across the remaining realtime bars, until the 03:35 bar brings in a new higher timeframe bar.
  During that 03:30 5min timeframe, we can see the lime line (#3) fluctuating, as higher highs are made on successive bars.
  This reveals the repainting behavior of a `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
  call on realtime bars.
- Our inputs appear on a single line in the "Settings/Inputs" tab because we use ``inline = "1"`` in both ``input.*()`` calls.
- One `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call
  fetches both `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ and
  `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ values by using a :ref:`tuple <PageTypeSystem_Tuples>`.



Timeframes
^^^^^^^^^^

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
function makes it possible for scripts to request data from other timeframes than the one the chart is running on,
which can be done while also accessing another symbol, or not. 
When another timeframe is accessed, it can be:

- Higher than the chart's (accessing 1D data from a 60min chart)
- Lower (accessing a 1min timeframe from a 60min chart)
- The same timeframe as the chart's 
  (when `timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__ or an empty string is used)

The behavior of `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
when accessing higher and lower timeframes is very different. We assume in our discussions that higher timeframes are accessed,
but we also discuss the special cases when :ref:`lower timeframes are accessed <PageOtherTimeframesAndData_RequestingDataFromALowerTimeframe>`
in a dedicated section.

Scripts not written specifically to use lower timeframe data, when they are published for a broader audience,
should ideally include protection against running them on chart timeframes where 
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
would be accessing lower timeframes than the chart's, as it will not produce reliable results in those cases.
See the :ref:`Comparing timeframes <PageTimeframes_ComparingTimeframes>` section for a code example 
providing error-checking to avoid just that.



Data feeds
^^^^^^^^^^

Different data feeds supplied by exchanges/brokers can be used to display information about an instrument on charts:

- Intraday historical data (for timeframes < 1D)
- End-of-day (EOD) historical data (for timeframes >= 1D)
- Realtime feed (which may be delayed, depending on your type of account and the extra data services you may have purchased)
- Extended hours data (which may be available or not, depending on instruments and the type of account you hold on TradingView)

Not all of these types of feed may exist for every instrument. "ICEEUR:BRN1!" for example, only has EOD data.

For some instruments where both intraday and EOD historical feeds exist, volume data will not be the same because some trades (block trades, OTC trades, etc.) 
may only be reported at the end of the day. That volume will thus appear in the EOD feed, but not in the intraday feed. 
Differences in volume data are almost inexistent in the crypto sector, but commonplace in stocks.

Slight prices discrepancies may also occur between both feeds, such that the `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ 
for one day's bar on the EOD feed may not match any of the `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ values of intraday bars for that day.

Another distinction between intraday and EOD feeds is that EOD feeds do not contain data from extended hours.

These differences may account for variations in the values fetched by 
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
when it is accessing data from varying timeframes, thus shifting between intraday and EOD feeds.
The differences may also cause discrepancies between data received in realtime vs the way it is reported on historical data.
There are no steadfast rules about the variations. 
To understand their details, one must consult the exchange/broker information on the feeds available for each of their markets.
As a rule, TradingView does not generate data; it relies on its data providers for the information displayed on charts.



.. _PageOtherTimeframesAndData_InformationRequested:

Information requested
^^^^^^^^^^^^^^^^^^^^^

The data fetched using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
is specified with the ``expression`` parameter. It can be of types "int", "float", "bool", "color", or an "array". Strings are thus not allowed.

The expression supplied to `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
can be:

- An array
- A built-in variable or function, such as `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__ or
  `ta.crossover() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}crossover>`__
- A variable previously calculated by your script, which will then be recalculated in
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__'s context
- A user-defined function call
- A tuple


Arrays
""""""

One relatively new feature on Pine Script™ is the inclusion of arrays which we will go over in depth in a separate article. In short, arrays
are a fairly complicated topic so not a recommended area to cover for a new Pine Script™ programmer. They are special data structures that are
one-dimensional and can be used to hold a collection of multiple values. 

  //@version=5
  indicator("New 60 Minute Highs")
  var highs = array.new_float(0)

  if ta.rising(high, 1)
      array.push(highs, high)
    
  src = request.security('AAPL', '60', highs)
  float[] srcArray = array.copy(src)
  plot(array.size(srcArray) > 0 ? array.pop(srcArray) : na)

Note that we are initializing an array at the first index by using the var keyword and adding new 2 bar highs to this array as they
appear. We use this array structure in a security function so we can easily use a custom timeframe like **60 minutes** in our example.
This allows us to use this same array format to use in a security call in combination with any timeframe.


Built-ins
"""""""""

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function is extremely
versatile and can easily be used in combination with one of TradingView's many built-in indicators. A common use case would be
to plot different timeframes of a built-in indicator on the same chart. 

Consider for example you are on a 5 minute chart and want to plot the 20 period SMA for the 1 day timeframe you might try the following::

  src = request.security('AAPL', '1D', close)
  sma = ta.sma(src, 20)

This would actually give you incorrect output because when you are on a lower timeframe, the security function would probably return
20 copies of the same daily bar since the current timeframe most likely falls on the same day. What you would want to do instead is pass in the built-in
indicator directly into the security call and allow TradingView to calculate it properly on their end by doing the following instead::

  sma = request.security('AAPL', '1D', ta.sma(close, 20))

Here is an example showing how you can easily plot a built-in indicator such as RSI 
for both the 5 minute and 30 minute timeframes on the same chart::

    //@version=5
    indicator("Relative Strength Index MTF", "RSI")
    sym = input.symbol('AAPL')
    rsi1 = request.security(sym, '5', ta.rsi(close, 14))
    rsi2 = request.security(sym, '30', ta.rsi(close, 14))
    plot(rsi1, color=color.red)
    plot(rsi2, color=color.blue)


Calculated variables
""""""""""""""""""""

One can declare the following variable::

    spread = high - low

and calculate it at *1 minute*, *15 minutes* and *60 minutes*::

    spread_1 = request.security(syminfo.tickerid, '1', spread)
    spread_15 = request.security(syminfo.tickerid, '15', spread)
    spread_60 = request.security(syminfo.tickerid, '60', spread)

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function
returns a series which is then adapted to the time scale of
the current chart's symbol. This result can be either shown directly on
the chart (i.e., with ``plot``), or used in further calculations.
The "Advance Decline Ratio" script illustrates a more
involved use of `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__::

    //@version=5
    indicator("Advance Decline Ratio", "ADR")
    ratio(t1, t2, source) =>
        s1 = request.security(t1, timeframe.period, source)
        s2 = request.security(t2, timeframe.period, source)
        s1 / s2
    plot(ratio("USI:ADVN.NY", "USI:DECL.NY", close))

The script requests two additional securities. The results of the
requests are then used in an arithmetic formula. As a result, we have a
stock market indicator used by investors to measure the number of
individual stocks participating in an upward or downward trend.


Function calls
""""""""""""""

A more advanced way of using the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function
would be to pass in a user defined function into the ``expression`` parameter. This would allow you to create a custom function and then
use this function to plot the results for different timeframes or for different symbols on the same chart. Keep in mind that the same limitations
for security functions apply when using function calls, so for example you wouldn't be able to use a custom function that returns a string.

    //@version=5
    indicator("`request.security()` User Defined Function Example")

    f_udf(_src, _length, _lbLength) =>
        uCount = 0, dCount = 0
        for i = 0 to _length - 1 by 1
            uCount += (nz(_src[i]) > nz(src[i + _lbLength]) ? 1 : 0)
            dCount += (nz(_src[i]) < nz(src[i + _lbLength]) ? 1 : 0)
        [uCount, dCount]

    [upCount, dnCount] = f_udf(close, 9, 4)
    sym = input.symbol('AAPL')
    // We are using a blank string for the timeframe so it defaults to the current timeframe
    plot(request.security(sym, ' ', upCount)
    plot(request.security(sym, ' ', dnCount)

Note that: this is a bit more complicated example that plots the sum amount of bars that were higher than X bars ago and vice versa. We are using a 
user defined function to create a tuple with our output which is the sum of up bars and the sum of down bars. We pass in a variable
from the tuple and Pine Script™ handles the heavy lifting for us.


Tuples
""""""

Tuples are a special data structure that is immutable (meaning it can't be changed once it is created). They can be used to combine different variables
into a single variable that you can reference much easier and using fewer lines of code. This is very handy for use cases where
you would like to declare a variable once and then reference it multiple times such as the following::

  //@version=5
  indicator("`request.security()` Tuple Example")
  [h5, l5] = request.security('AAPL', '5', [high, low])
  plot(math.avg(h5, high))
  plot(math.avg(l5, low))
  plot(math.avg(h5, l5))

Note that: we are creating a tuple variable using a request security function and we set the ``expression`` parameter to a tuple containing
the 5 minute timeframe ``high`` and ``low``. We are then plotting the average of the current timeframe and the aforementioned 5 minute timeframe
as well as the midpoint of our tuple values.


.. _PageOtherTimeframesAndData_OtherContextsWithTickerNew:

Other contexts, with \`ticker.new()\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. TODO write about syminfo.tickerid in extended format and function tickerid
`ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__,
        which allows access to :ref:`Non-standard chart data <PageNonStandardChartsData>` or :ref:`other sessions <PageSessions_UsingSessionsWithRequestSecurity>`



Historical vs realtime values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The behavior of `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
on historical and realtime bars is not the same. On historical bars, new values come in at the 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ of the last chart bar in the higher timeframe bar.
Values then do not move until another timeframe completes, which accounts for the staircase effect of higher timeframe values. 
In realtime, however, `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
will return the **current** value of the incomplete higher timeframe bar, which causes it to vary during a realtime bar,
and accross all bars until the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__
of the last realtime bar marking the end of the higher timeframe bar, at which point its value is final.

These fluctuating values of `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
values in realtime can sometimes be just what is needed by a script's logic — if it using volume information, for example,
and needs the current volume transacted at the current point in time of the incomplete higher timeframe bar.
Fluctuating values are also called *repainting* values.

In other circumstances, for example when a script is using higher timeframe information to provide a broader context to the script
executing on a lower timeframe, one will often need confirmed and stable — as opposed to fluctuating — higher timeframe values.
These are called *non-repainting* values because they are fixed values from a the previously **completed** higher timeframe bar only.



Avoiding repainting
^^^^^^^^^^^^^^^^^^^

In general, ``barmerge.lookahead_on`` should only be used when the series is offset, as when you want to avoid repainting::

    //@version=5
    //...
    a = request.security(syminfo.tickerid, 'D', close[1], lookahead = barmerge.lookahead_on)

If you use ``barmerge.lookahead_off``, a non-repainting value can still be achieved, but it's more complex::

    //@version=5
    //...
    indexHighTF = barstate.isrealtime ? 1 : 0
    indexCurrTF = barstate.isrealtime ? 0 : 1
    a0 = request.security(syminfo.tickerid, 'D', close[indexHighTF], lookahead = barmerge.lookahead_off)
    a = a0[indexCurrTF]

When an indicator is based on historical data (i.e.,
``barstate.isrealtime`` is ``false``), we take the current *close* of
the daily timeframe and shift the result of `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
function call one bar to the right in the current timeframe. When an indicator is calculated on
realtime data, we take the *close* of the previous day without shifting the
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ data.



.. _PageOtherTimeframesAndData_RequestingDataFromALowerTimeframe:

Requesting data from a lower timeframe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

\`request.security_lower_tf()\`
-------------------------------

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
function was designed to request data of a timeframe *higher*
than the current chart timeframe. On a *60 minutes* chart,
this would mean requesting 240, D, W, or any higher timeframe.

However if you are on a *60 minutes* chart and want to use the data from the *1 minute* bars, you would need
to specifically use the new `request.security_lower_tf() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security_lower_tf>`__
function. If you were to use the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
function in our example you would actually only get the final minute bar for the last hour since ``barmerge.lookahead_off`` is the default.
If you were to use ``barmerge.lookahead_on`` then you would get the first minute bar instead. 

This is why we added the `request.security_lower_tf() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security_lower_tf>`__
function so you will now receive an array containing all of the minute bars in the last hour as per our example. The returned array will contain
all of the available intrabars sorted by the timestamp in ascending order. However if you were to request a lower timeframe that is equal or 
higher than the current timeframe, you would get a runtime error. You can now do further calculations on this array as per our example below.

  //@version=5
  indicator("`request.security_lower_tf()` Example")
  float travel = math.abs(high - low)
  float[] ltfTravelArray = request.security_lower_tf(syminfo.tickerid, "1", travel)
  float volatility = nz(array.sum(ltfTravelArray) / travel)
  plot(volatility)

Note that:
  - There is a max of 40 function calls allowed in a script
  - The amount of intrabars will vary based on the chart's timeframe as well as the underlyingg instrument or sector so you may expect 60 intrabars returned 
  but receive a smaller amount.
  - We are calculating volatility in this example by comparing the absolute sum of high - low in the lower timeframe to the current timeframe of high - low.
  - Tuples are not allowed currently in the *expression* parameter and you will receive an error if you try to use a tuple.
  - You must use a lower timeframe than the chart timeframe so the same timeframe or a higher timeframe will throw an error.
  - This function only works on chart timeframes higher than *1 minute* or else a runtime error will occur.
  - A maximum of 100K total intrabars can be accessed by a script. This means that on a 24x7 market you have a max of 1440 intrabars per chart bar, 
  so will only see values for the last ~70 days because: 70 days * 24 hours * 60 minutes ═ 100,800 minutes.

Fetching standard prices from a non-standard chart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


\`request.economic()\`
----------------------

This function returns economic data for a given country or region (i.e. US or EU). Economic data includes information such as the state of a country's economy 
(GDP, inflation rate, etc.) or of a particular industry (steel production, ICU beds, etc.).

The signature of `request.economic() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}economic>`__ is: 

.. code-block:: text

    request.economic(country_code, field, gaps, ignore_invalid_symbol) → series float

We have covered the last two parameters in the :ref:`Common characteristics <PageOtherTimeframesAndData_CommonCharacteristics>` section of this page.
The first two parameters require a "simple string" argument. They are:

``country_code``
   This is the identifier for the country or region that you want to request economic data for such as "US" or "EU". 
   A full list of countries/regions and their codes can be found `here <https://www.tradingview.com/chart/?solution=43000665359>`__ and please note that
   the available metrics will depend on the country or region selected.

``field``
   This is the identifier of the required metric. We have a full list of the available metrics along with the list of countries that support each metric by 
   going `here <https://www.tradingview.com/support/folders/43000581956-list-of-available-economic-indicators/>`__

This example plots the current US GDP values

  //@version=5
  indicator("Economic Data Example")
  e = request.economic("US", "GDP")
  plot(e)

Note that:

  - You will receive an error if the requested metric is not available for the country or region you have selected.
  - You can also view this data on a chart like you would with a symbol so for this example you would replace
  the exchange name with Economic and the symbol name with a single string combining the ``country_code`` with ``field``.
  For this example you would use "/"Economic.USGDP"/" in the symbol search box.


  
\`request.dividends()\`, \`request.earnings()\` and \`request.splits()\`
------------------------------------------------------------------------

An easy method to determine the financial strength of a stock is using earnings data so we offer three options to receive the latest earnings data for a given stock: 
request.dividends(), request.earnings() and request.splits(). Much of the underlying data of a stock can be interpreted using these metrics but also keep in mind that not all stocks will have these stats available. 
Small cap stocks for example are not known for giving out dividends. 

It is important to remember that data for these functions is only available as the data comes in. This differs 
from the financial data originating from the `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__ function in 
that the underlying financial data becomes available according to the current fiscal period for the underlying financial instrument.

Below we have included an example that creates a handy table containing the latest earnings data for each stock using these three metrics. 

  //@version=5
  indicator("Dividends, Splits, and Earnings Example")

  dividends = request.dividends(syminfo.tickerid)
  splitsNum = request.splits(syminfo.tickerid, splits.numerator)
  splitsDenom = request.splits(syminfo.tickerid, splits.denominator)
  earnings = request.earnings(syminfo.tickerid)

  plot(earnings, color=color.blue)
  plot(dividends, color=color.red)

  if barstate.islast
      string tableText = "Current Stats \n\n Dividends: " + str.tostring(dividends) + "\n Splits: " + str.tostring(splitsNum) + 
      "/" + str.tostring(splitsDenom) + " \n Earnings: " + str.tostring(earnings)
      var table t = table.new(position.middle_right, 1, 3), table.cell(t, 0, 0, tableText, bgcolor = color.lime)

Note that:

- For the `ticker` parameter, you need to specifically use the symbol with the market instead of just the symbol ticker. e.g. "NASDAQ:AAPL" instead of "AAPL". 
- Also don't use syminfo.ticker because you will receive a runtime error so make sure you use syminfo.tickerid instead.
- When you request financial data using the dividends and earnings functions, the new value is returned on the bar where the report was published.
- When you use request.splits(), you need to specify the split type by using splits.denominator or splits.numerator.
- We are creating the table only when we are on the latest bar so we are saving allocated memory by only creating the table when it is necessary.



\`request.quandl()\`
--------------------

TradingView has partnered with many fintech companies to provide our users with vast amounts of information on everything from crypto to stocks and much much more.
One of our partners is Quandl and we have an example below that shows you how easy it is use this request function. Quandl has hundreds of thousands of available
feeds and was recently purchased by Nasdaq so the url may be changed to reflect that. Below we have an example showing you a small glimpse of the vast amount of data available. 

  //@version=5
  indicator("Quandl Example")

  // We are displaying FRED (Federal Reserve Economic Data) from Quandl showing the Federal Funds Rate as well as the current unemployment rate.
  f1 = request.quandl("FRED/FEDFUNDS", barmerge.gaps_off, 0)
  f2 = request.quandl("FRED/UNRATE", barmerge.gaps_off, 0)

  // Here we are displaying Bitcoin data showing the miner's revenue rate as well as the difficulty of completing the calculations.
  b1 = request.quandl("BCHAIN/MIREV", barmerge.gaps_off, 0)
  b2 = request.quandl("BCHAIN/DIFF", barmerge.gaps_off, 0)

  // The following 2 examples shows how to properly use the index parameter.
  // We are displaying Quandl data for University of Michigan Consumer Surveys with index 0 is a percentage of consumers 
  who believe it is a good time to buy a house, and index 2 is a percentage of consumers who believe it is a bad time to buy a house.
  m1 = request.quandl("UMICH/SOC35", barmerge.gaps_off, 0)
  m2 = request.quandl("UMICH/SOC35", barmerge.gaps_off, 2)

  plot(na)

  Note that:
  - The `barmerge.gaps_off` is used to remove any `na` values so we don't have any gaps in the plotted data.
  - For the `ticker` parameter, you need to specifically use the Quandl symbol matching the data that you want to import.
  - For the `index` parameter, you need to make sure to match the index information given on `Quandl <https://data.nasdaq.com/search?filters=%5B%22Quandl%22%5D>`__
  - For a full list of available Quandl data feeds, you can go `here <https://data.nasdaq.com/search?filters=%5B%22Quandl%22%5D>`__.



\`request.financial()\`
-----------------------

This function returns a financial metric from `FactSet <https://www.factset.com/>`__ for a given fiscal period. More than 200 financial 
metrics are available, although not for every symbol or fiscal period. 
Note that financial data is also available on TradingView through the chart's `"Fundamental metrics for stocks" button <https://www.tradingview.com/?solution=43000543506>`__ in the top menu.

It is important to remember that data for this function is only available according to the current fiscal period for the underlying 
financial instrument. This differs from the `request.dividends() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}dividends>`__, 
`request.earnings() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}earnings>`__, and 
`request.splits() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}splits>`__ functions in that the underlying financial data becomes available immediately. 

The signature of `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__ is: 

.. code-block:: text

    request.financial(symbol, financial_id, period, gaps, ignore_invalid_symbol, currency) → series float

We have covered the last three parameters in the :ref:`Common characteristics <PageOtherTimeframesAndData_CommonCharacteristics>` section of this page.
The first three parameters all require a "simple string" argument. They are:

``symbol``
   This is similar to the first parameter of the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.
   It is the name of the symbol for which a financial metric is requested. For example: `"NASDAQ:AAPL"`.

``financial_id``
   This is the identifier of the required metric. There are more than 200 IDs. They are listed in the third column of the :ref:`Financial IDs <PageOtherTimeframesAndData_FinancialIDs>` section below.

``period``
   This represents the frequency at which you require the values to update on your chart. There are three possible arguments: ``"FQ"`` (quarterly), ``"FY"`` (yearly) and ``"TTM"`` (trailing twelve months).
   Not all frequencies are available for all metrics. Possible values for each metric are listed in the second column of the :ref:`Financial IDs <PageOtherTimeframesAndData_FinancialIDs>` section below.
   Note that each frequency is fixed and independent of the exact date where the data is made available within each period.
   If for dividends or earnings you require the data when it is made available, use
   `request.dividends() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}dividends>`__ or
   `request.earnings() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}earnings>`__ instead.


This plots the quarterly value of accounts payable for Apple:

.. image:: images/OtherTimeframesAndData-RequestFinancial()-01.png

::

    //@version=5
    indicator("")
    f = request.financial("NASDAQ:AAPL", "ACCOUNTS_PAYABLE", "FQ")
    plot(f)

Note that:

- The data begins in 2013.
- We are not using gaps, so the fetched value stays the same for during each fiscal quarter.
- New values appear on the bar where the next fiscal period begins.



Calculated financial metrics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some common financial metrics cannot be fetched with `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__
because they require combining metrics with an instrument's current chart price.
Such is the case for:

- Market Capitalization (price X number of shares outstanding)
- Earnings Yield (earnings per share for the last 12-month / current market price)
- Price Book Ratio (price / book value per share)
- Price Earnings Ratio (price / earnings per share)
- Price Sales Ratio (company’s market capitalization / total revenue over the last twelve months)

Here, we calculates all five values:

.. image:: images/OtherTimeframesAndData-RequestFinancial()-02.png

::

    //@version=5
    indicator("")
    
    // ————— Market capitalization
    marketCap() =>
        totalSharesOutstanding = request.financial(syminfo.tickerid, "TOTAL_SHARES_OUTSTANDING", "FQ")
        marketCap = totalSharesOutstanding * close
    
    // ————— Earnings yield
    earningsYield() =>
        earningsPerShare = request.financial(syminfo.tickerid, "EARNINGS_PER_SHARE", "TTM")
        earningsYield = (earningsPerShare / close) * 100
    
    // ————— Price Book Ratio
    priceBookRatio() =>
        bookValuePerShare = request.financial(syminfo.tickerid, "BOOK_VALUE_PER_SHARE", "FQ")
        priceBookRatio = close / bookValuePerShare
    
    // ————— Price Earnings Ratio
    priceEarningsRatio() =>
        earningsPerShare = request.financial(syminfo.tickerid, "EARNINGS_PER_SHARE", "TTM")
        priceEarningsRatio = close / earningsPerShare
    
    // ————— Price Sales Ratio
    priseSalesRatio() =>
        totalSharesOutstanding = request.financial(syminfo.tickerid, "TOTAL_SHARES_OUTSTANDING", "FQ")
        mktCap = totalSharesOutstanding * close
        totalRevenue = request.financial(syminfo.tickerid, "TOTAL_REVENUE", "TTM")
        priseSalesRatio = mktCap / totalRevenue
    
    plot(earningsYield(), "Earnings yield", color.aqua, 2)
    plot(priceBookRatio(), "Price Book Ratio", color.orange, 2)
    plot(priceEarningsRatio(), "Price Earnings Ratio", color.purple, 2)
    plot(priseSalesRatio(), "Price Sales Ratio", color.teal, 2)
    
    // ————— Display market cap using a label because its values are too large compared to the others.
    // New function using gaps.
    marketCapWithGaps() =>
        totalSharesOutstanding = request.financial(syminfo.tickerid, "TOTAL_SHARES_OUTSTANDING", "FQ", gaps = barmerge.gaps_on)
        mktCapGaps = totalSharesOutstanding * close
    // Convert value to a string, abbreviating large values as is done for volume. Add currency.
    mktCapGapsTxt = str.tostring(marketCapWithGaps(), format.volume) + " " + syminfo.currency
    // Label's y position is the highest value among the last 50 of the four plotted values.
    labelY = ta.highest(math.max(earningsYield(), priceBookRatio(), priceEarningsRatio(), priseSalesRatio()), 50)
    // When the function returns a value instead of `na`, display a label.
    if not na(marketCapWithGaps())
        label.new(bar_index, labelY, mktCapGapsTxt, color = color.new(color.blue, 85), size = size.large)

Note that:

- We create a :ref:`user-defined function <PageUserDefinedFunctions>` for each value, which makes it easier to reuse the code.
- We plot all the values except the market cap. That value being much larger than the others, plotting it would more or less turn the other plots into flat lines.
- We use another method to display the market cap, which involves creating a version of its function that uses gaps, so we have an easy way to 
  detect when a new value comes in for it and should be shown. We also format the value using 
  `format.volume <https://www.tradingview.com/pine-script-reference/v5/#var_format{dot}volume>`__ to abbreviate large values,
  and add the currency using `syminfo.currency <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}currency>`__.
  To determine the height of the label, we calculate the maximum value plotted in the last 50 bars.



.. _PageOtherTimeframesAndData_FinancialIDs:

Financial IDs
^^^^^^^^^^^^^

All financial metrics available with `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__ is listed below. 
The table columns contain the following information:

- The "Financial" column is a description of the value. It links to a corresponding Help Center page providing more information on the metric.
- The ``period`` column lists the arguments that can be used for the namesake parameter in
  `request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__.
  Only one period can be used per function call. Not all periods are available for all metrics.
- The ``financial_id`` column lists the string to be used for the ``financial_id`` parameter.

Metrics are divided in four categories:

- :ref:`Income statements <PageOtherTimeframesAndData_IncomeStatements>`
- :ref:`Balance sheet <PageOtherTimeframesAndData_BalanceSheet>`
- :ref:`Cash flow <PageOtherTimeframesAndData_CashFlow>`
- :ref:`Statistics <PageOtherTimeframesAndData_Statistics>`


.. _PageOtherTimeframesAndData_IncomeStatements:

Income statements
"""""""""""""""""

+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| **Financial**                                                                                               | ``period``  | ``financial_id``                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `After tax other income/expense <https://www.tradingview.com/?solution=43000563497>`__                      | FQ, FY      | AFTER_TAX_OTHER_INCOME                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Average basic shares outstanding <https://www.tradingview.com/?solution=43000      >`__                    | FQ, FY      | BASIC_SHARES_OUTSTANDING                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other COGS <https://www.tradingview.com/?solution=43000563478>`__                                          | FQ, FY      | COST_OF_GOODS_EXCL_DEP_AMORT               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cost of goods <https://www.tradingview.com/?solution=43000553618>`__                                       | FQ, FY      | COST_OF_GOODS                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Deprecation and amortization <https://www.tradingview.com/?solution=43000563477>`__                        | FQ, FY      | DEP_AMORT_EXP_INCOME_S                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Diluted net income available to common stockholders <https://www.tradingview.com/?solution=43000563516>`__ | FQ, FY      | DILUTED_NET_INCOME                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Diluted shares outstanding <https://www.tradingview.com/?solution=43000553616>`__                          | FQ, FY      | DILUTED_SHARES_OUTSTANDING                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Dilution adjustment <https://www.tradingview.com/?solution=43000563504>`__                                 | FQ, FY      | DILUTION_ADJUSTMENT                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Discontinued operations <https://www.tradingview.com/?solution=43000563502>`__                             | FQ, FY      | DISCONTINUED_OPERATIONS                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Basic EPS <https://www.tradingview.com/?solution=43000563520>`__                                           | FQ, FY, TTM | EARNINGS_PER_SHARE_BASIC                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Diluted EPS <https://www.tradingview.com/?solution=43000553616>`__                                         | FQ, FY      | EARNINGS_PER_SHARE_DILUTED                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `EBIT <https://www.tradingview.com/?solution=43000      >`__                                                | FQ, FY      | EBIT                                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `EBITDA <https://www.tradingview.com/?solution=43000553610>`__                                              | FQ, FY, TTM | EBITDA                                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Equity in earnings <https://www.tradingview.com/?solution=43000563487>`__                                  | FQ, FY      | EQUITY_IN_EARNINGS                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Gross profit <https://www.tradingview.com/?solution=43000553611>`__                                        | FQ, FY      | GROSS_PROFIT                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Taxes <https://www.tradingview.com/?solution=43000563492>`__                                               | FQ, FY      | INCOME_TAX                                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Interest capitalized <https://www.tradingview.com/?solution=43000563468>`__                                | FQ, FY      | INTEREST_CAPITALIZED                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Interest expense on debt <https://www.tradingview.com/?solution=43000563467>`__                            | FQ, FY      | INTEREST_EXPENSE_ON_DEBT                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Non-controlling/minority interest <https://www.tradingview.com/?solution=43000563495>`__                   | FQ, FY      | MINORITY_INTEREST_EXP                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net income before discontinued operations <https://www.tradingview.com/?solution=43000563500>`__           | FQ, FY      | NET_INCOME_BEF_DISC_OPER                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net income <https://www.tradingview.com/?solution=43000553617>`__                                          | FQ, FY      | NET_INCOME                                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Non-operating income, excl. interest expenses <https://www.tradingview.com/?solution=43000563471>`__       | FQ, FY      | NON_OPER_INCOME                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Interest expense, net of interest capitalized <https://www.tradingview.com/?solution=43000563466>`__       | FQ, FY      | NON_OPER_INTEREST_EXP                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Non-operating interest income <https://www.tradingview.com/?solution=43000563473>`__                       | FQ, FY      | NON_OPER_INTEREST_INCOME                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Operating income <https://www.tradingview.com/?solution=43000563464>`__                                    | FQ, FY      | OPER_INCOME                                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Operating expenses (excl. COGS) <https://www.tradingview.com/?solution=43000563463>`__                     | FQ, FY      | OPERATING_EXPENSES                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Miscellaneous non-operating expense <https://www.tradingview.com/?solution=43000563479>`__                 | FQ, FY      | OTHER_INCOME                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other operating expenses, total <https://www.tradingview.com/?solution=43000563483>`__                     | FQ, FY      | OTHER_OPER_EXPENSE_TOTAL                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Preferred dividends <https://www.tradingview.com/?solution=43000563506>`__                                 | FQ, FY      | PREFERRED_DIVIDENDS                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Pretax equity in earnings <https://www.tradingview.com/?solution=43000563474>`__                           | FQ, FY      | PRETAX_EQUITY_IN_EARNINGS                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Pretax income <https://www.tradingview.com/?solution=43000563462>`__                                       | FQ, FY      | PRETAX_INCOME                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Research & development <https://www.tradingview.com/?solution=43000553612>`__                              | FQ, FY      | RESEARCH_AND_DEV                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Selling/general/admin expenses, other <https://www.tradingview.com/?solution=43000553614>`__               | FQ, FY      | SELL_GEN_ADMIN_EXP_OTHER                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Selling/general/admin expenses, total <https://www.tradingview.com/?solution=43000553613>`__               | FQ, FY      | SELL_GEN_ADMIN_EXP_TOTAL                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Non-operating income, total <https://www.tradingview.com/?solution=43000563473>`__                         | FQ, FY      | TOTAL_NON_OPER_INCOME                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total operating expenses <https://www.tradingview.com/?solution=43000553615>`__                            | FQ, FY      | TOTAL_OPER_EXPENSE                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total revenue <https://www.tradingview.com/?solution=43000553619>`__                                       | FQ, FY      | TOTAL_REVENUE                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Unusual income/expense <https://www.tradingview.com/?solution=43000563479>`__                              | FQ, FY      | UNUSUAL_EXPENSE_INC                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+



.. _PageOtherTimeframesAndData_BalanceSheet:

Balance sheet
"""""""""""""

+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| **Financial**                                                                                               | ``period``  | ``financial_id``                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Accounts payable <https://www.tradingview.com/?solution=43000563619>`__                                    | FQ, FY      | ACCOUNTS_PAYABLE                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Accounts receivable - trade, net <https://www.tradingview.com/?solution=43000563740>`__                    | FQ, FY      | ACCOUNTS_RECEIVABLES_NET                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Accrued payroll <https://www.tradingview.com/?solution=43000563628>`__                                     | FQ, FY      | ACCRUED_PAYROLL                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Accumulated depreciation, total <https://www.tradingview.com/?solution=43000563673>`__                     | FQ, FY      | ACCUM_DEPREC_TOTAL                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Additional paid-in capital/Capital surplus <https://www.tradingview.com/?solution=43000563874>`__          | FQ, FY      | ADDITIONAL_PAID_IN_CAPITAL                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Tangible book value per share <https://www.tradingview.com/?solution=43000597072>`__                       | FQ, FY      | BOOK_TANGIBLE_PER_SHARE                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Book value per share <https://www.tradingview.com/?solution=43000      >`__                                | FQ, FY      | BOOK_VALUE_PER_SHARE                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Capitalized lease obligations <https://www.tradingview.com/?solution=43000563527>`__                       | FQ, FY      | CAPITAL_LEASE_OBLIGATIONS                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Capital and operating lease obligations <https://www.tradingview.com/?solution=43000563522>`__             | FQ, FY      | CAPITAL_OPERATING_LEASE_OBLIGATIONS        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cash & equivalents <https://www.tradingview.com/?solution=43000563709>`__                                  | FQ, FY      | CASH_N_EQUIVALENTS                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cash and short term investments <https://www.tradingview.com/?solution=43000563702>`__                     | FQ, FY      | CASH_N_SHORT_TERM_INVEST                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Common equity, total <https://www.tradingview.com/?solution=43000563866>`__                                | FQ, FY      | COMMON_EQUITY_TOTAL                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Common stock par/Carrying value <https://www.tradingview.com/?solution=43000563873>`__                     | FQ, FY      | COMMON_STOCK_PAR                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Current portion of LT debt and capital leases <https://www.tradingview.com/?solution=43000563557>`__       | FQ, FY      | CURRENT_PORT_DEBT_CAPITAL_LEASES           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Deferred income, current <https://www.tradingview.com/?solution=43000563631>`__                            | FQ, FY      | DEFERRED_INCOME_CURRENT                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Deferred income, non-current <https://www.tradingview.com/?solution=43000563540>`__                        | FQ, FY      | DEFERRED_INCOME_NON_CURRENT                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Deferred tax assets <https://www.tradingview.com/?solution=43000563683>`__                                 | FQ, FY      | DEFERRED_TAX_ASSESTS                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Deferred tax liabilities <https://www.tradingview.com/?solution=43000563536>`__                            | FQ, FY      | DEFERRED_TAX_LIABILITIES                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Dividends payable <https://www.tradingview.com/?solution=43000563624>`__                                   | FY          | DIVIDENDS_PAYABLE                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Goodwill, net <https://www.tradingview.com/?solution=43000563688>`__                                       | FQ, FY      | GOODWILL                                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Income tax payable <https://www.tradingview.com/?solution=43000563621>`__                                  | FQ, FY      | INCOME_TAX_PAYABLE                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net intangible assets <https://www.tradingview.com/?solution=43000563686>`__                               | FQ, FY      | INTANGIBLES_NET                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Inventories - finished goods <https://www.tradingview.com/?solution=43000563749>`__                        | FQ, FY      | INVENTORY_FINISHED_GOODS                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Inventories - progress payments & other <https://www.tradingview.com/?solution=43000563748>`__             | FQ, FY      | INVENTORY_PROGRESS_PAYMENTS                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Inventories - raw materials <https://www.tradingview.com/?solution=43000563753>`__                         | FQ, FY      | INVENTORY_RAW_MATERIALS                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Inventories - work in progress <https://www.tradingview.com/?solution=43000563746>`__                      | FQ, FY      | INVENTORY_WORK_IN_PROGRESS                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Investments in unconsolidated subsidiaries <https://www.tradingview.com/?solution=43000563645>`__          | FQ, FY      | INVESTMENTS_IN_UNCONCSOLIDATE              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Long term debt excl. lease liabilities <https://www.tradingview.com/?solution=43000563521>`__              | FQ, FY      | LONG_TERM_DEBT_EXCL_CAPITAL_LEASE          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Long term debt <https://www.tradingview.com/?solution=43000553621>`__                                      | FQ, FY      | LONG_TERM_DEBT                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Long term investments <https://www.tradingview.com/?solution=43000563639>`__                               | FQ, FY      | LONG_TERM_INVESTMENTS                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Note receivable - long term <https://www.tradingview.com/?solution=43000563641>`__                         | FQ, FY      | LONG_TERM_NOTE_RECEIVABLE                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other long term assets, total <https://www.tradingview.com/?solution=43000563693>`__                       | FQ, FY      | LONG_TERM_OTHER_ASSETS_TOTAL               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Minority interest <https://www.tradingview.com/?solution=43000563884>`__                                   | FQ, FY      | MINORITY_INTEREST                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Notes payable <https://www.tradingview.com/?solution=43000563600>`__                                       | FY          | NOTES_PAYABLE_SHORT_TERM_DEBT              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Operating lease liabilities <https://www.tradingview.com/?solution=43000563532>`__                         | FQ, FY      | OPERATING_LEASE_LIABILITIES                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other common equity <https://www.tradingview.com/?solution=43000563877>`__                                 | FQ, FY      | OTHER_COMMON_EQUITY                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other current assets, total <https://www.tradingview.com/?solution=43000563761>`__                         | FQ, FY      | OTHER_CURRENT_ASSETS_TOTAL                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other current liabilities <https://www.tradingview.com/?solution=43000563635>`__                           | FQ, FY      | OTHER_CURRENT_LIABILITIES                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other intangibles, net <https://www.tradingview.com/?solution=43000563689>`__                              | FQ, FY      | OTHER_INTANGIBLES_NET                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other investments <https://www.tradingview.com/?solution=43000563649>`__                                   | FQ, FY      | OTHER_INVESTMENTS                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other liabilities, total <https://www.tradingview.com/?solution=43000563635>`__                            | FQ, FY      | OTHER_LIABILITIES_TOTAL                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other receivables <https://www.tradingview.com/?solution=43000563741>`__                                   | FQ, FY      | OTHER_RECEIVABLES                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other short term debt <https://www.tradingview.com/?solution=43000563614>`__                               | FY          | OTHER_SHORT_TERM_DEBT                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Paid in capital <https://www.tradingview.com/?solution=43000563871>`__                                     | FQ, FY      | PAID_IN_CAPITAL                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Gross property/plant/equipment <https://www.tradingview.com/?solution=43000563667>`__                      | FQ, FY      | PPE_TOTAL_GROSS                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net property/plant/equipment <https://www.tradingview.com/?solution=43000563657>`__                        | FQ, FY      | PPE_TOTAL_NET                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Preferred stock, carrying value <https://www.tradingview.com/?solution=43000563879>`__                     | FQ, FY      | PREFERRED_STOCK_CARRYING_VALUE             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Prepaid expenses <https://www.tradingview.com/?solution=43000563757>`__                                    | FQ, FY      | PREPAID_EXPENSES                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Provision for risks & charge <https://www.tradingview.com/?solution=43000563535>`__                        | FQ, FY      | PROVISION_F_RISKS                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Retained earnings <https://www.tradingview.com/?solution=43000563867>`__                                   | FQ, FY      | RETAINED_EARNINGS                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Short term debt excl. current portion of LT debt <https://www.tradingview.com/?solution=43000563563>`__    | FQ, FY      | SHORT_TERM_DEBT_EXCL_CURRENT_PORT          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Short term debt <https://www.tradingview.com/?solution=43000563554>`__                                     | FQ, FY      | SHORT_TERM_DEBT                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Short term investments <https://www.tradingview.com/?solution=43000563716>`__                              | FQ, FY      | SHORT_TERM_INVEST                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Shareholders' equity <https://www.tradingview.com/?solution=43000557442>`__                                | FQ, FY      | SHRHLDRS_EQUITY                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total assets <https://www.tradingview.com/?solution=43000553623>`__                                        | FQ, FY      | TOTAL_ASSETS                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total current assets <https://www.tradingview.com/?solution=43000557441>`__                                | FQ, FY      | TOTAL_CURRENT_ASSETS                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total current liabilities <https://www.tradingview.com/?solution=43000557437>`__                           | FQ, FY      | TOTAL_CURRENT_LIABILITIES                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total debt <https://www.tradingview.com/?solution=43000553622>`__                                          | FQ, FY      | TOTAL_DEBT                                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total equity <https://www.tradingview.com/?solution=43000553625>`__                                        | FQ, FY      | TOTAL_EQUITY                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total inventory <https://www.tradingview.com/?solution=43000563745>`__                                     | FQ, FY      | TOTAL_INVENTORY                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total liabilities <https://www.tradingview.com/?solution=43000553624>`__                                   | FQ, FY      | TOTAL_LIABILITIES                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total liabilities & shareholders' equities <https://www.tradingview.com/?solution=43000553626>`__          | FQ, FY      | TOTAL_LIABILITIES_SHRHLDRS_EQUITY          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total non-current assets <https://www.tradingview.com/?solution=43000557440>`__                            | FQ, FY      | TOTAL_NON_CURRENT_ASSETS                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total non-current liabilities <https://www.tradingview.com/?solution=43000557436>`__                       | FQ, FY      | TOTAL_NON_CURRENT_LIABILITIES              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total receivables, net <https://www.tradingview.com/?solution=43000563738>`__                              | FQ, FY      | TOTAL_RECEIVABLES_NET                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Treasury stock - common <https://www.tradingview.com/?solution=43000563875>`__                             | FQ, FY      | TREASURY_STOCK_COMMON                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+



.. _PageOtherTimeframesAndData_CashFlow:

Cash flow
"""""""""

+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| **Financial**                                                                                               | ``period``  | ``financial_id``                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Amortization <https://www.tradingview.com/?solution=43000564143>`__                                        | FQ, FY      | AMORTIZATION                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Capital expenditures - fixed assets <https://www.tradingview.com/?solution=43000564167>`__                 | FQ, FY      | CAPITAL_EXPENDITURES_FIXED_ASSETS          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Capital expenditures <https://www.tradingview.com/?solution=43000564166>`__                                | FQ, FY      | CAPITAL_EXPENDITURES                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Capital expenditures - other assets <https://www.tradingview.com/?solution=43000564168>`__                 | FQ, FY      | CAPITAL_EXPENDITURES_OTHER_ASSETS          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cash from financing activities <https://www.tradingview.com/?solution=43000553629>`__                      | FQ, FY      | CASH_F_FINANCING_ACTIVITIES                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cash from investing activities <https://www.tradingview.com/?solution=43000553628>`__                      | FQ, FY      | CASH_F_INVESTING_ACTIVITIES                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cash from operating activities <https://www.tradingview.com/?solution=43000553627>`__                      | FQ, FY      | CASH_F_OPERATING_ACTIVITIES                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Deferred taxes (cash flow) <https://www.tradingview.com/?solution=43000564144>`__                          | FQ, FY      | CASH_FLOW_DEFERRED_TAXES                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Depreciation & amortization (cash flow) <https://www.tradingview.com/?solution=43000563892>`__             | FQ, FY      | CASH_FLOW_DEPRECATION_N_AMORTIZATION       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Change in accounts payable <https://www.tradingview.com/?solution=43000564150>`__                          | FQ, FY      | CHANGE_IN_ACCOUNTS_PAYABLE                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Change in accounts receivable <https://www.tradingview.com/?solution=43000564148>`__                       | FQ, FY      | CHANGE_IN_ACCOUNTS_RECEIVABLE              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Change in accrued expenses <https://www.tradingview.com/?solution=43000564151>`__                          | FQ, FY      | CHANGE_IN_ACCRUED_EXPENSES                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Change in inventories <https://www.tradingview.com/?solution=43000564153>`__                               | FQ, FY      | CHANGE_IN_INVENTORIES                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Change in other assets/liabilities <https://www.tradingview.com/?solution=43000564154>`__                  | FQ, FY      | CHANGE_IN_OTHER_ASSETS                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Change in taxes payable <https://www.tradingview.com/?solution=43000564149>`__                             | FQ, FY      | CHANGE_IN_TAXES_PAYABLE                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Changes in working capital <https://www.tradingview.com/?solution=43000564147>`__                          | FQ, FY      | CHANGES_IN_WORKING_CAPITAL                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Common dividends paid <https://www.tradingview.com/?solution=43000564185>`__                               | FQ, FY      | COMMON_DIVIDENDS_CASH_FLOW                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Depreciation/depletion <https://www.tradingview.com/?solution=43000564142>`__                              | FQ, FY      | DEPRECIATION_DEPLETION                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Free cash flow <https://www.tradingview.com/?solution=43000553630>`__                                      | FQ, FY      | FREE_CASH_FLOW                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Funds from operations <https://www.tradingview.com/?solution=43000563886>`__                               | FQ, FY      | FUNDS_F_OPERATIONS                         |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Issuance/retirement of debt, net <https://www.tradingview.com/?solution=43000564172>`__                    | FQ, FY      | ISSUANCE_OF_DEBT_NET                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Issuance/retirement of long term debt <https://www.tradingview.com/?solution=43000564175>`__               | FQ, FY      | ISSUANCE_OF_LONG_TERM_DEBT                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Issuance/retirement of other debt <https://www.tradingview.com/?solution=43000564178>`__                   | FQ, FY      | ISSUANCE_OF_OTHER_DEBT                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Issuance/retirement of short term debt <https://www.tradingview.com/?solution=43000564173>`__              | FQ, FY      | ISSUANCE_OF_SHORT_TERM_DEBT                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Issuance/retirement of stock, net <https://www.tradingview.com/?solution=43000564169>`__                   | FQ, FY      | ISSUANCE_OF_STOCK_NET                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net income (cash flow) <https://www.tradingview.com/?solution=43000563888>`__                              | FQ, FY      | NET_INCOME_STARTING_LINE                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Non-cash items <https://www.tradingview.com/?solution=43000564146>`__                                      | FQ, FY      | NON_CASH_ITEMS                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other financing cash flow items, total <https://www.tradingview.com/?solution=43000564179>`__              | FQ, FY      | OTHER_FINANCING_CASH_FLOW_ITEMS_TOTAL      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Financing activities - other sources <https://www.tradingview.com/?solution=43000564181>`__                | FQ, FY      | OTHER_FINANCING_CASH_FLOW_SOURCES          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Financing activities - other uses <https://www.tradingview.com/?solution=43000564182>`__                   | FQ, FY      | OTHER_FINANCING_CASH_FLOW_USES             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Other investing cash flow items, total <https://www.tradingview.com/?solution=43000564163>`__              | FQ, FY      | OTHER_INVESTING_CASH_FLOW_ITEMS_TOTAL      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Investing activities - other sources <https://www.tradingview.com/?solution=43000564164>`__                | FQ, FY      | OTHER_INVESTING_CASH_FLOW_SOURCES          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Investing activities - other uses <https://www.tradingview.com/?solution=43000564165>`__                   | FQ, FY      | OTHER_INVESTING_CASH_FLOW_USES             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Preferred dividends paid <https://www.tradingview.com/?solution=43000564186>`__                            | FQ, FY      | PREFERRED_DIVIDENDS_CASH_FLOW              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Purchase/acquisition of business <https://www.tradingview.com/?solution=43000564159>`__                    | FQ, FY      | PURCHASE_OF_BUSINESS                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Purchase of investments <https://www.tradingview.com/?solution=43000564162>`__                             | FQ, FY      | PURCHASE_OF_INVESTMENTS                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Repurchase of common & preferred stock <https://www.tradingview.com/?solution=43000564171>`__              | FQ, FY      | PURCHASE_OF_STOCK                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Purchase/sale of business, net <https://www.tradingview.com/?solution=43000564156>`__                      | FQ, FY      | PURCHASE_SALE_BUSINESS                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Purchase/sale of investments, net <https://www.tradingview.com/?solution=43000564160>`__                   | FQ, FY      | PURCHASE_SALE_INVESTMENTS                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Reduction of long term debt <https://www.tradingview.com/?solution=43000564177>`__                         | FQ, FY      | REDUCTION_OF_LONG_TERM_DEBT                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Sale of common & preferred stock <https://www.tradingview.com/?solution=43000564170>`__                    | FQ, FY      | SALE_OF_STOCK                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Sale of fixed assets & businesses <https://www.tradingview.com/?solution=43000564158>`__                   | FQ, FY      | SALES_OF_BUSINESS                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Sale/maturity of investments <https://www.tradingview.com/?solution=43000564161>`__                        | FQ, FY      | SALES_OF_INVESTMENTS                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Supplying of long term debt <https://www.tradingview.com/?solution=43000564176>`__                         | FQ, FY      | SUPPLYING_OF_LONG_TERM_DEBT                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total cash dividends paid <https://www.tradingview.com/?solution=43000564183>`__                           | FQ, FY      | TOTAL_CASH_DIVIDENDS_PAID                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+



.. _PageOtherTimeframesAndData_Statistics:

Statistics
""""""""""

+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| **Financial**                                                                                               | ``period``  | ``financial_id``                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Accruals <https://www.tradingview.com/?solution=43000597073>`__                                            | FQ, FY      | ACCRUALS_RATIO                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Altman Z-score <https://www.tradingview.com/?solution=43000597092>`__                                      | FQ, FY      | ALTMAN_Z_SCORE                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Asset turnover <https://www.tradingview.com/?solution=43000597022>`__                                      | FQ, FY      | ASSET_TURNOVER                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Beneish M-score <https://www.tradingview.com/?solution=43000597835>`__                                     | FQ, FY      | BENEISH_M_SCORE                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Buyback yield % <https://www.tradingview.com/?solution=43000597088>`__                                     | FQ, FY      | BUYBACK_YIELD                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cash conversion cycle <https://www.tradingview.com/?solution=43000597089>`__                               | FQ, FY      | CASH_CONVERSION_CYCLE                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Cash to debt ratio <https://www.tradingview.com/?solution=43000597023>`__                                  | FQ, FY      | CASH_TO_DEBT                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `COGS to revenue ratio <https://www.tradingview.com/?solution=43000597026>`__                               | FQ, FY      | COGS_TO_REVENUE                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Current ratio <https://www.tradingview.com/?solution=43000597051>`__                                       | FQ, FY      | CURRENT_RATIO                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Days sales outstanding <https://www.tradingview.com/?solution=43000597030>`__                              | FQ, FY      | DAY_SALES_OUT                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Days inventory <https://www.tradingview.com/?solution=43000597028>`__                                      | FQ, FY      | DAYS_INVENT                                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Days payable <https://www.tradingview.com/?solution=43000597029>`__                                        | FQ, FY      | DAYS_PAY                                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Debt to assets ratio <https://www.tradingview.com/?solution=43000597031>`__                                | FQ, FY      | DEBT_TO_ASSET                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Debt to EBITDA ratio <https://www.tradingview.com/?solution=43000597032>`__                                | FQ, FY      | DEBT_TO_EBITDA                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Debt to equity ratio <https://www.tradingview.com/?solution=43000597078>`__                                | FQ, FY      | DEBT_TO_EQUITY                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Debt to revenue ratio <https://www.tradingview.com/?solution=43000597033>`__                               | FQ, FY      | DEBT_TO_REVENUE                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Dividend payout ratio % <https://www.tradingview.com/?solution=43000597738>`__                             | FQ, FY      | DIVIDEND_PAYOUT_RATIO                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Dividend yield % <https://www.tradingview.com/?solution=43000597817>`__                                    | FQ, FY      | DIVIDENDS_YIELD                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Dividends per share - common stock primary issue <https://www.tradingview.com/?solution=43000      >`__    | FQ, FY      | DPS_COMMON_STOCK_PRIM_ISSUE                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `EPS estimates <https://www.tradingview.com/?solution=43000597066>`__                                       | FQ, FY      | EARNINGS_ESTIMATE                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `EPS basic one year growth <https://www.tradingview.com/?solution=43000597069>`__                           | FQ, FY      | EARNINGS_PER_SHARE_BASIC_ONE_YEAR_GROWTH   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `EPS diluted one year growth <https://www.tradingview.com/?solution=43000597071>`__                         | FQ, FY      | EARNINGS_PER_SHARE_DILUTED_ONE_YEAR_GROWTH |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `EBITDA margin % <https://www.tradingview.com/?solution=43000597075>`__                                     | FQ, FY      | EBITDA_MARGIN                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Effective interest rate on debt % <https://www.tradingview.com/?solution=43000597034>`__                   | FQ, FY      | EFFECTIVE_INTEREST_RATE_ON_DEBT            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Enterprise value to EBITDA ratio <https://www.tradingview.com/?solution=43000597064>`__                    | FQ, FY      | ENTERPRISE_VALUE_EBITDA                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Enterprise value <https://www.tradingview.com/?solution=43000597077>`__                                    | FQ, FY      | ENTERPRISE_VALUE                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Equity to assets ratio <https://www.tradingview.com/?solution=43000597035>`__                              | FQ, FY      | EQUITY_TO_ASSET                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Enterprise value to EBIT ratio <https://www.tradingview.com/?solution=43000597063>`__                      | FQ, FY      | EV_EBIT                                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Enterprise value to revenue ratio <https://www.tradingview.com/?solution=43000597065>`__                   | FQ, FY      | EV_REVENUE                                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Float shares outstanding <https://www.tradingview.com/?solution=43000      >`__                            | FY          | FLOAT_SHARES_OUTSTANDING                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Free cash flow margin % <https://www.tradingview.com/?solution=43000597813>`__                             | FQ, FY      | FREE_CASH_FLOW_MARGIN                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Fulmer H factor <https://www.tradingview.com/?solution=43000597847>`__                                     | FQ, FY      | FULMER_H_FACTOR                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Goodwill to assets ratio <https://www.tradingview.com/?solution=43000597036>`__                            | FQ, FY      | GOODWILL_TO_ASSET                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Graham's number <https://www.tradingview.com/?solution=43000597084>`__                                     | FQ, FY      | GRAHAM_NUMBERS                             |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Gross margin % <https://www.tradingview.com/?solution=43000597811>`__                                      | FQ, FY      | GROSS_MARGIN                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Gross profit to assets ratio <https://www.tradingview.com/?solution=43000597087>`__                        | FQ, FY      | GROSS_PROFIT_TO_ASSET                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Interest coverage <https://www.tradingview.com/?solution=43000597037>`__                                   | FQ, FY      | INTERST_COVER                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Inventory to revenue ratio <https://www.tradingview.com/?solution=43000597047>`__                          | FQ, FY      | INVENT_TO_REVENUE                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Inventory turnover <https://www.tradingview.com/?solution=43000597046>`__                                  | FQ, FY      | INVENT_TURNOVER                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `KZ index <https://www.tradingview.com/?solution=43000597844>`__                                            | FY          | KZ_INDEX                                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Long term debt to total assets ratio <https://www.tradingview.com/?solution=43000597048>`__                | FQ, FY      | LONG_TERM_DEBT_TO_ASSETS                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net current asset value per share <https://www.tradingview.com/?solution=43000      >`__                   | FQ, FY      | NCAVPS_RATIO                               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net income per employee <https://www.tradingview.com/?solution=43000597082>`__                             | FY          | NET_INCOME_PER_EMPLOYEE                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Net margin % <https://www.tradingview.com/?solution=43000597074>`__                                        | FQ, FY      | NET_MARGIN                                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Number of employees <https://www.tradingview.com/?solution=43000597080>`__                                 | FY          | NUMBER_OF_EMPLOYEES                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Operating earnings yield % <https://www.tradingview.com/?solution=43000597010>`__                          | FQ, FY      | OPERATING_EARNINGS_YIELD                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Operating margin % <https://www.tradingview.com/?solution=43000597076>`__                                  | FQ, FY      | OPERATING_MARGIN                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `PEG ratio <https://www.tradingview.com/?solution=43000597090>`__                                           | FQ, FY      | PEG_RATIO                                  |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Piotroski F-score <https://www.tradingview.com/?solution=43000597734>`__                                   | FQ, FY      | PIOTROSKI_F_SCORE                          |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Price earnings ratio forward <https://www.tradingview.com/?solution=43000597831>`__                        | FQ, FY      | PRICE_EARNINGS_FORWARD                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Price sales ratio forward <https://www.tradingview.com/?solution=43000597832>`__                           | FQ, FY      | PRICE_SALES_FORWARD                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Price to free cash flow ratio <https://www.tradingview.com/?solution=43000597816>`__                       | FQ, FY      | PRICE_TO_FREE_CASH_FLOW                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Price to tangible book ratio <https://www.tradingview.com/?solution=43000597815>`__                        | FQ, FY      | PRICE_TO_TANGIBLE_BOOK                     |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Quality ratio <https://www.tradingview.com/?solution=43000597086>`__                                       | FQ, FY      | QUALITY_RATIO                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Quick ratio <https://www.tradingview.com/?solution=43000597050>`__                                         | FQ, FY      | QUICK_RATIO                                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Research & development to revenue ratio <https://www.tradingview.com/?solution=43000597739>`__             | FQ, FY      | RESEARCH_AND_DEVELOP_TO_REVENUE            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Return on assets % <https://www.tradingview.com/?solution=43000597054>`__                                  | FQ, FY      | RETURN_ON_ASSETS                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Return on equity adjusted to book value % <https://www.tradingview.com/?solution=43000597055>`__           | FQ, FY      | RETURN_ON_EQUITY_ADJUST_TO_BOOK            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Return on equity % <https://www.tradingview.com/?solution=43000597021>`__                                  | FQ, FY      | RETURN_ON_EQUITY                           |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Return on invested capital % <https://www.tradingview.com/?solution=43000597056>`__                        | FQ, FY      | RETURN_ON_INVESTED_CAPITAL                 |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Return on tangible assets % <https://www.tradingview.com/?solution=43000597052>`__                         | FQ, FY      | RETURN_ON_TANG_ASSETS                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Return on tangible equity % <https://www.tradingview.com/?solution=43000597053>`__                         | FQ, FY      | RETURN_ON_TANG_EQUITY                      |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Revenue one year growth <https://www.tradingview.com/?solution=43000597068>`__                             | FQ, FY      | REVENUE_ONE_YEAR_GROWTH                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Revenue per employee <https://www.tradingview.com/?solution=43000597081>`__                                | FY          | REVENUE_PER_EMPLOYEE                       |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Revenue estimates <https://www.tradingview.com/?solution=43000597067>`__                                   | FQ, FY      | SALES_ESTIMATES                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Shares buyback ratio % <https://www.tradingview.com/?solution=43000597057>`__                              | FQ, FY      | SHARE_BUYBACK_RATIO                        |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Sloan ratio % <https://www.tradingview.com/?solution=43000597058>`__                                       | FQ, FY      | SLOAN_RATIO                                |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Springate score <https://www.tradingview.com/?solution=43000597848>`__                                     | FQ, FY      | SPRINGATE_SCORE                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Sustainable growth rate <https://www.tradingview.com/?solution=43000597736>`__                             | FQ, FY      | SUSTAINABLE_GROWTH_RATE                    |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Tangible common equity ratio <https://www.tradingview.com/?solution=43000597079>`__                        | FQ, FY      | TANGIBLE_COMMON_EQUITY_RATIO               |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Tobin's Q (approximate) <https://www.tradingview.com/?solution=43000597834>`__                             | FQ, FY      | TOBIN_Q_RATIO                              |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Total common shares outstanding <https://www.tradingview.com/?solution=43000      >`__                     | FQ, FY      | TOTAL_SHARES_OUTSTANDING                   |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+
| `Zmijewski score <https://www.tradingview.com/?solution=43000597850>`__                                     | FQ, FY      | ZMIJEWSKI_SCORE                            |
+-------------------------------------------------------------------------------------------------------------+-------------+--------------------------------------------+



.. rubric:: Footnotes

.. [#minutes] Actually the highest supported minute timeframe is "1440" (which is the number of minutes in 24 hours).

.. [#hours] Requesting data of ``"1h"`` or ``"1H"`` timeframe would result in an error. Use ``"60"`` instead.

.. [#seconds] These are the only second-based timeframes available. To use a second-based timeframe, the timeframe of the chart should be equal to or less than the requested timeframe.


.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/