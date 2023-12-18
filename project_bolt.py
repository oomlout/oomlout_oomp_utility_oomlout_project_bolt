


def main(details):
    deets_order = ["classification", "type", "size", "color", "description_main", "description_extra", "manufacturer", "part_number"]
    deets = {}
    for deet in deets_order:
        if deet in details:
            deets[deet] = details[deet]
    
    # check whether to run
    matches_type = []
    matches_type.append("screw_socket_cap")

    typ = deets["type"]
    run = False
    for match in matches_type:
        if match in typ:
            run = True

    if run:
        details = get_name(details, deets)
        details = get_filenames(details, deets)

    return details


def get_filenames(details, deets):

    return details


def get_name(details, deets):

    oomlout_bolt_name = ""

    # get the type
    typ_source = deets["type"]
    typ_matches = []
    typ_matches.append(["screw_socket_cap","Socket Cap"])
    typ_matches.append(["screw_countersunk","Countersunk"])
    typ_matches.append(["bolt","Bolt"])
    typ_matches.append(["set_screw","Set Screw"])
    typ =""
    for match in typ_matches:
        if match[0] in typ_source:
            typ = match[1]
    details["oomlout_bolt_type"] = typ

    # get the size
    size_source = deets["size"]
    size = ""
    if "_mm" in size_source:
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

    # head_type
    head_type_source = deets["description_extra"]    
    head_type_matches = []
    head_type_matches.append(["flat_head","Flat"])
    head_type_matches.append(["phillips_head","Phillips"])
    head_type_matches.append(["hex_head","Hex"])
    head_type = ""
    for match in head_type_matches:
        if match[0] in head_type_source:
            head_type = match[1]
    details["oomlout_bolt_head_type"] = head_type

    oomlout_bolt_name = f"{typ} {size}X{length} {color} ({head_type})"
    details["oomlout_bolt_name"] = oomlout_bolt_name    
    


    return details