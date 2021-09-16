
.. _PageExpressionsDeclarationsStatements:

Expressions, declarations and statements
========================================

.. contents:: :local:
    :depth: 2



.. _PageExpressionsDeclarationsStatements_Expressions:

Expressions
-----------

An expression is a sequence where operators or function
calls are applied to operands (variables or values) to define the calculations
and actions required by the script. Expressions in Pine almost always
produce a result (exceptions are the functions
``indicator``, ``fill``, ``strategy.entry``, etc., which produce side effects and will be covered
later).

Here are some examples of simple expressions::

    (high + low + close)/3
    ta.sma(high - low, 10) + ta.sma(close, 20)

.. _variable_declaration:



.. _PageExpressionsDeclarationsStatements_VariableDeclaration:

Variable declaration
--------------------

Variables in Pine are declared with the special symbol ``=`` and an optional ``var`` keyword
in one of the following ways:

.. code-block:: text

    <identifier> = <expression>
    <type> <identifier> = <expression>
    var <identifier> = <expression>
    var <type> <identifier> = <expression>

``<identifier>`` is the name of the declared variable, see :doc:`Identifiers`.

``<type>`` can be one of the predefined keywords: ``float``, ``int``, ``bool``, ``color``, ``string``, ``line``, ``label``, ``box`` or ``table``.
However, in most cases, an explicit type declaration is redundant because type is automatically inferred from the ``<expression>``
on the right of the ``=`` at compile time, so the decision to use them is often a matter of preference. For example::

    baseLine0 = na          // compile time error!
    float baseLine1 = na    // OK
    baseLine2 = float(na)   // OK

In the first line of the example, the compiler cannot determine the type of the ``baseLine0`` variable because ``na`` is a generic value of no particular type. The declaration of the ``baseLine1`` variable is correct because its ``float`` type is declared explicitly.
The declaration of the ``baseLine2`` variable is also correct because its type can be derived from the expression ``float(na)``, which is an explicit cast of ``na`` value to ``float`` type. The declarations of ``baseLine1`` and ``baseLine2`` are equivalent.

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



.. _PageExpressionsDeclarationsStatements_VariableReassignment:

Variable reassignment
---------------------

A mutable variable is a variable which can be given a new value.
The operator ``:=`` must be used to give a new value to a variable.
A variable must be declared before you can assign a value to it
(see declaration of variables :ref:`above<PageExpressionsDeclarationsStatements_VariableDeclaration>`).

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



.. rubric:: Footnotes

.. [#tabs] TradingView's *Pine Editor* automatically replaces **Tab** with 4 spaces.
