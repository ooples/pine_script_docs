.. _PageScriptStructure:

Script Structure
================

.. contents:: :local:
    :depth: 3

.. include:: <isonum.txt>


A script in Pine follows this general structure:

.. code-block:: text

  <version>
  <declaration_statement>
  <code>



Version
-------

A compiler directive in the following form tells the compiler which of the versions of Pine the script is written in::

    //@version=5
    
- The version number can be 1 to 5.
- The compiler directive is not mandatory, but if omitted, version 1 is assumed. It is strongly recommended to always
  use the latest version.
- While it is synctactically correct to place the directive anywhere in the script, it is much more useful to readers when placed at the top of the script.

Notable changes to the language are documented in the :ref:`<PageReleaseNotes>`.



Declaration statement
---------------------

The script must also contain a *declaration statement*, which is a call to one of these functions:

- `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__
- `strategy() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__
- `library() <https://www.tradingview.com/pine-script-reference/v5/#fun_library>`__

The declaration statement:

- Identifies the type of the script, which in turn dictates which content is allowed in it, and how it be used and executed.
- Sets key properties of the script such as its name, where it will appear when it is added to a chart, the precision and format of the values it displays, 
  and certain values that govern its runtime behavior, such as the maximum number of drawing objects it will display on the chart. 
  With strategies, the properties include parameters that control backtesting such as initial capital, commission, slippage, etc.

Each type of script has distinct requirements:

- Indicators must contain at least one function call which produces output on the chart
  (e.g., `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__, 
  `plot() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotshape>`__,
  `plotshape() <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__,
  `barcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_barcolor>`__,
  `line.new() <https://www.tradingview.com/pine-script-reference/v5/#fun_line{dot}new>`__, etc.).
- Strategies must contain at least one ``strategy.*()`` call, e.g., 
  `strategy.entry <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy{dot}entry>`__.
- Libraries must contain at least one library function and cannot contain ``strategy.*()`` calls.



Code
----

Pine code consists of a collection of *statements* which implement the script's algorithm. Statements may be one of three kinds:

- :ref:`Variable declarations <PageExpressionsDeclarationsStatements_VariableDeclaration>`
- :ref:`Function declarations <PageUserDefinedFunctions_DeclaringFunctions>`
- Functions calls (see :ref:`how to call built-in functions <PageBuiltInFunctions_CallingBuiltInFunctions>`,
  :ref:`how to call user-defined functions <PageUserDefinedFunctions_CallingUserDefinedFunctions>`
  and :ref:`how to call library functions <PageLibraries_UsingALibrary>`


- Some statements can be expressed in one line (many variable declarations); others require multiple lines 
  (`if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__, 
  `for <https://www.tradingview.com/pine-script-reference/v5/#op_for>`__, 
  `switch <https://www.tradingview.com/pine-script-reference/v5/#op_switch>`__, etc.).
- Lines that are not part of a *local block* cannot begin with white space (space or tab). 
  Their first character must also be the line's first character.
  A local block is the code inside user-defined functions or other statements requiring indentation such as
  `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__.
- Multiple one-line statements can be concatenated on a single line by using the comma (``,``) as a separator.
- Lines can contain comments, or be comments.
- Lines can be wrapped.



  The simplest valid Pine v5 study can be generated using *Pine Editor* |rarr| *Open* |rarr| *New blank indicator*::

    //@version=5
    indicator("My Script")
    plot(close)

  A simple valid Pine v5 strategy can be generated using *Pine Editor* |rarr| *Open* |rarr| *New blank strategy*::

    //@version=5
    strategy("My Strategy", overlay=true, margin_long=100, margin_short=100)

    longCondition = crossover(sma(close, 14), sma(close, 28))
    if (longCondition)
        strategy.entry("My Long Entry Id", strategy.long)

    shortCondition = crossunder(sma(close, 14), sma(close, 28))
    if (shortCondition)
        strategy.entry("My Short Entry Id", strategy.short)



Comments
--------

Pine supports single-line comments. Any text from the symbol
``//`` until the end of the line is considered as comment. An example::

    //@version=5
    indicator("Test")
    // This line is a comment
    a = close // This is also a comment
    plot(a)

The *Pine Editor* has a hotkey for commenting/uncommenting:
``Ctrl + /``. Highlight a code fragment and press ``Ctrl + /``
to comment/uncomment whole blocks of code at a time.

Comments cannot be placed in the middle of a statement continued
on multiple lines. Read more on this here: :doc:`Line_wrapping`.



Line wrapping
-------------

Any statement that is too long in Pine Script can be placed on more than
one line. Syntactically, a statement **must** begin at the beginning of the
line. If it wraps to the next line then the continuation of the
statement **must** begin with one or several (different from multiple of 4)
spaces. For example::

    a = open + high + low + close

may be wrapped as:

::

    a = open +
          high +
              low +
                 close

A long ``plot`` call may be wrapped as:

::

    plot(ta.correlation(src, ovr, length),
       color=color.new(color.purple, 40),
       style=plot.style_area,
       trackprice=true)

Statements inside user functions can also be wrapped.
However, since a local statement must syntactically begin with an
indentation (4 spaces or 1 tab), when splitting it onto the
following line, the continuation of the statement must start with more
than one indentation (not equal to multiple of 4 spaces). For
example:

::

    updown(s) =>
        isEqual = s == s[1]
        isGrowing = s > s[1]
        ud = isEqual ?
               0 :
               isGrowing ?
                   (nz(ud[1]) <= 0 ?
                         1 :
                       nz(ud[1])+1) :
                   (nz(ud[1]) >= 0 ?
                       -1 :
                       nz(ud[1])-1)

Do not use comments with line wrapping.
The following code does NOT compile::

    //@version=5
    indicator("My Script")
    c = open > close ? color.red :
      high > high[1] ? color.lime : // a comment
      low < low[1] ? color.blue : color.black
    bgcolor(c)


The compiler fails with the error:
``Add to Chart operation failed, reason: line 3: syntax error at input 'end of line without line continuation'``.
To make this code compile, simply remove the ``// a comment`` comment.
