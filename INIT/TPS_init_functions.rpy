init -99 python:
    def initialize_TPS():
# master function initializing the TPS. Runs early at init time and generates the dicts required by the
# TPS to work properly
#
# args:
#       None
#
# usage:
#       initialize_TPS()
#
# returns:
#       None
        global _TPS_DATA_SKELETON

        TPS_data_checkin(_TPS_DATA_SKELETON)
        TPS_narrator_checkin()

    def TPS_data_checkin(init_data,namespace=store):
# Initializes the dicts required by the TPS to work properly
#
# args:
#       init_data --> a list of variables that require initializing
#       namespace --> the namespace where the variables will be initialized. Default is store
#
# usage:
#       TPS_data_checkin(init_data,namespace)
#
# returns:
#       None
        for key,value in init_data.items():
            if not hasattr(namespace,key):
                setattr(namespace,key,value)

    def TPS_narrator_checkin(profile="generic",namespace=store):
# Initializes the narrator as a generic profile, instancing all required variables in the TPS dicts
#
# args:
#       namespace --> the namespace where TPS variables are stored. Default is store
#
# usage:
#       TPS_narrator_checkin(namespace)
#
# returns:
#       None
        name = "narr"

        getattr(namespace,"TPS_characters_register").setdefault(name,profile)
        getattr(namespace,"moods")["start"].setdefault(name,"base")
        getattr(namespace,"moods")["target"].setdefault(name,"base")
        getattr(namespace,"transition_states").setdefault(name,[0,0])
        getattr(namespace,"jitter_states").setdefault(name,{group: 0 for group in [*_JITTER_GROUPS.keys(),"cps"]})
        getattr(namespace,"shared_states").setdefault(name,None)

    def TPS_character_checkin(TPS_Character,namespace=store):
# Initializes character-related subs inside certain dicts required by the TPS to work properly
#
# args:
#       namespace --> the namespace where TPS variables are stored. Default is store
#       TPSCharacter --> the TPSCharacter object with the data that have to be initialized
#
# usage:
#       TPS_characters_checkin(TPSCharacter)
#
# returns:
#       None
        global _JITTER_GROUPS
        name = TPS_Character.nick
        profile = TPS_Character.profile

        getattr(namespace,"TPS_characters_register").setdefault(name,profile)
        getattr(namespace,"moods")["start"].setdefault(name,"base")
        getattr(namespace,"moods")["target"].setdefault(name,"base")
        getattr(namespace,"transition_states").setdefault(name,[0,0])
        getattr(namespace,"jitter_states").setdefault(name,{group: 0 for group in [*_JITTER_GROUPS.keys(),"cps"]})
        getattr(namespace,"shared_states").setdefault(name,None)

    def TPS_charprofiles_checkin(namespace=store):
# Performs start-up checks on characters' profile dictionaries
#
# args:
#       TPSCharacter --> the TPSCharacter object with the data that have to be initialized
#
# usage:
#       TPS_charprofiles_checkin(namespace)
#
# returns:
#       None
        global _DEFAULT_PROFILE
        
        for default_mood,default_profile in _DEFAULT_PROFILE.items():
            variable_font_check(default_mood,default_profile)

        for character,profile in character_profiles.items():
            for mood,mood_params in profile.items():
                variable_font_check(mood,mood_params)

    def variable_font_check(mood,profile):
        if mood not in ["broken","default_broken_params"]:
            if profile.get("speech",False) and profile["speech"].get("modifiers",False) and len(profile["speech"]["modifiers"].keys()) > 0:
                for modifier in profile["speech"]["modifiers"].values():
                    if "font" in modifier.keys() and "path" in modifier["font"].keys():
                        font = modifier["font"]["path"]
                        if renpy.variable_font_info(font) is not None:
                            modifier["font"]["variable"] = True
                        else:
                            modifier["font"]["variable"] = False
        else:
            if profile.get("modifiers",False) and profile["modifiers"].get("font",False) and profile["modifiers"]["font"].get("path",False) and isinstance(profile["modifiers"]["font"]["path"],str):
                font = profile["modifiers"]["font"]["path"]
                if renpy.variable_font_info(font) is not None:
                    profile["modifiers"]["font"]["variable"] = True
                else:
                    profile["modifiers"]["font"]["variable"] = False

        if profile.get("write",False) and profile["write"].get("modifiers",False) and profile["write"]["modifiers"].get("font",False) and profile["write"]["modifiers"]["font"].get("path",False):
            font = profile["write"]["modifiers"]["font"]["path"]
            if renpy.variable_font_info(font) is not None:
                profile["write"]["modifiers"]["font"]["variable"] = True
            else:
                profile["write"]["modifiers"]["font"]["variable"] = False

        if profile.get("chat",False) and profile["chat"].get("modifiers",False) and profile["chat"]["modifiers"].get("font",False) and profile["chat"]["modifiers"]["font"].get("path",False):
            font = profile["chat"]["modifiers"]["font"]["path"]
            if renpy.variable_font_info(font) is not None:
                profile["chat"]["modifiers"]["font"]["variable"] = True
            else:
                profile["chat"]["modifiers"]["font"]["variable"] = False