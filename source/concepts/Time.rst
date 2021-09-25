.. _PageTime:

Time
====

.. contents:: :local:
    :depth: 2


Introduction
------------

The native format for time values in Pine is the **Unix time in milliseconds**. 
Unix time is the time elapsed since the **Unix Epoch on January 1st, 1970 at UTC**.
See here for the `current Unix time in seconds <https://www.unixtimestamp.com/>`__
and here for more information on `Unix Time <https://en.wikipedia.org/wiki/Unix_time>`__.
A value for the Unix time is called a *timestamp*.
Note that since Unix time is measured from a fixed reference, i.e., the Unix Epoch, it does not vary with time zones.

Pine has built-in **variables** to:

- Get timestamp information from the current bar: 
  `time <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__ and
  `time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__
- Get timestamp information for the beginning of the current trading day:
  `time_tradingday <https://www.tradingview.com/pine-script-reference/v5/#var_time_tradingday>`__
- Query the timezone of the exchange of the chart's symbol with
  `syminfo.timezone <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}timezone>`__
- Retrieve calendar and time values from the bar:
  `year <https://www.tradingview.com/pine-script-reference/v5/#var_year>`__,
  `month <https://www.tradingview.com/pine-script-reference/v5/#var_month>`__,
  `weekofyear <https://www.tradingview.com/pine-script-reference/v5/#var_weekofyear>`__,
  `dayofmonth <https://www.tradingview.com/pine-script-reference/v5/#var_dayofmonth>`__,
  `dayofweek <https://www.tradingview.com/pine-script-reference/v5/#var_dayofweek>`__,
  `hour <https://www.tradingview.com/pine-script-reference/v5/#var_hour>`__,
  `minute <https://www.tradingview.com/pine-script-reference/v5/#var_minute>`__ and
  `second <https://www.tradingview.com/pine-script-reference/v5/#var_second>`__
- Get the current time in one-second increments:
  `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__

There are also built-in **functions** that can:

- Return timestamps of bars from other timeframes 
  with `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__ and
  `time_close <https://www.tradingview.com/pine-script-reference/v5/#fun_time_close>`__,
  without the need for a `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call
- Retrieve calendar and time values from any timestamp, which can be offset with a time zone:
  `year() <https://www.tradingview.com/pine-script-reference/v5/#fun_year>`__,
  `month() <https://www.tradingview.com/pine-script-reference/v5/#fun_month>`__,
  `weekofyear() <https://www.tradingview.com/pine-script-reference/v5/#fun_weekofyear>`__,
  `dayofmonth() <https://www.tradingview.com/pine-script-reference/v5/#fun_dayofmonth>`__,
  `dayofweek() <https://www.tradingview.com/pine-script-reference/v5/#fun_dayofweek>`__,
  `hour() <https://www.tradingview.com/pine-script-reference/v5/#fun_hour>`__,
  `minute() <https://www.tradingview.com/pine-script-reference/v5/#fun_minute>`__ and
  `second() <https://www.tradingview.com/pine-script-reference/v5/#fun_second>`__

- Create a timestamp using `timestamp() <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__
- Input data and time values. See the section on :ref:`Inputs <PageInputs>`.
- Work with :ref:`session information <PageSessions>`.


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

