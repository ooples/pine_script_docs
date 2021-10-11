.. _PageOtherTimeframesAndData:

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
  at intrabar timeframes, i.e., timeframes lower than the charts.

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

.. note:: In Pine v1 and v2, ``security()`` did not include a ``lookahead`` parameter, but it behaved as it does in later versions of Pine
   with ``lookahead = barmerge.lookahead_on``, which means it was systematically using future data. 
   Scripts written with Pine v1 or v2 and using ``security()`` should therefore be treated with caution, unless they offset the series fetched, e.g., using ``close[1]``.



\`request.security()\`
----------------------

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function is used to request data from:

- Other symbols
- Other timeframes (see the page on :ref:`Timeframes <PageTimeframes>` to timeframe specifications in Pine)
- Other chart types (see the page on :ref:`Non-standard chart data <PageNonStandardChartsData>`)
- Other contexts, in combination with `ticker.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_ticker{dot}new>`__

Its signature is:

.. code-block:: text

    request.security(symbol, timeframe, expression, gaps, lookahead, ignore_resolve_errors, currency) → series int/float/bool/color

``symbol``
   This is the ticker identifier of the symbol whose information is to be fetched. It is a "simple string" value and can be defined in multiple ways:

      - With a literal string containing either a simple ticker, such as ``"IBM"``, ``"700"``, ``"BTCUSD"`` or ``"EURUSD"``.
        When an exchange is not provided, ``"BATS"`` will be used as the default.
        While this will work for certain instruments, it will not work with all tickers.
      - With a literal string include both the exchange (or data provider) and ticker information, such as ``"NYSE:IBM"``, ``"BATS:IBM"`` or ``"NASDAQ:AAPL"``.
      - Using the `syminfo.ticker <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}ticker>`__ or
        `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__ built-in variables,
        which respectively return only the ticker or the exchange:ticker information of the chart's symbol.
        It is recommended to use `syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__ 
        to avoid ambiguity. See the :ref:`Symbol information <PageChartInformation_SymbolInformation>` section for more information.
        Note that an empty string can also be supplied as a value, in which case the chart's symbol is used.

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
function enables scripts to request data from other symbols and/or timeframes than those of the active chart.
Let's assume the following script is running on an IBM chart at 1min. 
It will display the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ price of the IBM symbol, but from the 15min timeframe.

::

    //@version=5
    indicator("Example security 1", overlay = true)
    ibm_15 = request.security("NYSE:IBM", "15", close)
    plot(ibm_15)

.. image:: images/Chart_security_1.png


Using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__, one can view a 1min chart while
displaying an 1D SMA like this::

    //@version=5
    indicator("High Time Frame MA", overlay = true)
    src = close
    len = 9
    out = ta.sma(src, len)
    out1 = request.security(syminfo.tickerid, 'D', out)
    plot(out1)

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



Data feeds
^^^^^^^^^^

Different data feeds supplied by exchanges/brokers can be used to display information about an instrument on charts:

- Intraday historical data (for timeframes < 1D)
- End-of-day (EOD) historical data (for timeframes >= 1D)
- Realtime feed (which may or may not be delayed, depending on your type of account and the extra data services you may have purchased)
- Extended hours data (which may be available or not, depending on instruments and the type of account you hold on TradingView).

Not all of these types of feed may exist for every instrument. "ICEEUR:BRN1!" for example, only has EOD data.

For some instruments, where both intraday and EOD historical feeds exist, volume data will not be the same because some volume such as block trades or OTC trades 
may only be reported at the end of the day. It will thus appear in the EOD feed, but not in the intraday feed. 
Differences in volume data are almost inexistent in the crypto sector, but commonplace in stocks.

Prices discrepancies may also occur between both feeds, such that the `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ 
for one day's bar on the EOD feed may not match any of the `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ values of intraday bars for that day.

Another distinction between intraday and EOD feeds is that EOD feeds do not contain data from extended hours.

These differences may account for variations in the values fetched by 
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
because it can access data from varying timeframes, thus shifting between historical feeds.
The differences may also cause discrepancies between data received in realtime vs the way it is reported on historical data.
There are no steadfast rules about the variations. 
To understand their details, one must consult the exchange/broker information on the feeds available for each of their markets.
As a rule, TradingView does not generate data; it relies on its data providers for the information displayed on charts.



.. _PageOtherTimeframesAndData_InformationRequested:

Information requested
^^^^^^^^^^^^^^^^^^^^^

int/float/bool/color
no arrays, strings



Built-ins
"""""""""



Calculated variables
""""""""""""""""""""



Function calls
""""""""""""""



Tuples
""""""



Other contexts, with \`ticker.new()\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. TODO write about syminfo.tickerid in extended format and function tickerid



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

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ 
function was designed to request data of a timeframe *higher*
than the current chart timeframe. On a *60 minutes* chart,
this would mean requesting 240, D, W, or any higher timeframe.

It is not recommended to request data of a timeframe *lower* that the current chart timeframe,
for example *1 minute* data from a *5 minutes* chart. The main problem with such a case is that
some part of a 1 minute data will be inevitably lost, as it's impossible to display it on a *5 minutes*
chart and not to break the time axis. In such cases the behavior of 
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ can be rather unexpected.
The next example illustrates this::

    // Add this script on a "5" minute chart
    //@version=5
    indicator("Lookahead On/Off", overlay = true, precision = 5)
    l_on = request.security(syminfo.tickerid, "1", close, lookahead = barmerge.lookahead_on)
    l_off = request.security(syminfo.tickerid, "1", close, lookahead = barmerge.lookahead_off)
    plot(l_on, color = color.red)
    plot(l_off, color = color.blue)

.. image:: images/SecurityLowerTF_LookaheadOnOff.png

This study plots two lines which correspond to different values of the ``lookahead`` parameter.
The red line shows data returned by 
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ with ``lookahead = barmerge.lookahead_on``. 
The blue line with ``lookahead = barmerge.lookahead_off``. Let's look at the *5 minutes* bar starting at 07:50.
The red line at this bar has a value of 1.13151 which corresponds to the
value of *the first of the five 1 minute bars* that fall into the time range 07:50--07:54.
On the other hand, the blue line at the same bar has a value of 1.13121 which corresponds to
*the last of the five 1 minute bars* of the same time range.



Fetching standard prices from a non-standard chart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



\`request.financial()\`
-----------------------

All financial data available in Pine is listed below.

In the first column of each table are the names of each metric. The second column lists how frequently the corresponding data is published: TTM - Trailing Twelve Months, FY - Financial Year, and FQ - Financial Quarter. The third column lists the identifiers of the financial data.

In order to get the value of a certain financial metric, you need to use the function: 

financial(symbol, financial_id, period, gaps)

The first argument here is similar to the first argument of the security function, and is the name of the symbol for which the metric is requested. For example: ”NASDAQ:AAPL”.

The second argument is the identifier of the required metric: the value from the third column of the table.

The third argument indicates how frequently this metric is published: one of the values from the corresponding cells in the second column.

The fourth argument is optional and is similar to the gaps argument of the security function. If gaps = true, values are displayed only on bars corresponding to the publication date of the data.

The function returns the values of the requested financial data.

For example:

f = financial ("NASDAQ:AAPL", "ACCOUNTS_PAYABLE", "FQ")
You can read more about the financial data here.

Note that when you request financial data using the dividends and earnings functions, the new value is returned on the bar where the report was published. Using the financial function, you get a new value on the bar where the next fiscal period begins.

Ratios based on market price

Some of the financial indicators in the Financial menu are not in the table below because they are calculated using a financial metric and the current price on the chart. This entails you cannot request their values directly, but you can calculate them with a few lines of Pine code.

Market Capitalization

Market capitalization is equal to the share price multiplied by the number of shares outstanding (FQ).

TSO = financial(syminfo.tickerid, "TOTAL_SHARES_OUTSTANDING", "FQ")
MarketCap = TSO*close
Earnings Yield

The earnings yield is calculated by dividing earnings per share for the last 12-month period by the current market price per share. Multiplying the result by 100 yields the Earnings Yield % value.

EPS = financial(syminfo.tickerid, "EARNINGS_PER_SHARE", "TTM")
EarningsYield = (EPS/close)*100
Price Book Ratio

Price Book Ratio is calculated by dividing the price per share by the book value per share.

BVPS = financial(syminfo.tickerid, "BOOK_VALUE_PER_SHARE", "FQ")
PriceBookRatio = close/BVPS
Price Earnings Ratio

Price Earnings Ratio is calculated by dividing the current market price per share by the earnings per share for the last 12-month period.

EPS = financial(syminfo.tickerid, "EARNINGS_PER_SHARE", "TTM")
PriceEarningsRatio = close/EPS
Price Sales Ratio

Price Sales Ratio is calculated by dividing the company’s market capitalization by its total revenue over the last twelve months.

TSO = financial(syminfo.tickerid, "TOTAL_SHARES_OUTSTANDING", "FQ")
TR = financial(syminfo.tickerid, "TOTAL_REVENUE", "TTM")
MarketCap = TSO*close
PriseSalesRatio = MarketCap/TR



Financial IDs
^^^^^^^^^^^^^



Income statements
"""""""""""""""""

+-----------------------------------------------------+-------------+--------------------------------------------+
| After tax other income/expense                      | FQ, FY      | AFTER_TAX_OTHER_INCOME                     |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Average basic shares outstanding                    | FQ, FY      | BASIC_SHARES_OUTSTANDING                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Other COGS                                          | FQ, FY      | COST_OF_GOODS_EXCL_DEP_AMORT               |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Cost of goods                                       | FQ, FY      | COST_OF_GOODS                              |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Deprecation and amortization                        | FQ, FY      | DEP_AMORT_EXP_INCOME_S                     |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Diluted net income available to common stockholders | FQ, FY      | DILUTED_NET_INCOME                         |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Diluted shares outstanding                          | FQ, FY      | DILUTED_SHARES_OUTSTANDING                 |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Dilution adjustment                                 | FQ, FY      | DILUTION_ADJUSTMENT                        |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Discontinued operations                             | FQ, FY      | DISCONTINUED_OPERATIONS                    |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Basic EPS                                           | FQ, FY, TTM | EARNINGS_PER_SHARE_BASIC                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Diluted EPS                                         | FQ, FY      | EARNINGS_PER_SHARE_DILUTED                 |
+-----------------------------------------------------+-------------+--------------------------------------------+
| EBIT                                                | FQ, FY      | EBIT                                       |
+-----------------------------------------------------+-------------+--------------------------------------------+
| EBITDA                                              | FQ, FY, TTM | EBITDA                                     |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Equity in earnings                                  | FQ, FY      | EQUITY_IN_EARNINGS                         |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Gross profit                                        | FQ, FY      | GROSS_PROFIT                               |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Taxes                                               | FQ, FY      | INCOME_TAX                                 |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Interest capitalized                                | FQ, FY      | INTEREST_CAPITALIZED                       |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Interest expense on debt                            | FQ, FY      | INTEREST_EXPENSE_ON_DEBT                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Non-controlling/minority interest                   | FQ, FY      | MINORITY_INTEREST_EXP                      |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Net income before discontinued operations           | FQ, FY      | NET_INCOME_BEF_DISC_OPER                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Net income                                          | FQ, FY      | NET_INCOME                                 |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Non-operating income, excl. interest expenses       | FQ, FY      | NON_OPER_INCOME                            |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Interest expense, net of interest capitalized       | FQ, FY      | NON_OPER_INTEREST_EXP                      |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Non-operating interest income                       | FQ, FY      | NON_OPER_INTEREST_INCOME                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Operating income                                    | FQ, FY      | OPER_INCOME                                |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Operating expenses (excl. COGS)                     | FQ, FY      | OPERATING_EXPENSES                         |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Miscellaneous non-operating expense                 | FQ, FY      | OTHER_INCOME                               |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Other operating expenses, total                     | FQ, FY      | OTHER_OPER_EXPENSE_TOTAL                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Preferred dividends                                 | FQ, FY      | PREFERRED_DIVIDENDS                        |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Pretax equity in earnings                           | FQ, FY      | PRETAX_EQUITY_IN_EARNINGS                  |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Pretax income                                       | FQ, FY      | PRETAX_INCOME                              |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Research & development                              | FQ, FY      | RESEARCH_AND_DEV                           |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Selling/general/admin expenses, other               | FQ, FY      | SELL_GEN_ADMIN_EXP_OTHER                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Selling/general/admin expenses, total               | FQ, FY      | SELL_GEN_ADMIN_EXP_TOTAL                   |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Non-operating income, total                         | FQ, FY      | TOTAL_NON_OPER_INCOME                      |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Total operating expenses                            | FQ, FY      | TOTAL_OPER_EXPENSE                         |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Total revenue                                       | FQ, FY      | TOTAL_REVENUE                              |
+-----------------------------------------------------+-------------+--------------------------------------------+
| Unusual income/expense                              | FQ, FY      | UNUSUAL_EXPENSE_INC                        |
+-----------------------------------------------------+-------------+--------------------------------------------+




\`request.dividends()\`, \`request.earnings()\` and \`request.splits()\`
------------------------------------------------------------------------





\`request.quandl()\`
--------------------





.. rubric:: Footnotes

.. [#minutes] Actually the highest supported minute timeframe is "1440" (which is the number of minutes in 24 hours).

.. [#hours] Requesting data of ``"1h"`` or ``"1H"`` timeframe would result in an error. Use ``"60"`` instead.

.. [#seconds] These are the only second-based timeframes available. To use a second-based timeframe, the timeframe of the chart should be equal to or less than the requested timeframe.
