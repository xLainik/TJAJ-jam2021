import json, os

with open(os.path.join("scr", "config", "options.json"), "r", encoding="utf-8") as options_json_file:
    options = json.load(options_json_file)

with open(os.path.join("scr", "config", "colours.json"), "r") as colours_json_file:
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
