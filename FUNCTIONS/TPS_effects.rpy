# FUNCTIONS THE TPS INVOKES TO ADD SPECIAL EFFECTS such as sounds and/or anything
# I might came up with in the foreseeable future

init -1 python:
# ------------------------------------------------------------------------
# MASTER FUNCTION
# ------------------------------------------------------------------------
    def run_effects(effects):
# this function parses the effects list and then invokes one or more "slave" functions
# to create the required effect.
#
# args:
#       effects -> a list of effects
#
# usage:
#       $ run_effects(effects)
#
# returns:
#       None - unless playing an audio file or similar stuff can be considered an output...
        global _TPS_PARSING_EFFECTS

        if isinstance(effects,str):
            params = _TPS_PARSING_EFFECTS[effects]
            params["function"](*params["args"])
        else:
            for effect in effects:
                params = _TPS_PARSING_EFFECTS[effect]
                params["function"](*params["args"])
            
# ------------------------------------------------------------------------
# SLAVE FUNCTIONS
# ------------------------------------------------------------------------
    def play_sound_effect(audio_file):
# plays the provided audio file when invoked, using the dedicated TPS_sounds channel
#
# args:
#           audio_file -> path to the audio file required
#
# usage:
#           $ play_writing_effects(audio_file)
#
# returns:
#           None
        renpy.music.play(audio_file,channel="TPS_sounds")