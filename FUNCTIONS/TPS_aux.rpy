init -1 python:
# ------------------------------------------------------------------------
# AUXILIARY FUNCTIONS CENTRALIZING TEDIOUS ACTIVITIES...
# ------------------------------------------------------------------------
# function used for repetitive tasks and tools used in debugging

    def normalize_narrator_inputs(args):
        if not(args and args[0] in TPS_characters_register):
            print("Invalid call to set_narrator() - wrong character reference.")
            print ("Narrator was *not* changed!")
            return [store.current_narrator,store.moods["start"]["narr"],store.moods["target"]["narr"],store.transition_states["narr"]]

        character = args[0]

        if len(args) == 1:
            return [character,store.moods["start"][character],store.moods["target"][character],store.transition_states[character]]

        if len(args) == 2:
            if isinstance(args[1],str):
                return [character,args[1],args[1],[0,0]]
            
            print("Invalid call to set_narrator() - wrong character reference mood")
            print ("Narrator will be set to base mood!")
            return [character,"base","base",[0,0]]

        if len(args) == 3:
            print("Invalid call to set_narrator() - wrong number of inputs: function only accepts 1, 2 or 4 inputs!")
            if isinstance(args[2],str):
                print("Narrator's mood will be set to target mood")
            elif isinstance(args[1],str):
                print("Target mood is not a valid argument - narrator's mood will be set to starting mood")
            else:
                print("Starting and target moods are not valid arguments - narrator's mood will be set to base")

            mood = args[2] if isinstance(args[2],str) else args[1] if isinstance(args[1],str) else "base"
            return [character,mood,mood,[0,0]]

        if len(args) == 4:
            target = args[2] if isinstance(args[2],str) else args[1] if isinstance(args[1],str) else "base"
            start = args[1] if isinstance(args[1],str) else target
            transition = [0,args[3]] if isinstance(args[3],int) and target != start else [0,0]

            return [character,start,target,transition]

    def reset_jitter_state(char_id):
# Resets the jitter_state array for character
#
# args:
#       char_id --> the character id I'm resetting
#
# usage:
#       $ reset_jitter_state(char_id)
#
# returns:
#       None. Function acts on store's variables

        if char_id in jitter_states:
            create_jitter_state([char_id])

    def create_transitional_halo(old_text_color,new_text_color,old_halo,new_halo,t):        # WIP WIP WIP WIP #
# function that interpolates two halo dicts to create the intermediate state during a transition
#
# args:
#       old_text_color -> text color of the starting profile
#       new_text_color -> text color of the target profile
#       old_halo -> halo parameters of the starting profile
#       new_halo -> halo parameters of the target profile
#       t -> adimensional elapsed time since transition began
#
# usage:
#       transitional_halo = create_transitional_halo(old_halo,new_halo,old_text_color,new_text_color,t)
#
# returns:
#       Function returns a halo dictionary

# initialise the output dict
        out = {}
# just to make sure =3
        old_halo = old_halo or {}
        new_halo = new_halo or {}

#################################################################################################
# the first thing I do is, I build the database I will use to generate the transitional profile #
#################################################################################################
# blending params are either zero or the value from the dict
        if old_halo.get("blending",False):
            starting_blending = {
                                    "text_bleeds_into_glow": old_halo.get("blending",{}).get("text_bleeds_into_glow",0),
                                    "glow_bleeds_into_text": old_halo.get("blending",{}).get("glow_bleeds_into_text",0)
                                }
        else:
            starting_blending = {
                                    "text_bleeds_into_glow": 0.0,
                                    "glow_bleeds_into_text": 0.0
                                }
        if new_halo.get("blending",False):
            target_blending = {
                                    "text_bleeds_into_glow": new_halo.get("blending",{}).get("text_bleeds_into_glow",0),
                                    "glow_bleeds_into_text": new_halo.get("blending",{}).get("glow_bleeds_into_text",0)
                                }
        else:
            target_blending = {
                                    "text_bleeds_into_glow": 0.0,
                                    "glow_bleeds_into_text": 0.0
                                }

# glow gradient might be either representing a monochrome glow or an actual gradient so I must check how many colors have been put into the dict
        if old_halo.get("glow_gradient",False):
            if len(old_halo["glow_gradient"].get("colors",[])) == 1:
                starting_glow_gradient = {
                                            "colors": normalize_palette(old_halo["glow_gradient"].get("colors")),
                                            "frequencies": [0.0,0.0]
                                        }
            else:
                starting_glow_gradient = {
                                            "colors": normalize_palette(old_halo["glow_gradient"].get("colors")),
                                            "frequencies": radio_free_abermuth(old_halo["glow_gradient"].get("frequencies",None))
                                        }
        else:
            starting_glow_gradient = {
                                        "colors": ["#00000000","#00000000"],
                                        "frequencies": [0.0,0.0]
                                    }
        if new_halo.get("glow_gradient",False):
            if len(new_halo["glow_gradient"].get("colors",[])) == 1:
                target_glow_gradient = {
                                            "colors": normalize_palette(new_halo["glow_gradient"].get("colors")),
                                            "frequencies": [0.0,0.0]
                                        }
            else:
                target_glow_gradient = {
                                            "colors": normalize_palette(new_halo["glow_gradient"].get("colors")),
                                            "frequencies": radio_free_abermuth(new_halo["glow_gradient"].get("frequencies",None))
                                        }
        else:
            target_glow_gradient = {
                                        "colors": ["#00000000","#00000000"],
                                        "frequencies": [0.0,0.0]
                                    }
# text gradient may not exist at all - if it does, then it's complete. Otherwise text gradient uses text color
        if old_halo.get("text_gradient",False):
            starting_text_gradient = {
                                        "colors": normalize_palette(old_halo["text_gradient"].get("colors")),
                                        "frequencies": radio_free_abermuth(old_halo["text_gradient"].get("frequencies",None))
                                    }
        else:
            starting_text_gradient = {
                                        "colors": [old_text_color,old_text_color],
                                        "frequencies": [0.0,0.0]
                                    }
        if new_halo.get("text_gradient",False):
            target_text_gradient = {
                                        "colors": normalize_palette(new_halo["text_gradient"].get("colors")),
                                        "frequencies": radio_free_abermuth(new_halo["text_gradient"].get("frequencies",None))
                                    }
        else:
            target_text_gradient = {
                                        "colors": [new_text_color,new_text_color],
                                        "frequencies": [0.0,0.0]
                                    }

# glow decay must be always present and complete otherwise the glow itself won't work!
        if old_halo.get("glow_decay",False):
            starting_glow_decay = old_halo.get("glow_decay")
        else:
            starting_glow_decay = {
                                        "radius": 0,
                                        "sigma": 0.0
                                }
        if new_halo.get("glow_decay",False):
            target_glow_decay = new_halo.get("glow_decay")
        else:
            target_glow_decay = {
                                        "radius": 0,
                                        "sigma": 0.0
                                }

# text decay might not exist - if it does, then it's complete
        if old_halo.get("text_decay",False):
            starting_text_decay = old_halo.get("text_decay")
        else:
            starting_text_decay = {
                                        "radius": 0,
                                        "sigma": 0.0,
                                }
        if new_halo.get("text_decay",False):
            target_text_decay = new_halo.get("text_decay")
        else:
            target_text_decay = {
                                        "radius": 0,
                                        "sigma": 0.0,
                                }

#############################################################################
# now that all data is ready, interpolating betweem them is a piece of cake #
#############################################################################
        out = {
                "type": "transitional",
                "blending": {
                                "text_bleeds_into_glow": interp_float(starting_blending["text_bleeds_into_glow"],target_blending["text_bleeds_into_glow"],t),
                                "glow_bleeds_into_text": interp_float(starting_blending["glow_bleeds_into_text"],target_blending["glow_bleeds_into_text"],t)
                            },
                "glow_gradient": {
                                    "colors": [interp_hex(starting_glow_gradient["colors"][0],target_glow_gradient["colors"][0],t),interp_hex(starting_glow_gradient["colors"][1],target_glow_gradient["colors"][1],t)],
                                    "frequencies": [interp_float(starting_glow_gradient["frequencies"][0],target_glow_gradient["frequencies"][0],t),interp_float(starting_glow_gradient["frequencies"][1],target_glow_gradient["frequencies"][1],t)]
                                },
                "text_gradient": {
                                    "colors": [interp_hex(starting_text_gradient["colors"][0],target_text_gradient["colors"][0],t),interp_hex(starting_text_gradient["colors"][1],target_text_gradient["colors"][1],t)],
                                    "frequencies": [interp_float(starting_text_gradient["frequencies"][0],target_text_gradient["frequencies"][0],t),interp_float(starting_text_gradient["frequencies"][1],target_text_gradient["frequencies"][1],t)]
                                },
                "glow_decay": {
                                    "radius": interp_int(starting_glow_decay["radius"],target_glow_decay["radius"],t),
                                    "sigma": interp_float(starting_glow_decay["sigma"],target_glow_decay["sigma"],t)
                                },
                "text_decay": {
                                    "radius": interp_int(starting_text_decay["radius"],target_text_decay["radius"],t),
                                    "sigma": interp_float(starting_text_decay["sigma"],target_text_decay["sigma"],t),
                            }
        }
        return out

    def normalize_palette(colors):
# small helper function that returns the appropriate gradient palette depending on what's been put into the "colors" attribute of a halo dictionary
#
# args:
#        colors -> can either be:
#                        - None if author broke something
#                        - a string (ie. "#ff0000ff")
#                        - a list with just one item (ie. ["#ff0000ff"]) if author did something wrong
#                        - a list with two items (ie. ["#ff0000ff","#00ff00ff"]) if author is applying a gradient
#
# usage:
#        colors_array = normalize_palette(colors)
#
# returns:
#        function returns a list with two items, ready for use within the shader tag builder (or the transitional profile generator)

        if colors is None:
            return ["#00000000","#00000000"]
        elif isinstance(colors,str):
            return [colors,colors]
        elif len(colors) == 1:
            return [colors[0],colors[0]]
        elif len(colors) == 2:
            return colors
        else:
            raise Exception("Invalid palette: {}".format(colors))

    def radio_free_abermuth(frequencies):
# small helper function that returns the appropriate "frequency depending on what's been put into the "frequencies" attribute of a halo dictionary.
# note it returns numbers ie. it already enters the frequencies database and randomly chooses one.
#
# args:
#        frequencies -> can either be:
#                        - None if author broke something
#                        - a single string (ie. "slow")
#                        - a list with just one item (ie. ["slow"]) if author did something wrong
#                        - a list with two items (ie. ["slow,"fast"]) if author is applying a gradient
#
# usage:
#        frequencies_array = radio_free_abermuth(frequencies)
#
# returns:
#        function returns a list with two frequencies for use into TheOneShader

        if frequencies is None:
            return [0.0,0.0]
        elif isinstance(frequencies,str):
            resolved_freq_1 = random.choice(_PSYCHO_SHADER_FREQUENCIES.get(frequencies,"static"))
        elif isinstance(frequencies,float):
            resolved_freq_1 = frequencies
        elif len(frequencies) >= 1:
            if isinstance(frequencies[0],str):
                resolved_freq_1 = random.choice(_PSYCHO_SHADER_FREQUENCIES.get(frequencies[0],"static"))
            else:
                resolved_freq_1 = frequencies[0]
        if len(frequencies) == 2:
            if isinstance(frequencies[1],str):
                resolved_freq_2 = random.choice(_PSYCHO_SHADER_FREQUENCIES.get(frequencies[1],"static"))
            else:
                resolved_freq_2 = frequencies[1]
        else:
            resolved_freq_2 = 0.0
        return [resolved_freq_1,resolved_freq_2]

##### THIS FUNCTION IS CURRENTLY NOT BEING USED - KEEPING IT 'CAUSE YOU NEVER KNOW...
    def pimp_my_alpha(color,alpha):
# this function takes a color and changes its alpha to the value input by user
#
# args:
#       color -> the color whose alpha I want to change
#       alpha -> the alpha value I want to apply. Must be assigned as an INT between 0 and 255
#
# usage:
#       alpha_color = pimp_my_alpha(color,alpha)
#
# returns:
#       Function returns a color in the #RRGGBBAA format. Will return an error if the input color is not valid
        
        alpha_hex = f"{alpha:02x}"
        color = color.lstrip("#")
        
        if len(color) == 6:
            return f"#{color}{alpha_hex}"
        elif len(color) == 8:
            return f"#{color[:6]}{alpha_hex}"
        else:
            raise ValueError(f"Invalid color: #{color}")

    def build_shader_tag(shader_data):
# function that detects which kind of shader I want to use and builds the shader tag accordingly
#
# args:
#       shader_data-> a dict with all the information required to build the tag
#
# usage:
#       tag = build_shader_tag(shader_data)
#
# returns:
#       function returns the tag (without {})

# halo dict might be incomplete - merely because the required shader configuration does not need things such
# as a glow gradient, a text bloom expanding into the background glow, etc.
# the first thing I do is, I complete the dict with the missing data:
        shader_data_blending = shader_data.get("blending", {})
        shader_data_glow_gradient = shader_data.get("glow_gradient", {})
        shader_data_text_gradient = shader_data.get("text_gradient", {})
        shader_data_glow_decay = shader_data.get("glow_decay", {})
        shader_data_text_decay = shader_data.get("text_decay", {})
        shader_data = {
                "type": shader_data.get("type","nomen nescio"),
                "blending": {
                                "text_bleeds_into_glow": shader_data_blending.get("text_bleeds_into_glow",0.0),
                                "glow_bleeds_into_text": shader_data_blending.get("glow_bleeds_into_text",0.0)
                            },
                "glow_gradient": {
                                    "colors": normalize_palette(shader_data_glow_gradient.get("colors",None)),
                                    "frequencies": radio_free_abermuth(shader_data_glow_gradient.get("frequencies",None))
                                },
                "text_gradient": {
                                    "colors": normalize_palette(shader_data_text_gradient.get("colors",None)),
                                    "frequencies": radio_free_abermuth(shader_data_text_gradient.get("frequencies",None))
                                },
                "glow_decay": {
                                    "radius": shader_data_glow_decay.get("radius",0),
                                    "sigma": shader_data_glow_decay.get("sigma",0.0)
                                },
                "text_decay": {
                                    "radius": shader_data_text_decay.get("radius",0),
                                    "sigma": shader_data_text_decay.get("sigma",0.0),
                            }
        }


# assigns values to each shader param
        u__text_f1,u__text_f2 = shader_data["text_gradient"]["frequencies"]
        u__glow_f1,u__glow_f2 = shader_data["glow_gradient"]["frequencies"]
        u__text_col1,u__text_col2 = shader_data["text_gradient"]["colors"]
        u__glow_col1,u__glow_col2 = shader_data["glow_gradient"]["colors"]
        u__text_radius = shader_data["text_decay"]["radius"]
        u__text_sigma = shader_data["text_decay"]["sigma"]
        u__glow_radius = shader_data["glow_decay"]["radius"]
        u__glow_sigma = shader_data["glow_decay"]["sigma"]
        u__glow_bleeds_into_text = shader_data["blending"]["glow_bleeds_into_text"]
        u__text_bleeds_into_glow = shader_data["blending"]["text_bleeds_into_glow"]

# I build the shader like this otherwise it's 100% guaranteed I'll skip a ":" XD
        shader_parts = [
                        "TheOneShader",
                        f"u__text_f1={u__text_f1}",
                        f"u__text_f2={u__text_f2}",
                        f"u__glow_f1={u__glow_f1}",
                        f"u__glow_f2={u__glow_f2}",
                        f"u__text_col1={u__text_col1}",
                        f"u__text_col2={u__text_col2}",
                        f"u__glow_col1={u__glow_col1}",
                        f"u__glow_col2={u__glow_col2}",
                        f"u__text_radius={u__text_radius}",
                        f"u__text_sigma={u__text_sigma}",
                        f"u__glow_radius={u__glow_radius}",
                        f"u__glow_sigma={u__glow_sigma}",
                        f"u__glow_bleeds_into_text={u__glow_bleeds_into_text}",
                        f"u__text_bleeds_into_glow={u__text_bleeds_into_glow}"
                        ]

        print(u__glow_col1)
        print(u__glow_col2)
        print(u__glow_radius)
        print(u__glow_sigma)
        print(u__glow_bleeds_into_text)
        return ":".join(shader_parts)

    def merge_shaders(*shaders):
# helper function used to concatenate shaders together so that I can apply more than one at once
#
# args:
#        *shaders -> one or more shaders
#
# usage:
#        shader_tag_contet = merge_shaders(shader_1,shader_2,...)
#
# returns:
#        Function returns a string that can be passed to a f"{{{shader_tag_content}}}" command
        shaders = [s for s in shaders if s]

        if not shaders:
            return ""

        return "shader=" + "|".join(shaders)

# ------------------------------------------------------------------------
# STUFF I USE FOR DEBUGGING
# ------------------------------------------------------------------------
    def validate_tags(text, ctx=60):
# debugging function that checks that all tags are properly closed
#
# args:
#       text --> the string to be checked
#       ctx --> lenght of the context (ie. characters displayed in case an exception is raised). Default is 60.
#
# usage:
#       validate_tags(text,ctx)
#
# returns:
#       None
        if not isinstance(text, str):
            raise Exception(f"validate_tags received non-str: {type(text)}")

        stack = []
        length = len(text)

        for i, ch in enumerate(text):
            if ch == "{":
                stack.append(i)

            elif ch == "}":
                if not stack:
                    start = max(0, i - ctx)
                    end = min(length, i + ctx)
                    raise Exception(
                        "UNMATCHED '}'\n"
                        f"Index: {i}\n"
                        f"Context:\n{text[start:end]!r}\n"
                        f"Full text:\n{text!r}"
                    )
                stack.pop()

        if stack:
            i = stack[-1]
            start = max(0, i - ctx)
            end = min(length, i + ctx)
            raise Exception(
                "UNMATCHED '{'\n"
                f"Index: {i}\n"
                f"Context:\n{text[start:end]!r}\n"
                f"Full text:\n{text!r}"
            )

    def check_keys_match(d):
# helper function that checks that all pauses dictionaries are correctly set for every key in the master default_pauses
        return d is not None and set(d.keys()) == set(store.default_pauses.keys())
