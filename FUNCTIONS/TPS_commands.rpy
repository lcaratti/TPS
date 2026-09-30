# FUNCTIONS USER CALLS FROM WITHIN THE SCRIPT TO MODIFY A CHARACTER'S BEHAVIOUR
# things user will actually use within their script to make the system run

init -1 python:
# ------------------------------------------------------------------------
# COMMAND & CONTROL FUNCTIONS
# ------------------------------------------------------------------------
    def set_narrator(*args):
# this function assigns a character the role of the current narrator
#
# args:
#       *args --> can either be:
#               - a single value (char_id)
#               - two separated values (char_id,mood)
#               - four separated values (char_id,starting_mood,target_mood,transition_duration)
# usage:
#       $ set_mood(character) -> assigns a character the role of narrator and defaults them to their base profile
#       $ set_mood(character,mood) -> assigns a character the role of narrator and assigns the specific mood profile
#
# returns:
#       None. Function acts on store's variable

# update the TPS_characters_register entry about the narrator's profile

        TPS_characters_register["narr"] = TPS_characters_register[args[0]]

# reads the inputs and converts them into data that will be then fed to the TPS dicts for the narrator
        character,starting_mood,target_mood,transition = normalize_narrator_inputs(args)

        store.current_narrator = character 
        store.moods["start"]["narr"] = starting_mood
        store.moods["target"]["narr"] = target_mood
        store.transition_states["narr"] = transition


    def set_mood(*args,match=True):
# this function is called from inside the script to change the mood of a character
#
# args:
#       *args --> can either be:
#               - two separated values (char_id,mood) representing the character whose mood we have to change and the target mood. Transition is supposed to occur immediately
#               - three separated values (char_id,mood,lines) representing the character whose mood we have to change, the target mood, and the number of lines
#                 the transition is meant to take
#               - a SharedGroup object which declares a number of characters switching mood independently from each other
#               - a SharedGroup object where characters are grouped - and each group switches in unison (each character line influences that of other characters
#                 in the same group)
#       match --> if True, the function will align the mood of the narrator to that of the corresponding character.
#
# usage:
#       $ set_mood(character,mood,lines) -> changes mood for single character
#       $ set_mood (Sharedgroup) -> changes mood for multiple character, possibly grouping characters to share transition among multiple characters (each character influences the others in the same group)
#
# returns:
#       None. Function acts on store's variables

        global _group_id_counter

        groups = []
        characters = []
        
        if len(args) == 2 and isinstance(args[0], str):
            if _DEBUG:
# debugging step: prints a message in the console, telling which branch the function is taking
                print("Two arguments case - trying to set ",args[0],"'s mood as ",args[1]," with no transition")

            groups.append({
                'triplets': [(args[0], args[1], 0)],
                'shared': False
            })

        elif len(args) == 3 and isinstance(args[0], str):
            if _DEBUG:
# debugging step: prints a message in the console, telling which branch the function is taking
                print("Three arguments case - trying to set ",args[0],"'s mood as ",args[1]," with transition lasting ",args[2]," dialogue lines")
            groups.append({
                'triplets': [(args[0], args[1], args[2])],
                'shared': False
            })

        else:
            for arg in args:
                if isinstance(arg, SharedGroup):
                    if _DEBUG:
# debugging step: prints a message in the console, telling which branch the function is taking
                        print("SharedGroup detected")

                    groups.append({
                        'triplets': arg.triplets,
                        'shared': True
                    })

                elif isinstance(arg, tuple) and len(arg) >= 2:
                    if _DEBUG:
# debugging step: prints a message in the console, telling which branch the function is taking
                        print("Multiple independent character are being instanced at once")

                    if len(arg) ==2:
                        groups.append({
                            'triplets': [(arg[0],arg[1],0)],
                            'shared': False
                        })
                    else:
                        groups.append({
                            'triplets': [arg],
                            'shared': False
                        })


        for group_data in groups:
            triplets = group_data['triplets']
            is_shared = group_data['shared']
            if is_shared:
                _group_id_counter += 1
                group_id = _group_id_counter
            else:
                group_id = None

            for char,mood,lines in triplets:
                store.moods["start"][char] = store.moods["target"].get(char,"base")
                store.moods["target"][char] = mood

                characters.append(char)

                if mood == "broken":
                    reset_jitter_state(char)
                    store.transition_states[char] = [0,0]
                elif lines <= 1:
                    store.transition_states[char] = [0,0]
                else:
                    store.transition_states[char] = [0,lines]

                if is_shared:
                    store.shared_states[char] = group_id
                else:
                    store.shared_states[char] = None

        if match and store.current_narrator in characters:
            store.moods["target"]["narr"] = store.moods["target"][store.current_narrator]

    def reset_moods(*char_list,match=True):
# function that resets the mood of one or more characters back to their base state
#
# args:
#       char_list --> a list characters the function will process
#       match --> if True, the function will align the mood of the narrator to that of the corresponding character.
#
# usage:
#        $ reset_moods(["list_of_characters"],match)
#
# returns:
#       None. Function acts on store's variables
        for character in char_list:
            set_mood(character,"base",match=match)

    def set_mode(mode):
# simple function that modifies the store.presentation_mode param to initialize a persistent presentation mode.This way
# user doesn't have to put a parser tag at the beginning of each line when LOTS of line requires so.
#
# args:
#      mode --> the required presentation mode (ie. "speech","write", "chat")
#
# usage:
#      $ set_mode(mode)
#
# returns:
#       None. Function acts on store's variables
        store.mode = mode

    def reset_mode():
# simple function that resets the store.presentation_mode param to its default value (ie. "speech")
#
# args:
#       None
#
# usage:
#       $ reset_mode
#
# returns:
#       None. Function acts on store's variables
        store.mode = "speech"

    def start_monologue():
# function enabling NVL mode for a scene. Note this is acting on *all* characters involved in the scene ie. NVL mode will
# be used for all lines spoken by all characters that take part to the dialogue
#
# args:
#       None
#
# usage:
#       $ start_monologue()
#
# returns:
#       None. Function acts on store's variables
        store.presentation_mode = "nvl"

    def end_monologue():
# function that ends an NVL monologue and resumes standard ADV mode. Note this is acting on *all* characters involved in
# the scene ie. NVL mode will be used for all lines spoken by all characters that take part to the dialogue
#
# args:
#       None
#
# usage:
#       $ end_monologue()
#
# returns:
#       None. Function acts on store's variables
        store.presentation_mode = "adv"