.. _PageLimitations:

.. image:: /images/Pine_Script_logo.svg
   :alt: Pine Script™ logo
   :target: https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html
   :align: right
   :width: 100
   :height: 100

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

Here are the limits imposed in the Pine Script™ environment. 



Time
----



Script compile time
^^^^^^^^^^^^^^^^^^^

When a script is run on a chart, you may not be aware that we compile it in an effort to save resources. We will go into more detail below in our Script size section but just know that when a script contains many objects
like loops or variables, then it will take more time for us to be able to compile it. We restrict total compilation time for any script at a max of 2 minutes. We run the compilation step once and then it gets cached
so your script will compile much faster after the very first time. Keep in mind that if your script compilation exceeds this limit then 
we will issue a warning. There is a max of 3 warnings and after the final warning, if you still try to compile the script again without fixing the underlying issues then we will issue a ban of one hour. 
This means that you won't be able to compile any scripts until the ban period is complete. It is always good code practice to never repeat code so if you do have repeating code then try to merge this code into one location like a custom function.

// example below



Loop execution time
^^^^^^^^^^^^^^^^^^^

Loops can be very useful in programming but can also take quite awhile to execute if you have a particularly complicated loop. There is a max of 500 milliseconds per loop in Pine Script™ which means you will receive a timeout error if any loop 
in your script exceeds this time. Keep in mind that this timeout is for each bar so this doesn't mean that your script will only have 500 milliseconds to execute all loops in your entire script. Of course you may wonder about situations involving 
nested loops so we will explain with some examples below as well as a hypothetical example. We set an invisible timer per loop so if you have a loop inside 
of another loop then we throw the error when either timer surpasses the time limit. Of course this means that the parent loop will timeout first and if this does happen in your script then the easiest solution is to break down this parent loop
into smaller loops that don't execute as much code. 

// example below

Script execution time
^^^^^^^^^^^^^^^^^^^^^

Script execution time isn't to be confused with script compile time. A script will be compiled once and then it passess off the script to a separate process to be executed on each bar of data. There are actually differences in max execution time 
limits depending on your account type so free users have a max of 20 seconds to execute their script and any paid user will have a max of 40 seconds to execute their script. 

// example below


Chart visuals
-------------


Table limits
^^^^^^^^^^^^

In Pine Script™ there are 9 possible locations to choose for a table location: position.bottom_center, position.bottom_left, position.bottom_right, position.middle_center, position.middle_left, position.middle_right, position.top_center, 
position.top_left, or position.top_right. If you place two tables in the same position on a chart then you will only see the most recent table added to that position. Pine Script™ will override the older table in that same position and only 
display the newer table. This means that there is a hard limit of 9 tables that you are able to add to a chart as long as you place each table in a different position.


Plot limits
^^^^^^^^^^^

A fairly misleading limitation in Pine Script™ is the max limit of plotting 64 objects on a chart. Most users assume that it is as simple as only calling any plot functions no more than the 64 times but what most users aren't aware of is that each 
plot function can actually use multiple plots. Perfect example of this would be either the plotbar or plotcandle functions since they actually plot 4 objects per function. A bar or candle of course is made up of 4 variables: Open, High, Low, and Close.
Some functions like hline() or tables you would assume are counted towards this plotting limit since they are visually added to a chart but they aren't actually plotted on the chart. Other functions like plotchar() can change based on the underlying information
used. If you are plotting 


Line, box, and label limits
^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the most overlooked script settings is the abilities to set the max_lines_count, max_boxes_count, and max_labels_count. The default for all 3 is set to 50 but you are allowed to increase that to a max of 500. Pine Script™ utilizes
a very efficient garbage collection system so by default you will only ever be able to view the last 50 labels as an example. Below we have an example showing how to increase these limits in the indicator settings.

// example below



Request.*() calls
-----------------


Intrabars
^^^^^^^^^

This limitation only applies to the request.security_lower_tf function and this is because when you request data from a lower timeframe compared to the chart's timeframe, you will have multiple bars of data for each current bar. 
For example, if you are looking at a 1H chart and you want to use 1M data in your script then you will receive up to 60 1M intrabars for each 1H bar. We have a max of 100,000 intrabars allowed so for reference this means that viewing
a 1D chart on BTC and requesting the 1S data for each bar will give you a max of 86,400 intrabars. 


Request calls (need ideas for better naming)
^^^^^^^^^^^^^^^^^

All function calls using the request namespace such as request.security(), request.security_lower_tf(), request.quandl(), request.financial(), etc are all treated the same on the compiler. This means that since there is a hard limit of 40 
request calls per script then this can either be 40 request.security() calls or a combination like 34 request.quandl() calls and 6 request.financial() calls. 



Memory
------


Script size
^^^^^^^^^^^

Before a script is executed, it is compiled into an Intermediate Language (IL). Using an IL allows Pine Script™ to work with longer scripts and to optimize the script before we begin executing it.
There is a hard limit on the length that the individual script can have in its IL form: 60,000 tokens for a regular indicator or strategy, and 1 million tokens for a library.
Due to various optimizations, there is no way to check the length of the IL that any specific script will generate. Compiling using the IL will remove unused code and comments, shortens variable and function names, calculates some expressions where possible, etc.
To work around the limit, you can offload some code into a library and use the library functions in your script instead. Replacing duplicate code with functions should also shorten the length of the IL tokens.


Array size
^^^^^^^^^^

Arrays are a complicated topic for new Pine Script™ programmers so make sure to take a good look at the arrays page if you need a refresher. We will give a very brief explainer of arrays to better explain the limits. Arrays are a custom collection of data that
is similar to a data series in that it can hold data in the background while your script is executing on each bar. However that is where most of the similarities end. For a data series, we use the historical operator [] to pull a value from X bars back. For example
if we want to use the close from 2 bars back then we would use close[2] but if you were to do this on an array, you would get the third value from the start of the array since arrays start from the 0 index. Arrays are much easier to work with overall because 
there are many built-in functions that you can execute on an array. For more information on the full list of array functions then please check out the full array user manual page. There is a max of 100,000 objects inside an array and below we will show how to
properly utilize these limits inside your script.


Variables
^^^^^^^^^

Variables are objects that store data in programming languages and can be initialized in many different ways depending on the language you are using. In Pine Script™ we have a max of 1000 variables allowed per scope and there are two scopes in every script. You 
have a global scope which would be variables accessible from anywhere in the script and a local scope which would be variables accessible from a local block like an if statement or inside a loop. Since variables have to be created manually then exceeding 1000
variables per scope would mean your script would be thousands of lines long so chances are you will never see this associated error. Keep in mind that variables in Pine Script™ are the only factor that directly contributes to how much physical memory your script uses.


Scripts
-------


Local blocks
^^^^^^^^^^^^

You might be asking yourself: what is a local block? As we discussed in the variables section, each script will have a local scope and a global scope. The local scope is what is inside a local block so in other words, if statements, loops, etc. There is a max of 
500 local blocks allowed which is one of those limits that will be very difficult to surpass. 

    //@version=5
    indicator("")
    int length = 14
    var volSma = float(na)
    if close > open
        volSma := ta.wma(volume, length)
    plot(volSma)

    Note that: 
    
    - We are calculating the volume wma only when the close is higher than the open to save on processing time


Max bars back
^^^^^^^^^^^^^

When we create a script that depends on past data then it is vital that we make sure that there is enough previous data to be able to perform the needed calculations. A common error that users receive is that there isn't enough data to be able to properly
execute the script and this is where max_bars_back comes in. For example if you are use close[499] in your script then the compiler knows that you will need at least 500 past values of close for each bar. However if you create a series integar 
variable called y and use this instead of the 499 then the compiler isn't able to automatically detect how much past values of close we will need for the script to execute. This is why sometimes you will see an error message telling you that Pine Script™ can't
determine the length of a reference series. An easy solution for this common issue is to increase the max_bars_back to a number high enough so that the compiler will always have enough past references for any variable in the script. The max value you can set it to is 5000
and the default is 0.


Max bars forward
^^^^^^^^^^^^^^^^

Contrary to the name, this limitation doesn't work in quite the same way as the above max_bars_back. This is a special case that only works with future data. Here is an example that shows you how to create a line that projects forward using this concept. We are 
projecting a line into the future that displays the current slope of the last two high values projected into the future using our forwardBars input. We are also drawing a line on the last bar which helps us to not only save resources but also slightly speeds 
up the script execution time.

    //@version=5
    indicator('[Example_ForwardBar]', overlay=true)

    //Functions
    f_drawLine(t1, t2, Y1, Y2) =>
        //init variables on last bar only
        if barstate.islast
            var line proj_line = line.new(x1=t1, y1=Y1, x2=t2, y2=Y2, xloc=xloc.bar_index, extend=extend.none, color=color.silver, style=line.style_dashed)
            line.set_xy1(proj_line, t1, Y1)
            line.set_xy2(proj_line, t2, Y2)
        
    //Declare Input Variables
    forwardBars = input.int(defval=10, title='Forward Bars to Display', minval=0, step=1, maxval=499) + 1

    //Main logic
    float signal = high
    float m = (signal[1] - signal[2]) / (bar_index[1] - bar_index[2])
    float b = signal[2]
    int t2 = bar_index[2] + forwardBars

    f_drawLine(bar_index[2], t2, b, m * forwardBars + b)


Historical bars
^^^^^^^^^^^^^^^

As discussed in more detail on our historical references page, the historical operator will give you the value from X bars ago. So for our example above in the array size section, close[2] will give you the close price 2 bars ago. There is a limit for 
historical bars based on your account status. I will put the full breakdown of the limits per account type below. 

These are the account-specific bar limits:
	*20000 historical bars for the Premium plan.
	*10000 historical bars for Pro and Pro+ plans.
	*5000 historical bars for other plans.

This means that if you have a Free plan for your account then you are limited to 5000 historical bars so if you try close[5001] then you will receive an historical bar error.

// example below

Backtesting
^^^^^^^^^^^

This particular limitation only applies to strategy scripts and in most cases you probably won't see the error message associated with this limit. You have a max of 9,000 orders that can be placed when you run a backtesting script. 
There is a new user feature that was recently launched for Premium users only called Deep Backtesting. If you use this new feature, this will increase your max limit from 9,000 orders to 200,000 orders.

.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/