.. _PageLimitations:

.. image:: /images/Pine_Script_logo_small.png
   :alt: Pine Script™
   :target: https://www.tradingview.com/pine-script-docs/en/v5/index.html
   :align: right
   :width: 50
   :height: 50

Limitations
===========

.. contents:: :local:
    :depth: 3



Introduction
------------

As is mentioned in our :ref:`Welcome <PageWelcomeToPine>` page:

    Because each script uses computational resources in the cloud, we must impose limits in order to share these resources fairly among our users. 
    We strive to set as few limits as possible, but will of course have to implement as many as needed for the platform to run smoothly. 
    Limitations apply to the amount of data requested from additional symbols, execution time, memory usage and script size.

If you develop complex scripts using Pine Script™, sooner or later you will run into some of the limitations we impose.
This section provides you with an overview of the limitations that you may encounter.
There are currently no means for Pine Script™ programmers to get data on the resources consumed by their scripts.
We hope this will change in the future.

In the meantime, when you are considering large projects, it is safest to make a proof of concept 
in order to assess the probability of your script running into limitations later in your project.

The most frequent limitations Pine Script™ programmers encounter are:

- The 500 ms maximum execution time for any loop on one bar.
- The limit of 40 `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ calls.

Here are the limits imposed in the Pine Script™ environment. They are divided into ones imposed at compile time and runtime.



Compiler
--------



Code
^^^^

- 60K compiled tokens
- 100,000 elements array size
- 1K variables per local block
- 500 local blocks
- 9 tables (one in each of the possible locations)



Plot count
^^^^^^^^^^

- plot*()
- alertcondition()



\`request.*()\` functions
^^^^^^^^^^^^^^^^^^^^^^^^^

- 40 calls
- 100K intrabars (20K bars and no replay mode if a spread is used)



Compile time
^^^^^^^^^^^^

- Two-minute compile time limit issues warning. After three warnings, you are blocked for 1 hour.



Runtime
-------

- 500 ms per loop
- 40,000 ms per script
- Memory


•	syminfo.ticker does not work properly on spreads. When a non-standard chart uses a spread, the function returns "Cannot get a 'ticker' of a spread symbol",.
•	External Indicator input: only one is allowed per script.
•	& not allowed in options= strings


.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/