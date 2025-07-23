import os
import shutil


def main(**kwargs):
    directory_absolute = kwargs["directory_absolute"]
    details = kwargs["details"]
    deets_order = ["classification", "type", "size", "color", "description_main", "description_extra", "manufacturer", "part_number"]
    deets = {}
    if details != None:
        for deet in deets_order:
            if deet in details:
                deets[deet] = details[deet]
        
        # check whether to run
        matches_type = []
        matches_type.append("screw_countersunk")
        matches_type.append("screw_flat_head")
        matches_type.append("screw_socket_cap")        
        matches_type.append("screw_self_tapping")        
        matches_type.append("screw_thread_forming")
        matches_type.append("bolt")
        matches_type.append("set_screw")
        matches_type.append("spacer")
        matches_type.append("standoff")

        typ = deets["type"]
        run = False
        for match in matches_type:
            if match in typ:
                run = True

        if run:
            #print(f"    generating for {directory_absolute}")
            details = get_name_screw(details, deets, directory_absolute)        
            details = get_md5_split(details, deets)
            return details


def get_md5_split(details, deets):
    md5_6 = details["md5_6"]
    md5_6_first_3 = md5_6[0:3]
    details["oomlout_bolt_md5_6_first_3"] = md5_6_first_3
    details["oomlout_bolt_md5_6_first_3_upper"] = md5_6_first_3.upper()
    md5_6_last_3 = md5_6[3:]
    details["oomlout_bolt_md5_6_last_3"] = md5_6_last_3
    details["oomlout_bolt_md5_6_last_3_upper"] = md5_6_last_3.upper()
    #now for md5_6 alpha
    md5_6_alpha = details["md5_6_alpha"]
    md5_6_alpha_first_3 = md5_6_alpha[0:3]
    details["oomlout_bolt_md5_6_alpha_first_3"] = md5_6_alpha_first_3
    details["oomlout_bolt_md5_6_alpha_first_3_upper"] = md5_6_alpha_first_3.upper()
    md5_6_alpha_last_3 = md5_6_alpha[3:]
    details["oomlout_bolt_md5_6_alpha_last_3"] = md5_6_alpha_last_3
    details["oomlout_bolt_md5_6_alpha_last_3_upper"] = md5_6_alpha_last_3.upper()    
    return details




def get_name_screw(details, deets, directory_absolute):

    oomlout_bolt_name = ""

    # get the type
    typ_source = deets["type"]
    typ_matches = []
    typ_matches.append(["screw_countersunk","Countersunk"])
    typ_matches.append(["screw_flat_head","Flat Head"])
    typ_matches.append(["screw_machine_screw","Machine Screw"])
    typ_matches.append(["screw_socket_cap","Socket Cap"])
    typ_matches.append(["screw_self_tapping","Self Tapping"])
    typ_matches.append(["screw_thread_forming","Thread Forming"])

    
    
    
    typ_matches.append(["bolt","Bolt"])
    typ_matches.append(["set_screw","Set Screw"])
    typ_matches.append(["spacer","Spacer"])
    typ =""
    for match in typ_matches:
        if match[0] in typ_source:
            typ = match[1]
    details["oomlout_bolt_type"] = typ    
    # file copy
    file_base = os.path.dirname(__file__)
    file_source = f"template/type_diagram_{typ_source}.png"    
    file_source = os.path.join(file_base, file_source)
    file_destination = os.path.join(directory_absolute, "type_diagram.png")
    if os.path.exists(file_source):
        details["oomlout_bolt_type_diagram_diagram"] = "type_diagram.png"
        if os.path.exists(file_destination):
            os.remove(file_destination)
        #print(f"    copying {file_source} to {file_destination}")
        shutil.copyfile(file_source, file_destination)
    else:
        print(f"    {file_source} not found")

    # get the size
    size_source = deets["size"]
    size = ""
    if typ_source == "spacer":
        size = size_source.replace("_id_","X")
        size = size.replace("_mm_od","")
        size = f"{size}".upper()
        details["oomlout_bolt_size_long"] = size
        details["oomlout_bolt_size"] = ""
    #if size_source starts with an m and the next charachter is a digit
    elif size_source.startswith("m") and size_source[1].isdigit():
        size = size_source.replace("_mm","")
        size = f"{size}".upper()
        #if size is longer than 2 characters
        if len(size) > 2:
            details["oomlout_bolt_size"] = ""
            details["oomlout_bolt_size_long"] = size.replace("_",".")
        else:
            details["oomlout_bolt_size"] = size

    # get the color
    color_source = deets["color"]
    color_matches = []
    color_matches.append(["black","Black"])
    color_matches.append(["stainless","Stainless"])
    color = ""
    for match in color_matches:
        if match[0] in color_source:
            color = match[1]
    details["oomlout_bolt_color"] = color

    # get the length
    length_source = deets["description_main"]
    length = ""
    if "_mm" in length_source:
        length = length_source.replace("_mm_length","").replace("_mm","")
        length = f"{length} mm"
    details["oomlout_bolt_length"] = length
    details["oomlout_bolt_length_no_unit"] = length.replace(" mm","")

    # head_type
    head_type_source = deets["description_extra"]    
    head_type_matches = []
    head_type_matches.append(["flat_head","Flat"])
    head_type_matches.append(["phillips_head","Phillips"])
    head_type_matches.append(["pozidrive_head","Pozidrive"])
    head_type_matches.append(["hex_head","Hex Head"])
    head_type_matches.append(["set_screw","Hex"])
    head_type_matches.append(["bolt","Hex"])
    head_type = "Bolt"
    for match in head_type_matches:
        if match[0] in head_type_source:
            head_type = match[1]
    details["oomlout_bolt_head_type"] = head_type
    
    ## copy file
    file_base = os.path.dirname(__file__)
    file_source = f"template/head_type_diagram_{head_type_source}.png"    
    file_source = os.path.join(file_base, file_source)
    file_destination = os.path.join(directory_absolute, "head_type_diagram.png")
    #print(f"    copying {file_source} to {file_destination}")
    if os.path.exists(file_source):
        details["oomlout_bolt_head_type_diagram"] = "head_type_diagram.png"
        if os.path.exists(file_destination):
            os.remove(file_destination)
        shutil.copyfile(file_source, file_destination)
    else:
        print(f"    {file_source} not found")

    oomlout_bolt_name = f"{typ} {size}X{length} {color} ({head_type})"
    details["oomlout_bolt_name"] = oomlout_bolt_name    
    


    return details