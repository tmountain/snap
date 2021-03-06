import sys

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
PURPLE = "\033[35m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_c(text,colors):
    '''Prints a string with the given colors

    Example: print_c("hello world",RED+BOLD)
    '''
    sys.stdout.write(colors+text+RESET)
    sys.stdout.flush()

def error(text):
    print_c(text,RED)

def big_error(text):
    print_c(text,RED+BOLD)

def clear():
    '''Clears terminal'''
    print(chr(27)+chr(91)+'H'+chr(27)+chr(91)+'J')

def readline():
    return sys.stdin.readline().rstrip() 

def choice(text,default=False,colors=""):
    if default: yn = "[y]/n"
    else: yn = "y/[n]"

    print_c("{0} {1} ".format(text,yn),colors)

    answer = readline()
    if   answer.lower() == "y": return True
    elif answer.lower() == "n": return False
    else:                       return default
