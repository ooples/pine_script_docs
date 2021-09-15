.. _PageConditionalStatements:

Conditional statements
======================

.. contents:: :local:
    :depth: 2



.. _PageConditionalStatementsIf:

\`if\`
------

An ``if`` statement defines a block of statements to be executed when
the ``if``'s conditional expression evaluates to ``true``, and optionally,
an alternative block to be executed when the expression is ``false``.

General code form:

.. code-block:: text

    <var_declarationX> = if <condition>
        <var_decl_then0>
        <var_decl_then1>
        ...
        <var_decl_thenN>
    else if [optional block]
        <var_decl_else0>
        <var_decl_else1>
        ...
        <var_decl_elseN>
    else
        <var_decl_else0>
        <var_decl_else1>
        ...
        <var_decl_elseN>
        <return_expression_else>

where:

-  ``var_declarationX`` --- this variable is assigned the value of the ``if``
   statement as a whole.
-  ``condition`` --- if the ``condition`` expression is true, the logic from the *then* block immediately following the ``if`` first line
   (``var_decl_then0``, ``var_decl_then1``, etc.) is used, if the
   ``condition`` is false, the logic from the *else* block
   (``var_decl_else0``, ``var_decl_else1``, etc.) is used.
-  ``return_expression_then``, ``return_expression_else`` --- the last
   expression from the *then* block or from the *else* block will
   determine the final value of the whole ``if`` statement.

The type of the returning value of the ``if`` statement is determined by the type of
``return_expression_then`` and ``return_expression_else``. Their types
must match. It is not possible to return an integer value from the *then* block
if the *else* block returns a string value.

Example::

    // This code compiles
    x = if close > open
        close
    else
        open
    // This code doesn't compile
    x = if close > open
        close
    else
        "open"

It is possible to omit the *else* block. In this case, if the ``condition``
is false, an *empty* value (``na``, ``false``, or ``""``) will be assigned to the
``var_declarationX`` variable.

Example::

    x = if close > open
        close
    // If current close > current open, then x = close.
    // Otherwise the x = na.
    
It is possible to use either multiple *else if* blocks or none at all.

Example::

    x = if open > close
        5
    else if high > low
        close
    else
        open
        
The *then*, *else if* and *else* blocks are shifted by four spaces [#tabs]_. ``if`` statements can
be nested by adding four more spaces::

    x = if close > open
        b = if close > close[1]
            close
        else
            close[1]
        b
    else
        open

It is possible and quite frequent to ignore the resulting value of an ``if`` statement
(``var_declarationX =`` can be omited). This form is used when you need the
side effect of the expression, for example in ``strategy.*()`` calls:

::

    if (ta.crossover(source, lower))
        strategy.entry("BBandLE", strategy.long, stop=lower,
                       oca_name="BollingerBands",
                       oca_type=strategy.oca.cancel, comment="BBandLE")
    else
        strategy.cancel(id="BBandLE")



\`switch\`
----------

