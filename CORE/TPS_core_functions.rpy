init -1 python:
    def check_TPS_applicability(what,kwargs):
# function that detects all cases where the TPS should not apply.
#
# args:
#       what --> the original what string to be parsed
#
# usage:
#       clean_what = check_TPS_applicability(what)
#
# returns:
#       function returns None if the TPS can be used, otherwise ti returns the "cleaned" string (ie. a string cleared
#       of all TPS custom tags) that is then sent to the original export.say().

        if not isinstance(what,str):                        # what is not a string
            return remove_custom_tags(what)
        if renpy.predicting():                              # Ren'Py is predicting
            return remove_custom_tags(what)
        if not persistent.dynamic_text_speed:               # user disabled the TPS
            return remove_custom_tags(what) 
        if kwargs.get("_rhythmic"):                         # string has been already parsed by the TPS
            return what
        if "{norhythm}" in str(what):                       # user applied the special {norhythm} tag
            return remove_custom_tags(what)

        return None                                         # all other conditions not met - use the TPS

    def resolve_who(who,presentation_mode="adv"):
# helper function that resolves the TPSCharacter object by returning the character's name, its TPS profile, and the
# Character "kind" corresponding to the actual presentation mode (ADV or NVL). If the character is not a TPSCharacter
# object, they're taken as a standard Ren'Py character and treated consequently
#
# args:
#       who -> a TPSCharacter object
#       presentation_mode -> the way the speaker's text should be presented on-screen (adv or nvl). Default is adv
#
# usage:
#       char_name,char_profile,char_who = resolve_who(who,presentation_mode)
#
# returns:
#       Function returns three parameters:
#           - the character's name
#           - their TPS profile
#           - a standard Ren'Py Character object (ADVCharacter or NVLCharacter)

        if who is None:
            who = getattr(store,"narrator",None)

        if isinstance(who,TPSCharacter):
            return resolve_TPSCharacter(who,presentation_mode)
        else:
            return resolve_RenpyCharacter(who)

    def resolve_TPSCharacter(who,presentation_mode):
        resolved_name = "narr" if who.nick is None else who.nick
        
        if resolved_name == "narr":
            resolved_profile = TPS_characters_register[store.current_narrator] if store.current_narrator in TPS_characters_register else "generic"
        else:
            resolved_profile = TPS_characters_register[resolved_name] if resolved_name in TPS_characters_register else "generic"

        resolved_char_obj = getattr(who,presentation_mode)

        return resolved_name,resolved_profile,resolved_char_obj

    def resolve_RenpyCharacter(who):
        resolved_name = "narr" if who is None else who.name

        return resolved_name,"generic",who

    def reset_after_transition(char):
# simple helper function that updates a character's TPS state (mood and transition state) once a transition has ended
#
# args:
#       char -> a TPSCharacter reference tag
#
# usage:
#       $ reset_after_transition(char)
#
# returns:
#       None. Function acts on state variables

        if store.moods["start"][char] != store.moods["target"][char]:
            store.moods["start"][char] = store.moods["target"][char]
        if store.transition_states[char] != [0,0]:
            store.transition_states[char] = [0,0]

    def update_transition_state(char,start_dict,target_dict,step):
# helper function calculating the profile for the n-th step of a transition and updating the transition state of a character.
# If multiple characters are provided, the function updates the state of every character provided, but only calculates
# one profile
#
# args:
#           char -> a TPSCharacter reference tag or a list of TPSCharacter reference tags
#           start_dict -> the profile dict that applied before transition started
#           target_dict -> the profile dict that will apply once transition ends
#           step -> transition's adimensional time
#
# usage:
#           $ actual_profile = update_transition_state(char,start_dict,target_dict,step)
#
# returns:
#           Function returns a TPS profile dict. Function also increases a char's transition state

        actual_profile = interpolate_dicts(start_dict,target_dict,step)

        if isinstance(char,str):
            if not renpy.in_rollback():
                store.transition_states[char][0] += 1
        else:
            for single_char in char:
                if store.transition_states[single_char] != [0,0]:
                    store.transition_states[single_char][0] += 1
        
        return actual_profile

    def find_speaker(who):
# simple helper function that retrieves the speaker based on the who Ren'Py throws at the renpy.exports.say
#
# args:
#       who --> the character actually speaking. Can be a character object or None
#
# usage:
#       speaker = find_speaker(who)
#
# returns:
#       function returns a string corresponding to the speaker
        if who == None:
            return getattr(narrator,"profile","generic")
        
        return(getattr(who,"profile","generic"))

    def fetch_profile(lookup_char_id,mood):
# function that generates the mood profile for the TPS - data that's not explicitly input in the character's mood profile
# is taken from the default profile dict
#
# args:
#        lookup_char_id --> the TPSCharacter's char_ID corresponding to a character_profiles' dictionary key
#        mood --> the specific mood the function should look for into the dictionary
#
# usage:
#       profile = fetch_profile(lookup_char_id,mood)
#
# returns:
#       function returns the dict specific for that character/mood combo

        char_dict = store.character_profiles.get(lookup_char_id,store.character_profiles.get("generic",_DEFAULT_PROFILE))

        if mood == "broken":
            default_dict = _DEFAULT_PROFILE["default_broken_params"]
            target = char_dict.get("broken",default_dict)
        else:
            default_dict = _DEFAULT_PROFILE["default_base_params"]
            target = char_dict.get(mood,char_dict.get("base", default_dict))

        return complete_profile(target, default_dict)

    def complete_profile(target,source):
# completes a mood profile by extracting all missing data from the default dictionary
#
# args:
#        target --> the dictionary I want to complete (will work on a copy to avoid overwriting the original dict - I know, might be paranoia. Still...)
#        source --> the  sub-section in the default dictionary that'll act as a source to compile empty fields
#
# usage:
#       completed_profile = complete_profile(target,source):
#
# returns:
#       function returns a complete dict for a TPS mood profile

        out = target.copy()

        for key, value in source.items():
            if key not in out:
                out[key] = value
            elif isinstance(value,dict) and isinstance(out[key],dict):
                out[key] = complete_profile(out[key],value)

        return out

    def interpolate_dicts(start_dict,target_dict,t,path=()):
# helper function that interpolates corresponding values of two dicts. The dicts must have the same identical
# structure
#
# args:
#       start_dict --> starting dict. At t=0 the function will return start_dict
#       target_dict --> final dict. At t=1 the function will return target_dict
#       t --> non-dimensional time in the [0,1] indicating where we are along the interpolation axis
#       path --> records the single keys the parser had to go through while searching the store.characters_profile dabatase
#
# usage:
#       profile = interpolate_dicts(start_dict,target_dict,t)
#
# returns:
#       a dict() with the interpolated values for each relevant field

        if _DEBUG:
# debugging step: check on which step we are and shows it on the console
            print("== TRANSITIONING - We're ",t*100,"%% done!")

# initialize the output dict
        output_dict = {}


        for key,value in start_dict.items():
            updated_path = path + (key,)


            if should_stop_recursion(updated_path):
                output_dict[key] = interpolate_jitter(start_dict[key],target_dict[key],t,updated_path)
            elif isinstance(value,dict):
                output_dict[key] = interpolate_dicts(start_dict[key],target_dict[key],t,updated_path)
            else:
                output_dict[key] = interpolate_values(start_dict[key],target_dict[key],t,updated_path)

        return output_dict

    def should_stop_recursion(path):
# small helper function that prevents the interpolate_dicts() function from interpolating pauses jitter dicts
#
# args:
#           path -> the list of keys the interpolate_dicts() recursive function has investigated so far
#
# usage:
#           should_stop_recursion(path)
#
# returns:
#           Fucntion returns True if the recursion should stop; False otherwise
        if path[-2:] == ("cps","jitter"):
            return True
        if len(path) >=3 and path[-3:-1] == ("pauses","jitter") and path[-1] in ("strong","weak","ellipsis"):
            return True

        return False

    def interpolate_jitter(start,target,t,path):
# helper function that interpolates jitter states as follows:
#     cps and "strong" punctuation marks keep behaving accoding to the starting profile, and gets updated only at the end of
#     the transition
#     "ellispses" switch immediately to the target behaviour
#     "weak" punctuation marks switch around mid-transition
#
# args:
#       start --> jitter parameters of the starting profile
#       target --> jitter parameters of the target profile
#       t --> adimensional transition time
#       path --> the list of keys the interpolate_dicts() recursive function has investigated so far
#
# usage:
#       jitter_dict = interpolate_jitter(start,target,t,path)
#
# returns:
#       function returns the jitter sub-dictionary used by the transitional profile
        if path[-2:] == ("cps","jitter") or path[-1] == "strong":
            return target if t >= 1 else start
        if path[-1] == "ellipsis":
            return target
        if path[-1] == "weak":
            return target if t > 0.5 else start
            
    def interpolate_values(val_1,val_2,t,path):
# this function actually is just a dispatcher - depending on the inputs' types it'll call a different interpolating function
#
# args:
#       val_1 -> first value (typically that of the starting profile)
#       val_2 -> second value (typically that of the target profile)
#       t --> adimensional transition time
#       path --> the list of keys the interpolate_dicts() recursive function has investigated so far
#
# usage:
#       interpolated_value = interpolate_values(val_1,val_2,t)
#
# returns:
#       function returns a variable the same type as val_1 and val_2
        if isinstance(val_1,(int,float)) and isinstance(val_2,(int,float)):
            return interp_numbers(val_1,val_2,t)
        elif isinstance(val_1,str) or isinstance (val_2,str):
            return interp_strings(val_1,val_2,t,path)
        else:
            return interp_bools(val_1,val_2,t,path)

    def interp_bools(val_1,val_2,t,path):
# small function that returns the correct boolean value for specific fields in the transitional dictionary.
# also takes care of pretty much every variable not covered by other functions - it's my "litter bin" interpolator XD
#
# args:
#       val_1 -> first value (typically that of the starting profile)
#       val_2 -> second value (typically that of the target profile)
#       t --> adimensional transition time
#       path --> the list of keys the interpolate_dicts() recursive function has investigated so far
#
# usage:
#       interpolated_bool = interp_bools(val_1,val_2,t,path)
#
# returns:
#       function returns a value the same type of val_1 and val_2
        if path[-2] == "anxiety":
            return val_1 or val_2
        elif path[-1] == "halo":
            return None
        elif path[-1] == "variable":
            if t <= 0.5:
                return val_1
            else:
                return val_2
        else:
            return val_1 if t <= 0.5 else val_2

    def interp_numbers(val_1,val_2,t):
# dispatcher discrimating between ints and floats.
#
# args:
#       val_1 -> first value (typically that of the starting profile)
#       val_2 -> second value (typically that of the target profile)
#       t --> adimensional transition time
#
# usage:
#       interpolated_value = interp_numbers(val_1,val_2,t)
#
# returns:
#       function returns an INT of both val_1 and val_2 are INTs; FLOAT otherwise
        if isinstance(val_1,float) or isinstance(val_2,float):
            return interp_float(val_1,val_2,t)
        else:
            return interp_int(val_1,val_2,t)


    def interp_strings(val_1,val_2,t,path):
# dispatcher discriminating different fields in the dictionary and calling the correct interpolating
# function - applies to string type params
#
# args:
#       val_1 -> first value (typically that of the starting profile)
#       val_2 -> second value (typically that of the target profile)
#       t --> adimensional transition time
#       path --> the list of keys the interpolate_dicts() recursive function has investigated so far

# usage:
#       interpolated_string = interp_numbers(val_1,val_2,t)
#
# returns:
#       function returns a string
        if path[-1] == "col":
            return interp_hex(val_1,val_2,t)
        elif path[-1] == "style":
            return interp_tags(val_1,val_2,t)
        elif path[-1] == "path":
            if t <= 0.5:
                return val_1
            else:
                return val_2

    def interp_int(old,new,t,up_or_down="up"):
# simple helper function that interpolates between two numbers and returns the nearest INT.
#
# args:
#       old --> starting value
#       new --> target value
#       t --> non-dimensional parameter that states where we are in the transition - ie. step / number_of_steps
#       up_or_down = establishes whether "halfies" should be rounded up or down - default is up so for instance 20.5 is rounded as 21
#
# usage:
#       $ value = interp_int(old,new,t,up_or_down="up")
#
# returns:
#       Function returns an INT
        if up_or_down == "up":
            return math.floor(.5 + old + (new - old) * t)
        else:
            return math.ceil(-.5 + old + (new - old) * t)

    def interp_float(old,new,t,precision = 3):
# simple helper function that interpolates between two numbers and returns the nearest floating point number
#
# args:
#       old --> starting value
#       new --> target value
#       t --> non-dimensional parameter that states where we are in the transition - ie. step / number_of_steps
#       precision --> number of decimals the result will keep. Default is 3
#
# usage:
#       $ value = interp_float(old,new,t,precision=3)
#
# returns:
#       Function returns a FLOAT
        return round(old + (new - old) * t,precision)

    def interp_tags(old,new,t):
# helper function that returns an array with the text style tags for the transient profile. It does so with
# the following logic:
# - b: bold. This is considered as the most "conscious" tag therefore it appears last (if present in the target
#      profile) or disappears first (if present in the starting profile)
# - i: italic. This is considered as the most "unconscious" tag therefore it appears first (if present in the target
#      profile) or disappears last (if present in the starting profile)
# - s: strike-through. This is considered as an "almost-conscious" tag therefore it appears around 66% transition time
#      (if present in the target profile) or disappears around 33% transition time (if present in the starting profile)
# - u: underline. This is considered as an "almost-unconscious" tag therefore it appears around 33% transition time
#      (if present in the target profile) or disappears around 66% transition time (if present in the starting profile)
#
# args:
#       old --> list of style tags that apply to the old profile
#       new --> list of style tags that apply to the target profile
#       t --> non-dimensional parameter that states where we are in the transition - ie. step / number_of_steps
#
# usage:
#       $ value = interp_float(old,new,t,precision=3)
#
# returns:
#       Function returns an array of tags to be applied to text

        if isinstance(old,str):
            old = list(old)
        if isinstance(new,str):
            new = list(new)

        output = []

# tagging logic for bold tag
        if ("b" in new and t > 0) or ("b" in old and t <= 0):
            output.append("b")

# tagging logic for italic tag
        if ("i" in new and t < 1) or ("i" in old and t >= 1):
            output.append("i")

# tagging logic for underline tag
        if ("u" in new and t <= 0.66) or ("u" in old and t >= 0.33):
            output.append("u")

# tagging logic for strikethrough tag
        if ("s" in new and t <= 0.33) or ("s" in old and t >= 0.66):
            output.append("s")     
    
        return output

    def interp_hex(old,new,t):
# helper function interpolating between two colors and returning the intermediate hex code
#
# args:
#       old --> starting color
#       new --> target color
#       t --> non-dimensional parameter that states where we are in the transition - ie. step / number_of_steps
#
# usage:
#       $ interpolated_color = interp_float(old,new,t,)
#
# returns:
#       Function returns a hex color code that includes alpha (ie. "#xxxxxxxx")

        def hex_to_rgb(color):
    # internal method converting a hex color code string into their red, green, and blue components
            stripped_color = color.lstrip("#")
            if len(stripped_color) == 6:
                stripped_color += "FF"
            return (int(stripped_color[0:2], 16),int(stripped_color[2:4], 16),int(stripped_color[4:6], 16),int(stripped_color[6:8], 16))

        r1,g1,b1,a1 = hex_to_rgb(old)
        r2,g2,b2,a2 = hex_to_rgb(new)

        r_int = interp_int(r1,r2,t)
        g_int = interp_int(g1,g2,t)
        b_int = interp_int(b1,b2,t)
        a_int = interp_int(a1,a2,t)

        def rgb_to_hex(r,g,b,a):
    # internal method converting three INT values to the corresponding hex color code
            return "#{:02x}{:02x}{:02x}{:02x}".format(r,g,b,a)

        return rgb_to_hex(r_int,g_int,b_int,a_int)