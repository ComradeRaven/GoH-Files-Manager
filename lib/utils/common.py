# Files
import fileinput
# Operating system
import os
# Regular expressions
import re
# System
import sys
# Custom modules
import lib.utils.printing as printing
import lib.utils.file_applied as file_applied


####################
### Common Utils ###
####################


#==============
#=== Generic ====
#==============


def validate_directories(directories: list) -> bool:
    '''Validates if provided directories exist.'''
    
    for directory in directories:
        if not os.path.exists(directory):
            printing.print_red('NO SUCH DIRECTORY: ' + directory)
            return False
    return True


def query_yes_no(question):
    '''Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    '''
    
    # Valid answers
    valid = {'yes': True, 'y': True, 'no': False, 'n': False}

    while True:
        # Show question
        sys.stdout.write(question + ' [Y/n] ')
        # Get input
        choice = input().lower()
        # Input procces
        if choice == '':
            return True
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


#=============================
#=== File Function Applying ====
#=============================


def apply_function_to_files(function, function_args: list, extension: str, directory: str) -> int:
    '''Applies given function with given parameters to files with provided extension (use dots, e.g. ".def") that were found in given
    directory. Note: before function is applied directory root and file name are added to the beginning of the function arguments list.
    The function should return 1 on complete for the counter to work properly.'''
    count = 0
    try:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith(extension):
                    # Apply function
                    count += function(*([root] + [filename] + function_args))
        return count
    except Exception as e:
        printing.print_exception(e)
        return count


#==========================
#=== Structure Extenders ====
#==========================


def modify_structure_extender_add_prefix(token: str, prefix: str) -> tuple[str, str]:
    '''Adds prefix to structure extender values.'''
    
    return (token, '"' + prefix + token[1:])


def modify_structure_extender_replace_prefix(token: str, old_prefix: str, new_prefix: str) -> tuple[str, str]:
    '''Replaces prefix in structure extender values.'''
    
    return (token, '"' + new_prefix + token[len(old_prefix) + 1:])


#==================
#=== File Tokens ====
#==================


def get_tokens_from_file(root: str, filename: str) -> list:
    '''Returns all tokens in file (separation is done at ' ', '{', '}', '\t', '\n').'''
        
    # Init file tokens list
    tokens = []
    with fileinput.FileInput(os.path.join(root, filename)) as file:
        for line in file:
            # Get tokens in line
            tokens += [x for x in re.split(' |{|}|\t|\n', line) if x]
    return tokens


def find_token_occurrences(tokens: list, token: str) -> list:
    '''Returns list of indexes where provided token is located in token list.'''
    
    return [idx for idx, value in enumerate(tokens) if value == token]


#====================
#=== Texture Files ====
#====================


def list_all_texture_files(directory: str, sub_directory: str, discard_variations: bool) -> list:
    '''Returns list of texture files, concatenated with their paths and without path of provided subdirectory
    (can discard symbols after '#', if needed).'''
        
    texture_files = []
    try:
        # Combine paths
        path = os.path.join(directory, sub_directory)
        # Check resulting path
        if not os.path.exists(path):
            raise Exception('NO SUCH DIRECTORY: ' + path)
        
        for root, dirs, files in os.walk(path):
            for filename in files:
                # Append properly modified filename with its path
                texture_file = os.path.join(root, filename).replace(directory + '\\', '').split('.', 1)[0].lower()
                if discard_variations:
                    texture_file = texture_file.split('#', 1)[0]
                texture_files.append(texture_file)
        
        return texture_files
    except Exception as e:
        printing.print_exception(e)
        return texture_files


def delete_unused_texture_files(directory: str, sub_directory: str, unused_texture_files: set) -> int:
    '''Deletes file if its name without extension (will discard symbols after '#') is in provided set of names.'''
    
    try:
        # Combine paths
        path = os.path.join(directory, sub_directory)
        # Check resulting path
        if not os.path.exists(path):
            raise Exception('NO SUCH DIRECTORY: ' + path)
        
        for root, dirs, files in os.walk(directory):
            for filename in files:
                # Convert filename
                file_name = os.path.join(root, filename).replace(directory + '\\', '').split('.', 1)[0].lower()
                file_name = file_name.split('#', 1)[0]
                
                if file_name in unused_texture_files:
                    file_applied.delete_file(root, filename)
    except Exception as e:
        printing.print_exception(e)