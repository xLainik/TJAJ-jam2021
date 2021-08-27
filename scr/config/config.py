import json, os

with open(os.path.join("scr", "config", "options.json"), "r", encoding="utf-8") as options_json_file:
    options = json.load(options_json_file)

with open(os.path.join("scr", "config", "colours.json"), "r", encoding="utf-8") as colours_json_file:
    colours = json.load(colours_json_file)

    for colour in colours:
        # Check for errors in the JSON file.
        if type(colours[colour]) != list:
            raise TypeError(f"In {colour}: should be a list when in JSON form.")
        if len(colours[colour]) != 3:
            raise ValueError(f"In {colour}: list should have 3 values")
        for number in colours[colour]:
            if number > 255:
                raise ValueError(f"In {colour}: {number} is to high in order to display an RGB value. Must be between 0 and 255.")
            if number < 0:
                raise ValueError(f"In {colour}: {number} is to low in order to display an RGB value. Must be between 0 and 255.")
        
        # Make all the lists with RGB values into tuples.
        colours[colour] = tuple(colours[colour])

levels = []
for lvl_number, level in enumerate(os.listdir(os.path.join("scr", "levels"))):
    dump = []
    with open(os.path.join("scr", "levels", level, "level_" + str(lvl_number) + ".json"), "r", encoding="utf-8") as level_json_file:
        dump.append(json.load(level_json_file))
    dialogs = {}
    for dialog_num, dialog_queue in enumerate(os.listdir(os.path.join("scr", "levels", level, "level_" + str(lvl_number) + "_dialogs"))):
        with open(os.path.join("scr", "levels", level, "level_" + str(lvl_number) + "_dialogs", "dialog_" + str(dialog_num) + ".json"), "r", encoding="utf-8") as dialog_json_file:
            dialogs["dialog_" + str(dialog_num)] = json.load(dialog_json_file)
    dump.append(dialogs)
    levels.append(dump)
        
with open(os.path.join("scr", "config", "tiles_color_keys.json"), "r", encoding="utf-8") as tiles_color_keys_json_file:
    tiles_color_keys = json.load(tiles_color_keys_json_file)

    for tile in tiles_color_keys:
        # Make all the lists with RGB values into tuples.
        tiles_color_keys[tile] = tuple(tiles_color_keys[tile])

with open(os.path.join("scr", "config", "entities_color_keys.json"), "r", encoding="utf-8") as entities_color_keys_json_file:
    entities_color_keys = json.load(entities_color_keys_json_file)

    for entity in entities_color_keys:
        # Make all the lists with RGB values into tuples.
        entities_color_keys[entity] = tuple(entities_color_keys[entity])
