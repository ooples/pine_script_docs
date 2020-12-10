Debugging
=========

.. contents:: :local:
    :depth: 2



Introduction
------------

TradingView's close integration between the Pine Editor and charts allows for efficient and interactive debugging of Pine code. 
Once a Pine programmer understands the most appropriate technique to debug each type of situation, he will be able to debug quickly and thoroughly. 
This page demonstrates the most useful techniques to debug Pine code.

If you are not yet familiar with Pine's execution model, it is important that you read the :doc:`/language/Execution_model` page of this User Manual 
so you understand how your debugging code will behave in the Pine environment.



The lay of the land
-------------------

Values plotted by Pine scripts can be displayed in four distinct places:

#. Next to the script's name (controlled by the *Indicator Values* checkbox in the *Chart settings/Status Line* tab).
#. In the script's pane, whether your script is an overlay on the chart or in a separate pane.
#. In the scale (only displays the last bar's value and is controlled by the *Indicator Last Value Label* in the *Chart settings/Scale* tab).
#. In the Data Window (which you can bring up using the fourth icon down to the right of your chart).

.. image:: images/Debugging-TheLayOfTheLand-1.png

Note the following in the preceding screenshot:

- The chart's cursor is on the dataset's first bar, where ``bar_index`` is zero. That value is reflected in its display next to the indicator's name and in the Data Window. **Moving your cursor on other bars would update the value shown so that it always represents the value of the plot on that bar.** This is a good way to inspect the value of a variable as the script's execution progresses from bar to bar.
- The `plot() <https://www.tradingview.com/pine-script-reference/v4/#fun_plot>`__ call in our script plots the value of ``bar_index`` in the indicator's pane, which shows the increasing value of the variable.
- The precision of the values displayed in the Data Window is dependent on the chart symbol's tick value. You can modify it in two ways:
 
  - By changing the value of the *Precision* field in the script's *Settings/Style* tab. You can obtain up to eight digits of precision using this method.

  - By using the ``precision`` parameter in your script's `study() <https://www.tradingview.com/pine-script-reference/v4/#fun_study>`__ or `strategy() <https://www.tradingview.com/pine-script-reference/v4/#fun_strategy>`__ declaration statement. This method allows specifying up to 16 digits precision.



Displaying numeric values
-------------------------

The script used in the preceding screenshot uses the simplest way to inspect numerical values: a `plot() <https://www.tradingview.com/pine-script-reference/v4/#fun_plot>`__ 
call, which plots a line corresponding to the variable's value.  in the script's display area. We use this technique to plot the value of `bar_index <https://www.tradingview.com/pine-script-reference/v4/#var_bar_index>`__ 
on each bar. ``bar_index`` is a built-in variable in Pine. It contains a bar's number, which begins at zero on the dataset's first bar and increases by one on each 
subsequent bar::

    //@version=4
    study("Plot `bar_index`")
    plot(bar_index)


Preserving the script's scale
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Plotting values in the script's scale is not always possible, as they may distort the script's scale and make other plots unreadable.
Displaying values 


Preserving the script's scale
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Displaying strings
------------------


Debugging from inside functions
-------------------------------


Debugging from inside 'for' loops
---------------------------------


Debugging conditions
--------------------


