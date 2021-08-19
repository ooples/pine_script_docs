In Pine Script v4 the following built-in constants, variables, and functions were renamed:

Renaming of built-in constants, variables, and functions
--------------------------------------------------------

- Color constants (e.g ``red``) are moved to the ``color.*`` namespace (e.g. ``color.red``).
- The ``color`` function has been renamed to ``color.new``.
- Constants for ``input()`` types (e.g. ``integer``) are moved to the ``input.*`` namespace (e.g. ``input.integer``).
- The plot style constants (e.g. ``histogram`` style) are moved to the ``plot.style_*`` namespace (e.g. ``plot.style_histogram``).
- Style constants for the ``hline`` function (e.g. the ``dotted`` style) are moved to the ``hline.style_*`` namespace (e.g. ``hline.style_dotted``).
- Constants of days of the week (e.g. ``sunday``) are moved to the ``dayofweek.*`` namespace (e.g.  ``dayofweek.sunday``).
- The variables of the current chart timeframe (e.g. ``period``, ``isintraday``) are moved to the ``timeframe.*`` namespace (e.g. ``timeframe.period``, ``timeframe.isintraday``).
- The ``interval`` variable was renamed to ``timeframe.multiplier``.
- The ``ticker`` and ``tickerid`` variables are renamed to ``syminfo.ticker`` and ``syminfo.tickerid`` respectively.
- The ``n`` variable that contains the bar index value has been renamed to ``bar_index``.

The reason behind renaming all of the above was to structure the standard language tools and make working with code easier. New names are grouped according to assignments under common prefixes. For example, you will see a list with all available color constants if you type 'color' in the editor and press Ctrl + Space.

Explicit variable type declaration
----------------------------------
In Pine Script v4 it's no longer possible to create variables with an unknown data type at the time of their declaration. This was done to avoid a number of issues that arise when the variable type changes after its initialization with the na value. From now on, you need to explicitly specify their type using keywords or type functions (for example, ``float``) when declaring variables with the na value::

  //@version=4
  study("NA", overlay=true)
  float a = na
  a := if close >= open
      high
  else
      low
  plot(a)
