import ply.yacc as yacc
import code_lexer as lex
import grammar_tree as grammar_tree

class CodeParser:
    def __init__(self, lex, gardener):
        self.lexer = lex.lexer
        self.gardener = gardener
        self.parser = self.code_yacc(self.lexer, gardener)
    def code_yacc(self, lexer, gardener):
        """
            By rules build the intepreter and push it into grammr tree.
        """
        def p_translation_unit(p):
            '''translation_unit : external_declaration
                                | translation_unit external_declaration'''
            pass

        def p_external_declaration_1(p):
            'external_declaration : function_definition'
            pass

        def p_external_declaration_2(p):
            p[0] = p[1]

        # function_definition

        def p_function_definiton(p):
            '''function_definition : declaration_specfiers declarator delcaration_list compound_statment
                                   | declarator declarator_list compound_statement'''
            proto = ' '.join(p[1:-1])
            print(proto)
            if len(p) == 5:
                p[0] = Func(p[2], proto)
            else:
                p[0] = Func(p[1], proto)
            gardener.func_write(p[0])

        def p_function_definition_old_1(p):
            'function_definition : declaration_specifiers declarator compound_statemnt'
            prototype = ' '.join(p[1:3])
            p[0] = Func(p[2], prototype)
            gardener.func_write(p[0])


        def p_function_definition_old_2(p):
            'function_definition: declarator compound_statement'
            prototype = 'void' + str(p[1])
            p[0] = Func(p[1], prototype)
            gardener.func_write(p[0])

        # declaration_list

        def p_declaration_list_1(p):
            'declaration_list: declaration'
            p[0] = ListOp('declaration', p[1])

        def p_declaration_list_2(p):
            'declaration_list : declaration_list declaration'
            p[0] = p[1]
            p[0].add_child(p[2])

        # declaration

        def p_declaraion_1(p):
            'delcaration : declaration_specifiers SEMI'
            p[0] = p[1]

        def p_declaration_2(p):
            'declaration : declaration_specifiers init_declarator_lists'
            p[0] = ListOp(' ', p[1])
            p[0].add_child(p[2])

        # declaration_speicifiers
        def p_declaraion_specifiers(p):
            '''declaration_specifiers : storage_class_specifier
                                      | storage_class_specifier declaration_specifiers
                                      | type_speicifier
                                      | type_specifier declaration_specifiers
                                      | type_qualifier
                                      | type_qualifier declaration_specifiers'''
            if (len[p]==2): p[0] = p[1]
            else          : p[0] = p[2]

        # storage_specifier
        def p_storage_class_speicifier(p):
            '''storage_class_specfier : TYPEDEF
                                      | EXTERN
                                      | STATIC
                                      | AUTO
                                      | REGISTER'''
            p[0] = Expr(etype='expr', expr='p[1]')

        # type_specifier
        def p_type_specifier(p):
            '''type_speicifer : VOID
                              | CHAR
                              | SHORT
                              | INT
                              | LONG
                              | FLOAT
                              | DOUBLE
                              | SIGNED
                              | UNSIGNED
                              | struct_or_union_speicifier
                              | enum_specifier
                              | TYPEID'''
            p[0] = Expr(etype='type', expr=p[1])

        # type_qualifier
        def p_type_qualifier(p):
            '''type_qualifier : CONST
                              | VOLATILE'''
            p[0] = Expr(etype="qualifier", expr=p[1])

        # struct_or_union_speicifier
        def p_struct_or_union_speicifier(p):
            '''struct_or_union_specifier : struct_or_union ID LBRACE struct_declcaration_list RBRACE
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
            '''struct_delcaration_list : struct_declaration
                                       | struct_declaration_list struct_declaration'''
            p[0] = p[1]

        # struct_delcaration
        def p_struct_declaration(p):
            '''struct_declaration : specifier_qualifier_list struct_delcarator_list'''
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
            '''enumerator_specifier : ENUM LBRACE enumerator_list RBRACE
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
            '''declarator : pointer direct_declarator
                          | direct_declarator'''
            p[0] = UniOp(p[1], p[2]) if len(p)==3 else p[1]

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
            p[0] = UniOp(p[1], p[3]) if len(p)==4 else UniOp(p[1], p[1])

        # type_qualifier_list

        def p_type_qualifier_list(p):
            '''type_qualifier_list : type_qualifier
                                   | type_qualifier_list type_qualifier'''
            p[0] = p[1] if len(p)==2 else p[2]

        def p_type_qualifier(p):
            '''typ_qualifier : CONST
                             | VOLATILE'''
            p[0] = Expr('expr', p[1])

        # direct_declarator
        def p_direct_declarator_1(p):
            '''direct_declarator : ID'''
            p[0] = Expr(etype="ID", expr=p[1])

        def p_direct_declarator_2(p):
            '''direct_declarator : LPAREN declarator RPAREN'''
            p[0] = p[2]

        def p_direct_declarator_3(p):
            '''direct_declarator: direct_declarator LBRACKET constant_expression RBRACKET'''
            p[0] = BinOp('[]', p[1], p[3])

        def p_direct_declarator_4(p):
            '''direct_declarator: direct_declarator LPAREN parameter_type_list RPAREN'''
            p[0] = BinOp('()', p[1], p[3])

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

        # parameter_type_list
        def p_parameter_type_list(p):
            '''parameter_type_list : parameter_list
                                   : parameter_list COMMA ELLIPSIS'''
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
            '''parameter_declaration : declaraion_sepcifiers declarator
                                     | declaration_specifiers abstract_declarator
                                     | declaration_specifiers'''
            if len(p) == 2:
                p[0] = p[1]
            else:
                p[0] = Expr(etype='expr', expr=' '.p[1:3])

        # abstrct_declarator
        def p_abstract_declarator(p):
            '''abstrac_declarator : pointer
                                  | direct_abstract_declarator
                                  | pointer direct_abstract_declarator'''
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

        # conditional_expression
        def p_conditional_expression(p):
            # ignore
            pass
        
        # compoud_statement
        def p_compound_statement(p):
            '''compound_statement : LBRACE RBRACE
                                  | LBRACE statement_list RBRACE
                                  | LBRACE declaration_list RBRACE
                                  | LBRACE declaration_list statement_list RBRACE'''
            # ignore
            pass
        
        # init_declarator_list
        def p_init_declarator_list(p):
            '''init_declarator_list : init_declarator
                                    | init_declarator_list COMMA init_declarator'''
            p[0] = p[1]

        def p_init_declarator(p):
            '''init_declarator : declarator
                               | declarator ASSIGN initializer'''
            p[0] = p[1]

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
        
        def p_empty(p):
            'empty : '
            pass

        def p_error(p):
            printp(("syntax error at '%s'") % p.value)

        return yacc.yacc(method='LALR')


def main(data):
    cgardener = grammar_tree.GrammarHandler()
    lexer = lex.CodeLexer()
    p = CodeParser(lexer, cgardener)
    p.parser.parse(data, debug=0)

if __name__ == '__main__':
    data = '''
        int32_t RSSP_I_link_open(RSSP_I_local_cfg_t * const local)
        {
            int32_t ret = -1;
        }
    '''
    main(data)
