.. _PageIdentifiers:

.. image:: /images/Pine_Script_logo_small.png
   :alt: Pine Script™
   :target: https://www.tradingview.com/pine-script-docs/en/v5/index.html
   :align: right
   :width: 50
   :height: 50

Identifiers
===========

Identifiers are names used for user-defined variables and functions:

- They must begin with an uppercase (``A-Z``) or lowercase (``a-z``) letter, or an underscore (``_``).
- The next characters can be letters, underscores or digits (``0-9``).
- They are case-sensitive.

Here are some examples::

    myVar
    _myVar
    my123Var
    functionName
    MAX_LEN
    max_len
    maxLen
    3barsDown  // NOT VALID!

The :ref:`Pine Script™ Style Guide <PageStyleGuide>` recommends using uppercase SNAKE_CASE for constants, and camelCase for other identifiers::

    GREEN_COLOR = #4CAF50
    MAX_LOOKBACK = 100
    int fastLength = 7
    // Returns 1 if the argument is `true`, 0 if it is `false` or `na`.
    zeroOne(boolValue) => boolValue ? 1 : 0
    

.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/