.. _PageTypeSystem::


Type system
===========

.. contents:: :local:
    :depth: 3

.. include:: <isonum.txt>


Introduction
------------

Pine's type system is important because it determines what sort of values can be used when calling Pine functions, which is a requirement to do pretty much anything in Pine.
While it is possible to write very simple scripts without knowing anything about the type system, 
a reasonable understanding of it is necessary to achieve any degree of profiency with the language, 
and in-depth knowledge of its subtleties will allow you to exploit the full potential of Pine.

The type system uses the *form type* pair to qualify the type of all values, be they literals, a variable, the result of an expression, 
the value returned by functions or the arguments supplied when calling a function.

The *form* expresses when a value is known. 

The *type* denotes the nature of a value.

.. note:: We will often use "type" to refer to the "form type" pair.


Forms
^^^^^

The Pine **forms** are:

- "const" for values known at compile time (when adding an indicator to a chart or saving it in the Pine Editor)
- "input" for values known at input time (when values are changed in a script's "Settings/Inputs" tab)
- "simple" for values known at bar zero (when the script begins execution on the chart's first historical bar)
- "series" for values known on each bar (any time during the execution of a script on any bar)

Forms are organized in the following hierarchy: **const < input < simple < series**, where "const" is considered a *weaker* form than "input", for example, and "series" *stronger* than "simple". The form hierarchy translates into the rule that, whenever a given form is required, a weaker form is also allowed.

An expression's result is always of the strongest form used in the expression's calculation. Furthermore, once a variable acquires a stronger form, that state is irreversible; it can never be converted back to a weaker form. A variable of "series" form can thus never be converted back to a "simple" form, for use with a function that requires arguments of that form.

Note that of all these forms, only the "series" form allows values to change dynamically, bar to bar, during the script's execution over each bar of the chart's history. Such values include `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ or `hlc3 <https://www.tradingview.com/pine-script-reference/v5/#var_hlc3>`__ or any variable calculated using values of "series" form. Variables of "const", "input" or "simple" forms cannot change values once execution of the script has begun.


Types
^^^^^

The Pine **types** are:

- The fundamental types: "int", "float", "bool", "color" and "string"
- The special types: "plot", "hline", "line", "label", "box", "table", "array"
- "void"
- tuples

Each type refers to the nature of the value contained in a variable: ``1`` is of type "int", ``1.0`` is of type "float", ``"AAPL"`` is of type "string", etc.

The Pine compiler can automatically convert some types into others when a value is not of the required type. The auto-casting rules are: **int** |rarr| **float** |rarr| **bool**. See the :ref:`<PageTypeSystem_TypeCasting>` section of this page for more information on type casting.

Except in library function signatures, Pine forms are implicit in code; they are never declared because they are always determined by the compiler. Types, however, can be specified when declaring variables, e.g.::

    //@version=5
    indicator("", "", true)
    int periodInput = input.int(100, "Period", minval = 2)
    float ma = ta.sma(close, periodInput)
    bool xUp = ta.crossover(close, ma)
    color maColor = close > ma ? color.lime : color.fuchsia
    plot(ma, "MA", maColor)
    plotchar(xUp, "Cross Up", "▲", location.top, size = size.tiny)


.. _PageTypeSystem_TimeSeries:

Time series
^^^^^^^^^^^

Much of the power of Pine stems from the fact that it is designed to process *time series* efficiently. Time series are not a form or a type; they are the fundamental structure Pine uses to store the successive values of a variable over time, where each value is tethered to a point in time. Since charts are composed of bars, each representing a particular point in time, time series are the ideal data structure to work with values that may change with time. The concept of time series is intimately linked to Pine's :ref:`execution model <PageExecutionModel>`. Understanding both is key to making the most of the power of Pine.

Take the built-in `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__ variable, which contains the "open" price of each bar in the dataset. If your script is running on a 5min chart, then each value in the `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__ time series is the "open" price of the consecutive 5min chart bars. When your script refers to `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__, it is referring to the "open" price of the bar the script is executing on. To refer to past values in a time series, we use the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ history-referencing operator. When a script is executing on a given bar, ``open[1]`` refers to the value of the `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__ time series on the previous bar.

While time series may remind programmers of arrays, they are totally different. Pine does use an array data structure, but it is completely different concept than a time series.

Time series in Pine, combined with its special type of runtime engine and built-in functions, are what makes it easy to compute the running total of `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ values without using a `for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__ loop, with only ``ta.cum(close)``. Similarly, the mean of the difference between the last 14 `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ and `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__ values can be expressed as ``ta.sma(high - low, 14)``, or the distance in bars since the last time the chart made five consecutive higher highs as ``barssince(rising(high, 5))``.

Even the result of function calls on successive bars leaves a trace of values in a time series that can be referenced using the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ history-referencing operator. This can be useful, for example, when testing the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ of the current bar for a breach of the highest `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ in the last 10 bars, but excluding the current bar, which we could write as ``breach = close > highest(close, 10)[1]``. The same statement could also be written as ``breach = close > highest(close[1], 10)``.

Do not confuse "time series" with the "series" form. The *time series* concept explains how consecutive values of variables are stored in Pine; the "series" form denotes variables whose values can change bar to bar. Consider, for example, the `timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__ built-in variable which is of form "simple" and type "string", so "simple string". The "simple" form entails that the variable's value is known on bar zero (the first bar where the script executes) and will not change during the script's execution on all the chart's bars. The variable's value is the chart's timeframe in string format, so ``"D"`` for a 1D chart, for example. Even though its value cannot change during the script, it would be syntactically correct in Pine (though not very useful) to refer to its value 10 bars ago using ``timeframe.period[10]``. This is possible because the successive values of `timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__  for each bar are stored in a time series, even though all the values in that particular time series are similar. Note, however, that when the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ operator is used to access past values of a variable, it yields a result of "series" form, even though the variable without an offset is of another form, such as "simple" in the case of `timeframe.period <https://www.tradingview.com/pine-script-reference/v5/#var_timeframe{dot}period>`__.

When you grasp how time series can be efficiently handled using Pine's syntax and its :ref:`execution model <PageExecutionModel>`, you can define complex calculations using just a few lines of Pine code.



Using forms and types
---------------------


Forms
^^^^^

const
"""""

Values of "const" form must be known at compile time, before your script has access to any information related to the symbol/timeframe information it is running on. Compilation occurs when you save a script in the Pine Editor, which doesn't even require it to already be running on your chart. "const" variables cannot change during the execution of a script.

Variables of "const" form can be intialized using a *literal* value, or calculated from expressions using only literal values or other variables of "const" form. Pine's style guide recommends using upper case SNAKE_CASE to name variables of "const" form. While it is not a requirement, "const" variables are often declared using the `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__ keyword so they are only initialized on the first bar of the dataset. Declaring "const" variables using `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__ improves script execution time due to the fact that the variable is not re-initialized on every bar.

These are examples of literal values:

- *literal int*: ``1``, ``-1``, ``42``
- *literal float*: ``1.``, ``1.0``, ``3.14``, ``6.02E-23``, ``3e8``
- *literal bool*: ``true``, ``false``
- *literal string*: ``"A text literal"``, ``"Embedded single quotes 'text'"``, ``'Embedded double quotes "text"'``
- *literal color*: ``#FF55C6``, ``#FF55C6ff``

.. note:: In Pine, the built-in variables ``open``, ``high``, ``low``, ``close``, ``volume``, ``time``,
    ``hl2``, ``hlc3``, ``ohlc4``, etc., are not of "const" form. Because they change bar to bar, they are of *series* form.

The "const" form is a requirement for the arguments to the ``title`` and ``shorttitle`` parameters in `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__, for example. All these are valid variables that can be used as arguments for those parameters when calling the function::

    //@version=5
    NAME1 = "My indicator"
    var NAME2 = "My Indicator"
    var NAME3 = "My" + "Indicator"
    var NAME4 = NAME2 + " No. 2"
    indicator(NAME4, "", true)
    plot(close)

This will trigger a compilation error::

    //@version=5
    var NAME = "My indicator for " + syminfo.type
    indicator(NAME, "", true)
    plot(close)

The reason for the error is that the ``NAME`` variable's calculation depends on the value of `syminfo.type <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}type>`__ which is a "simple string" (`syminfo.type <https://www.tradingview.com/pine-script-reference/v5/#var_syminfo{dot}type>`__ returns a string corresponding to the sector the chart's symbol belongs to, eg., ``"crypto"``, ``"forex"``, etc.).

Note that using the ``:=`` operator to assign a new value to a previously declared "const" variable will transform it into a "simple" variable, e.g., here with ``name1``, for which we do not use an uppercase name because it is not a constant::

    var name1 = "My Indicator "
    var NAME2 = "No. 2"
    name1 := name1 + NAME2


input
"""""

Values of "input" form are known when the values initialized through ``input.*()`` functions are determined. These functions determine the values that can be modified by script users in the script's "Settings/Inputs" tab. When these values are changed, this always triggers a re-execution of the script from the beginning of the chart's history (bar zero), so variables of "input" form are always known when the script begins execution, and they do not change during the script's execution.

.. note:: The `input.source() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}source>`__ function yields a value of "series" type — not "input". 
    This is because built-in variables such as `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__, 
    `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__, 
    `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__, 
    `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__, 
    `hl2 <https://www.tradingview.com/pine-script-reference/v5/#var_hl2>`__, 
    `hlc3 <https://www.tradingview.com/pine-script-reference/v5/#var_hlc3>`__, 
    `ohlc4 <https://www.tradingview.com/pine-script-reference/v5/#var_ohlc4>`__, etc., are of "series" form.

The script plots the moving average of a user-defined source and period from a symbol and timeframe also determined through inputs::

    //@version=5
    indicator("", "", true)
    symbolInput = input.symbol("AAPL", "Symbol")
    timeframeInput = input.timeframe("D", "Timeframe")
    sourceInput = input.source(close, "Source")
    periodInput = input(10, "Period")
    v = request.security(symbolInput, timeframeInput, ta.sma(sourceInput, periodInput))
    plot(v)

Note that:

- The ``symbolInput``, ``timeframeInput`` and ``periodInput`` variables are of "input" form.
- The ``sourceInput`` variable is of "series" form because it is determined from a call to `input.source() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}source>`__.
- Our `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call is valid because its ``symbol`` and ``timeframe`` parameters require a "simple" argument and the "input" form we use is weaker than "simple". The function's ``expression`` parameter requires a "series" form argument, and that is what form our ``sourceInput`` variable is. Note that because a "series" form is required there, we could have used "const", "input" or "simple" forms as well.
- As per our style guide's recommendations, we use the "Input" suffix with our input variables to help readers of our code remember the origin of these variables.

Wherever an "input" form is required, a "const" form can also be used.


simple
""""""

Values of "simple" form are known only when a script begins execution on the first bar of a chart's history, and they never change during the execution of the script. Built-in variables of the ``syminfo.*``, ``timeframe.*`` and ``ticker.*`` families, for example, all return results of "simple" form because their value depends on the chart's symbol, which can only be detected when the script executes on it.

A "simple" form argument is also required for the ``length`` argument of functions such as `ta.ema() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}ema>`__ or `ta.rma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}rma>`__ which cannot work with dynamic lengths that could change during the script's execution.

Wherever a "simple" form is required, a "const" or "input" form can also be used.


series
""""""

Values of "series" form (also sometimes called *dynamic*) provide the most flexibility because they can change on any bar, or even multiples times during the same bar, in loops for example. Built-in variables such as `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__, 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__,
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__, 
`time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__ or
`volume <https://www.tradingview.com/pine-script-reference/v5/#var_volume>`__ are of "series" form, as would be the result of expressions calculated using them. Functions such as `barssince() <https://www.tradingview.com/pine-script-reference/v5/#fun_barssince>`__ or `crossover() <https://www.tradingview.com/pine-script-reference/v5/#fun_crossover>`__ yield a result of "series" form because it varies bar to bar, as does that of the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ history-referencing operator used to access past values of a time series. While the "series" form is the most common form used in Pine, it is not always allowed as arguments to Pine built-in functions.

Suppose you want to display the value of pivots on your chart. This will require converting values into strings, so the string values your code will be using will be of "series string" type. Pine's `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__ function can be used to place such "series string" text on the chart because its ``text`` parameter accepts arguments of "series" form::

    //@version=5
    indicator("", "", true)
    pivotBarsInput = input(3)
    hiP = ta.pivothigh(high, pivotBarsInput, pivotBarsInput)
    if not na(hiP)
        label.new(bar_index[pivotBarsInput], hiP, str.tostring(hiP, format.mintick), 
         style = label.style_label_down, 
         color = na, 
         textcolor = color.silver)
    plotchar(hiP, "hiP", "•", location.top, size = size.tiny)

Note that:

- The ``str.tostring(hiP, format.mintick)`` call we use to convert the pivot's value to a string yields a "series string" result, which will work with `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__.
- While prices appear at the pivot, the pivots actually require ``pivotBarsInput`` bars to have elapsed before they can be detected. Pivot prices only appear on the pivot because we plot them in the past after the pivot's detection, using ``bar_index[pivotBarsInput]`` (the `bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__'s value, offset ``pivotBarsInput`` bars back). In real time, these prices would only appear ``pivotBarsInput`` bars after the actual pivot.
- We print a blue dot using `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ when a pivot is detected in our code.
- Pine's `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ can also be used to position text on the chart, but because its ``text`` parameter requires a "const string" argument, we could not have used it in place of `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__ in our script.

Wherever a "series" form is required, a "const", "input" or "simple" form can also be used.



Types
^^^^^


int
"""

Integer literals must be written in decimal notation, e.g.::

    1
    -1
    750

Built-in variables such as 
`bar_index <https://www.tradingview.com/pine-script-reference/v5/#var_bar_index>`__, 
`time <https://www.tradingview.com/pine-script-reference/v5/#var_time>`__, 
`timenow <https://www.tradingview.com/pine-script-reference/v5/#var_timenow>`__, 
`time_close <https://www.tradingview.com/pine-script-reference/v5/#var_time_close>`__, or
`dayofmonth <https://www.tradingview.com/pine-script-reference/v5/#var_dayofmonth>`__ all return values of type "int".


float
"""""

Floating-point literals contain a delimiter (the symbol ``.``) and may also contain the symbol ``e`` or ``E`` 
(which means "multiply by 10 to the power of X", where X is the number after the symbol ``e``), e.g.::

    3.14159    // Rounded value of Pi (π)
    - 3.0
    6.02e23    // 6.02 * 10^23 (a very large value)
    1.6e-19    // 1.6 * 10^-19 (a very small value)


The internal precision of floats in Pine is 1e-10.


bool
""""

There are only two literals representing *bool* values::

    true    // true value
    false   // false value

When an expression of type "bool" returns `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ and it is used to test a conditional statement or operator, the "false" branch is executed.


color
"""""

Color literals have the following format: ``#RRGGBB`` or ``#RRGGBBAA``. The letter pairs represent ``00`` to ``FF`` hexadecimal values (0 to 255 in decimal) where:

- ``RR``, ``GG`` and ``BB`` pairs are the values for the color's red, green and blue components
- ``AA`` is an optional value for the color's transparency (or *alpha* component) where ``00`` is invisble and ``FF`` opaque. When no ``AA`` pair is supplied, ``FF`` is used.
- The hexadecimal letters can be upper or lower case

Examples::

    #000000      // black color
    #FF0000      // red color
    #00FF00      // green color
    #0000FF      // blue color
    #FFFFFF      // white color
    #808080      // gray color
    #3ff7a0      // some custom color
    #FF000080    // 50% transparent red color
    #FF0000ff    // same as #FF0000, fully opaque red color
    #FF000000    // completely transparent color

Pine also has built-in color constants such as 
`color.green <https://www.tradingview.com/pine-script-reference/v5/#var_color{dot}green>`__, 
`color.red <https://www.tradingview.com/pine-script-reference/v5/#var_color{dot}red>`__, 
`color.orange <https://www.tradingview.com/pine-script-reference/v5/#var_color{dot}orange>`__, 
`color.blue <https://www.tradingview.com/pine-script-reference/v5/#var_color{dot}blue>`__
(the default color used in `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ and other plotting functions),  etc. 

When using color built-ins, is possible to add transparency information to them with 
`color.new <https://www.tradingview.com/pine-script-reference/v5/#fun_color{dot}new>`__. 

Note that when specifying red, green or blue components in ``color.*()`` functions, a 0-255 decimal value must be used. When specifying transparency in such functions, it is in the form of a 0-100 value (which can be of "float" type to access the underlying 255 potential valoues) where the scale 00-FF scale for color literals is inverted: 100 is thus invisible and 0 is opaque.

Here is an example::

    //@version=5
    indicator("Shading the chart's background", "", true)
    BASE_COLOR = color.navy
    bgColor = dayofweek == dayofweek.monday    ? color.new(BASE_COLOR, 50) :
              dayofweek == dayofweek.tuesday   ? color.new(BASE_COLOR, 60) :
              dayofweek == dayofweek.wednesday ? color.new(BASE_COLOR, 70) :
              dayofweek == dayofweek.thursday  ? color.new(BASE_COLOR, 80) :
              dayofweek == dayofweek.friday    ? color.new(BASE_COLOR, 90) :
              color.new(color.blue, 80)
    bgcolor(bgColor)

See the page on :ref:`colors <PageColors>` for more information on using colors in Pine.


string
""""""

String literals may be enclosed in single or double quotation marks, e.g.::

    "This is a double quoted string literal"
    'This is a single quoted string literal'

Single and double quotation marks are functionally equivalent.
A string enclosed within double quotation marks
may contain any number of single quotation marks, and vice versa::

    "It's an example"
    'The "Star" indicator'

You can escape the string's delimiter in the string by using a backslash. For example::

    'It\'s an example'
    "The \"Star\" indicator"

You can concatenate strings using the ``+`` operator.


plot and hline
""""""""""""""

Pine's `fill() <https://www.tradingview.com/pine-script-reference/v5/#fun_fill>`__ function fills the space between two lines with a color. Both lines must have been plotted with either `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ or `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__ function calls. Each plotted line is referred to in the `fill() <https://www.tradingview.com/pine-script-reference/v5/#fun_fill>`__ function using line IDs which are of "plot" or "hline" type, e.g.::

    //@version=5
    indicator("", "", true)
    plotID1 = plot(high)
    plotID2 = plot(math.max(close, open))
    fill(plotID1, plotID2, color.yellow)

Note that there is no ``plot`` or ``hline`` keyword to explicitly declare the type of `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ or `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__ IDs.


line, label, box and table
""""""""""""""""""""""""""

Drawings were introduced in Pine v4. These objects are created with the
`line.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_line{dot}new>`__,
and `label.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_label{dot}new>`__,
`box.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_box{dot}new>`__ and
`table.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_table{dot}new>`__ functions. 

These functions all return an ID that uniquely identifies each drawing object. The ID's type is "series line", "series label", "series box" and "series table", respectively, and an ID can exist in no other form than "series". Drawing IDs act like pointer in that they are used to reference a specific instance of a drawing in all the related functions of its namespace. The line ID returned by a `line.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_line{dot}new>`__ call is then used to refer to that line using `line.delete() <https://www.tradingview.com/pine-script-reference/v5/#fun_line{dot}delete>`__, for example.


array
"""""

Arrays in Pine are identified by an array ID. There is no single type representing an array ID, 
but rather an overloaded version of a subset of Pine types which represents the type of an array's elements. 
These type names are constructed by appending the ``[]`` suffix (not to be confused with the `[] <https://www.tradingview.com/pine-script-reference/v5/#op_[]>`__ history-referencing operator) to one of the Pine types allowed for array elements:

- ``int[]``
- ``float[]``
- ``bool[]``
- ``color[]``
- ``string[]``
- ``line[]``
- ``label[]``
- ``box[]``
- ``table[]``

An array containing elements of type "int" initalized with one element of value 10 can be declared in the following, equivalent ways::

    a1 = array.new_int(1, 10)
    int[] a2 = array.new_int(1, 10)
    a3 = array.from(10)
    int[] a4 = array.from(10)


void
""""

There is a "void" type in Pine. Functions having only side-effects and returning no usable result return the "void" type. An example of such a function is `alert() <https://www.tradingview.com/pine-script-reference/v5/#fun_alert>`__; it does something (triggers an alert event), but it returns no useful value.

A "void" result cannot be used in an expression or assigned to a variable. No ``void`` keyword exists in Pine, as variables cannot be declared using the "void" type.


Tuples
""""""

There is limited support for a "tuple" type in Pine. A *tuple* is a comma-separated set of expressions enclosed in brackets that can be used when a function or a local block must return more than one variable as a result. For example::

    calcSumAndMult(a, b) =>
        sum = a + b
        mult = a * b
        [sum, mult]

In this example there is a 2-tuple on the last statement of the function's code block, which is the result returned by the function. Tuple elements can be of any type.
There is also a special syntax for calling functions that return tuples. Accordingly, ``calcSumAndMul()`` must be called as follows::

    [s, m] = calcSumAndMul(high, low)

where the value of local variables ``sum`` and ``mul`` will be assigned to the ``s`` and ``m`` variables. Note that the type of ``s`` and ``m`` cannot be explicitly defined; it is always inferred by the type of the function return results.

Tuples can be useful to request multiple values in one `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ call, e.g.::

    roundedOHLC() =>
        [math.round_to_mintick(open), math.round_to_mintick(high), math.round_to_mintick(low), math.round_to_mintick(close)]
    [op, hi, lo, cl] = request.security(syminfo.tickerid, "D", roundedOHLC())

Tuples can also be used as return results of local blocks, in an `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ statement for example::

    [v1, v2] = if close > open
        [high, close]
    else
        [close, low]

They cannot be used in ternaries, however, because the return values of a ternary statement are not considered as local blocks. This is not allowed::

    // Not allowed.
    [v1, v2] = close > open ? [high, close] : [close, low]



\`na\` value
------------

In Pine there is a special value called `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__, which is an acronym for *not available*, meaning
the value of an expression or variable is undefined. It is similar to the ``null`` value in Java, or ``None`` in Python.

`na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ values can be automatically cast to almost any type. In some cases, however, the Pine compiler cannot automatically infer a type for an `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ value because more that one automatic type-casting rule can be applied. For example::

    // Compilation error!
    myVar = na

Here, the compiler cannot determine if ``myVar`` will be used to plot something, as in ``plot(myVar)`` where its type would be "float", or to set some text as in
``label.set_text(lb, text = myVar)`` where its type would be "string", or for some other purpose. Such cases must be explicitly resolved in one of two ways::

    float myVar = na

or::

    myVar = float(na)

To test if some value is `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__, 
a special function must be used: `na() <https://www.tradingview.com/pine-script-reference/v4/#fun_na>`__. For example::

    myClose = na(myVar) ? 0 : close

Do not use the ``==`` operator to test for `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ values, as this method is unreliable.

Designing your calculations so they are `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__-resistant is often useful. In this example, we define a condition that is ``true`` when the bar's `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ is higher than the previous one. For this calculation to work correctly on the dataset's first bar where no previous close exists and ``close[1]`` will return `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__, we use the `nz() <https://www.tradingview.com/pine-script-reference/v4/#fun_nz>`__ function to replace it with the current bar's `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__ for that special case::

    bool risingClose = close > nz(close[1], open)

Protecting against `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ values can also be useful to prevent an initial `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ value from propagating in a calculation's result on all bars. This happens here because the initial value of ``ath`` is `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__, and `math.max() <https://www.tradingview.com/pine-script-reference/v5/#fun_math{dot}max>`__ returns `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ if one of its arguments is `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__::

    // Declare `ath` and initialize it with `na` on the first bar.
    var float ath = na
    // On all bars, calculate the maximum between the `high` and the previous value of `ath`.
    ath := math.max(ath, high)

To protect against this, we could instead use::

    var float ath = na
    ath := math.max(nz(ath), high)

where we are replacing any `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ values of ``ath`` with zero. Even better would be::

    var float ath = high
    ath := math.max(ath, high)


.. _PageTypeSystem_TypeCasting::

Type casting
------------

There is an automatic type-casting mechanism in Pine which can *cast* (or convert) certain types to another. 
The auto-casting rules are: **int** |rarr| **float** |rarr| **bool**, which means that when a "float" is required, an "int" can be used in its place, 
and when a "bool" value is required, an "int" or "float" value can be used in its place.

See auto-casting in action in this code::

    //@version=5
    indicator("")
    plotshape(close)

Note that:

- `plotshape(() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ requires a "series bool" argument for its first parameter named ``series``. The ``true``/``false`` value of that "bool" argument determines if the function plots a shape or not.
- We are here calling `plotshape(() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__ with `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ as its first argument. This would not be allowed without Pine's auto-casting rules, which allow a "float" to be cast to a "bool". When a "float" is cast to a bool, any non-zero values are converted to ``true``, and zero values are converted to ``false``. As a result of this, our code will plot an "X" on all bars, as long as `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ is not equal to zero.

It may sometimes be necessary to cast one type into another because auto-casting rules will not suffice. 
For these cases, explicit type-casting functions exist. They are:

- `int() <https://www.tradingview.com/pine-script-reference/v5/#fun_int>`__
- `float() <https://www.tradingview.com/pine-script-reference/v5/#fun_float>`__
- `bool() <https://www.tradingview.com/pine-script-reference/v5/#fun_bool>`__
- `color() <https://www.tradingview.com/pine-script-reference/v5/#fun_color>`__
- `string() <https://www.tradingview.com/pine-script-reference/v5/#fun_string>`__
- `line() <https://www.tradingview.com/pine-script-reference/v5/#fun_line>`__
- `label() <https://www.tradingview.com/pine-script-reference/v5/#fun_label>`__
- `box() <https://www.tradingview.com/pine-script-reference/v5/#fun_box>`__
- `table() <https://www.tradingview.com/pine-script-reference/v5/#fun_table>`__

This is code that will not compile because we fail to convert the type of the argument used for ``length`` when calling 
`ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__::

    //@version=5
    indicator("")
    len = 10.0
    s = ta.sma(close, len) // Compilation error!
    plot(s)

The code fails to compile with the following error: 
*Cannot call 'ta.sma` with argument 'length'='len'. An argument of 'const float' type was used but a 'series int' is expected;*. 
The compiler is telling us that we supplied a "float" value where an "int" is required. There is no auto-casting rule that can automatically cast a "float" to an "int", 
so we will need to do the job ourselves. For this, we will use the `int() <https://www.tradingview.com/pine-script-reference/v5/#fun_int>`__ function to force the type conversion of the value we supply as a length to `ta.sma() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}sma>`__ from "float" to "int"::

    //@version=5
    indicator("")
    len = 10.0
    s = ta.sma(close, int(len))
    plot(s)

Explicit type-casting can also be useful when declaring variables and initializing them to `na <https://www.tradingview.com/pine-script-reference/v4/#var_na>`__ which can be done in two ways::

    // Cast `na` to the "label" type.
    lbl = label(na)
    // Explicitly declare the type of the new variable.
    label lbl = na
