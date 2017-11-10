# -*- coding: utf-8 -*-
import sys

class Expr:
    def __init__(self, etype=None, expr=None):
        self.etype = etype
        self.expr  = expr
        self.value = expr
    def __str__(self):
        return self.value

class UniOp(Expr):
    def __init__(self, operator="-", operand=None):
        Expr.__init__(self,etype="uniop", expr=operator)
        self.operand = operand
        self.operator = str(operator)
        if self.operator == '()':
            self.value = '(' + str(self.operand) + ')'
        elif self.operator == 'case':
            self.value = self.operator + ' ' + str(self.operand) + ':'
        elif self.operator == '-':
            self.value = self.operator + str(self.operand)
        else:
            self.value = self.operator + ' ' + str(self.operand)

class BinOp(Expr):
    def __init__(self, operator="=", loperand=None, roperand=None):
        Expr.__init__(self, "binop", operator)
        self.loperand = loperand
        self.roperand = roperand
        if operator == '()':
            self.value = str(self.loperand) + str(operator[0]) + str(self.roperand) + str(operator[1])
        else:
            self.value = str(self.loperand) + str(operator) + str(self.roperand)

class ListOp(Expr):
    def __init__(self, operator="{}", operand=None):
        self.sep = ' '
        self.children = list()
        if isinstance(operator, str):
            Expr.__init__(self, etype="list", expr=operator)
            if (operand is None):
                self.children = list()
            elif isinstance(operand, list):
                self.children = operand
                self.value = ' '.join(operand)
            else: 
                self.chidren = list(operand.value)
                self.value = str(operand)
        elif isinstance(oeraotr, Expr):
            Expr.__init__(self, etype="expr", expr=operator)
            self.children = list(operand)
            self.value = str(operand)
        else:
            pass

    def add_child(self, child):
        if isinstance(child, list):
            self.children.extend(child)
            for e in child:
                self.value += ' '
                self.value += str(e)
        elif isinstance(child, ListOp):
            self.children.extend(child.value)
            for e in child.value:
                self.value += ' '
                self.value += str(e)
        elif isinstance(child, Expr):
            self.children.append(child.value)
            self.value += ' '
            self.value += str(child.value)
        else:
            self.children.append(child)
            self.value += ' '
            self.value += str(child)


class Func(Expr):
    def __init__(self, name="", prototype=""):
        Expr.__init__(self, "func", prototype)
        self.name = str(name)
        self.prototype = str(prototype)

class GrammarHandler:
    def __init__(self):
        self.funcs = list()

    def reset(self):
        self.funcs.clear()

    def func_write(self, func):
        self.funcs.append(func)
        print("##########################", func)

def debug_info(p):
    print("DEBUG_INFO:--------------------")
    print("\t", p.value)
    print("-------------------------------")
