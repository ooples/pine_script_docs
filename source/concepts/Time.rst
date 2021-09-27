.. _PageTime:

Time
====

.. contents:: :local:
    :depth: 2


Introduction
------------



Four references
^^^^^^^^^^^^^^^

Four different references come into play when using date and time values in Pine:

#. **UTC**: The native format for time values in Pine is the **Unix time in milliseconds**. 
   Unix time is the time elapsed since the **Unix Epoch on January 1st, 1970 at UTC**.
   See here for the `current Unix time in seconds <https://www.unixtimestamp.com/>`__
   and here for more information on `Unix Time <https://en.wikipedia.org/wiki/Unix_time>`__.
   A value for the Unix time is called a *timestamp*.
   Unix timestamps are always expressed in the UTC (or "GMT", or "GMT+0") time zone.
   They are measured from a fixed reference, i.e., the Unix Epoch, and do not vary with time zones.
   Some Pine built-ins use the UTC time zone as a reference.
#. **Exchange time zone**: A second time-related key reference for traders is the time zone of the exchange where an instrument is traded.
   Some built-ins like `hour <https://www.tradingview.com/pine-script-reference/v5/#var_hour>`__
   return values in the exchange's time zone.
#. ``timezone`` parameter: Some functions that normally return values in the exchange's time zone,
   such as `hour() <https://www.tradingview.com/pine-script-reference/v5/#fun_hour>`__
   include a ``timezone`` parameter that allows you to adapt the function's result to another time zone.
   Other functions like `time() <https://www.tradingview.com/pine-script-reference/v5/#fun_time>`__
   include both ``session`` and ``timezone`` parameters. In those cases, the ``timezone`` arguments
   applies to how the ``session`` argument is interpreted — not to the time value returned by the function.
#. **Chart's time zone**: This is the time zone chosen by the user from the chart using the "Chart Settings/Symbol/Time Zone" field.
   This setting only affects the display of dates and times on the chart. 
   It does not affect the behavior of Pine scripts, and they have no visiblity over this setting.


We will note, when discussing variables or functions, if they return dates or times in UTC or exchange time zone.
Scripts do not have visibility on the user's time zone setting on his chart.



Time built-ins
^^^^^^^^^^^^^^

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
- Return the time zone of the exchange of the chart's symbol with
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



Time zones
^^^^^^^^^^

TragingViewers can change the time zone used to display bar times on their charts.
Pine scripts have no visiblity over this setting.
While there is a `syminfo.timezone <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}timezone>`__
variable to return the time zone of the exchange where the chart's intrument is traded,
there is **no** ``chart.timezone`` equivalent.

When displaying times on the chart, this shows one way of providing users a way of adjusting your script's time values to those of their chart.
This way, your displayed times can match the time zone used by traders on their chart::

    //@version=5
    indicator("Time zone control")
    MS_IN_1H = 1000 * 60 * 60
    TOOLTIP01 = "Enter your time zone's offset (+ or −), including a decimal fraction if needed."
    hoursOffsetInput = input.float(0.0, "Timezone offset (in hours)", minval = -12.0, maxval = 14.0, step = 0.5, tooltip = TOOLTIP01)
    
    printTable(txt) => 
        var table t = table.new(position.middle_right, 1, 1)
        table.cell(t, 0, 0, txt, text_halign = text.align_right, bgcolor = color.yellow)
    
    msOffsetInput = hoursOffsetInput * MS_IN_1H
    printTable(
      str.format("Last bar''s open time UTC: {0,date,HH:mm:ss yyyy.MM.dd}", time) +
      str.format("\nLast bar''s close time UTC: {0,date,HH:mm:ss yyyy.MM.dd}", time_close) +
      str.format("\n\nLast bar''s open time EXCHANGE: {0,date,HH:mm:ss yyyy.MM.dd}", time(timeframe.period, syminfo.session, syminfo.timezone)) +
      str.format("\nLast bar''s close time EXCHANGE: {0,date,HH:mm:ss yyyy.MM.dd}", time_close(timeframe.period, syminfo.session, syminfo.timezone)) +
      str.format("\n\nLast bar''s open time OFFSET ({0}): {1,date,HH:mm:ss yyyy.MM.dd}", hoursOffsetInput, time + msOffsetInput) +
      str.format("\nLast bar''s close time OFFSET ({0}): {1,date,HH:mm:ss yyyy.MM.dd}", hoursOffsetInput, time_close + msOffsetInput) +
      str.format("\n\nCurrent time OFFSET ({0}): {1,date,HH:mm:ss yyyy.MM.dd}", hoursOffsetInput, timenow + msOffsetInput))

.. image:: images/Time-TimeZones-01.png

Note that:

- We convert the user offset expressed in hours to milliseconds with ``msOffsetInput``.
  We then add that offset to a timstamp in UTC format before converting it to display format, e.g., ``time + msOffsetInput`` and ``timenow + msOffsetInput``.
- We use a tooltip to provide instructions to users.
- We provide ``minval`` and ``maxval`` values to protect the input field, 
  and a ``step`` value of 0.5 so that when they use the field's up/down arrows, they can intuitively figure out that fractions can be used.
- The `str.format() <https://www.tradingview.com/pine-script-reference/v5/#fun_str{dot}format>`__
  function formats our time values, namely the last bar's time and the current time.

Some functions that normally return values in the exchange's time zone provide means to adapt their result to another time zone.
This script illustrates how to do this with `hour() <https://www.tradingview.com/pine-script-reference/v5/#fun_hour>`__::

    //@version=5
    indicator('`hour(time, "GMT+0")` in orange')
    color BLUE_LIGHT = #0000FF30
    plot(hour, "", BLUE_LIGHT, 8)
    plot(hour(time, syminfo.timezone))
    plot(hour(time, "GMT+0"),"UTC", color.orange)

.. image:: images/Time-TimeZones-02.png

Note that:

- The `hour <https://www.tradingview.com/pine-script-reference/v5/#var_hour>`__ variable and the 
  `hour() <https://www.tradingview.com/pine-script-reference/v5/#fun_hour>`__ function normally returns a value in the exchange's time zone.
  Accordingly, plots in blue for both ``hour`` and ``hour(time, syminfo.timezone)`` overlap.
  Using the function form with ``syminfo.timezone`` is thus redundant if the exchange's hour is what's required.
- The orange line plotting ``hour(time, "GMT+0")``, however, returns the bar's hour at UTC, or "GMT+0" time,
  which in this case is four hours less than the exchange's time, since MSFT trades on the NASDAQ whose time zone is UTC-4.



Time variables
--------------



\`time\` and \`time_close\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's start by plotting `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__ and
`time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__,
the Unix timestamp in milliseconds of the bar's opening and closing time::

    //@version=5
    indicator("`time` and `time_close` values on bars")
    plot(time, "`time`")
    plot(time_close, "`time_close`")

.. image:: images/Time-TimeAndTimeclose-01.png

Note that:

- The `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__ and
  `time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__ variables
  returns a timestamp in `UNIX time <https://en.wikipedia.org/wiki/Unix_time>`__, which is independent of the timezone selected by the user on his chart.
  In this case, the **chart's** time zone setting is the exchange time zone, so whatever symbol is on the chart, 
  its exchange time zone will be used for the display of the date and time values on the chart's cursor.
  The NASDAQ's time zone is UTC-4, but this only affects the chart's display of date/time values; it has no impact on the
  values plotted by the script.
- The last `time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__
  value for the plot shown in the scale is the number of milliseconds elapsed from 00:00:00 UTC, 1 January, 1970, until the bar's opening time.
  It corresponds to 17:30 on the 27th of September 2021. However, because the chart is using the UTC-4 time zone (the NASDAQ's time zone),
  it is displaying the 13:30 time, four hours earlier than UTC time.
- The difference between the two values on the last bar is the number of milliseconds in one hour (1000 * 60 * 60 = 3,600,000)
  because we are on a 1H chart.



\`time_tradingday\`
^^^^^^^^^^^^^^^^^^^^^

`time_tradingday <https://www.tradingview.com/pine-script-reference/v5/#var_time_tradingday>`__ is useful
when a symbol trades on overnight sessions that start and close on different calendar days.
This happens in forex markets, for example, where a session can open Sunday at 17:00 and close Monday at 17:00.

The variable returns the time of the beginning of the trading day when used at timeframes of 1D and less.
When used on timeframes higher than 1D, 
it returns the starting time of the last trading day in the bar (e.g., at 1W it will return the starting time of the last trading day of the week).



\`timenow\`
^^^^^^^^^^^

`timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__ returns the current time.
It works in realtime, but also when a script executes on historical bars. 
While `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__ is expressed in milliseconds,
it has a second resolution, i.e., it will only move in increments of one second.
Accordingly, it will only change during execution on historical bars if the script takes longer than one second to execute on them.
In realtime, your scripts will only perceive changes when they execute on feed updates.
When no updates occur the script is idle, so it cannot update its display.
See the page on Pine's :ref:`execution model <PageExecutionModel>` for more information.

This script uses the values of `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__
and `time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__
to calculate a realtime countdown for intraday bars.
Contrary to the countdown on the chart, this one will only update when a feed update causes the script to execute another iteration::

    //@version=5
    indicator("", "", true)
    
    printTable(txt) => 
        var table t = table.new(position.middle_right, 1, 1)
        table.cell(t, 0, 0, txt, text_halign = text.align_right, bgcolor = color.yellow)
    
    printTable(str.format("{0,time,HH:mm:ss}", time_close - timenow))



Calendar dates and times
^^^^^^^^^^^^^^^^^^^^^^^^

Calendar dates and times such as
`year <https://www.tradingview.com/pine-script-reference/v5/#var_year>`__,
`month <https://www.tradingview.com/pine-script-reference/v5/#var_month>`__,
`weekofyear <https://www.tradingview.com/pine-script-reference/v5/#var_weekofyear>`__,
`dayofmonth <https://www.tradingview.com/pine-script-reference/v5/#var_dayofmonth>`__,
`dayofweek <https://www.tradingview.com/pine-script-reference/v5/#var_dayofweek>`__,
`hour <https://www.tradingview.com/pine-script-reference/v5/#var_hour>`__,
`minute <https://www.tradingview.com/pine-script-reference/v5/#var_minute>`__ and
`second <https://www.tradingview.com/pine-script-reference/v5/#var_second>`__
can be useful to test for specific dates or times, and as arguments to 
`timestamp() <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__.

When testing for specific dates or times, ones needs to account for the possibility that the script will be executing on timeframes
where the tested condition cannot be detected, or for cases where a bar with the specific requirement will not exist.
Suppose, for example, we wanted to detect the first trading day of the month.
This script shows how using only `dayofmonth <https://www.tradingview.com/pine-script-reference/v5/#var_dayofmonth>`__
will not work when a weekly chart is used or when no trading occurs on the 1st of the month::

    //@version=5
    indicator("", "", true)
    firstDayIncorrect = dayofmonth == 1
    firstDay = ta.change(time("M"))
    plotchar(firstDayIncorrect, "firstDayIncorrect", "•", location.top, size = size.small)
    bgcolor(firstDay ? color.silver : na)

.. image:: images/Time-CalendarDatesAndTimes-01.png

Note that: 

- Using ``ta.change(time("M"))`` is more robust as it works on all months (#1 and #2), displayed as the silver background,
  whereas the blue dot detected using ``dayofmonth == 1`` does not work (#1) when the first trading day of September occurs on the 2nd.
- The ``dayofmonth == 1`` condition will be ``true`` on all intrabars of the first day of the month,
  but ``ta.change(time("M"))`` will only be ``true`` on the first.

 


\`syminfo.timezone()\`
^^^^^^^^^^^^^^^^^^^^^

`syminfo.timezone <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}timezone>`__
returns the time zone of the chart symbol's exchange.



aa
Time functions
--------------



\`time()\` and \`time_close()\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
See the `timestamp() <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__ entry in the Reference Manual for more information.

`timestamp() <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__ 
is useful to generate a timestamp for a specific date.
To generate a timestamp for Jan 1, 2021, use either one of these methods::

    //@version=5
    indicator("")
    yearBeginning1 = timestamp("2021-01-01")
    yearBeginning2 = timestamp(2021, 1, 1, 0, 0)
    printTable(txt) => var table t = table.new(position.middle_right, 1, 1), table.cell(t, 0, 0, txt, bgcolor = color.yellow)
    printTable(str.format("yearBeginning1: {0,date,yyyy.MM.dd hh:mm}\nyearBeginning2: {1,date,yyyy.MM.dd hh:mm}", yearBeginning1, yearBeginning1))

You can use offsets in `timestamp() <https://www.tradingview.com/pine-script-reference/v5/#fun_timestamp>`__ arguments.
Here, we subtract 2 from the value supplied for its ``day`` parameter to get the date/time two days ago from the chart's last bar.
Note that because of different bar alignments on different instruments,
the returned timestamp may not always be exactly 48 hours away::

    //@version=5
    indicator("")
    twoDaysAgo = timestamp(year, month, dayofmonth - 2, hour, minute)
    printTable(txt) => var table t = table.new(position.middle_right, 1, 1), table.cell(t, 0, 0, txt, bgcolor = color.yellow)
    printTable(str.format("{0,date,yyyy.MM.dd hh:mm}", twoDaysAgo))



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
