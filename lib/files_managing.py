# Operating system
import os
# Custom modules
import lib.utils.printing as printing
import lib.utils.common as common
import lib.utils.file_applied as file_applied


################################
### Files Managing Functions ###
################################


def add_buffer_dir_to_texture_paths(buffer_dir_name: str, directory: str):
    '''Adds buffer directory into file paths of texture files.'''
    
    replacements = [('{diffuse "$/', '{diffuse "$/' + buffer_dir_name + '/'),
                    ('{bump "$/', '{bump "$/' + buffer_dir_name + '/'),
                    ('{specular "$/', '{specular "$/' + buffer_dir_name + '/'),
                    ('{height "$/', '{height "$/' + buffer_dir_name + '/'),
                    ('{mask "$/', '{mask "$/' + buffer_dir_name + '/')]
    count = common.apply_function_to_files(file_applied.replace_str_in_file, [replacements], ".mtl", directory)
    printing.print_green('Count of processed texture files = ' + str(count))


def add_buffer_dir_to_ebm(buffer_dir_name: str, textures_directory: str, textures_sub_directory: str):
    '''Adds buffer directory to .ebm references.'''
    
    # Combine paths
    directory = os.path.join(textures_directory, textures_sub_directory)
    # Check resulting path
    if not os.path.exists(directory):
        raise Exception('NO SUCH DIRECTORY: ' + directory)
    
    # Perform replacements
    replacements = [('{reference "$/', '{reference "$/' + buffer_dir_name + '/')]
    count = common.apply_function_to_files(file_applied.replace_str_in_file, [replacements], ".ebm", directory)
    printing.print_green('Count of processed .ebm files = ' + str(count))


def replace_buffer_dir_in_texture_paths(old_buffer_dir_name: str, new_buffer_dir_name: str, directory: str):
    '''Replaces buffer directory in file paths of texture files.'''
    
    replacements = [('\\', '/'),
                    ('{diffuse "$/' + old_buffer_dir_name + '/', '{diffuse "$/' + new_buffer_dir_name + '/'),
                    ('{bump "$/' + old_buffer_dir_name + '/', '{bump "$/' + new_buffer_dir_name + '/'),
                    ('{specular "$/' + old_buffer_dir_name + '/', '{specular "$/' + new_buffer_dir_name + '/'),
                    ('{height "$/' + old_buffer_dir_name + '/', '{height "$/' + new_buffer_dir_name + '/'),
                    ('{mask "$/' + old_buffer_dir_name + '/', '{mask "$/' + new_buffer_dir_name + '/')]
    count = common.apply_function_to_files(file_applied.replace_str_in_file, [replacements], ".mtl", directory)
    printing.print_green('Count of processed texture files = ' + str(count))


def replace_buffer_dir_in_ebm(old_buffer_dir_name: str, new_buffer_dir_name: str, textures_directory: str, textures_sub_directory: str):
    '''Replaces buffer directory to .ebm references.'''
    
    # Combine paths
    directory = os.path.join(textures_directory, textures_sub_directory)
    # Check resulting path
    if not os.path.exists(directory):
        raise Exception('NO SUCH DIRECTORY: ' + directory)
    
    # Perform replacements
    replacements = [('{reference "$/' + old_buffer_dir_name + '/', '{reference "$/' + new_buffer_dir_name + '/')]
    count = common.apply_function_to_files(file_applied.replace_str_in_file, [replacements], ".ebm", directory)
    printing.print_green('Count of processed .ebm files = ' + str(count))


def add_def_files_prefix(prefix: str, directory: str):
    '''Adds specified prefix to .def files and updates 'structure' extender.'''
    
    count = common.apply_function_to_files(file_applied.filename_add_prefix, [prefix], '.def', directory)
    printing.print_green('Count of processed def files = ' + str(count))
    count = common.apply_function_to_files(file_applied.modify_structure_extender, [common.modify_structure_extender_add_prefix, [prefix]], '.def', directory)
    printing.print_green('Count of processed def files where extender was replaced = ' + str(count))
    printing.print_green('Count of backup files = ' + str(common.apply_function_to_files(file_applied.count_file, [], '.bak', directory)))
    common.apply_function_to_files(file_applied.backup_file, [], '.bak', directory)
    printing.print_green('Count of backup files after backup = ' + str(common.apply_function_to_files(file_applied.count_file, [], '.bak', directory)))


def replace_def_files_prefix(old_prefix: str, new_prefix: str, directory: str):
    '''Replaces specified prefix to .def files and updates 'structure' extender.'''
    
    count = common.apply_function_to_files(file_applied.filename_replace_prefix, [old_prefix, new_prefix], '.def', directory)
    printing.print_green('Count of processed def files = ' + str(count))
    count = common.apply_function_to_files(file_applied.modify_structure_extender, [common.modify_structure_extender_replace_prefix, [old_prefix, new_prefix]], '.def', directory)
    printing.print_green('Count of processed def files where extender was replaced = ' + str(count))
    printing.print_green('Count of backup files = ' + str(common.apply_function_to_files(file_applied.count_file, [], '.bak', directory)))
    common.apply_function_to_files(file_applied.backup_file, [], '.bak', directory)
    printing.print_green('Count of backup files after backup = ' + str(common.apply_function_to_files(file_applied.count_file, [], '.bak', directory)))


def validate_textures(textures_directory: str, textures_sub_directory: str, entities_directories: list):
    '''Prints list of unused and missing texture files.'''
    
    # Get texture files paths (without variations)
    present_texture_files = set(common.list_all_texture_files(textures_directory, textures_sub_directory, True))
    # Get used texture files paths (without variations) from .mtl files
    used_texture_files = []
    for entities_directory in entities_directories:
        common.apply_function_to_files(file_applied.get_mtl_texture_paths, [['diffuse', 'bump', 'specular', 'height', 'mask'], True, used_texture_files], '.mtl', entities_directory)
    used_texture_files = set(used_texture_files)
    
    # Construct missing files set
    missing_texture_files = used_texture_files - present_texture_files
    # Construct unused files set
    unused_texture_files = present_texture_files - used_texture_files
    
    # Print missing files (if present)
    if missing_texture_files:
        printing.print_yellow('FOUND MISSING TEXTURE FILES:')
        for missing_texture_file in sorted(missing_texture_files):
            print(missing_texture_file)
    else:
        printing.print_green('NO MISSING TEXTURE FILES WERE FOUND')
    # Print unused files (if present)
    if unused_texture_files:
        printing.print_yellow('FOUND UNUSED TEXTURE FILES:')
        for unused_texture_file in sorted(unused_texture_files):
            print(unused_texture_file)
        
        # Ask to delete unused files
        if common.query_yes_no('Remove unused textures?'):
            common.delete_unused_texture_files(textures_directory, textures_sub_directory, unused_texture_files)
    else:
        printing.print_green('NO UNUSED TEXTURE FILES WERE FOUND')