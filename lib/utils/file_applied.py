# Files
import fileinput
# Operating system
import os
# Custom modules
import lib.utils.printing as printing
import lib.utils.common as common


##############################
### File Applied Functions ###
##############################


def count_file(root: str, filename: str) -> int:
    '''Counts file.'''
    
    return 1


def count_file_with_str(root: str, filename: str, str_to_find: str):
    '''Counts file if in has specified str in it.'''
    
    with fileinput.FileInput(os.path.join(root, filename)) as file:
        for line in file:
            if str_to_find in line:
                return 1
    
    return 0


def delete_file(root: str, filename: str) -> int:
    '''Deletes file.'''
    
    os.remove(os.path.join(root, filename))
    return 1


def backup_file(root: str, filename: str) -> int:
    '''Backups file that has backup for it in the same directory.'''
    
    # Removes file that was backuped
    os.remove(os.path.join(root, filename).replace('.bak', ''))
    # Removes '.bak' extension from the end of the backup file
    os.replace(os.path.join(root, filename), os.path.join(root, filename).replace('.bak', ''))
    
    return 1


def filename_add_prefix(root: str, filename: str, prefix: str):
    '''Adds specified prefix to file.'''
    
    os.replace(os.path.join(root, filename), os.path.join(root, prefix + filename))
    
    return 1


def filename_replace_prefix(root: str, filename: str, old_prefix: str, new_prefix: str) -> int:
    '''Replaces specified prefix of file.'''
    
    os.replace(os.path.join(root, filename), os.path.join(root, new_prefix + filename[len(old_prefix):]))
    
    return 1


def replace_str_in_file(root: str, filename: str, replacements: tuple[str, str]) -> int:
    '''Performs specified replacements in each line of file.'''
    
    # Open file for writing and create backup for it
    with fileinput.FileInput(os.path.join(root, filename), inplace=True, backup='.bak') as file:
        # For each line in file
        for line in file:
            # Save line
            new_line = line
            # Perform all replacements
            for replacement in replacements:
                new_line = new_line.replace(replacement[0], replacement[1])
            # Print string into file
            print(new_line, end='')
        
    # Remove file backup
    os.remove(os.path.join(root, filename) + ".bak")
    
    return 1


def modify_structure_extender(root: str, filename: str, replacemant_construct_func, replacemant_construct_func_args: list) -> int:
    '''Modifies structure extender (in '.def' file).'''
    
    # Get file tokens
    tokens = common.get_tokens_from_file(root, filename)
    # Find indexes of all occurrences of 'extender' token in file
    extender_indexes = common.find_token_occurrences(tokens, 'extender')
    # If token exists in file
    if extender_indexes:
        # For all occurrences in list
        for extender_index in extender_indexes:
            # Index of possible token definition
            extender_def_index = extender_index + 1
            # If it is not outside of tokens list and token is '"structure"'
            if extender_def_index < len(tokens) and tokens[extender_def_index] == '"structure"':
                # Init replacements list
                replacements = []
                # Set current index in tokens list
                i = extender_def_index + 1
                # While index is in tokens list length and currently observed token is 'place'
                while i < len(tokens) and tokens[i] == 'place':
                    # Construct replacement from second token after current ('place') and modified token
                    replacements.append(replacemant_construct_func(*([tokens[i + 2]] + replacemant_construct_func_args)))
                    # Update index
                    i += 3
                
                return replace_str_in_file(root, filename, replacements)
    return 0


def get_mtl_texture_paths(root: str, filename: str, maps: list, discard_variations: bool, used_texture_files: list) -> int:
    '''Extracts used textures paths from .mtl file.'''
    
    # Get file tokens
    tokens = common.get_tokens_from_file(root, filename)
    for map in maps:
        # Find indexes of all occurrences of <map_type> token in file
        map_indexes = common.find_token_occurrences(tokens, map)
        # If map exists in file
        if map_indexes:
            # For all occurrences in list
            for map_index in map_indexes:
                # Index of prev token
                prev_token = map_index - 1
                # Continue only if this extender was not commented with ';'
                if prev_token >= 0 and tokens[prev_token] != ';':
                    # Index of possible token definition
                    map_path_index = map_index + 1
                    # If it did not went outside of tokens list and next token is a path to texture file
                    if map_path_index < len(tokens) and '$' in tokens[map_path_index]:
                        # Add extracted path
                        map_path = tokens[map_path_index][3:][:-1].replace('/', '\\').lower()
                        if discard_variations:
                            map_path = map_path.split('#', 1)[0]
                        used_texture_files.append(map_path)
                else:
                    printing.print_yellow('Commented texture in file: ' +  os.path.join(root, filename))
    return 1