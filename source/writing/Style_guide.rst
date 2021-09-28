.. _PageStyleGuide:

Style guide
===========

.. contents:: :local:
    :depth: 2

.. include:: <isonum.txt>



Introduction
------------

This style guide provides recommendations on how to name variables and organize your Pine scripts in a standard way that works well. 
Scripts that follow our best practices will be easier to read, understand and maintain. 

Every Pine programmer is, of course, free to use all or as many of our recommendations as he pleases. 
As Ed Seykota says: *Follow the rules without question, and know when to break the rules*.


Naming Conventions
------------------

We recommend the use of:

- ``camelCase`` for all identifiers, i.e., variable or function names: ``ma``, ``maFast``, ``maLengthInput``, ``maColor``, ``roundedOHLC()``, ``pivotHi()``.
- All caps ``SNAKE_CASE`` for constants: ``BULL_COLOR``, ``BEAR_COLOR``, ``MAX_LOOKBACK``.
- The use of qualifying suffixes when it provides valuable clues to the nature of the variable: ``maShowInput``, ``bearColor``, ``bearColorInput``, ``volumesArray``, ``maPlotID``, ``resultsTable``, ``levelsColorArray``.


Script organization
-------------------

The Pine compiler is quite forgiving of the positioning of specific statements or compiler directives in the script. While other arrangements are syntactically correct, this is how we recommend organizing scripts:

.. code-block:: text

    <license>
    <version>
    <indicator/strategy/library_declaration_statement>
    <import_statements>
    <constant_declarations>
    <inputs>
    <function_declarations>
    <calculations>
    <strategy_calls>
    <plots>
    <alerts>



<license>
^^^^^^^^^
If you publish your open-source scripts publicly on TradingView (scripts can also be published privately), your open-source code is by default protected by the Mozilla license. You may choose any other license you prefer.

The reuse of code from those scripts is governed by our `House Rules on Script Publishing <https://www.tradingview.com/house-rules/?solution=43000590599>`__ which preempt the author's license. Because these rules require permission from the author before one can reuse his code in other public scripts, authors who do not wish to receive requests for reuse may find it useful to mention their preference in the license section, e.g.,::

    // REUSING THIS CODE: You are welcome to reuse this code without permission. Credits are appreciated.

or::

    // REUSING THIS CODE: You are welcome to reuse this code without permission, including in closed-source publications. Credits are always appreciated.


<version>
^^^^^^^^^
This is the compiler directive defining the version of Pine the script will use. If none is present, v1 is used. For v5, use::

    //@version=5


<indicator/strategy/library_declaration_statement>
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the call to `indicator() <https://www.tradingview.com/pine-script-reference/v5/#fun_indicator>`__, `strategy() <https://www.tradingview.com/pine-script-reference/v5/#fun_strategy>`__ or  `library() <https://www.tradingview.com/pine-script-reference/v5/#fun_library>`__, which defines the type of your script.


<import_statements>
^^^^^^^^^^^^^^^^^^^
If your script uses one or more Pine :ref:`here <PageLibraries>`, your `import <https://www.tradingview.com/pine-script-reference/v5/#op_import>`__ statements belong here.


<constant_declarations>
^^^^^^^^^^^^^^^^^^^^^^^
What we consider to be constant definitions to be included in this section — and thus named using our ``SNAKE_CASE`` convention — are variables:

- Initialized using a literal (e.g., ``100`` or ``"AAPL"``) or a built-in of "const" form (e.g., ``color.green``)
- Whose value does not change during the script's execution

Literals used in more than one place in a script should always be used to initialize a constant. Using the constant rather than the literal makes it more readable if it is given a meaningful name, and the practice makes code easier to maintain. Even though the quantity of milliseconds in a day is unlikely to change in the future, ``MS_IN_1D`` is more meaningful than ``1000 * 60 * 60 * 24``.

Note that:

- Constants only used in the local block of a function or `if <https://www.tradingview.com/pine-script-reference/v5/#op_if>`__, `while <https://www.tradingview.com/pine-script-reference/v5/#op_while>`__, etc., statement for example, can be declared in that local block.
- Using the `var <https://www.tradingview.com/pine-script-reference/v5/#op_var>`__ to initialize constants is unnecessary, and will incur a minor penalty on script performance.


<inputs>
^^^^^^^^

It is **much** easier to read scripts when all their inputs are in the same code section. Placing that section at the beginning of the script also corresponds to how they are processed, i.e., before the script begins execution.


<function_declarations>
^^^^^^^^^^^^^^^^^^^^^^^

All user-defined functions must be defined in the script's global scope; nested function definitions are not allowed in Pine.

Optimal function design should minimize the use of global variables in the function's scope, as they undermine function portability. When it cannot be avoided, those functions must follow the global variable declarations in the code, which entails they cannot always be placed in the <function_declarations> section. Such dependencies on global variables should ideally be documented in the function's comments.

It will also help readers if you document the function's objective, parameters and result. The same syntax used in :ref:`libraries <PageLibraries>` can be used to document your functions. This can make it easier to port your functions to a library should you ever decide to do so. Placing the documentation inside the function, as opposed to outside of it as is done in libraries, will prevent confusion::


    //@version=5
    indicator("", "", true)
    
    SIZE_LARGE  = "Large"
    SIZE_NORMAL = "Normal"
    SIZE_SMALL  = "Small"

    sizeInput = input.string(SIZE_NORMAL, "Size", options = [SIZE_LARGE, SIZE_NORMAL, SIZE_SMALL])

    getSize(userSize) =>
        // @function Used to produce an argument for a `size` parameter in built-in functions.
        // @param string userSize User-selected size.
        // @returns One of the `size.*` built-in constants.
        // Dependencies: SIZE_LARGE, SIZE_NORMAL, SIZE_SMALL
        userSize  == SIZE_LARGE  ? size.large  :
         userSize == SIZE_NORMAL ? size.normal :
         userSize == SIZE_SMALL  ? size.small  : size.auto

    if ta.rising(close, 3)
        label.new(bar_index, na, yloc = yloc.abovebar, style = label.style_arrowup, size = getSize(sizeInput))


<calculations>
^^^^^^^^^^^^^^

This is where the script's core calculations and logic should be placed. Code can be easier to read when variable declarations are placed near the code segment using the variables. Some coders prefer to place all their non-constant variable declarations at the beginning of this section, which is not always possible for all variables, as some may require some calculations to have been executed before their declaration.


<strategy_calls>
^^^^^^^^^^^^^^^^

Strategies are easier to read when strategy calls are grouped in the same section of the script.


<plots>
^^^^^^^

This section should ideally include all the statements producing the script's visuals, whether they be plots, drawings, background colors, candle-plotting, etc. 
See the User Manual's section on :ref:`here <PageColors_ZIndex>` for more information on how the relative depth of visuals is determined.


<alerts>
^^^^^^^^

Alert code will usually require the script's calculations to have executed before it, so it makes sense to put it at the end of the script.



Spacing
-------

A space should be used on both sides of all operators, except unary operators (``-1``). A space is also recommended after all commas and when using named function arguments, as in ``plot(series = close)``::

    a = close > open ? 1 : -1
    var newLen = 2
    newLen := min(20, newlen + 1)
    a = -b
    c = d > e ? d - e : d
    index = bar_index % 2 == 0 ? 1 : 2
    plot(close, color = color.red)



Line Wrapping
-------------

Line wrapping can make long lines easier to read. Line wraps are defined by using an indentation level that is not a multiple of four, as four spaces or a tab are used to define local blocks. Here we use two spaces::

    plot(
      series = close,
      title = "Close",
      color = color.blue,
      show_last = 10
      )



Collapsible code sections
-------------------------

Code sections in larger projects can be more cleanly defined using comments that make them easily identifiable and expandable/collapsible. Curly braces can be used in comments to define the beginning and end of code sections, which you can then expand or collapse using the small arrows in the Editor's left margin::

    // ———————————————————— Constants {
    <constant_declarations>
    // }



Vertical alignment
------------------

Vertical alignment using tabs or spaces can be useful in code sections containing many similar lines such as constant declarations or inputs. 
They can make mass edits much easier using the Editor's multi-cursor feature (:kbd:`ctrl` + :kbd:`alt` + :kbd:`🠅`/:kbd:`🠇`)::

    // ———————————————————— Constants {

    // Colors used as defaults in inputs.
    color COLOR_AQUA    = #0080FFff
    color COLOR_BLACK   = #000000ff
    color COLOR_BLUE    = #013BCAff
    color COLOR_CORAL   = #FF8080ff
    color COLOR_GOLD    = #CCCC00ff
    // }



Explicit typing
---------------

Including the type of variables when declaring them is not required and is usually overkill for small scripts; we rarely use it in this manual. It can be useful to make the type of a function's result clearer, and to distinguish a variable's declaration (using ``=``) from its reassignments (using ``:=``). Using explicit typing can also make it easier for readers to find their way in larger scripts. We use explicit typing in both variable declarations here::

    //@version=5
    indicator("", "", true)
    var float allTimeHi = high
    allTimeHi := math.max(allTimeHi, high)
    bool newAllTimeHi = ta.change(allTimeHi)
    plot(allTimeHi)
    plotchar(newAllTimeHi, "newAllTimeHi", "•", location.top, size = size.tiny)
