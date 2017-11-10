import ply.yacc as yacc
from code_lexer import *
from grammar_tree import *

def cparser(mylex, gardener, debug=0):
    """
        By rules build the intepreter and push it into grammr tree.
    """
    def p_translation_unit(p):
        '''translation_unit : external_declaration
                            | translation_unit external_declaration'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_external_declaration_1(p):
        'external_declaration : function_definition'
        p[0] = p[1]

    def p_external_declaration_2(p):
        'external_declaration : declaration'
        proto = str(p[1].value)
        p[0] = Func(p[1].value, proto)
        gardener.func_write(p[0])

    # function_definition

    def p_function_definiton(p):
        '''function_definition : declaration_specifiers direct_declarator declaration_list compound_statement
                               | direct_declarator declaration_list compound_statement'''
        proto = ' '.join(p[1:-1])
        if len(p) == 5:
            p[0] = Func(p[2], proto)
        else:
            p[0] = Func(p[1], proto)
        gardener.func_write(p[0])

    def p_function_definition_old_1(p):
        'function_definition : declaration_specifiers declarator compound_statement'
        prototype = ' '.join(p[1:3])
        p[0] = Func(p[2], prototype)
        gardener.func_write(p[0])


    def p_function_definition_old_2(p):
        'function_definition : declarator compound_statement'
        prototype = 'void' + str(p[1])
        p[0] = Func(p[1], prototype)
        gardener.func_write(p[0])

    # declaration
    def p_declaraion_1(p):
        'declaration : declaration_specifiers SEMI'
        p[0] = p[1]

    def p_declaration_2(p):
        'declaration : declaration_specifiers init_declarator_list'
        p[0] = ListOp(' ', p[1])
        p[0].add_child(p[2])

    # declaration_list
    def p_declaration_list_1(p):
        'declaration_list : declaration'
        p[0] = ListOp('declaration', p[1])

    def p_declaration_list_2(p):
        'declaration_list : declaration_list declaration'
        p[0] = p[1]
        p[0].add_child(p[2])

    # declaration_speicifiers
    def p_declaration_specifiers(p):
        '''declaration_specifiers : storage_class_specifier
                                    | storage_class_specifier declaration_specifiers
                                    | type_specifier
                                    | type_specifier declaration_specifiers
                                    | type_qualifier
                                    | type_qualifier declaration_specifiers'''
        if (len(p)==2): p[0] = p[1]
        else          : p[0] = p[2]

    # storage_specifier
    def p_storage_class_specifier(p):
        '''storage_class_specifier : TYPEDEF
                                    | EXTERN
                                    | STATIC
                                    | AUTO
                                    | REGISTER'''
        p[0] = Expr(etype='expr', expr='p[1]')

    # type_specifier
    def p_type_specifier(p):
        '''type_specifier : VOID
                            | CHAR
                            | SHORT
                            | INT
                            | LONG
                            | FLOAT
                            | DOUBLE
                            | SIGNED
                            | UNSIGNED
                            | struct_or_union_specifier
                            | enum_specifier
                            | TYPEID'''
        p[0] = Expr(etype='type', expr=p[1])

    # type_qualifier
    def p_type_qualifier(p):
        '''type_qualifier : CONST
                            | VOLATILE'''
        p[0] = Expr(etype="qualifier", expr=p[1])

    # struct_or_union_speicifier
    def p_struct_or_union_specifier(p):
        '''struct_or_union_specifier : struct_or_union ID LBRACE struct_declaration_list RBRACE
                                        | struct_or_union LBRACE struct_declaration_list RBRACE
                                        | struct_or_union ID'''
        p[0] = UniOp(p[1], "anonymous") if len(p)==5 else UniOp(p[1], p[2])

    # struct_or_union
    def p_struct_or_union(p):
        '''struct_or_union : STRUCT
                            | UNION'''
        p[0] = p[1]

    # struct_declaration_list
    def p_struct_declaration_list(p):
        '''struct_declaration_list : struct_declaration
                                   | struct_declaration_list struct_declaration'''
        p[0] = p[1]

    # init_declarator_list
    def p_init_declarator_list(p):
        '''init_declarator_list : init_declarator
                                | init_declarator_list COMMA init_declarator'''
        p[0] = p[1]

    def p_init_declarator(p):
        '''init_declarator : declarator ASSIGN initializer
                           | declarator'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinOp(p[2], p[1], p[3])

    # struct_delcaration
    def p_struct_declaration(p):
        '''struct_declaration : specifier_qualifier_list struct_declarator_list'''
        p[0] = p[2]

    # specifier_qualifier_list
    def p_specifier_qualifier_list(p):
        '''specifier_qualifier_list : type_specifier specifier_qualifier_list
                                    | type_specifier
                                    | type_qualifier specifier_qualifier_list
                                    | type_qualifier'''
        p[0] = p[1]

    # struct_declarator_list
    def p_struct_declarator_list(p):
        '''struct_declarator_list : struct_declarator
                                    | struct_declarator_list COMMA struct_declarator'''
        p[0] = p[1]

    # struct declarator
    def p_struct_declarator(p):
        '''struct_declarator : declarator
                                | declarator COLON constant_expression
                                | COLON constant_expression'''
        p[0] = p[2] if len[p]==3 else p[1]

    # enum_specifier
    def p_enum_specifier(p):
        '''enum_specifier : ENUM LBRACE enumerator_list RBRACE
                          | ENUM ID LBRACE enumerator_list RBRACE
                          | ENUM ID'''
        p[0] = BinOp(p[1], p[2])

    # enumerator_list
    def p_enum_list(p):
        '''enumerator_list : enumerator
                            | enumerator_list COMMA enumerator'''
        p[0] = p[1] if len(p)==2 else p[3]

    # eumerator
    def p_enumerator(p):
        '''enumerator : ID
                        | ID ASSIGN constant_expression'''
        p[0] = p[1]

    # declarator
    def p_declarator(p):
        '''declarator : direct_declarator
                      | pointer direct_declarator'''
        p[0] = UniOp(p[1], p[2]) if len(p)==3 else p[1]

    # direct_declarator
    def p_direct_declarator_1(p):
        '''direct_declarator : ID'''
        p[0] = Expr(etype="ID", expr=p[1])

    def p_direct_declarator_2(p):
        '''direct_declarator : LPAREN declarator RPAREN'''
        p[0] = p[2]

    def p_direct_declarator_3(p):
        '''direct_declarator : direct_declarator LBRACKET constant_expression RBRACKET'''
        p[0] = BinOp('[]', p[1], p[3])

    def p_direct_declarator_4(p):
        '''direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN'''
        p[0] = BinOp('()', p[1], p[3])
        debug_info(p[0])

    def p_direct_declarator_5(p):
        '''direct_declarator : direct_declarator LPAREN identifier_list RPAREN'''
        p[0] = BinOp('()', p[1], p[3])

    def p_direct_declarator_6(p):
        '''direct_declarator : direct_declarator LPAREN RPAREN
                                | direct_declarator LBRACKET RBRACKET'''
        if p[2] == 'LPAREN':
            op = '()'
        elif p[2] == 'LBRACKET':
            op = '[]'
        p[0] = UniOp(op, p[1])

    # pointer
    def p_pointer_1(p):
        'pointer : TIMES'
        p[0] = Expr("uniop", p[1])

    def p_pointer_2(p):
        'pointer : TIMES pointer'
        p[0] = UniOp(p[1], p[2])

    def p_pointer_3(p):
        '''pointer : TIMES type_qualifier_list
                    | TIMES type_qualifier_list pointer'''
        p[0] = UniOp(p[1], p[3]) if len(p)==4 else UniOp(p[1], p[2])

    # type_qualifier_list

    def p_type_qualifier_list(p):
        '''type_qualifier_list : type_qualifier
                                | type_qualifier_list type_qualifier'''
        p[0] = p[1] if len(p)==2 else p[2]

    # parameter_type_list
    def p_parameter_type_list(p):
        '''parameter_type_list : parameter_list
                               | parameter_list COMMA ELLIPSIS'''
        p[0] = p[1]

    # parameter_list
    def p_parameter_list(p):
        '''parameter_list : parameter_declaration
                          | parameter_list COMMA parameter_declaration'''
        if len(p)==2:
            p[0] = p[1]
        else:
            p[0] = ListOp(',', p[1])
            p[0].add_child(p[3])

    # parameter_declaration
    def p_parameter_declaration(p):
        '''parameter_declaration : declaration_specifiers declarator
                                 | declaration_specifiers abstract_declarator
                                 | declaration_specifiers'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            expr = [x.value for x in p[1:3]]
            p[0] = Expr('declaration', expr=' '.join(expr))
            print("----------------------------", p[0])

    # identifier_list
    def p_identifier_list(p):
        '''identifier_list : ID
                           | identifier_list COMMA ID'''
        if len(p) == 2:
            p[0] = ListOp(p[1])
        else:
            p[0] = ListOp(p[1])
            p[0].add_child(p[3])

    # initializer
    def p_initializer_1(p):
        '''initializer : assignment_expression'''
        p[0] = p[1]

    def p_initializer_2(p):
        '''initializer : LBRACE initializer_list RBRACE
                        | LBRACE initializer_list COMMA RBRACE'''
        if len(p) == 4:
            p[0] = Expr('expr', '{}')
        else:
            p[0] = Expr('expr', '{,}')

    # initializer_lit
    def p_initializer_list(p):
        '''initializer_list : initializer
                            | initializer_list COMMA initializer'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = UniOp(p[2], p[3])
    
    def p_type_name(p):
        '''type_name : specifier_qualifier_list
                     | specifier_qualifier_list abstract_declarator'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = p[2]

    # abstrct_declarator
    def p_abstract_declarator(p):
        '''abstract_declarator : pointer
                               | pointer direct_abstract_declarator
                               | direct_abstract_declarator'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = UniOp('*', p[2])

    # direct_abstract_declarator
    def p_direct_abstract_declarator_1(p):
        '''direct_abstract_declarator : LPAREN abstract_declarator RPAREN
                                        | LPAREN parameter_type_list RPAREN
                                        | LBRACKET constant_expression RBRACKET'''
        if p[1] == 'LPAREN':
            p[0] = UniOp('()', p[2])
        else:
            p[0] = UniOp('[]', p[2])

    def p_direct_abstract_declarator_2(p):
        '''direct_abstract_declarator : direct_abstract_declarator LBRACKET constant_expression RBRACKET
                                        | direct_abstract_declarator LPAREN parameter_type_list RPAREN'''
        if p[2] == 'LPAREN':
            p[0] = BinOp('()', p[1], p[3])
        else:
            p[0] = BinOp('[]', p[1], p[3])

    # constant_expression
    def p_constant_expression(p):
        '''constant_expression : conditional_expression'''
        p[0] = p[1]

    def p_assignment_expression(p):
        '''assignment_expression : conditional_expression
                                 | unary_expression assignment_operator assignment_expression'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = BinOp(p[2], p[1], p[3])
        else:
            pass

    def p_assignment_operator(p):
        '''assignment_operator : ASSIGN
                               | MULASSIGN
                               | DIVASSIGN
                               | MODASSIGN
                               | ADDASSIGN
                               | SUBASSIGN
                               | LSHIFTASSIGN
                               | RSHIFTASSIGN
                               | ANDASSIGN
                               | ORASSIGN
                               | XORASSIGN'''
        p[0] = Expr('=', p[1])

    def p_expression(p):
        '''expression : assignment_expression
                      | expression COMMA assignment_expression'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = BinOp(p[2], p[1], p[3])
        else:
            pass

    # conditional_expression
    def p_conditional_expression(p):
        '''conditional_expression : logical_or_expression
                                  | logical_or_expression TERNARY expression COLON conditional_expression'''
        pass

    # logical_or_expression
    def p_logical_or_expression(p):
        '''logical_or_expression : logical_and_expression
                                 | logical_or_expression LOR logical_and_expression'''
        pass

    # logical_and_expression
    def p_logical_and_expression(p):
        '''logical_and_expression : inclusive_or_expression
                                  | logical_and_expression LAND inclusive_or_expression'''
        pass

    def p_inclusive_or_expression(p):
        '''inclusive_or_expression : exclusive_or_expression
                                   | inclusive_or_expression OR exclusive_or_expression'''
        pass

    def p_exclusive_or_expression(p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression XOR and_expression'''
        pass

    def p_and_expression(p):
        '''and_expression : equality_expression
                          | and_expression AND equality_expression'''
        pass

    def p_equality_expression(p):
        '''equality_expression : relational_expression
                               | equality_expression EQ relational_expression
                               | equality_expression NE relational_expression'''
        pass

    def p_relational_expression(p):
        '''relational_expression : shift_expression
                                 | relational_expression LT shift_expression
                                 | relational_expression LE shift_expression
                                 | relational_expression GT shift_expression
                                 | relational_expression GE shift_expression'''
        pass

    def p_shift_expression(p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression'''
        pass

    def p_additie_expression(p):
        '''additive_expression : multiplicative_expression
                               | additive_expression PLUS multiplicative_expression
                               | additive_expression MINUS multiplicative_expression'''
        pass

    def p_multiplicative_expression(p):
        '''multiplicative_expression : cast_expression
                                     | multiplicative_expression TIMES cast_expression
                                     | multiplicative_expression DIVIDE cast_expression
                                     | multiplicative_expression MODULO cast_expression'''
        pass

    def p_cast_expression(p):
        '''cast_expression : unary_expression
                           | LPAREN type_name RPAREN cast_expression'''
        pass

    def p_unary_expression_1(p):
        '''unary_expression : postfix_expression'''
        p[0] = p[1]
    def p_unary_expression_2(p):
        '''cast_expression : INCREMENT unary_expression
                           | DECREMENT unary_expression
                           | unary_operator cast_expression'''
        p[0] = UniOp(p[1], p[2])
    def p_unary_expression_3(p):
        '''cast_expression : SIZEOF unary_expression
                           | SIZEOF LPAREN type_name RPAREN'''
        p[0] = Expr(etype='expr', expr=p[1])

    def p_unary_operator(p):
        '''unary_operator : AND
                          | TIMES
                          | PLUS
                          | MINUS
                          | NOT
                          | LNOT'''
        p[0] = Expr(p[1])

    def p_primary_expression(p):
        '''primary_expression : ID
                              | constant
                              | STRING
                              | LPAREN expression RPAREN'''
        if len(p) == 2:
            p[0] = Expr(etype='expr', expr=str(p[1]))
        else:
            p[0] = UniOp('()', p[2])

    def p_constant(p):
        '''constant : INTEGER
                    | FCONST
                    | CHARACTER
                    | HEXCONST'''
        p[0] = Expr('const', str(p[1]))

    def p_postfix_expression_1(p):
        '''postfix_expression : primary_expression'''
        p[0] = p[1]

    def p_postfix_expression_2(p):
        '''postfix_expression : postfix_expression LBRACKET expression RBRACKET'''
        p[0] = BinOp('[]', p[1], p[3])

    def p_postfix_expression_3(p):
        '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
        p[0] = BinOp('call', p[1], p[3])

    def p_postfix_expression_4(p):
        '''postfix_expression : postfix_expression LPAREN RPAREN'''
        p[0] = UniOp('emptycall', p[1])

    def p_postfix_expression_5(p):
        '''postfix_expression : postfix_expression DOT ID'''
        p[0] = BinOp('.', p[1], p[3])

    def p_postfix_expression_6(p):
        '''postfix_expression : postfix_expression PTR ID'''
        p[0] = BinOp('->', p[1], P[3])

    def p_postfix_expression_7(p):
        '''postfix_expression : postfix_expression INCREMENT
                              | postfix_expression DECREMENT'''
        p[0] = UniOp(p[2], p[1])
    
    def p_argument_expresssion_list(p):
        '''argument_expression_list : assignment_expression
                                    | argument_expression_list COMMA assignment_expression'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = BinOp(',', p[1], p[3])
        else:
            pass

    def p_statement_list(p):
        '''statement_list : statement
                          | statement_list statement'''
        if len(p) == 2:
            p[0] = ListOp('statement', p[1])
        elif len(p) == 3:
            p[0] = p[1]
            p[0].add_child(p[2])

    def p_statement(p):
        '''statement : labeled_statement
                     | compound_statement
                     | expression_statement
                     | selection_statement
                     | iteration_statement
                     | jump_statement'''
        p[0] = p[1]

    def p_labeled_statement(p):
        '''labeled_statement : ID COLON statement
                             | CASE constant_expression COLON statement
                             | DEFAULT COLON'''
        pass

    # compoud_statement
    def p_compound_statement(p):
        '''compound_statement : LBRACE RBRACE
                              | LBRACE statement_list RBRACE
                              | LBRACE declaration_list RBRACE
                              | LBRACE declaration_list statement_list RBRACE'''
        # ignore
        pass
    
    def p_expression_statement(p):
        '''expression_statement : empty
                                | expression'''
        p[0] = p[1]

    def p_selection_statement(p):
        '''selection_statement : IF LPAREN expression RPAREN statement
                               | IF LPAREN expression RPAREN statement ELSE statement
                               | SWITCH LPAREN expression RPAREN statement'''
        pass

    def p_iteration_statement(p):
        '''iteration_statement : WHILE LPAREN expression RPAREN statement
                               | DO statement WHILE LPAREN expression RPAREN
                               | FOR LPAREN expression_statement expression statement RPAREN statement
                               | FOR LPAREN expression_statement expression_statement expression RPAREN statement'''
        pass

    def p_jump_statement(p):
        '''jump_statement : GOTO ID
                          | CONTINUE
                          | BREAK SEMI
                          | RETURN SEMI
                          | RETURN expression SEMI'''
        pass

    def p_empty(p):
        'empty : '
        pass

    def p_error(p):
        pass

    lexer = mylex.lexer
    tokens = mylex.tokens
    p = yacc.yacc(method='LALR', tabmodule='c_tab', debugfile='cparser.out', debug=1)
    return p

def cparser_main(data):
    cgardener = GrammarHandler()
    code_lex = CodeLexer()
    p = cparser(code_lex, cgardener)
    p.parse(data, debug=1)

if __name__ == '__main__':
    data = '''int32_t RSSP_I_link_open(RSSP_I_local_cfg_t * const local)'''
    cparser_main(data)
