#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import re
import glob
import argparse as apa

import utils.interp  as fip
import utils.fwriter as fw
import utils.twriter as tw

from __init__ import __version__

_c_ext_pattern = re.compile(r'^(\w)+(\.c)$')

class CodeParser:
    '''Shape a code paser for each single .c file'''
    def __init__(self, path, debug=False):
        '''Initialiser of code parser
        Accepting a .c file path and debug mode trigger

        Initialise and store the infomation in these instance variables:
            - .c file path
            - the working directory of this parser
            - initialised empty list for function definitions
            - debug mode or not
        
        The Validation of the .c file is checked before calling this creator
        '''
        self.filepath    = path
        self.working_dir = os.path.dirname(self.filepath)
        self.def_list    = list()
        self._debug       = debug

        self.parse_process()

    def parse_process(self):
        '''Pass the .c file contents to the interpreter module'''

        self.def_list.clear()
        with open(self.filepath) as f:
            self.defs_list = fip.interpret(f.readlines(), debug=self._debug)

        if len(self.defs_list) is 0 and self._debug:
            print("INFO : None of function definitions were founded.")

def parse_all_in_dir(path=os.getcwd(), debug=False):
    '''
    parse all .c files in giving working dir
    '''
    for f in os.listdir(path):
        filepath = os.path.join(path, f)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            if _c_ext_pattern.match(f) is None:
                if debug: print("ERROR: {:s} isn't a validate .c file.".format(f))
            else:
                filename = os.path.splitext(f)[0]
                if filename[:4]=="ver_" or filename[-5:len(filename)]=="_stub":
                    pass
                else:
                    print("INFO : Current working dir: {:s}".format(filepath))
                    #main_process(tblpath, filepath, debug=debug)
                    print()
        else:
            pass
    
def parse_file(fn, debug=False):
    '''Handling the file validation check before parsing its content
    @Param fn           Should be the absolute or relative path of a .c file
    
    @Param debug        Debug mode trigger

    @Return None
    '''
    filepath = os.path.abspath(fn)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        if _c_ext_pattern.match(os.path.basename(fn)) is None:
            print("ERROR: {:s} isn't a .c file.".format(fn))
        else:
            print("INFO : Current working dir: {:s}".format(filepath))
            parser = CodeParser(filepath,debug)
            #parse_process(filepath, debug=debug)
    else:
        print("ERROR: Input={:s} is not a file".format(fn))

def parse_command_process(args):
    '''Subcommand 'parse' handling function
    @Detail Parsing options and their given values passed by args
    
            Giving multiple directory or files values are allowed, and would be parsed
            one by one.

    @Param  args        Arguments passed by command line
    
    @Return None
    '''
    path_list = list()
    # argparse captures the single value followed -d as str type
    # but multiple values as a list type
    # And single value to positional arguments is passed as list type as well.
    # Integrating the args to be a list hence trowelling this weird difference
    # of args capture.
    if type(args.filepath) is list:
        path_list.extend(args.filepath)
    else:
        path_list.append(args.filepath)

    if args.Dir:
        for filepath in path_list:
            if os.path.exists(filepath) and os.path.isdir(filepath):
                parse_all_in_dir(filepath, args.Debug)
            else:
                print("ERROR: Directory is NOT found. A dir path is expected.")
    else:
        for filepath in path_list:
            parse_file(filepath, args.Debug)

def table_command_process(args):
        if args.Funclist:
            print("list")
        if args.Output:
            print("output")
        else:
            print("table command has undefined option")

def main():
    '''Accept and process arguments from command-line

    Including:
        Options:
            -h, --help,                 help usage(default builtin by argparse module)
            -v, --version,              version print

        Sub-commands(and options):
            + parse:
                * -d, --dir, -a, --all  accept a directory path and parse all .c files inside
            + table
                * -l, --list,           list out all functions within .c files in the given directory
                * -o, --output,         output the function list to the excel file and make it a checklist for unittest

    Any other subcommands and options are expanded below.
    '''
    # Arguments parser and subparser
    arg_parser    = apa.ArgumentParser(prog="Gstub", description="Generate interpositioning stubs or/and test checklist from .c file")
    arg_subparser = arg_parser.add_subparsers(help="Commands in Gstub for various situations")
    # this module version print option -v and --version
    arg_parser.add_argument("-v", "--version", action='version', version="%(prog)s@{:s}".format(__version__))

    # Parser of "parse" sub-command and its' options
    parse_parser = arg_subparser.add_parser("parse", 
            help="Parse the .c file(s) and generate interpositioning stubs for the unittest")
    # Accept a str type path as positional option value
    parse_parser.add_argument(
            dest    = "filepath",
            type    = str,
            nargs   = '*',
            default = os.getcwd(),
            help="accept a file or directory path as parser input and working dir")
    # Debug mode option
    parse_parser.add_argument(
            "--debug", 
            dest    = "Debug", 
            help    = "Debug mode", 
            action  = 'store_true'
            )
    # Directory option trigger
    parse_parser.add_argument(
            '-d', '--dir', '-a', '--all', 
            dest    = "Dir",
            action  = "store_true",
            help    = "Parse all .c files in the given directories' path"
            )
    parse_parser.set_defaults(func=parse_command_process)

    # parser of "table" sub-command and its' options
    table_parser = arg_subparser.add_parser(
            "table", 
            help="Output a list of .c files and contained functions")
    table_parser.add_argument(
            '-l', "--list", 
            dest   = "Funclist", 
            help   = "List out all functions", 
            action = 'store_true'
            )
    table_parser.add_argument(
            '-o', "--output", 
            dest   = "Output", 
            help   = "Output the function list to excel file", 
            action = 'store_true'
            )
    table_parser.set_defaults(func=table_command_process)

    try:
        # Print help usage if there's no args followed the command
        if len(sys.argv) is 1:
            arg_parser.print_help()
            sys.exit(1)

        args = arg_parser.parse_args()
        args.func(args)

    except apa.ArgumentError as e:
        arg_parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
