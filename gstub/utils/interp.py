import re

__doc__ = ""
__version__ = "0.0.1"

func_def_pattern = re.compile(r'^((\w)+\s)+(\w)+\((.*)\)(\{)?')
func_defs = list()
class FuncElem:
    func_idx = 0
    QUALIFIERS = ['const', 'volatile']
    SPECIFIERS = ['static', 'extern']
    def __init__(self, proto=None, debug=False):
        FuncElem.func_idx += 1
        self.idx = FuncElem.func_idx
        self.prototype = proto
        self.return_type = ""
        self.specifier  = list()
        self.func_name = ""
        self.params = list()

        self.decl_pattern  = re.compile(r'[^\(\)]+')
        self.decla_parser(self.prototype, debug)

        if debug:
            self.debug_info()

    def debug_info(self):
            print("{:02d}  {:s}".format(self.idx, self.func_name), end='')
            for i in range(40-len(self.func_name)):
                print("=", end='')
            print()
            for p in self.params:
                print("    "+str(p))
            print()

    def decla_parser(self, proto=None, debug=False):
        if proto is None:
            if debug: print("{:0d}  ERROR: Function prototype is not defined.".format(self.idx))
            return
        decl_literal  = ""
        param_literal = ""
        match = self.decl_pattern.findall(proto)
        if match:
            decl_literal = match[0]

            # parse the func return type
            self.return_type = " ".join(decl_literal.split(' ')[:-1])
            for s in FuncElem.SPECIFIERS:
                s_beg = self.return_type.find(s)
                if s_beg != -1:
                    self.return_type = self.return_type[:s_beg].strip() + self.return_type[(s_beg+len(s)):].strip()
                    self.return_type.strip()
                    self.specifier.append(str(s))

            # parse the func name
            self.func_name   = decl_literal.split(' ')[-1]

            # find if there is any parameter matched
            if len(match) > 1:
                param_literal = match[1]
                if param_literal == "void":
                    fparams = ["void"]
                else:
                    fparams = [e.strip(' ') for e in param_literal.split(',')]
            else:
                # param list is empty and "void" token isn't found
                if debug: print("{:0d}  WARNING: Func \"{:s}\" has empty parameters.".format(self.idx, self.func_name))
                fparams = ["void"]
            # write parameters in tuple form of (param_type, param_name)
            for fp in fparams:
                if fp == "void":
                    self.params = [("void", "void")]
                else:
                    param_type = " ".join(fp.split(' ')[:-1])
                    param_name = str(fp.split(' ')[-1])
                    # deal with if any qualifier
                    param_qualifier = list()
                    for q in FuncElem.QUALIFIERS:
                        q_beg = param_type.find(q)
                        if q_beg != -1:
                            param_type = param_type[:q_beg] + param_type[(q_beg+len(q)):]
                            param_qualifier.append(str(q))
                    if param_name[0] == '*':
                        param_name = param_name[1:]
                        param_type += " *"
                    param_dic = {
                        'type': param_type,
                        'qualifier': param_qualifier,
                        'name': param_name,
                    }
                    self.params.append(param_dic)
        else:
            if debug: print("{:0d}  ERROR: Declaration pattern didn't match.".format(self.idx))

    def __str__(self):
        return self.prototype

def func_parser(code, debug=False):
    find = func_def_pattern.search(code)
    if find is None:
        pass
    else:
        p = find.group().strip(' ')
        p = p.strip('{')
        p = p.strip('}')
        func_defs.append(FuncElem(p, debug))

def interpret(code_lines, debug=False):
    if code_lines is None or len(code_lines)==0:
        return
    else:
        for l in code_lines:
            func_parser(l, debug=debug)
    return func_defs
