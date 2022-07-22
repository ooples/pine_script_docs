.. image:: /images/Pine_Script_logo.svg
   :alt: Pine Script™ logo
   :target: https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html
   :align: right
   :width: 100
   :height: 100


.. _PageLimitations:


Limitations
===========

.. contents:: :local:
    :depth: 3



Introduction
------------

As is mentioned in our :ref:`Welcome <PageWelcomeToPine>` page:

    *Because each script uses computational resources in the cloud, we must impose limits in order to share these resources fairly among our users. 
    We strive to set as few limits as possible, but will of course have to implement as many as needed for the platform to run smoothly. 
    Limitations apply to the amount of data requested from additional symbols, execution time, memory usage and script size.*

If you develop complex scripts using Pine Script™, sooner or later you will run into some of the limitations we impose.
This section provides you with an overview of the limitations that you may encounter.
There are currently no means for Pine Script™ programmers to get data on the resources consumed by their scripts.
We hope this will change in the future.

In the meantime, when you are considering large projects, it is safest to make a proof of concept 
in order to assess the probability of your script running into limitations later in your project.

Here are the limits imposed in the Pine Script™ environment. 



Time
----



Script execution time
^^^^^^^^^^^^^^^^^^^^^

Script execution time isn't to be confused with script compile time. 
A script will be compiled once and then it passess off the script to a separate process to be executed on each bar of data. 
There are actually differences in max execution time limits depending on your account type so free users have a max of 20 seconds to execute their script 
and any paid user will have a max of 40 seconds to execute their script. 



Script compile time
^^^^^^^^^^^^^^^^^^^

When a script is run on a chart, you may not be aware that we compile it in an effort to save resources. 
We will go into more detail below in our Script size section but just know that when a script contains many objects like loops or variables, 
then it will take more time for us to be able to compile it. We restrict total compilation time for any script at a max of 2 minutes. 
We run the compilation step once and then it gets cached so your script will compile much faster after the very first time. 
Keep in mind that if your script compilation exceeds this limit then we will issue a warning. 
There is a max of 3 warnings and after the final warning, if you still try to compile the script again without fixing the underlying issues then we will issue a ban of one hour. 
This means that you won't be able to compile any scripts until the ban period is complete. 
It is always good code practice to never repeat code so if you do have repeating code then try to merge this code into one location like a custom function.



Loop execution time
^^^^^^^^^^^^^^^^^^^

Loops can be very useful in programming but can also take quite awhile to execute if you have a particularly complicated loop. 
There is a max of 500 milliseconds per loop in Pine Script™ which means you will receive a timeout error if any loop in your script exceeds this time. 
Keep in mind that this timeout is for each bar so this doesn't mean that your script will only have 500 milliseconds to execute all loops in your entire script. 
Of course you may wonder about situations involving nested loops so we will explain with some examples below as well as a hypothetical example. 
We set an invisible timer per loop so if you have a loop inside of another loop then we throw the error when either timer surpasses the time limit. 
Of course this means that the parent loop will timeout first and if this does happen in your script then the easiest solution is to break down this parent loop
into smaller loops that don't execute as much code. 



Chart visuals
-------------



Plot limits
^^^^^^^^^^^

A fairly misleading limitation in Pine Script™ is the max limit of plotting 64 objects on a chart. 
Most users assume that it is as simple as only calling any plot functions no more than the 64 times but what most users aren't aware of is that each 
plot function can actually use multiple plots. 
A perfect example of this would be either the plotbar or plotcandle functions since they actually plot 4 objects per function. 
A bar or candle of course is made up of 4 variables: `open <https://www.tradingview.com/pine-script-reference/v5/#var_open>`__, 
`high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__, `low <https://www.tradingview.com/pine-script-reference/v5/#var_low>`__, and 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__.
Some functions like `hline() <https://www.tradingview.com/pine-script-reference/v5/#fun_hline>`__ or tables you would assume are counted towards this plotting 
limit since they are visually added to a chart but they aren't actually plotted on the chart. 
Other functions like `plotchar() <https://www.tradingview.com/pine-script-reference/v5/#fun_plotchar>`__ can change based on the underlying information used.


:: 

    //@version=5
    indicator("Plot count example")

    bool isUp = close > open
    color isUpColor = isUp ? color.green : color.red
    bool isDn = not isUp
    color isDnColor = isDn ? color.red : color.green

    // uses one plot count for close series
    plot(close, color = color.white)

    // uses two plot counts (1 for close series and 1 for color series)
    plot(close, color = isUpColor)

    // uses one plot count for close series
    plotarrow(close, colorup = color.green, colordown = color.red)

    // uses two plot counts (1 for close series and 1 for colorup series)
    plotarrow(close, colorup = isUpColor)

    // uses three plot counts (1 for close series, 1 for colorup series, and 1 for colordown series)
    plotarrow(close, colorup = isUpColor, colordown = isDnColor)

    // uses four plot counts for open, high, low, and close series
    plotbar(open, high, low, close, color = color.white)

    // uses five plot counts for open, high, low, close, and color series
    plotbar(open, high, low, close, color = isUpColor)

    // uses four plot counts for open, high, low, and close series
    plotcandle(open, high, low, close, color = color.white, wickcolor = color.white, bordercolor = color.purple)

    // uses five plot counts for open, high, low, close, and color series
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = color.white, bordercolor = color.purple)

    // uses six plot counts for open, high, low, close, color, and wickcolor series
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = color.purple)

    // uses seven plot counts for open, high, low, close, color, wickcolor, and bordercolor series
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)

    // uses one plot count for close series
    plotchar(close, color = color.white, text = '⭐', textcolor = color.white)

    // uses two plot counts for close, and color series
    plotchar(close, color = isUpColor, text = '⭐', textcolor = color.white)

    // uses three plot counts for close, color, and textcolor series
    plotchar(close, color = isUpColor, text = '⭐', textcolor = isUp ? color.yellow : color.white)

    // uses one plot count for close series
    plotshape(close, color = color.white, textcolor = color.white)

    // uses two plot counts for close, and color series
    plotshape(close, color = isUpColor, textcolor = color.white)

    // uses three plot counts for close, color, and textcolor series
    plotshape(close, color = isUpColor, textcolor = isUp ? color.yellow : color.white)


.. note:: This is a full list of all plot count combinations for each plot function so feel free to use this list as a reference guide.

::

    //@version=5
    indicator("Plot count limits example")

    bool isUp = close > open
    color isUpColor = isUp ? color.green : color.red

    // uses seven plot counts for open, high, low, close, color, wickcolor, and bordercolor series
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)

    // including this last line will throw an error stating maximum number of 64 plot elements were reached and that the script contains 70
    plotcandle(open, high, low, close, color = isUpColor, wickcolor = isUpColor , bordercolor = isUp ? color.lime : color.maroon)



Line, box, and label limits
^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the most overlooked script settings is the abilities to set the ``max_lines_count``, ``max_boxes_count``, and ``max_labels_count``. 
The default for all 3 is set to 50 but you are allowed to increase that to a max of 500. 
Pine Script™ utilizes a very efficient garbage collection system so by default you will only ever be able to view the last 50 labels as an example. 
Below we have an example showing how to increase these limits in the indicator settings.

::

    //@version=5
    indicator("Label limits example", max_labels_count = 100, overlay=true)
    cond = close > open ? 1 : close < open ? -1 : 0
    label.new(bar_index, close, yloc = cond > 0 ? yloc.abovebar : yloc.belowbar, style = cond > 0 ? label.style_arrowup : label.style_arrowdown, 
        color = cond > 0 ? color.green : color.red, size = size.huge)

.. note:: Only the last 100 bars will have labels on them and this is because of the garbage collection process that Pine Script™ does in the back-end to only show the most recent labels.



Table limits
^^^^^^^^^^^^

In Pine Script™ there are 9 possible locations to choose for a table location: 
`position.bottom_center <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}bottom_center>`__, 
`position.bottom_left <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}bottom_left>`__, 
`position.bottom_right <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}bottom_right>`__, 
`position.middle_center <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}middle_center>`__, 
`position.middle_left <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}middle_left>`__, 
`position.top_center <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}top_center>`__, 
`position.top_left <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}top_left>`__, 
or `position.top_right <https://www.tradingview.com/pine-script-reference/v5/#var_position{dot}top_right>`__.
If you place two tables in the same position on a chart then you will only see the most recent table added to that position. 
Pine Script™ will override the older table in that same position and only display the newer table. 
This means that there is a hard limit of 9 tables that you are able to add to a chart as long as you place each table in a different position.



request.*() calls
-----------------



Request calls
^^^^^^^^^^^^^

All function calls using the request namespace such as `request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__, 
`request.security_lower_tf() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security_lower_tf>`__, 
`request.quandl() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}quandl>`__, 
`request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__, etc are all treated the same on the compiler. 
This means that since there is a hard limit of 40 request calls per script then this can either be 40 
`request.security() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security>`__ calls or a combination like 34 
`request.quandl() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}quandl>`__ calls and 6 
`request.financial() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}financial>`__ calls. 



Intrabars
^^^^^^^^^

This limitation only applies to the `request.security_lower_tf() <https://www.tradingview.com/pine-script-reference/v5/#fun_request{dot}security_lower_tf>`__ function and this is 
because when you request data from a lower timeframe compared to the chart's timeframe, you will have multiple bars of data for each current bar. 
For example, if you are looking at a 1H chart and you want to use 1M data in your script then you will receive up to 60 1M intrabars for each 1H bar. 
We have a max of 100,000 intrabars allowed so for reference this means that viewing a 1D chart on BTC and requesting the 1S data for each bar will give you a max of 86,400 intrabars. 



Memory
------



Script size
^^^^^^^^^^^

Before a script is executed, it is compiled into an Intermediate Language (IL). 
Using an IL allows Pine Script™ to work with longer scripts and to optimize the script before we begin executing it.
There is a hard limit on the length that the individual script can have in its IL form: 60,000 tokens for a regular indicator or strategy, and 1 million tokens for a library.
Due to various optimizations, there is no way to check the length of the IL that any specific script will generate. 
Compiling using the IL will remove unused code and comments, shortens variable and function names, calculates some expressions where possible, etc.
To work around the limit, you can offload some code into a library and use the library functions in your script instead. 
Replacing duplicate code with functions should also shorten the length of the IL tokens.



Arrays and matrices
^^^^^^^^^^^^^^^^^^^

Arrays and matrices are both very complicated topics for new Pine Script™ programmers so make sure to take a good look at the 
`arrays page <https://www.tradingview.com/pine-script-docs/en/v5/language/Arrays.html>`__ or the 
`matrices page <https://www.tradingview.com/pine-script-docs/en/v5/language/Arrays.html>`__ if you need a refresher. 
Arrays and matrices are both special objects that are collections of data in slightly different data formats. 
Arrays can be thought of as a variation of a data time series and matrices add an extra dimension to this concept which allows for arrays inside arrays. 
Both types have the same limit where you have a max of 100,000 elements allowed inside each collection object. 



Variables
^^^^^^^^^

Variables are objects that store data in programming languages and can be initialized in many different ways depending on the language you are using. 
In Pine Script™ we have a max of 1000 variables allowed per scope and there are two scopes in every script. 
You have a global scope which would be variables accessible from anywhere in the script and a local scope which would be variables accessible from a local block 
like an if statement or inside a loop. Since variables have to be created manually then exceeding 1000
variables per scope would mean your script would be thousands of lines long so chances are you will never see this associated error. 
Keep in mind that variables in Pine Script™ are the only factor that directly contributes to how much physical memory your script uses.

::

    //@version=5
    indicator("Variables scope example", overlay = true)
    float ema = ta.ema(close, 14) // declared in global scope

    upperBand = ema, lowerBand = ema
    if close > open
        float trueRange = ta.tr // declared in local scope
        upperBand += trueRange
        lowerBand -= trueRange
        
    plot(upperBand, color = color.yellow)
    plot(lowerBand, color = color.yellow)



Scripts
-------



Max bars back
^^^^^^^^^^^^^

When we create a script that depends on past data then it is vital that we make sure that there is enough previous data to be able to perform the needed calculations. 
A common error that users receive is that there isn't enough data to be able to properly execute the script and this is where ``max_bars_back`` comes in. 
For example if you are use ``close[499]`` in your script then the compiler knows that you will need at least 500 past values of 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ for each bar. 
However if you create a series integar variable called y and use this instead of the 499 then the compiler isn't able to automatically detect how much past values of 
`close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ we will need for the script to execute. 
This is why sometimes you will see an error message telling you that Pine Script™ can't determine the length of a reference series. 
An easy solution for this common issue is to increase the ``max_bars_back`` to a number high enough so that the compiler will always have enough past references for 
any variable in the script. The max value you can set it to is 5000 and the default is 0.



Max bars forward
^^^^^^^^^^^^^^^^

Contrary to the name, this limitation doesn't work in quite the same way as the above ``max_bars_back``. This is a special case that only works with future data. 
Here is an example that shows you how to create a line that projects forward using this concept. 
We are projecting a line into the future that displays the current slope of the last two `high <https://www.tradingview.com/pine-script-reference/v5/#var_high>`__ values 
projected into the future using our ``forwardBars`` input. 
We are also drawing a line on the last bar which helps us to not only save resources but also slightly speeds up the script execution time.

::

    //@version=5
    indicator("Max bars forward example", overlay=true)

    //Functions
    drawLine(t1, t2, Y1, Y2) =>
        //init variables on last bar only
        if barstate.islast
            var line proj_line = line.new(x1 = t1, y1 = Y1, x2 = t2, y2 = Y2, xloc = xloc.bar_index, extend = extend.none, color = color.silver, style = line.style_dashed)
            line.set_xy1(proj_line, t1, Y1)
            line.set_xy2(proj_line, t2, Y2)
        
    //Declare Input Variables
    forwardBars = input.int(defval = 10, title = "Forward Bars to Display", minval = 0, step = 1, maxval = 499) + 1

    //Main logic
    float signal = high
    float m = (signal[1] - signal[2]) / (bar_index[1] - bar_index[2])
    float b = signal[2]
    int t2 = bar_index[2] + forwardBars

    drawLine(bar_index[2], t2, b, m * forwardBars + b)



Local blocks
^^^^^^^^^^^^

As we discussed in the variables section, each script will have a local scope and a global scope. 
The local block is another way to describe a local scope so in other words, if statements, loops, etc. 
There is a max of 500 local blocks allowed which is one of those limits that will be very difficult to surpass. 

::

    //@version=5
    indicator("Local block example")
    int length = 14
    var volMa = float(na)
    if close > open
        volMa := ta.wma(volume, length)
    
    // we can simplify the above by removing the local block and using a ternary instead
    var volMaAlt = float(na)
    volMaAlt := close > open ? ta.wma(volume, length) : nz(volMaAlt[1])

    plot(volMa)
    plot(volMaAlt)

.. note:: We are calculating the volume wma only when the close is higher than the open to save on processing time



Backtesting
^^^^^^^^^^^

This particular limitation only applies to strategy scripts and in most cases you probably won't see the error message associated with this limit. 
You have a max of 9,000 orders that can be placed when you run a backtesting script. 
There is a new user feature that was recently launched for Premium users only called Deep Backtesting. 
If you use this new feature, this will increase your max limit from 9,000 orders to 200,000 orders.



Historical bars
^^^^^^^^^^^^^^^

As discussed in more detail on our historical references page, the historical operator will give you the value from X bars ago. 
So for our example above in the array size section, ``close[2]`` will give you the `close <https://www.tradingview.com/pine-script-reference/v5/#var_close>`__ price 2 bars ago. 
There is a limit for historical bars based on your account status. I will put the full breakdown of the limits per account type below. 

These are the account-specific bar limits:
 - 20000 historical bars for the Premium plan.
 - 10000 historical bars for Pro and Pro+ plans.
 - 5000 historical bars for other plans.

This means that if you have a Free plan for your account then you are limited to 5000 historical bars so if you try ``close[5001]`` then you will receive an historical bar error.



.. image:: /images/TradingView-Logo-Block.svg
    :width: 200px
    :align: center
    :target: https://www.tradingview.com/
