import ply.yacc as yacc
import grammer.grammer_tree as grammer_tree

class CodeParser:
    def __init__(self, lexer, gardener):
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
            prototype = ' '.join(p[1:-1])
            print(prototype)
            p[0] = (len[p]==5) ? grammer_tree.NodeFunc(name=p[2], prototype)
                               : grammer_tree.NodeFunc(name=p[1], prototype)
            gardener.func_write(p[0])

        def p_function_definition_old_1(p):
            'function_definition : declaration_specifiers declarator compound_statemnt'
            prototype = ' '.join(p[1:3])
            p[0] = grammer_tree.NodeFunc(name=p[2], prototype)
            gardener.func_write(p[0])


        def p_function_definition_old_2(p):
            'function_definition: declarator compound_statement'
            prototype = 'void' + str(p[1])
            p[0] = grammer_tree.NodeFunc(name=p[1], prototype)
            gardener.func_write(p[0])

        # declaration_list

        def p_declaration_list_1(p):
            'declaration_list: declaration'
            p[0] = ListOp('declaration', p[1])

        def p_declaration_list_2(p):
            'declaration_list : declaration_list declaration'
            p[0] = p[1]
            p[0].add_child(p[2])



        # declarator

        def p_declarator(p):
            '''declarator : pointer direct_declarator
                          | direct_declarator'''
            p[0] = (len(p)==2) ? NodeUniOp(p[1], p[2])
                               : p[1]

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
            p[0] = (len(p)==3) ? UniOp(p[1], p[3])
                               : UniOp(p[1], p[1])

        # type_qualifier_list

        def p_type_qualifier_list(p):
            '''type_qualifier_list : type_qualifier
                                   | type_qualifier_list type_qualifier'''
            p[0] = (len[0]==1) ? p[1]
                               : p[2]

        def p_type_qualifier(p):
            '''typ_qualifier : CONST
                             | VOLATILE'''
            p[0] = Expr('expr', p[1])


