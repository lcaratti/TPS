init -1 python:
# ------------------------------------------------------------------------
# INJECTOR
# ------------------------------------------------------------------------  
    def rhythmize_string(speaker, text, full_dict, broken_flag):
# this function parses a text string adding text speed and pauses for punctuation. The parser itself is split into other
# functions so this is just a master that dispatches stuff to its messy minions =]
#
# args:
#       speaker --> the character ID (corresponding to a TPSCharacter's profile) whose dialogue or narration line belongs to
#       text --> the string to be parsed
#       full_dict --> the speaker's dictionary with the data required for proper pre-parsing
#       broken_flag --> flag informing the rhythmizer that the charactrer is in the broken state hence it must use the "broken" parser
#
# usage:
#       new_what = rhythmize_string(text,jitter_state,profile)
#
# returns:
#       function returns a string 

########################################################
# PRELIMINARIES: initialize variables, run some checks #
########################################################
#0) import globals
        global _TPS_PARSERS
# 1) not 100% sure Ren'Py is passing me a string instead of a tokenized array (renpy.text.text.whatever) - happened at least once so I make sure
# the input is a string                                                                                                                  
        text = str(text)

# 2) Initalize a few variables
        out = []
        i = 0
        effects = []

#############################################
# DEFINE WHICH BRANCH OF THE PARSER APPLIES #
#############################################
# 1) injects partser tags based on the value of the store.mode variable
        text = inject_persistent_mode(speaker, text)

        print("set_mode is: ",repr(store.mode))
        print("Line processed by the injector: ",repr(text))

# 2) check that the string is correctly formatted: the TPS parser can only accept 1 special parsing tag
# The broken state overrides special tags hence it'll only throw a warning message in the console
# having multiple tags without the broken state override will instead result in an error
        detect_multiple_parsing_tags(text,broken_flag)

# 3) selects the parser and retrieve the applicable data from the profile dict
        if broken_flag:
            parser_name = "broken"
            parser_data = full_dict
        else:
            parser_name = select_parser(text)
            parser_data = full_dict[parser_name]

        actual_parser = _TPS_PARSERS[parser_name]

# 4) launches the required parser

        return actual_parser(speaker,text,parser_data)