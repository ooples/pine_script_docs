.. _PageTime:

Time
====

.. contents:: :local:
    :depth: 2


Introduction
------------



Three references
^^^^^^^^^^^^^^^^

The native format for time values in Pine is the **Unix time in milliseconds**. 
Unix time is the time elapsed since the **Unix Epoch on January 1st, 1970 at UTC**.
See here for the `current Unix time in seconds <https://www.unixtimestamp.com/>`__
and here for more information on `Unix Time <https://en.wikipedia.org/wiki/Unix_time>`__.
A value for the Unix time is called a *timestamp*.
Note that since Unix time is measured from a fixed reference, i.e., the Unix Epoch, it does not vary with time zones.
Some Pine built-ins use the UTC time zone as a reference.

A second time-related key reference for traders is the **time zone of the exchange** where an instrument is traded.
Some built-ins use the exchange's time zone.

A third time-related reference that comes into play is the chart's time zone,
which is selected by traders.

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
it has a second resolution, i.e., it will only update on seconds.
Accordingly, it will only change during execution on historical bars if the script takes longer than one second to execute on them.
In realtime, your scripts will only perceive changes when they execute on feed updates.

This script uses variations in `timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__
during the script's execution on historical bars to time its performance::

    //@version=5
    indicator("Stopwatch", "", true, precision = 4, scale = scale.none)
    loopCount = input.int(100000, "Loop iterations per bar", minval = 0, step = 10000)
    
    stopwatch() =>
        // Get time at first bar.
        var timeBegin = timenow
        // Get ms elapsed since first bar.
        var timeElapsed = 0.
        if not barstate.islast
            timeElapsed := timenow - timeBegin
        // Calculate avg/bar only when time changes.
        var msPerBar = 0.
        // Total bars timed before last change in "timenow".
        var barsTimed = 0
        // ————— Bars elapsed since last change in "timenow".
        var barsNotTimed = 0
        if ta.change(timeElapsed)
            barsTimed := bar_index + 1
            msPerBar  := timeElapsed / barsTimed
        // ————— In between time changes, which only occur every second, estimate elapsed time using avg time per bar.
        if not barstate.islast
            // Bars elapsed since last change of time.
            barsNotTimed := bar_index  + 1 - barsTimed
        // ————— Add (bars since "timenow" change * avg bar time) to time elapsed since last "timenow" change to get better estimate of total time elapsed.
        totalTime = timeElapsed + (barsNotTimed * msPerBar)
        [msPerBar, totalTime, barsTimed, barsNotTimed]
    
    [msPerBar, totalTime, barsTimed, barsNotTimed] = stopwatch()
    
    // ————— Script code to time.
    var a = 0
    for i = 0 to loopCount
    	a := int(a + i + close)
    	a := int(math.abs(a))
    
    // —————————— Display results
    // ————— Print table at the end of chart.
    if barstate.islast
        var table t = table.new(position.middle_right, 1, 1)
        var txt = str.tostring(msPerBar, "Avg time per bar\n#.#### ms\n\n") +
                  str.tostring(totalTime / 1000, "Total time\n#.#### seconds\n\n") + 
                  str.tostring(barsTimed + barsNotTimed, "Bars analyzed\n#")
        table.cell(t, 0, 0, txt, bgcolor = color.yellow)
    // ————— Plot elapsed time.
    plot(totalTime,        "Execution time (ms)", color.gray)
    // ————— Print Data Window values.
    plotchar(msPerBar,     "Avg time / bar (ms)",  "", location.top)
    plotchar(totalTime,    "Execution time (ms)",  "", location.top)
    plotchar(barsTimed,    "Bars timed",           "", location.top)
    
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
can be useful to test for specific dates or times and as arguments to 
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

Note how using ``ta.change(time("M"))`` is more robust as it works on all months (#1 and #2), displayed as the silver background,
whereas the blue dot detected using ``dayofmonth == 1`` does not work (#1) when the first trading day of September occurs on the 2nd.



\`syminfo.timezone()\`
^^^^^^^^^^^^^^^^^^^^^




aa
Time functions
--------------



\`time()\` and \`time_close()\`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The 


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
