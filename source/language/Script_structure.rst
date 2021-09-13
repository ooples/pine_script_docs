
Script Structure
================

.. include:: <isonum.txt>

A script in Pine usually consists of:

* ``//@version=5`` A compiler directive in a comment that specifies which version of Pine the script will use.
  If the ``@version`` directive is missing, version 1 will be used. It is strongly recommended to always
  use the latest version available.
* An `indicator <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__ or a
  `strategy <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__ annotation call.
  Their parameters define the script's title and other properties.
* A series of statements which implement the script's algorithm.
  Each statement is usually placed on a separate line. It is possible to place more
  than one statement on a line by using the comma (``,``) as a separator.
  Lines containing statements that are not part of local blocks cannot begin with
  white space. Their first character must also be the line's first character.
  Statements may be one of three kinds:

    -  :ref:`variable declarations <variable_declaration>`
    -  :doc:`function declarations <Declaring_functions>`
    -  :doc:`functions and annotations calls <Functions_and_annotations>`

* An *indicator* must contain at least one function/annotation call which produces some output on the chart
  (e.g., ``plot``, ``plotshape``, ``barcolor``, ``line.new``, etc.).
  A *strategy* must contain at least one ``strategy.*`` call, e.g., ``strategy.entry``.

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


Versions
--------

There are currently five versions of the Pine Script Language. A compiler
directive must be used in the first line of a script to specify the version or Pine
used by the script: ``//@version=N`` where ``N`` is the version number (1--5). Note that
different Pine Script Language versions are incompatible with each other.

Notable changes to the language are documented in the :ref:`<PageReleaseNotes>`.



Comments
--------

Pine Script supports single-line comments. Any text from the symbol
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
