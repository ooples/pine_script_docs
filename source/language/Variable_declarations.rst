.. _PageVariableDeclarations:

Variable declarations
=====================

.. contents:: :local:
    :depth: 2



Introduction
------------

Variables are :ref:`identifiers <PageIdentifiers>` that hold values. 
They must be *declared* in your code, which means defining:

- A name, using an :ref:`identifier <PageIdentifiers>`
- The initial value they will have, by using the ``=`` assignment operator. 
  The initial value can be an expression, a function call or an 
  `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__,
  `for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__,
  `while <https://www.tradingview.com/pine-script-reference/v5/#op_while>`__ or
  `switch <https://www.tradingview.com/pine-script-reference/v5/#op_switch>`__ *structure*
- When they will be initialized (by using the
  `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__ or 
  `varip <https://www.tradingview.com/pine-script-reference/v5/#op_varip>`__ keyword, or nothing)
- Optionally, their :ref:`type <PageTypeSystem_Types>`

These are all valid variable declarations. The last one requires four lines::

    BULL_COLOR = color.lime
    i = 1
    len = input(20, "Length)
    float f = 10.5
    closeRounded = math.round(close)
    closeRoundedToTick = math.round_to_mintick(close)
    var barRange = high - low
    var firstBarOpen = open
    varip float lastClose = na
    ma = ta.sma(close, 14)
    st = ta.supertrend(4, 14)
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
    	[var | varip] [<type>] <identifier> = <expression> | <function_call> | <structure>
        |
        <tupleOfIdentifiers> = <function_call> | <structure>

``<identifier>`` is the name of the declared variable, see :doc:`Identifiers`.

``<type>`` can be one of the predefined keywords: ``float``, ``int``, ``bool``, ``color``, ``string``, ``line``, ``label``, ``box`` or ``table``.
However, in most cases, an explicit type declaration is redundant because type is automatically inferred from the ``<expression>``
on the right of the ``=`` at compile time, so the decision to use them is often a matter of preference. For example::

    baseLine0 = na          // compile time error!
    float baseLine1 = na    // OK
    baseLine2 = float(na)   // OK

In the first line of the example, the compiler cannot determine the type of the ``baseLine0`` variable because ``na`` is a generic value of no particular type. The declaration of the ``baseLine1`` variable is correct because its ``float`` type is declared explicitly.
The declaration of the ``baseLine2`` variable is also correct because its type can be derived from the expression ``float(na)``, which is an explicit cast of ``na`` value to ``float`` type. The declarations of ``baseLine1`` and ``baseLine2`` are equivalent.



.. _PageVariableDeclarations_VariableReassignment:

Variable reassignment
---------------------


<variable_reassignment>
	<identifier> := <expression> | <function_call> | <structure>

A mutable variable is a variable which can be given a new value.
The operator ``:=`` must be used to give a new value to a variable.
A variable must be declared before you can assign a value to it
(see declaration of variables :ref:`above<PageVariableDeclarations_VariableDeclaration>`).

The type of a variable is identified at declaration time. From then on, a variable can
be given a value of expression only if both the expression and the
variable belong to the same type, otherwise a
compilation error will occur.

Variable assignment example::

    //@version=5
    indicator("My Script")
    price = close
    if hl2 > price
        price := hl2
    plot(price)




Declaration modes
-----------------


On each bar
^^^^^^^^^^^




.. _PageVariableDeclarations_Var:

\`var\`
^^^^^^^

The ``var`` keyword is a special modifier that instructs the compiler to *create and initialize the variable only once*. This behavior is very useful in cases where a variable's value must persist through the iterations of a script across successive bars. For example, suppose we'd like to count the number of green bars on the chart::

    //@version=5
    indicator("Green Bars Count")
    var count = 0
    isGreen = close >= open
    if isGreen
        count := count + 1
    plot(count)

.. image:: images/GreenBarsCount.png

Without the ``var`` modifier, variable ``count`` would be reset to zero (thus losing it's value) every time a new bar update triggered a script recalculation.

In Pine v3 the study "Green Bars Count" could be written without using the ``var`` keyword::

    //@version=3
    study("Green Bars Count")
    count = 0                       // These two lines could be replaced in v4 or v5
    count := nz(count[1], count)    // with 'var count = 0'
    isGreen = close >= open
    if isGreen
        count := count + 1
    plot(count)

The v5 code is more readable and can be more efficient if, for example, the ``count`` variable is
initialized with an expensive function call instead of ``0``.

Examples of simple variable declarations::

    src = close
    len = 10
    ma = ta.sma(src, len) + high

Examples with type modifiers and var keyword::

    float f = 10            // NOTE: while the expression is of type int, the variable is float
    i = int(close)          // NOTE: explicit cast of float expression close to type int
    r = round(close)        // NOTE: round() and int() are different... int() simply throws fractional part away
    var hl = high - low

Example, illustrating the effect of ``var`` keyword::

    // Creates a new label object on every bar:
    label lb = label.new(bar_index, close, text="Hello, World!")

    // Creates a label object only on the first bar in history:
    var label lb = label.new(bar_index, close, text="Hello, World!")



.. _PageVariableDeclarations_Varip:

\`varip\`
^^^^^^^^^




