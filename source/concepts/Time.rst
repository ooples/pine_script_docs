.. _PageTime:

Time
====

.. contents:: :local:
    :depth: 2


Introduction
------------


Dates and time built-ins



time_close
timenow


\`time\`
--------

Pine provides means to work with trade session, time and date information. On this 30min chart, two scripts are running: "Bar date/time" and "Session bars".

.. image:: images/Chart_time_1.png


This is the "Bar date/time" script:

::

    //@version=5
    indicator("Bar date/time")
    plot(time)

The `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__
variable returns the date/time (timestamp) of each bar's opening time in `UNIX
format <https://en.wikipedia.org/wiki/Unix_time>`__ [#millis]_ and **in the exchange's timezone**, 
which is independent of the timezone selected by the user on his chart.
As can be seen from the screenshot, the `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__ value on the
last bar is equal to 1397593800000. This value is the number of
milliseconds that have passed since 00:00:00 UTC, 1 January, 1970 and
corresponds to Tuesday, 15th of April, 2014 at 20:30:00 UTC.
The chart's time gauge in the screenshot shows the time of the last bar
as 2014-04-15 16:30 because it has a 4-hour difference between the exchange's timezone returned by the 
`time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__ variable.

Our second script will introduces the 
`time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ function, which has the following signature::

    time(timeframe, session, timezone)

The `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ function accepts
three arguments:

- ``timeframe``, a string in `timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__ format
- ``session``, an optional string in session specification format: ``"hhmm-hhmm[:days]"``, where the ``[:days]`` part is optional
- ``timezone``, which is only allowed when ``session`` is used. See the `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ entry in the Reference Manual for more information.

::

    //@version=5
    indicator("Session bars")
    t = time(timeframe.period, "0930-1600")
    plot(na(t) ? 0 : 1)

This shows how the user can distinguish between regular session and extended hours bars
by using the built-in `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__
function rather than the `time <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ variable. 
The `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ call in our script returns the time of the
bar's open in UNIX time (milliseconds), or `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ if the bar is located outside
the 09:30-16:00 trading session.



\`time()\`
----------



Built-in variables for working with time
----------------------------------------

Pine's standard library has an assortment of built-in variables and functions which
make it possible to use time in the script's logic.

The most basic variables:

-  `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__ --- UNIX time of the *current bar start* in milliseconds, UTC timezone.
-  `time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__ --- UNIX time of the *current bar close* in milliseconds, UTC timezone.
-  `time_tradingday <https://www.tradingview.com/pine-script-reference/v5/#var_time_tradingday>`__ --- UNIX time of the *beginning of the trading day that the current bar belongs to, in milliseconds, UTC timezone.
-  `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__ --- Current UNIX time in milliseconds, UTC timezone.
-  `syminfo.timezone <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}timezone>`__ --- Exchange timezone of the chart main symbol series.

Variables that give information about the current bar start time:

-  `year <https://www.tradingview.com/pine-script-reference/v5/#var_year>`__ --- Current bar year.
-  `month <https://www.tradingview.com/pine-script-reference/v5/#var_month>`__ --- Current bar month.
-  `weekofyear <https://www.tradingview.com/pine-script-reference/v5/#var_weekofyear>`__ --- Week number of current bar.
-  `dayofmonth <https://www.tradingview.com/pine-script-reference/v5/#var_dayofmonth>`__ --- Date of current bar.
-  `dayofweek <https://www.tradingview.com/pine-script-reference/v5/#var_dayofweek>`__ --- Day of week for current bar. You can use
   ``dayofweek.sunday``, ``dayofweek.monday``, ``dayofweek.tuesday``, ``dayofweek.wednesday``, ``dayofweek.thursday``, ``dayofweek.friday`` and ``dayofweek.saturday`` variables for comparisons.
-  `hour <https://www.tradingview.com/pine-script-reference/v5/#var_hour>`__ --- Hour of the current bar start time (in exchange timezone).
-  `minute <https://www.tradingview.com/pine-script-reference/v5/#var_minute>`__ --- Minute of the current bar start time (in exchange timezone).
-  `second <https://www.tradingview.com/pine-script-reference/v5/#var_second>`__ --- Second of the current bar start time (in exchange timezone).

Functions for UNIX time "construction":

-  `year(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_year>`__ --- Returns year for provided UTC time ``time``.
-  `month(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_month>`__ --- Returns month for provided UTC time ``time``.
-  `weekofyear(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_weekofyear>`__ --- Returns week of year for provided UTC time ``time``.
-  `dayofmonth(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_dayofmonth>`__ --- Returns day of month for provided UTC time ``time``.
-  `dayofweek(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_dayofweek>`__ --- Returns day of week for provided UTC time ``time``.
-  `hour(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_hour>`__ --- Returns hour for provided UTC time ``time``.
-  `minute(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_minute>`__ --- Returns minute for provided UTC time ``time``.
-  `second(time) <https://www.tradingview.com/pine-script-reference/v5/#fun_second>`__ --- Returns second for provided UTC time ``time``.
-  `timestamp(year, month, day, hour, minute) <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__ ---
   Returns UNIX time of specified date and time. Note, there is also an overloaded version with an additional ``timezone`` parameter.

All these variables and functions return time in the **exchange time zone**,
except for the `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__, 
`time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__, 
`time_tradingday <https://www.tradingview.com/pine-script-reference/v5/#var_time_tradingday>`__, and 
`timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__ variables which return time in **UTC timezone**.



\`timestamp()\`
---------------


.. rubric:: Footnotes

.. [#millis] UNIX time is measured in seconds. Pine Script uses UNIX time multiplied by 1000, so it's in millisecods.

