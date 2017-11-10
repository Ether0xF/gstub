# -*- coding: utf-8 -*-

import ply.lex as lex

__version__ = ""
__doc__ = ""


class CodeLexer:
    def __init__(self, autobuild=1):
        if autobuild == 1:
            self.build(lextab="srclextab")

    #Reserved words
    reserved = {
            'auto'     : 'AUTO',
            'break'    : 'BREAK',
            'case'     : 'CASE',
            'char'     : 'CHAR',
            'const'    : 'CONST',
            'continue' : 'CONTINUE',
            'default'  : 'DEFAULT',
            'do'       : 'DO',
            'double'   : 'DOUBLE',
            'else'     : 'ELSE',
            'enum'     : 'ENUM',
            'extern'   : 'EXTERN',
            'for'      : 'FOR',
            'float'    : 'FLOAT',
            'goto'     : 'GOTO',
            'if'       : 'IF',
            'int'      : 'INT',
            'long'     : 'LONG',
            'register' : 'REGISTER',
            'return'   : 'RETURN',
            'short'    : 'SHORT',
            'signed'   : 'SIGNED',
            'sizeof'   : 'SIZEOF',
            'static'   : 'STATIC',
            'struct'   : 'STRUCT',
            'switch'   : 'SWITCH',
            'typedef'  : 'TYPEDEF',
            'union'    : 'UNION',
            'unsigned' : 'UNSIGNED',
            'void'     : 'VOID',
            'volatile' : 'VOLATILE',
            'while'    : 'WHILE',
    }

    tokens = [
        # Literals
        # identifiers
        'ID', 'TYPEID', 
        # integer constant, float constant
        'INTEGER', 'HEXCONST', 'FCONST', 
        #string constant, character constant
        'STRING', 'CHARACTER', 

        # Operators
        # (+, -, *, /, %)
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
        # (|, &, ~, ^, <<, >>)
        'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
        # (||, && , !)
        'LOR', 'LAND', 'LNOT',
        # (<, <=, >, >=, ==, !=)
        'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

        # Assignment
        # (=, +=, -=, *=, /=, %=)
        'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'MODASSIGN',
        # (<<=, >>=, |=, &=, ^=)
        'LSHIFTASSIGN', 'RSHIFTASSIGN', 'ORASSIGN', 'ANDASSIGN', 'XORASSIGN',

        # Increment/decrement (++, --)
        'INCREMENT', 'DECREMENT',

        # Struct dereference (->)
        'PTR',
        # Ternary operator (?)
        'TERNARY',

        #Delimeters ( ) [ ] { } , . ; :
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LBRACE', 'RBRACE',
        'COMMA', 'DOT', 'SEMI', 'COLON',

        # Ellipsis (...)
        'ELLIPSIS',
    ] + list(reserved.values())

    # Ignored
    t_ignore     = '[ \t\f\v]'

    ID           = r'[A-Za-z_][A-Za-z0-9_]*'
    # Identifiers
    # Integer literal
    t_INTEGER    = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

    # Hex literal
    HEXCONST     = r'((0x)|(0X))[0-9a-fA-F]+([uU]|[lL]|[uU][lL]|[lL][uU])?'
    # Hex constant handler

    # Floating literal
    t_FCONST= r'((\d+)(\.\d+)+(e(\+|-)?(\d+))?([lL]|[fF])?) | ((\d+)e(\+|-)?(\d+)([lL]|[uU])?)'

    # String literal
    STRING       = r'\"([^\\\n]|(\\.))*?\"'
    # String handler

    # Character constant 'c' or L'c
    t_CHARACTER  = r'(L)?\'([^\\\n]|(\\.))*?\''

    # Operators
    t_PLUS        = r'\+'
    t_MINUS       = r'-'
    t_TIMES       = r'\*'
    t_MODULO      = r'%'
    t_OR          = r'\|'
    t_AND         = r'&'
    t_NOT         = r'~'
    t_XOR         = r'\^'
    t_LSHIFT      = r'<<'
    t_RSHIFT      = r'>>'
    t_LOR         = r'\|\|'
    t_LAND        = r'&&'
    t_LNOT        = r'!'
    t_LT          = r'<'
    t_LE          = r'<= '
    t_GT          = r'>'
    t_GE          = r'>= '
    t_EQ          = r'== '
    t_NE          = r'!= '

    # Assignment operators
    t_ASSIGN       = r'='
    t_ADDASSIGN    = r'\+='
    t_SUBASSIGN    = r'-='
    t_MULASSIGN    = r'\*='
    t_DIVASSIGN    = r'/='
    t_MODASSIGN    = r'%='
    t_LSHIFTASSIGN = r'<<='
    t_RSHIFTASSIGN = r'>>='
    t_ORASSIGN     = r'\|='
    t_ANDASSIGN    = r'&='
    t_XORASSIGN    = r'\^='

    # Increment/decrement
    t_INCREMENT   = r'\+\+'
    t_DECREMENT   = r'--'

    # ->
    t_PTR       = r'->'

    # ?
    t_TERNARY     = r'\?'

    # Delimeers
    t_LPAREN      = r'\('
    t_RPAREN      = r'\)'
    t_LBRACKET    = r'\['
    t_RBRACKET    = r'\]'
    t_LBRACE      = r'\{'
    t_RBRACE      = r'\}'
    t_COMMA       = r','
    t_DOT         = r'\.'
    t_SEMI        = r';'
    t_COLON       = r':'
    t_ELLIPSIS    = r'\.\.\.'

    # identifier handler
    @lex.TOKEN(ID)
    def t_ID(self, t):
        if (    len(t.value) > 2 
                and t.value[-1].lower() == 't'
                and t.value[-2] == '_'
            ):
            t.type = "TYPEID"
        elif t.value.upper() == 'FAR':
            t.type = 'AUTO'
        else:
            t.type = self.reserved.get(t.value, "ID")
        return t

    @lex.TOKEN(HEXCONST)
    def t_HEXCONST(self, t):
        t.type = 'INTEGER'
        return t

    @lex.TOKEN(STRING)
    def t_STRING(self, t):
        t.type = 'STRING'
        t.value = t.value[1:-1]
        return t

    # Newline
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_ILCOMMENT(self, t):
        r'/\*(\*)*-<(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    def t_LCOMMENT(self, t):
        r'/\*(\*)*-(.|\n)*?\*/'
        t.lexer.lineno == t.value.count('\n')

    def t_BLANK(self, t):
        r'\s'
        pass

    def t_error(self, t):
        print("illegal character %s" % repr(t.value[0]))
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    )

if __name__ == '__main__':
    lexer = CodeLexer().lexer
    data = '''
        int32_t RSSP_I_link_open(RSSP_I_local_cfg_t * const local)
        {
            int32_t ret = -1;
        }
    '''
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: break
        print(tok)
