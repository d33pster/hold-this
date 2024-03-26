#!/usr/bin/env python3

__version__ = '0.1.6'

from sys import argv as gotargs
from os import listdir
from optioner import options
import subprocess
from colorama import init as color, Fore as _
from re import search as searchin
import pydoc
import curses

def hold(dothis: str, argCTRL: options | None, dothat=[]):
    _foundfiles = None
    _allfiles = None
    _check = None | list[str]
    
    ## STAND-ALONE ARGUMENTS ##
    if len(dothat)==0:
        ## GIT CLONE ##
        if dothis=='-g' or dothis=='--github':
            ## could be of the form <username>/<repo>
            _check = argCTRL._what_is_(dothis.split('-')[len(dothis.split('-'))-1]).split('/')

            if len(_check) == 2:
                _foundfiles = listdir()
                subprocess.Popen(['git', 'clone', f'https://github.com/{_check[0]}/{_check[1]}.git']).wait()
                _allfiles = listdir()
            else:
                ## could be link
                # get current directory file list:
                _foundfiles = listdir()
                # run command and wait for it
                subprocess.Popen(['git', 'clone', f'{argCTRL._what_is_(dothis.split('-')[len(dothis.split('-'))-1])}']).wait()
                _allfiles = listdir()
            
            for f in _allfiles:
                if f not in _foundfiles:
                    print(f'\n{_.BLUE}hold>{_.RESET} run \'cd {f}\' to go into the cloned directory')
        elif dothis=='-h' or dothis=='--help':
            hold_help()
        elif dothis=='-v' or dothis=='--version':
            version()

    _allfiles = None
    _foundfiles = None
    _check = None
    exit(0)

def hold_help():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    try:
        stdscr.addstr('? help for <hold>\n\n')
        stdscr.addstr('     - ?help? -\n\n')
        stdscr.addstr('  |    -h or --help\n')
        stdscr.addstr('  |         => show this help text.\n  |\n')
        stdscr.addstr('  |    -v or --version\n')
        stdscr.addstr('  |         => show version.\n  |\n')
        stdscr.addstr('  |    -g or --github\n')
        stdscr.addstr('  |         => git clone repository\n')
        stdscr.addstr('  |         format: <username>/repository> or link')
        stdscr.addstr('\n\nEND')
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
    
    exit(0)

def version():
    print(f'{_.BLUE}hold-this{_.RESET} - {_.BLACK}copyright Soumyo Deep Gupta{_.RESET}')
    print(f'            version {_.RED}v{__version__}.{_.RESET}')
    print(f'            author: d33pster, github: {_.LIGHTBLUE_EX}https://github.com/d33pster{_.RESET}')
    exit(0)

def recommend(arg: str):
    if searchin('^\w+/\w+$', arg)!=None:
        print(f'{_.YELLOW}hold>{_.RESET} Arguments Missing. Perhaps \'-g\' option might be missing')
    else:
        print(f'{_.RED}hold>{_.RESET} no options provided. Dont just give me details. tell me what to do first.')
    
    exit(1)

def main():
    # colorama init
    color()
    # define short arguments
    shortargs = ['g', 'h', 'v']
    # define long arguments
    longargs = ['github', 'help', 'version']
    # define argument control
    argumentCTRL = options(shortargs, longargs, gotargs[1:])
    # get argument parse results
    actualargs, argcheck, argerror, falseargs = argumentCTRL._argparse()
    
    if argcheck:
        if len(actualargs)>1:
            hold(actualargs[0], argumentCTRL, actualargs[1:])
        elif len(actualargs)>0:
            hold(actualargs[0], argumentCTRL)
        elif len(actualargs)==0:
            if len(gotargs[1:])>0:
                recommend(gotargs[1])

if __name__=="__main__":
    main()