#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import re
import getopt
import glob
import gstub.utils.interp as fip
import gstub.utils.fwriter as fw

__version__ = "V0.0.1 2017-11-14"

decl_pattern  = re.compile(r'[^\(\)]+')
param_pattern = re.compile(r'\(.*?\)')
c_file_pattern = re.compile(r'^(\w)+(\.c)$')

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

def main_process(filepath, debug=False):
    defs = list()
    defs.clear()
    prototypes = list()
    with open(filepath) as f:
        defs = fip.interpret(f.readlines(), debug=debug)
    if len(defs) == 0:
        if debug: print("INFO : None of function definitions were founded.")
    else:
        fw.stubs_composer(filepath, defs)

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

def parse_all_in_dir(path=os.getcwd(), debug=False):
    '''
    parse all .c files in giving working dir
    '''
    for f in os.listdir(path):
        filepath = os.path.join(path, f)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            if c_file_pattern.match(f) is None:
                if debug: print("ERROR: {:s} isn't a validate .c file.".format(f))
            else:
                filename = os.path.splitext(f)[0]
                if filename[:4]=="ver_" or filename[-5:len(filename)]=="_stub":
                    pass
                else:
                    print("INFO : Current working dir: {:s}".format(filepath))
                    main_process(filepath, debug=debug)
                    print()
        else:
            print("{:s} is ignored".format(f))
            pass
    
def parse_file(fn, debug=False):
    filepath = os.path.abspath(fn)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        if c_file_pattern.match(fn) is None:
            print("ERROR: {:s} isn't a .c file.".format(fn))
        else:
            print("INFO : Current working dir: {:s}".format(filepath))
            main_process(filepath, debug=debug)
            print()
    else:
        print("ERROR: filename={:s} -> File not found.".format(fn), end=' ')

def main():
    debugmod = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvad", ["debug", "dir", "all"])
        if len(opts)==0 and len(args)==0:
            helpman()
            sys.exit(0)
        if ('--debug', '') in opts:
            debugmod = True
        if len(opts)==0 or (len(opts)==1 and ('--debug', '') in opts):
            for a in args:
                parse_file(a, debugmod)
        else:
            for (o,a) in opts:
                if o in ['-v', '--version']:
                    print("gstub @ ", __version__)
                elif o in ['-h', '--help']:
                    helpman()
                elif o in ['-a', '--all', '-d']:
                    if o == '-d':
                        for p in args:
                            if os.path.isdir(p):
                                parse_all_in_dir(p, debugmod)
                            else:
                                if debug: print("{:s} is not a valid path.".format(p))
                    else:
                        parse_all_in_dir(os.getcwd(), debugmod)
                else:
                    if o == "--debug":
                        pass
                    else:
                        helpman()
                        sys.exit(0)
    except getopt.GetoptError as e:
        helpman()
        sys.exit(2)

if __name__ == '__main__':
    main()
