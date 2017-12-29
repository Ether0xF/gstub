#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import re
import glob
import argparse as apa

import gstub.utils.interp  as fip
import gstub.utils.fwriter as fw
import gstub.utils.twriter as tw

from gstub.__init__ import __version__

decl_pattern  = re.compile(r'[^\(\)]+')
param_pattern = re.compile(r'\(.*?\)')
c_file_pattern = re.compile(r'^(\w)+(\.c)$')

func_dict = dict()

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

def parse_process(filepath, debug=False):
    defs = list()
    defs.clear()
    prototypes = list()
    with open(filepath) as f:
        defs = fip.interpret(f.readlines(), debug=debug)

    if len(defs)==0 and debug: print("INFO : None of function definitions were founded.")

    return defs

def main_process(tblpath, filepath, debug=False):
    func_defs = list()
    func_defs = parse_process(filepath, debug)

    tw.utest_check_list_processor(tblpath, filepath, func_defs, debug)

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
                -d             parse all .c files in a given path. 
                                a valid path should follow this option
                -a, --all      parse all .c files in current working dir.
                ''')

def parse_all_in_dir(path=os.getcwd(), debug=False):
    '''
    parse all .c files in giving working dir
    '''
    tblpath = tw.utest_create_checklist_file(path)
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
                    main_process(tblpath, filepath, debug=debug)
                    print()
        else:
            pass
    
def parse_file(fn, debug=False):
    filepath = os.path.abspath(fn)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        if c_file_pattern.match(os.path.basename(fn)) is None:
            print("ERROR: {:s} isn't a .c file.".format(fn))
        else:
            print("INFO : Current working dir: {:s}".format(filepath))
            tblpath = tw.utest_create_checklist_file(os.path.dirname(filepath))
            main_process(tblpath, filepath, debug=debug)
            print()
    else:
        print("ERROR: filename={:s} -> File not found.".format(fn), end=' ')

def parse_command_process(args):
        if args.Debug:
            debugmode = True
        else:
            debugmode = False

        if args.Path:
            print("dir")
        elif args.File:
            parse_file(args.File, debugmode)
        else:
            print("parse command has undefined option")

def table_command_process(args):
        if args.Funclist:
            print("list")
        if args.Output:
            print("output")
        else:
            print("table command has undefined option")

def main_command_process(args):
    args.print_help()

def main():
    '''Accept and process arguments from command-line

    Including:
        Options:
            -h, --help,                 help usage(default builtin by argparse module)
            -v, --version,              version print

        Sub-commands(and options):
            + parse:
                * -f, --file,           default option under "parse" command, accept a .c filename(path)
                * -d, --dir, -a, --all  accept a directory path and parse all .c files inside
            - table
                * -l, --list,           list out all functions within .c files in the given directory
                * -o, --output,         output the function list to the excel file and make it a checklist for unittest

    Any other subcommands and options are expanded below.
    '''
    try:
        # Arguments parser and subparser
        arg_parser    = apa.ArgumentParser(prog="Gstub", description="Generate interpositioning stubs or/and test checklist from .c file")
        arg_subparser = arg_parser.add_subparsers(help="Commands in Gstub for various situations")
        # this module version print option -v and --version
        arg_parser.add_argument("-v", "--version", action='version', version="%(prog)s@{:s}".format(__version__))
        arg_parser.set_defaults(func=main_command_process)

        # parser of "parse" sub-command and its' options
        parse_parser = arg_subparser.add_parser("parse", 
                help="Parse the .c file(s) and generate interpositioning stubs for the unittest")
        # exclusive group options consisted [-f, --file] against [-d, --dir, -a, --all]
        parse_parser_exgroup = parse_parser.add_mutually_exclusive_group()
        parse_parser_exgroup.add_argument('-d', '--dir', '-a', '--all', 
                                          dest    = "Path",
                                          metavar = "Path",
                                          help    = "parse all .c files in the given directories' path")
        parse_parser_exgroup.add_argument('-f', '--file', 
                                          dest    = "File",
                                          metavar = "Filename",
                                          help    = "parse a single .c file by accepting its path")
        parse_parser.add_argument        ("--debug", 
                                          dest    = "Debug", 
                                          help    = "Debug mode", 
                                          action  = 'store_true')
        parse_parser.set_defaults(func=parse_command_process)

        # parser of "table" sub-command and its' options
        table_parser = arg_subparser.add_parser("table", 
                help="Output a list of .c files and contained functions")
        table_parser.add_argument        ('-l', "--list", 
                                          dest   = "Funclist", 
                                          help   = "List out all functions", 
                                          action = 'store_true')
        table_parser.add_argument        ('-o', "--output", 
                                          dest   ="Output", 
                                          help   ="Output the function list to excel file", 
                                          action ='store_true')
        table_parser.set_defaults(func=table_command_process)


        args = arg_parser.parse_args()
        args.func(args)

    except apa.ArgumentError as e:
        helpman()
        sys.exit(2)

if __name__ == '__main__':
    main()
