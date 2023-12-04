# Terminal colors
from colorama import Fore, Style


######################
### Printing Utils ###
######################


def print_green(messsage):
    '''Prints green message.'''
    
    print(Fore.GREEN + messsage + Style.RESET_ALL)


def print_yellow(messsage):
    '''Prints yellow message.'''
    
    print(Fore.YELLOW + messsage + Style.RESET_ALL)


def print_red(messsage):
    '''Prints red message.'''
    
    print(Fore.RED + messsage + Style.RESET_ALL)


def print_exception(exception):
    '''Prints exception message.'''
    
    print_red("EXCEPTION: " + str(exception))


def print_exception_with_filename(exception: Exception, filename: str):
    '''Prints exception message and filename, whose processing led to this exception.'''
    
    print_red("EXCEPTION: " + str(exception) + ' IN FILE: ' + filename)