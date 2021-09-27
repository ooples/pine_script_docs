from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Literal, Punctuation, Generic, Other, Error

# Many examples are here https://bitbucket.org/birkenfeld/pygments-main/src/default/pygments/lexers/
class PinePygmentsLexer(RegexLexer):
    name = 'pine'

    tokens = {
        'root': [
            (r'\#([0-9a-fA-F]{8})|\#([0-9a-fA-F]{6})', Literal), # Color literal
            (r'[0-9]+', Number.Integer),
            (r'(\.\d+|[0-9]+\.[0-9]*)([eE][-+]?[0-9]+)?', Number.Float),
            (r'\s+', Text.Whitespace),
            (r'//.*?$', Comment), 
            (r'(for|continue|break|if|else|var|varip|while|switch|export|import|as|series|simple|float|int|bool|string|color|line|label|box|table|true|false)\s', Keyword),
            (r'(open|high|low|close|volume|time|hl2|hlc3|ohlc4|na)\b', Name.Constant), # Built-in series 'open', 'high', ...
            # No group is for unique names (e.g. `bar_index`)
            # First group is for names that can be used both separately and as a namespace (e.g. `plot` is both `plot()` and `plot.style_*`)
            # Second group is for exclusively namespaces (e.g. `ta`)
            (r'(bar_index|dayofmonth|hour|minute|month|na|second|time_close|time_tradingday|timenow|year|alertcondition|barcolor|'
             r'bgcolor|bool|fill|fixnan|float|hour|indicator|int|library|nz|plotarrow|plotbar|plotcandle|plotchar|'
             r'plotshape|string|timestamp|weekofyear|'
             r'(strategy|input|plot|hline|alert|color|dayofweek|dividends|earnings|label|line|splits|box|table)(\.\w+)?|'
             r'(adjustment|barmerge|barstate|currency|dayofweek|display|extend|format|location|math|position|scale|session|'
             r'shape|size|syminfo|ta|text|timeframe|xloc|yloc|array|request|str|ticker)\.\w+)\b', Name.Entity), # Built-in functions and variables
            (r'[\w\.]+', Name.Other),
            (r'\+|\-|\*|\/|\%|\=|\[|\]|and|or|not|\?|\:|\<|\>|\!', Operator),
            (r'\(|\)|\,', Punctuation),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
        ]
    }
