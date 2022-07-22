.. image:: /images/Pine_Script_logo.svg
   :alt: Pine Script™ logo
   :target: https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html
   :align: right
   :width: 100
   :height: 100


.. _PageIndicatorsFaq:


Indicators FAQ
==============


.. contents:: :local:
    :depth: 3



Can I use a Pine script with the TradingView screener?
------------------------------------------------------

At present, Pine Script™ cannot be used to generate a stock screener. 
However, a custom screener can be built by using `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ to get the data 
of other tickers within indicator or strategy script. 
However, limitation of this method will be:

 - Only 40 tickers can be used in the screener and users will need to feed the tickers manually.
 - Expect a slower performance of the script due to the loading time required for security calls.



Can I create an indicator that plots like the built-in Volume or Volume Profile indicators?
-------------------------------------------------------------------------------------------

No. A few of the built-in indicators TradingView publishes are written in JavaScript because their behavior cannot be replicated in Pine Script™. 
The Volume and Volume Profile indicators are among those. 
This `Stack Overflow answer <https://stackoverflow.com/questions/60346464/tradingview-pine-script-how-can-i-make-custom-volume-indicator-behave-like-a-b>`__ provides an 
imperfect workaround.



How can I use one script’s output as an input into another?
-----------------------------------------------------------

This can be done by using the `input.source() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}source>`__ function. 
When an input is declared with `input.source() <https://www.tradingview.com/pine-script-reference/v5/#fun_input{dot}source>`__, 
it gives the script an ability to select the output of other scripts for the given value. This can be done in the script settings.

Limitations include:
 - Only plots can be used as an input for other scripts.
 - Every time an indicator is loaded on a chart, inputs will need to be manually selected.



Is it possible to export indicator data to a file?
--------------------------------------------------

Yes, through the ``Export chart data...`` item in the dropdown menu at the top right of your chart. 
The exported CSV data will include time and OHLC data, plus any plots your script is plotting. It is thus a matter of plotting the information you want to appear in the CSV file. 
When plotting values outside the scale of your indicator, or if you simply don’t want the plots to show, you may find it useful to use the 
`plot()'s <https://www.tradingview.com/pine-script-reference/v5/#fun_plot>`__ function ``display = parameter`` so that it doesn’t disrupt your script’s scale. 
The name of the plot will appear in the CSV column header:

::

    plot(close * 0.5, "No Display", display = display.none)

Note that you can export strategy data using the same method.



Can my script place something on the chart when it is running from a pane?
--------------------------------------------------------------------------

The only thing that can be changed on the chart from within a pane is the color of the bars. 
See the `barcolor() <https://www.tradingview.com/pine-script-reference/v5/#fun_barcolor>`__ function.



.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/