init -10 python:
# store the original exports.say so that I can use it elsewhere without breaking stuff (too much =P)
    original_say = renpy.exports.say

init -1 python:
# ------------------------------------------------------------------------
# MASTER FUNCTION REPLACING THE BASE RENPY's SAY
# ------------------------------------------------------------------------  
    def TPS_say(who, what, *args, **kwargs):
# Bypasses Ren'Py's basic say() to add character-based pauses in dialogue lines, and then forwards the result
# back into the original Ren'Py say() function
#
# args:
#       who --> the character who's actually speaking
#       what --> what the character is saying
#                note: these two items basically are the who "what" of every single statement in the script!
#       *args and **kwargs --> optional arguments - do NOT touch them unless you really know what you're doing ;D
#                              **** added because the original say() has them (--> found in sayexports.py)
# usage:
#       this function is invoked auto-magically because I force
#           renpy.exports.say = rhythmic_say
#       no need to call it anywhere ;D
#
# returns:
#       None
#       function calls back the original renpy.exports.say and injects everything back into Ren'Py's pipeline

##########################################################################################################
# PRELIMINARIES: resolve the speaking character and detect all cases where the TPS should not be applied #
##########################################################################################################
        char_name,char_profile,char_obj = resolve_who(who,store.presentation_mode)

        clean_what = check_TPS_applicability(what,kwargs)

        if clean_what != None:
            return original_say(char_obj,clean_what,*args,**kwargs)

# debugging step: printing speaker's data
        if _DEBUG:
            print("==== TPS LOOKUP ====")
            print("Ren'Py who =", repr(who))
            print("Current speaker is ", char_name, " (could as well be the narrator, \"narr\")")
            print("His character profile is ", char_profile)

# 2) retrieve character's mood (which will be used to fetch the correct sub in the character's profiles dict)
        mood = {}

        mood["start"] = store.moods["start"].get(char_name,"base")
        mood["target"] = store.moods["target"].get(char_name,"base")

        profile = {}
        is_broken = False
        for key,specific_mood in mood.items():
            profile[key] = fetch_profile(char_profile,specific_mood)

#######################################################################
# THIS SECTION DEALS WITH TRANSITION BETWEEN FDIFFERENT MOOD PROFILES #
#######################################################################

# 1) retrieve information regarding transition of a character across two different mood states
# !!! "broken" state does not accept transitions !!!
        if "broken" in (mood["start"], mood["target"]):
            elapsed = 0
            total = 0
            if mood["target"] == "broken":
                is_broken = True
        else:
            elapsed = store.transition_states.get(char_name,[0,0])[0]       # how many lines have passed since transition started
            total = store.transition_states.get(char_name,[0,0])[1]         # how many lines the transition is supposed to take

# debugging step: prints data related to the mood profiles the TPS is about to use
        if _DEBUG:
            if total > 1 and elapsed < total:
                print("target profile =", mood["target"])
                print("starting profile =", mood["start"])
                print("now on step ",elapsed," out of ",total)
            else:
                print("No transition occurring. Character already in their final mood state - ",mood["target"])

# 2) if a character belongs to a SharedGroup, retrieve the group's ID number
        group = store.shared_states.get(char_name)

        if _DEBUG:
# debugging step: print whether a character belongs to a group or not
            if group is not None:
                print("Character ",repr(char_name)," resolved as ",repr(char_profile)," belongs to SharedGroup #",repr(group))
            else:
                print("Character ",repr(char_name)," resolved as ",repr(char_profile)," does not belong to any SharedGroup")

# 3) builds profile for a character not belonging to a SharedGroup & update transition parameters                                                                                                                          
        if group is None:
            if total > 0 and elapsed < total:                                                        # transition occurring, update transitional profile
                step = (elapsed+1) / (total+1)
                actual_profile = update_transition_state(char_name,profile["start"],profile["target"],step)
            else:                                                                                   # transition complete, resets transitional profiles database
                reset_after_transition(char_name)
                actual_profile = profile["target"]

        else:
# 4) builds profile for a character in a SharedGroup & updates shared transition parameters
            members = [char for char,grp in store.shared_states.items() if grp == group]
            if total > 0 and elapsed < total:
                step = (elapsed+1) / (total+1)
                actual_profile = update_transition_state(members,profile["start"],profile["target"],step)
            else:
                reset_after_transition(char_name)
                actual_profile = profile["target"] 

            # this checks group status - has everybody ended their transition?    
            grp_transition_complete = True
            for char in members:
                char_elapsed,char_total = store.transition_states.get(char,[0,0])
                if char_total > 0 and char_elapsed < char_total:
                    grp_transition_complete = False
                else:
                    reset_after_transition(char)

            if grp_transition_complete:
                reset_shared_states(members)

# 4) applies rhythm to the "what" string and retrieves special effects
        effects, new_what = rhythmize_string(char_name, what, actual_profile, is_broken)

        if _DEBUG:
# debugging step: the validate_tags() function checks the modified dialogue line for broken tags
            validate_tags(new_what)
            print("RHYTHMIZED STRING: ",repr(new_what))
        
# 5) applies special effects
        if effects != None:
            if _DEBUG:
                print(effects)
            run_effects(effects)

# 6) applies special effects
        return original_say(char_obj, new_what, *args, _rhythmic=True, **kwargs)
