.. _PageOtherTimeframesAndData:

Other timeframes and data
=========================

.. contents:: :local:
    :depth: 2



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

The ``request`` family of functions have many different applications and their use can be quite involved.
Accordingly, this page is quite lengthy.



Common parameters
-----------------

Many of the functions in the ``request`` namespace share common parameters.
Before exploring each function, let's go over their common parameters.



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
the shares outstanding for stocks:

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
``lookahead`` is only useful in special circumstances, when they don't compromise the integrity of your script's logic. e.g.:

- When retrieving the underlying normal chart data from non-standard charts.
- When used with an offset on the series (such as ``close[1]``), is to produce non-repainting
  `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ calls.

The parameter only affects the script's behavior on historical bars, as there are no future bars to look forward to in realtime, where the future is unknown — as it should.

.. note:: Using ``lookahead = barmerge.lookahead_on`` to access future price information on historical bars causes *future leak*, or *lookahead bias*,
   which means your script is using future information it should **not** have access to.
   Except in very rare cases, this is a bad idea. Using ``request.*()`` functions this way is misleading, and not allowed in script publications.
   It is considered a serious violation, so it is your responsability, if you publish scripts, 
   to ensure you do not mislead users of your script by using future information on historical bars.
   While your plots on historical bars will look great because your script will magically acquire prescience (which will not reproduce in realtime),
   you will be misleading users of your scripts — and yourself.

The default value for ``lookahead`` is `barmerge.lookahead_off <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}lookahead_off>`__.
To enable it, use `barmerge.lookahead_on <https://www.tradingview.com/pine-script-reference/v5/#var_barmerge{dot}lookahead_on>`__.

This example shows the difference when fetching the 1min `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ from a 5sec chart:

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

.. note:: In Pine v1 and v2, the ``security()`` did not include a ``lookahead`` parameter, but it behaved as it does in later versions of Pine
   with ``lookahead = barmerge.lookahead_on``. This means that is was systematically using future data. 
   Scripts written with Pine v1 and v2 that use ``security()`` should therefore be treated with caution, unless they offset the series fetched, e.g., using ``close[1]``.


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



\`request.security()\`
----------------------

The function's signature is:

.. code-block:: text

    request.security(symbol, timeframe, expression, gaps, lookahead, ignore_resolve_errors, currency) → series int/float/bool/color



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

The `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__
function's first argument is the name of the requested symbol. The second
argument is the required timeframe and the third one is an expression
which will be calculated on the requested series *within* the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call.

The name of the symbol can be defined using two variants: with a prefix that
contains the exchange (or data provider), or without it. For example:
``"NYSE:IBM"``, ``"BATS:IBM"`` or ``"IBM"``. When an exchange is not provided,
BATS will be used as the default. The current symbol name is stored in the
`syminfo.ticker <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}ticker>`__ and
`syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__
built-in variables. `syminfo.ticker <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}ticker>`__ 
contains the value of the symbol name without its exchange prefix, for example ``"MSFT"``.
`syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__ 
contains the value of the symbol name with its exchange prefix, for example,
``"BATS:MSFT"`` or ``"NASDAQ:MSFT"``. It is recommended to use 
`syminfo.tickerid <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}tickerid>`__ to avoid
ambiguity in the values returned by `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__.

.. TODO write about syminfo.tickerid in extended format and function tickerid

The second argument of the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function, ``timeframe``, is
also a string. All intraday timeframes are defined using a
number of minutes (from ``"1"`` to ``"1440"``), with the exception of four second-based timeframes: ``"1S"``, ``"5S"``, ``"15S"``, and ``"30S"`` [#seconds]_. It is possible to request any [#minutes]_ number of minutes: ``"5"``, ``"10"``,
``"21"``, etc. *Hourly* timeframe is also set by minutes [#hours]_. For example, the
following lines signify one hour, two hours and four hours respectively:
``"60"``, ``"120"``, ``"240"``. A timeframe with a value of *1 day* is indicated by
``"D"`` or ``"1D"``. It is possible to request any number of days: ``"2D"``,
``"3D"``, etc. *Weekly* and *Monthly* timeframes are set in a similar way: ``"W"``,
``"1W"``, ``"2W"``, ..., ``"M"``, ``"1M"``, ``"2M"``. ``"M"`` and ``"1M"`` denote the same monthly
timeframe, and ``"W"`` and ``"1W"`` the same weekly timeframe. The
third parameter of the `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ function can be any arithmetic
expression or a function call, which will be calculated in the context of the chosen series.
The timeframe of the main chart's symbol is stored in the
`timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__
built-in variable.

Using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__, one can view a 1min chart while
displaying an 1D SMA like this::

    //@version=5
    indicator("High Time Frame MA", overlay = true)
    src = close
    len = 9
    out = ta.sma(src, len)
    out1 = request.security(syminfo.tickerid, 'D', out)
    plot(out1)

One can declare the following variable:

::

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



Avoiding repainting
^^^^^^^^^^^^^^^^^^^



Returning tuples
^^^^^^^^^^^^^^^^



.. _PageOtherTimeframesAndData_RequestingDataOfALowerTimeframe:

Requesting data of a lower timeframe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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



Fetching standard prices for a non-standard chart
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



\`request.financial()\`
-----------------------




\`request.dividends()\`, \`request.earnings()\` and \`request.splits()\`
------------------------------------------------------------------------





\`request.quandl()\`
--------------------





.. rubric:: Footnotes

.. [#minutes] Actually the highest supported minute timeframe is "1440" (which is the number of minutes in 24 hours).

.. [#hours] Requesting data of ``"1h"`` or ``"1H"`` timeframe would result in an error. Use ``"60"`` instead.

.. [#seconds] These are the only second-based timeframes available. To use a second-based timeframe, the timeframe of the chart should be equal to or less than the requested timeframe.
