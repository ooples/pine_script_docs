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

Another time-related key reference for traders is the **time zone of the exchange** where an instrument are traded.
Some variables or functions use the UTC time zone, others use the exchange's time zone.
We will note which time zone each one uses when mentioning them.

Pine has built-in **variables** to:

- Get timestamp information from the current bar (UTC time zone): 
  `time <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__ and
  `time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__
- Get timestamp information for the beginning of the current trading day (UTC time zone):
  `time_tradingday <https://www.tradingview.com/pine-script-reference/v5/#var_time_tradingday>`__
- Get the current time in one-second increments (UTC time zone):
  `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__
- Retrieve calendar and time values from the bar (exchange time zone):
  `year <https://www.tradingview.com/pine-script-reference/v5/#var_year>`__,
  `month <https://www.tradingview.com/pine-script-reference/v5/#var_month>`__,
  `weekofyear <https://www.tradingview.com/pine-script-reference/v5/#var_weekofyear>`__,
  `dayofmonth <https://www.tradingview.com/pine-script-reference/v5/#var_dayofmonth>`__,
  `dayofweek <https://www.tradingview.com/pine-script-reference/v5/#var_dayofweek>`__,
  `hour <https://www.tradingview.com/pine-script-reference/v5/#var_hour>`__,
  `minute <https://www.tradingview.com/pine-script-reference/v5/#var_minute>`__ and
  `second <https://www.tradingview.com/pine-script-reference/v5/#var_second>`__
- Query the timezone of the exchange of the chart's symbol with
  `syminfo.timezone <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}timezone>`__

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
- Convert a timestamp to a formatted date/time string for display, 
  using `str.format() <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}format>`__
- Input data and time values. See the section on :ref:`Inputs <PageInputs>`.
- Work with :ref:`session information <PageSessions>`.


Time variables
--------------



\`time\` and \`time_close\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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



\`time_tradingday\`
^^^^^^^^^^^^^^^^^^^^^



\`timenow\`
^^^^^^^^^^^



Calendar dates and times
^^^^^^^^^^^^^^^^^^^^^^^^





\`syminfo.timezone()\`
^^^^^^^^^^^^^^^^^^^^^





Time functions
--------------



\`time()\` and \`time_close()\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Calendar dates and times
^^^^^^^^^^^^^^^^^^^^^^^^



\`timestamp()\`
^^^^^^^^^^^^^^^^^^^^^

The `timestamp() <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__ function has a few different signatures:

.. code-block:: text

    timestamp(year, month, day, hour, minute, second) → simple/series int
    timestamp(timezone, year, month, day, hour, minute, second) → simple/series int
    timestamp(dateString) → const int

The only difference between the first two is the ``timezone`` parameter.
Its default value is `syminfo.timezone <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}timezone>`__.
It can be specified in GMT notation (e.g. "GMT-5") or as an 
`IANA time zone database name <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`__
(e.g., "America/New_York").

The third form is used as a ``defval`` value in `input.time() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}time>`__.



Formatting dates and time
-------------------------

Timestamps can be formatted using `str.format() <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}format>`__.
These are examples of various formats::

    //@version=5
    indicator("", "", true)
    
    print(txt, styl) => 
        var alignment = styl == label.style_label_right ? text.align_right : text.align_left
        var lbl = label.new(na, na, "", xloc.bar_index, yloc.price, color(na), styl, color.black, size.large, alignment)
        if barstate.islast
            label.set_xy(lbl, bar_index, hl2[1])
            label.set_text(lbl, txt)
    
    var string format = 
      "{0,date,yyyy.MM.dd hh:mm:ss}\n" +
      "{1,date,short}\n" +
      "{2,date,medium}\n" +
      "{3,date,long}\n" +
      "{4,date,full}\n" +
      "{5,date,h a z (zzzz)}\n" +
      "{6,time,short}\n" +
      "{7,time,medium}\n" +
      "{8,date,'Month 'MM, 'Week' ww, 'Day 'DD}\n" +
      "{9,time,full}\n" + 
      "{10,time,hh:mm:ss}\n" +
      "{11,time,HH:mm:ss}\n" +
      "{12,time,HH:mm:ss} Left in bar\n"
    
    print(format, label.style_label_right)
    print(str.format(format,
      time, time, time, time, time, time, time, 
      timenow, timenow, timenow, timenow, 
      timenow - time, time_close - timenow), label.style_label_left)

.. image:: images/Time-FormattingDatesAndTime-01.png
