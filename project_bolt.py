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
        matches_type.append("screw_socket_cap")
        matches_type.append("screw_countersunk")
        matches_type.append("screw_flat_head")
        matches_type.append("bolt")
        matches_type.append("set_screw")
        matches_type.append("spacer")

        typ = deets["type"]
        run = False
        for match in matches_type:
            if match in typ:
                run = True

        if run:
            print(f"    generating for {directory_absolute}")
            details = get_name_screw(details, deets, directory_absolute)        
            return details


def get_filenames(details, deets):

    return details


def get_name_screw(details, deets, directory_absolute):

    oomlout_bolt_name = ""

    # get the type
    typ_source = deets["type"]
    typ_matches = []
    typ_matches.append(["screw_machine_screw","Machine Screw"])
    typ_matches.append(["screw_socket_cap","Socket Cap"])
    typ_matches.append(["screw_countersunk","Countersunk"])
    typ_matches.append(["screw_flat_head","Flat Head"])
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
        print(f"    copying {file_source} to {file_destination}")
        shutil.copyfile(file_source, file_destination)
    else:
        print(f"    {file_source} not found")

    # get the size
    size_source = deets["size"]
    size = ""
    if "_mm_id" in size_source:
        size = size_source.replace("_mm_id_","X")
        size = size.replace("_mm_od","")
        size = f"M{size}"
        details["oomlout_bolt_size_long"] = size
    elif "_mm" in size_source:
        size = size_source.replace("_mm","")
        size = f"M{size}"
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
        length = length_source.replace("_mm","")
        length = f"{length} mm"
    details["oomlout_bolt_length"] = length
    details["oomlout_bolt_length_no_unit"] = length.replace(" mm","")

    # head_type
    head_type_source = deets["description_extra"]    
    head_type_matches = []
    head_type_matches.append(["flat_head","Flat"])
    head_type_matches.append(["phillips_head","Phillips"])
    head_type_matches.append(["pozidrive_head","Pozidrive"])
    head_type_matches.append(["hex_head","Hex"])
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
    print(f"    copying {file_source} to {file_destination}")
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