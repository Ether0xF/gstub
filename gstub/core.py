#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import re
import getopt
import gstub.utils.interp as fip
import gstub.utils.fwriter as fw

__version__ = "V0.0.1 2017-11-14"

decl_pattern = re.compile(r'[^\(\)]+')
param_pattern = re.compile(r'\(.*?\)')

def funcdef_writer(deflist=None):
    if deflist is None:
        return

    proto_list = list()
    decl = ""
    param_list = ""
    for d in deflist:
        match = decl_pattern.search(d)
        if match:
            decl = match.group()
        paren_beg = d.find('(')
        paren_end = d.find(')')
        if (paren_beg!=-1) and (paren_end!=-1):
            formal_params = d[paren_beg+1 : paren_end]
            params_list   = [e.strip(' ') for e in formal_params.split(',')]
            params        = list()
            for p in params_list:
                param_type = ' '.join(p.split(' ')[:-1])
                param_name = p.split(' ')[-1]
                param_set = (param_type, param_name)
                params.append(param_set)

        proto_list.append(
                { "ret_type": decl.split(' ')[0], 
                  "name"    : decl.split(' ')[1],
                  "params"  : params})
    return proto_list

def main_process(filename, debug=False):
    defs = list()
    prototypes = list()
    with open(filename) as f:
        defs = fip.interpret(f.readlines(), debug=debug)
    fw.stubs_composer("".join(filename.split('.')[:-1]), defs)

def helpman():
        print(
        '''
        ====Usage===
            gstub [options] <filename>
            gsb   [options] <filename>
                The script accept a .c filename and generates stubed-funcs by
                scanning the source code inside.
                please append the .c file name followed the command.
                    e.g. python stubs.py abc.c
            
            Options:
                -h, --help     this help information
                -v, --version  version print
                --debug        debug mode, output function names and params
                ''')

def main():
    debugmod = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["debug"])
        if len(opts)==0:
            helpman()
            sys.exit(0)
        for o,a in opts:
            if o in ['-v', '--version']:
                print("stub.py @ ", __version__)
            elif o in ['-h', '--help']:
                helpman()
            elif o in ['--debug']:
                debugmod = True

        for filename in args[0:]:
            if os.path.exists(filename) and os.path.isfile(filename):
                if re.compile(r'(\w)+(\.c)$').match(filename) is None:
                    print("ERROR: Validate .c file is not found!!!!")
                else:
                    print("INFO : Current working dir: {:s}".format(os.path.abspath(filename)))
                    main_process(filename, debug=debugmod)
                    print()
            else:
                print("ERROR: filename={:s} -> File not found.".format(filename), end=' ')
    except getopt.GetoptError as e:
        helpman()
        sys.exit(2)

if __name__ == '__main__':
    main()
