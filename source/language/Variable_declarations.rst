.. _PageVariableDeclarations:

Variable declarations
=====================

.. contents:: :local:
    :depth: 2



Introduction
------------

Variables are :ref:`identifiers <PageIdentifiers>` that hold values. 
They must be *declared* in your code, which means defining, in order:

- Their declaration mode, by using the
  `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__ or 
  `varip <https://www.tradingview.com/pine-script-reference/v5/#op_varip>`__ keyword, or nothing
- Optionally, their :ref:`type <PageTypeSystem_Types>`
- A name, using an :ref:`identifier <PageIdentifiers>`
- The initial value they will have, by using the ``=`` assignment operator. 
  The initial value can be an expression, a function call or an 
  `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__,
  `for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__,
  `while <https://www.tradingview.com/pine-script-reference/v5/#op_while>`__ or
  `switch <https://www.tradingview.com/pine-script-reference/v5/#op_switch>`__ *structure*

These are all valid variable declarations. The last one requires four lines::

    BULL_COLOR = color.lime
    i = 1
    len = input(20, "Length)
    float f = 10.5
    closeRoundedToTick = math.round_to_mintick(close)
    st = ta.supertrend(4, 14)
    var barRange = float(na)
    var firstBarOpen = open
    varip float lastClose = na
    [macdLine, signalLine, histLine] = ta.macd(close, 12, 26, 9)
    plotColor = if close > open
        color.green
    else
        color.red
 
.. note:: The above statements all contain the ``=`` assignment operator because they are **variable declarations**.
  When you see similar lines using the :ref:`:= <PageOperators_ReassignmentOperator>` reassignment operator, 
  the code is **reassigning** a value to a variable that was **already declared**.
  Those are **variable reassignments**.
  Be sure you understand the distinction as this is a common stumbling block for newcomers to Pine. 
  See the next :ref:`Variable reassignment <PageVariableDeclarations_VariableReassignment>` section for details.

The formal syntax of a variable declaration is:

.. code-block:: text

    <variable_declaration>
    	[<declaration_mode>] [<type>] <identifier> = <expression> | <structure>
        |
        <tuple_declaration> = <function_call> | <structure>

    <declaration_mode>
        var | varip

    <type>
        int   | float   | bool   | color   | string   | label   | line   | box   | table | 
        int[] | float[] | bool[] | color[] | string[] | label[] | line[] | box[] | table[]



Initialization with \`na\`
^^^^^^^^^^^^^^^^^^^^^^^^^^

In most cases, an explicit type declaration is redundant 
because type is automatically inferred from the value
on the right of the ``=`` at compile time, 
so the decision to use them is often a matter of preference. For example::

    baseLine0 = na          // compile time error!
    float baseLine1 = na    // OK
    baseLine2 = float(na)   // OK

In the first line of the example, the compiler cannot determine the type of the ``baseLine0`` variable 
because `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ is a generic value of no particular type. 
The declaration of the ``baseLine1`` variable is correct because its 
`float <https://www.tradingview.com/pine-script-reference/v5/#op_float>`__ type is declared explicitly.
The declaration of the ``baseLine2`` variable is also correct because its type can be derived from the expression ``float(na)``, 
which is an explicit cast of the `na <https://www.tradingview.com/pine-script-reference/v5/#var_na>`__ 
value to the `float <https://www.tradingview.com/pine-script-reference/v5/#op_float>`__ type. 
The declarations of ``baseLine1`` and ``baseLine2`` are equivalent.



.. _PageVariableDeclarations_TupleDeclarations:

Tuple declarations
^^^^^^^^^^^^^^^^^^

Function calls or structures are allowed to return multiple values. 
When we call them and want to store the values they return,
a *tuple declaration* must be used, which is a comma-separated set of one or more values enclosed in brackets.
This allows us to declare multiple variables simultaneously.
As an example, the `ta.bb() <https://www.tradingview.com/pine-script-reference/v5/#fun_ta{dot}bb>`__
built-in function for Bollinger bands returns three values::

    [bbMiddle, bbUpper, bbLower] = ta.bb(close, 5, 4)



.. _PageVariableDeclarations_VariableReassignment:

Variable reassignment
---------------------

A variable reassignment is done using the :ref:`:= <PageOperators_ReassignmentOperator>` reassignment operator.
It can only be done after a variable has been first declared and given an initial value.
Reassigning a new value to a variable is often necessary in calculations,
and it is always necessary when a variable from the global scope must be assigned a new value from within a structure's local block, e.g.::

    //@version=5
    indicator("", "", true)
    sensitivityInput = input.int(2, "Sensitivity", minval = 1, tooltip = "Higher values make color changes less sensitive.")
    ma = ta.sma(close, 20)
    maUp = ta.rising(ma, sensitivityInput)
    maDn = ta.falling(ma, sensitivityInput)
    
    // On first bar only, initialize color to gray
    var maColor = color.gray
    if maUp
        // MA has risen for two bars in a row; make it lime.
        maColor := color.lime
    else if maDn
        // MA has fallen for two bars in a row; make it fuchsia.
        maColor := color.fuchsia
    
    plot(ma, "MA", maColor, 2)

Note that:

- We initialize ``maColor`` on the first bar only, so it preserves its value across bars.
- On every bar, the `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__
  statement checks if the MA has been rising or falling for the user-specified number of bars
  (the default is 2). When that happens, the value of ``maColor`` must be reassigned a new value
  from within the `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__ local blocks.
  To do this, we use the :ref:`:= <PageOperators_ReassignmentOperator>` reassignment operator.
- If we did not use the :ref:`:= <PageOperators_ReassignmentOperator>` reassignment operator,
  the effect would be to initialize a new ``maColor`` local variable which would have the same name
  as that of the global scope, but actually be a very confusing independent entity that would persist
  only for the length of the local block, and then disappear without a trace.

A variable can be reassigned as many times as needed during the script's execution on one bar,
so a script can contain any number of reassignments of one variable.

Reassigning a value to a variable makes it a **mutable variable**.
It may also change a variable's *form* 
(see the page on Pine's :ref:`type system <PageTypeSystem>` for more information).



.. _PageVariableDeclarations_DeclarationModes:

Declaration modes
-----------------

Understanding the impact that declaration modes have on the behavior of variables requires
prior knowledge of Pine's :ref:`execution model <PageExecutionModel>`.

The declaration mode, if it is specified, must come first when you declare a variable.
Three modes can be used:

- "On each bar", when none is specified
- `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__
- `varip <https://www.tradingview.com/pine-script-reference/v5/#op_varip>`__



On each bar
^^^^^^^^^^^

When no explicit declaration mode is specified, i.e.  
no `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__ or 
`varip <https://www.tradingview.com/pine-script-reference/v5/#op_varip>`__ keyword is used,
the variable is declared and initialized on each bar, e.g.,
the following declarations from our first set of examples in this page's introduction::

    BULL_COLOR = color.lime
    i = 1
    len = input(20, "Length)
    float f = 10.5
    closeRoundedToTick = math.round_to_mintick(close)
    st = ta.supertrend(4, 14)
    [macdLine, signalLine, histLine] = ta.macd(close, 12, 26, 9)
    plotColor = if close > open
        color.green
    else
        color.red



.. _PageVariableDeclarations_Var:

\`var\`
^^^^^^^

When the `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__ keyword is used,
the variable is only initilized once, on the first bar. After that, it will preserve its last value 
on successive bars, until we reassign a new value to it.
This behavior is very useful in many cases where a variable's value must persist through the iterations of a script across successive bars. 
For example, suppose we'd like to count the number of green bars on the chart::

    //@version=5
    indicator("Green Bars Count")
    var count = 0
    isGreen = close >= open
    if isGreen
        count := count + 1
    plot(count)

.. image:: images/VariableDeclarations-GreenBarsCount.png

Without the ``var`` modifier, variable ``count`` would be reset to zero (thus losing it's value) 
every time a new bar update triggered a script recalculation.

Using Example, illustrating the effect of ``var`` keyword::

    // Creates a new label object on every bar:
    label lb = label.new(bar_index, close, text="Hello, World!")

    // Creates a label object only on the first bar in history:
    var label lb = label.new(bar_index, close, text="Hello, World!")



.. _PageVariableDeclarations_Varip:

\`varip\`
^^^^^^^^^




