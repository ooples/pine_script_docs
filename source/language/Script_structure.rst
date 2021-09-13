
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


