import os
import yaml
import glob

folder_configuration = "configuration"
folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)
file_configuration = os.path.join(folder_configuration, "configuration.yaml")
#check if exists
if not os.path.exists(file_configuration):
    print(f"no configuration.yaml found in {folder_configuration} using default")
    file_configuration = os.path.join(folder_configuration, "configuration_default.yaml")



#import configuration
configuration = {}
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)


def main(**kwargs):
    folder = kwargs.get("folder", f"{os.path.dirname(__file__)}/parts")
    folder = folder.replace("\\","/")
    
    kwargs["configuration"] = configuration
    print(f"running utility oomlout_oomp_utiltiy_project_bolt for: {folder}")
    create_recursive(**kwargs)

def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    #if folder exists
    filter = kwargs.get("filter", "")
    if os.path.exists(folder):        
        count = 0
        for item in os.listdir(folder):
            if filter in item:
                directory_absolute = os.path.join(folder, item)
                directory_absolute = directory_absolute.replace("\\","/")
                if os.path.isdir(directory_absolute):
                    #if working.yaml exists in the folder
                    if os.path.exists(os.path.join(directory_absolute, "working.yaml")):
                        kwargs["directory_absolute"] = directory_absolute
                        create(**kwargs)
                        count += 1
                        if count > 100:
                            print(f"{count} parts processed")
    else:
        print(f"no folder found at {folder}")

def create(**kwargs):
    directory_absolute = kwargs.get("directory_absolute", os.getcwd())    
    kwargs["directory_absolute"] = directory_absolute    
    generate(**kwargs)
    

def generate(**kwargs):    
    directory_absolute = kwargs.get("directory_absolute", os.getcwd())
    kwargs["directory_absolute"] = directory_absolute
    folder = kwargs.get("folder", os.getcwd())
    yaml_file = os.path.join(directory_absolute, "working.yaml")
    kwargs["yaml_file"] = yaml_file
    #load the yaml file
    details = {}
    with open(yaml_file, 'r') as stream:
        try:
            details = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:   
            print(exc)
    kwargs["details"] = details

    if details != {}:                
        #import from this folder
        # impotoomp_word from this files directory even if that isn't the cwd
        import sys
        sys.path.append(os.path.dirname(__file__))
        import project_bolt
        
        ##### process part here
        details = project_bolt.main(**kwargs)



        
        if details != None:
            #write back to yaml file
            with open(yaml_file, 'w') as outfile:
                yaml.dump(details, outfile, default_flow_style=False)
        else:   
            pass
        print(".", end="")
        


    else:
        print(f"no yaml file found in {directory_absolute}")    



if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    #folder = "C:/gh/oomlout_oobb_version_4/things"
    #folder = "C:/gh/oomlout_oomp_current_version"
    kwargs["folder"] = folder
    overwrite = False
    kwargs["overwrite"] = overwrite
    main(**kwargs)