# Custom modules
import lib.utils.printing as printing
import lib.utils.common as common
import lib.utils.file_applied as file_applied
import lib.files_managing as files_managing


##############
### Script ###
##############


# Directories setup
raven_construction_directory = r'C:\Games\Steam\steamapps\common\Call to Arms - Gates of Hell\mods\raven\resource\entity\construction\_raven'
cta_construction_directory = r'C:\Games\Steam\steamapps\common\Call to Arms - Gates of Hell\mods\raven\resource\entity\construction\_cta'
cta_landscape_directory = r'C:\Games\Steam\steamapps\common\Call to Arms - Gates of Hell\mods\raven\resource\entity\landscape\_cta'
inventory_directory = r'C:\Games\Steam\steamapps\common\Call to Arms - Gates of Hell\mods\raven\resource\entity\inventory'
textures_directory = r'C:\Games\Steam\steamapps\common\Call to Arms - Gates of Hell\mods\raven\resource\texture\common'
raven_textures_sub_directory = r'_raven'
cta_textures_sub_directory = r'_cta'

# If specified directories exist
dirs = [raven_construction_directory, cta_construction_directory,
        cta_landscape_directory, inventory_directory, textures_directory]
if common.validate_directories(dirs):
    printing.print_green('DIRECTORIES ARE VALID')
    
    # Validate Ravens textures
    files_managing.validate_textures(textures_directory, raven_textures_sub_directory,
                                     [raven_construction_directory, inventory_directory])
    # Validate CtA textures
    files_managing.validate_textures(textures_directory, cta_textures_sub_directory, [cta_construction_directory, cta_landscape_directory])
    
    # Count usage of .ext files
    #count = common.apply_function_to_files(file_applied.count_file_with_str, ['properties/cta_physics_wood.ext'], ".def",
    #                                       cta_construction_directory)
    #print(count)