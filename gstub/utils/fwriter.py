#-*- coding: utf-8 -*-

import os

__doc__ = ""
__version = "0.0.1"

stub_cfgs = list()

def stubs_header_preprocess_writer(filename):
    codes = list()
    line = "#ifndef __{:s}_H\n".format(filename.upper())
    line += "#define __{:s}_H\n\n".format(filename.upper())
    codes.append(line)

    line = "ifdef __cplusplus\n"
    line += "extern \"C\"{\n"
    line += "#endif\n\n"
    codes.append(line)

    line = "#include \"unifw.h\"\n\n"
    codes.append(line)

    for c in stub_cfgs:
        codes.append(c+"\n")
    codes.append("\n")

    line = "#ifdef __cplusplus\n}\n#endif\n\n"
    codes.append(line)
    line = "#endif //__{:s}_H".format(filename.upper())
    codes.append(line)

    return codes


def stubs_preprocess_writer(filename):
    codes = list()
    line = "#include \"cpptest.h\"\n"
    line += "#include \"{:s}.h\"\n\n".format(filename)
    codes.append(line)
    
    return codes

def stubs_cfg_writer(ret, name, params):
    # ---------------global_vars-----------------------
    codes = list()
    line = "uint8_t __{:s}_stub_flag = 0;\n".format(name)
    codes.append(line)
    line = "uint32_t __{:s}_cfg_nbr  = 0;\n".format(name)
    codes.append(line)
    line = "uint32_t __{:s}_run_loop = 0;\n".format(name)
    codes.append(line)
    line = "{:s} * __{:s}_ret_list   = NULL;\n".format(ret, name)
    codes.append(line)
    for (t, n) in params:
        line = "{:s} * __{:s}_{:s}_ret_list = NULL;\n".format(t, name, n)
        codes.append(line)

    # ---------------cfg_func_definition-----------------------
    line = "void {0:s}_stub_cfg( uint8_t stub, int32_t nbr, {1:s} * {0:s}_ret_list, \n".format(name, ret)
    param_lines = list()
    for (t, n) in params:
        lpadding = "".join([" " for i in range(line.find('(')+2)])
        param_str = "{:s} * {:s}_ret_list".format(t, n)
        param_line = lpadding + param_str
        param_lines.append(param_line)
    line += ", \n".join(param_lines)
    line += ")"
    # add stub cfg func into list
    stub_cfgs.append(line+";")
    line += "{\n"
    codes.append(line)

    # ---------------cfg_func_definition-----------------------
    line = "    __{:s}_stub_flag = stub;\n".format(name)
    codes.append(line)
    line = "    __{:s}_cfg_nbr   = nbr;\n".format(name)
    codes.append(line)
    line = "    __{:s}_run_loop  = 0;\n".format(name)
    codes.append(line)
    line = "    __{0:s}_ret_list = {0:s}_ret_list;\n".format(name)
    codes.append(line)
    for (t, n) in params:
        line = "    __{0:s}_{1:s}_ret_list = {1:s}_ret_list\n".format(name, n)
        codes.append(line)
    line = "}\n"
    codes.append(line)
    return codes

def stubs_test_writer(ret, name, params):
    codes = list()
    param_lines = list()

    line = "EXTERN_C_LINKAGE {:s} {:s} (".format(ret, name)
    for (t, n) in params:
        if (t, n) == ("void", "void"):
            line += "void"
            break
        else:
            param_lines.append("{:s} {:s}".format(t, n))
    if len(param_lines) != 0:
        line += ", ".join(param_lines)
    line += ");\n"
    codes.append(line)

    line = "EXTERN_C_LINKAGE {:s} CppTest_Stubs_{:s} (".format(ret, name)
    for (t, n) in params:
        if (t, n) == ("void", "void"):
            line += "void"
            break
        else:
            param_lines.append("{:s} {:s}".format(t, n))
    if len(param_lines) != 0:
        line += ", ".join(param_lines)
    line += ")\n"
    codes.append(line)

    line = "{\n"
    line += "    {:s} * ret;\n".format(ret)
    codes.append(line)
    line = "    uint32_t index = __{:s}_run_loop;\n".format(name)
    codes.append(line)
    line = "    if (0 == {:s}_stub_flag)\n".format(name)
    codes.append(line)
    line = "    {\n"
    line += "        return {:s} (".format(name)
    if len(param_lines) == 0:
        line += "void"
    else:
        line += ", ".join(param_lines)
    line += ");\n    }\n"
    codes.append(line)
    line = "    else\n    {\n"
    line += "        __{:s}_run_loop++;\n".format(name)
    line += "        if (__{0:s}_run_loop >= __{0:s}_cfg_nbr) __{0:s}_run_lopp--;\n".format(name)
    line += "        if (index < __{:s}_cfg_nbr)\n".format(name)
    line += "        {\n"
    line += "            ret = &__{:s}_ret_list[indx];\n".format(name)
    codes.append(line)

    line = ""
    for (t, n) in params:
        if t == "void":
            param_stub_type = "0"
        else:
            param_stub_type = "1"
        line += "            __STUB_PARAM_ASSIGN( {:s}, {:s}, {:s}, {:s});\n".format(name, n, t, param_stub_type)
    line += "        }else{\n"
    codes.append(line)
    line = "            printp(\"\\r\\nUTEST stub crash at: %s L%d\\r\\n\", __FILE__, __LINE__);\n"
    codes.append(line)
    line = "            while(1);\n        }\n"
    codes.append(line)

    if "void" in ret:
        ret_stub_type = "0"
    else:
        ret_stub_type = "1"
    line = "    if (0 != {:s}))\n        return (*ret);\n".format(ret_stub_type)
    line += "    }\n}\n\n"
    codes.append(line)

    return codes

def stubs_code_writer(f, p):
    '''
        p is dict type that consists func definition with: 
            - return type
            - func name
            - formal param list formated as (param_type, param_name)
    '''
    ret_type  = p.return_type
    func_name = p.func_name
    params    = p.params
    f.writelines(stubs_cfg_writer(ret_type, func_name, params))
    f.writelines(stubs_test_writer(ret_type, func_name, params))

def stubs_composer(fn, func_list):
    if func_list is None :
        return
    elif len(func_list) == 0:
        print("ERROR: None of validate function definitions are found.")
    else:
        filename  = fn + '_stub'

        with open(filename+'.c', 'w') as f:
            f.writelines(stubs_preprocess_writer(filename))
            for p in func_list:
                stubs_code_writer(f, p)
        with open (filename+'.h', 'w') as h:
            h.writelines(stubs_header_preprocess_writer(filename))
