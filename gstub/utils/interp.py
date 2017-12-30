import re

_func_def_pattern  = re.compile(r'^(\w+\s+)+(\w+)\s*\(\s*(.+)\s*(\)?|(\)\{)?)')
_param_dec_pattern = re.compile(r'\(\s*((?:void)|[^!=<>]+\s*)(\)?|(\)\{)?|,?)$')
_merge_status      = False
_merge_line        = ""

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
            self.format_debug_info()

    def __str__(self):
        return self.prototype

    def format_debug_info(self):
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
                    self.params = [{'type': "void", 'qualifier':'', 'name': "void"}]
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

def func_parser(defs, code, debug=False):
    global _merge_status
    global _merge_line
    code = code.strip().strip('\n')
    if _merge_status == False:
        found = _func_def_pattern.match(code)
        if found is None:
            pass
        else:
            line = found.group()
            if _param_dec_pattern.search(line) is not None:
                line = line.rstrip('{')
                if line.endswith(r','):
                    _merge_status = True
                    _merge_line  += line
                else:
                    defs.append(FuncElem(line, debug))
            else:
                pass

    else:
        if code.endswith(r','):
            _merge_line += code
        if code.endswith(r')'):
            _merge_status = False
            _merge_line += code
            _merge_line = ' '.join(re.split(r'\s+', _merge_line))
            defs.append(FuncElem(_merge_line, debug))
            _merge_line = ""
        elif code.endswith(r');'):
            # 函数原型声明，丢弃已解析部分
            # TODO: 添加deflist中函数名是否已存在的查找函数，对函数声明也加入解析，函数定义解析后不用再重复加入列表
            _merge_status = False
            _merge_line = ""
        else:
            pass

def interpret(code_lines, debug=False):
    func_defs = list()
    func_defs.clear()
    if code_lines is None or len(code_lines)==0:
        return
    else:
        for l in code_lines:
            func_parser(func_defs, l, debug=debug)
    return func_defs
