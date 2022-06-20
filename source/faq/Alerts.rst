.. image:: /images/Pine_Script_logo.svg
   :alt: Pine Script™ logo
   :target: https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html
   :align: right
   :width: 100
   :height: 100

.. _PageAlertsFaq:

Alerts FAQ
==========


.. contents:: :local:
    :depth: 3




How do I make an alert available from my script?
------------------------------------------------

Two steps are required:

    1. Insert an alertcondition() call in a script.
    2. Create an alert from the TV Web user interface (ALT-A) and choose the script’s alert condition.

See the User Manual page on alertcondition(). Code to create an alert condition looks like:

::

    triggerCondition = close > close[1]
    alertcondition(triggerCondition, title = "Create Alert dialog box name", message = "Text sent with alert.")
    
When you need to create multiple alerts you can repeat the method above for every alert you want your indicator to generate, but you can also use the method shown in this indicator. Here, all the different alert conditions 
are bunched up in one alertcondition() statement. In this case, you must provide the means for users to first select which conditions will trigger the alert in the Inputs dialog box. When all the required conditions are 
selected, the user creates an alert using the only alert this indicator makes available, but since TradingView remembers the state of the Inputs when creating an alert, only the selected conditions will trigger the alert once it’s 
created, even if Inputs selections are modified by the user after the alert is created.

When more than one condition can trigger a single alert, you will most probably need to have visual cues for each condition so that when users bring up a chart on which an alert triggered they can figure out which condition 
caused the alert to trigger. This is a method that allows users of your script to customize the alert to their needs.

When TradingView creates an alert, it saves a snapshot of the environment that will enable the alert to run on the servers. The elements saved with an alert are:

    * Current symbol
    * Current time frame
    * State of the script’s Inputs selections
    * Current version of the script. Subsequent updates to the script’s code will not affect the alerts created with prior versions

Note that while alert condition code will compile in strategy scripts, alerts are only functional in studies.




How can I include values that change in my alerts?
--------------------------------------------------

Numeric values plotted by an indicator can be inserted in alert text using placeholders. If you use:

::

    plot(myRsi, "rsiLine")

in your script, then you can include that plot’s value in an alert message by using:

::

    alertcondition(close > open, message='RSI value is: {{plot("rsiLine")}}')

If you are not already plotting a value which you must include in an alert message, you can plot it using this method so that plotting the value will not affect the price scale unless you use:

::
    
    plotchar(myRsi, "myRsi", "", location.top)

You can use other pre-defined placeholders to include variable information in alert messages. See this TV blog post on variable alerts for more information.

    Note that there is still no way to include variable text in an alert message.


.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/
