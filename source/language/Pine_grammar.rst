Pine v5 grammar
===============

``{}`` Curly braces content can be repeated zero or more times: {, <parameter>}

``[]`` Square brackets content can appear zero or one time: [ by <expression>]

``\``  Backslash escapes one character: \[ means a literal [ in the syntax.

``|``  Pipe means "or".

``<token_name>`` is a token called "token_name".




<Pine_script>
    [<version>]
    <declaration_statement>
    <statement>
    {<statement>}

<declaration_statement>
    indicator() | strategy() | library()

<statement>
    <variable_declaration> | <variable_reassignment> | <function_declaration> | <function_call> | <structure>

<variable_initialization>
    <variable_declaration> = <expression> | <structure>

<variable_declaration>
    [<declaration_mode>] [<type>] <identifier>
    |
    <tuple_declaration>

<declaration_mode>
    [var | varip]

<type>
    [int  | float   | bool   | color   | string   | label   | line   | box   | table |
    int[] | float[] | bool[] | color[] | string[] | label[] | line[] | box[] | table[]]

<variable_reassignment>
    <identifier> := <expression> | <function_call> | <structure>

<function_declaration>
    <identifier>(<parameter_list>) => 
        <local_block>
    |
    <identifier>(<parameter_list>) => <return_value>

<parameter_list>
    {<parameter_definition>{, <parameter_definition>}}

<parameter_definition>
    [<identifier> = <default_value>]

<structure>
    <if_structure> | <for_structure> | <while_structure> | <switch_structure>

<if_structure>
    if <expression>
        <local_block>
    {else if <expression>
        <local_block>}
    [else
        <local_block>]

<for_structure>
    for <identifier> = <expression> to <expression>[ by <expression>]
        <local_block_loop>

<for_structure>
    for <identifier> = <expression> to <expression>[ by <expression>]
        <local_block_loop>

<while_structure>
    while <expression>
        <local_block_loop>

<local_block_loop>
    {<statement> | break | continue}
    <return_value>

<switch_structure>
    <switch_structure_expression> | <switch_structure_values>

<switch_structure_expression>
    switch <expression>
        {<expression> => <local_block>}
        => <local_block>

<switch_structure_values>
    switch
        {<expression> => <local_block>}
        => <local_block>

<local_block>
    {<statement>}
    <return_value>

<return_value>
    <statement> | <expression> | <tuple>

<tuple_declaration>
    \[<identifier>{, <identifier>}\]

<tuple>
    \[<expression>{, <expression>]\]

<expression>
    <literal> | <identifier> | <function_call> | 
    <arithmetic_expression> | <comparison_expression> | <logical_expression>

<function_call>
    functionName({<expression>{, <expression>}})

<arithmetic_expression>


<comparison_expression>


<logical_expression>


<identifier>
    <letter> | <underscore> {<letter><underscore><digit>}

<arithmetic_operators>::
    + | - | * | / | %

<comparison_operators>::
    < | <= | != | == | > | >=

<logical_operators>::
    not | and | or

<literal>
    <literal_int> | <literal_float> | <literal_bool> | <literal_color> | <literal_string>

<literal_int>
    [- | +]<digit>{<digit>}

<literal_float>
    [- | +]<digit>{<digit>}[.][E|e<digit>{<digit>}]

<literal_bool>
    true | false | bool(na)

<literal_color>
    #RRGGBB | #RRGGBBAA | <built-in_color_constant>

<literal_string>
    "<characters>" | '<characters>'
