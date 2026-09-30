init -1 python:
    def select_parser(text):
# simple helper function that tells the master dispatcher which parser to use. Works with "write", "speech", and "chat" parsers.
# Parser for broken state gets a different treatment as it's not a property of the script line but rather it's character-specific (ie.
# it's a special "mood" for the character).
#
# args:
#           text -> the script line
#
# usage:
#           parser_to_be_used = select_parser(speaker,text,parser_data)
#
# return:
#           function returns a string corresponding to the key the dispatcher will then use to find the correct parsers in the parsers dict.
        global _TPS_PARSING_TAGS

        for key,parser_ref in _TPS_PARSING_TAGS.items():
            if key in text:
                return parser_ref
        return "speech"

    def inject_persistent_mode(speaker,text):
# function that adds a specific text production mode (speech, write, chat) to each and every line depending on the value of the value of store.mode.
# automatically skips {speech} tag and forces speech mode for each and avery modifier tag (as they belong to speech mode alone).
        global _TPS_PARSING_TAGS,_TPS_MODIFIER_TAGS

        if text.startswith("{speech}") or any(text.startswith(tag) for tag in _TPS_MODIFIER_TAGS):
            print("Skipping because I found {speech} or a modifier tag")
            return text

        if store.mode in (None, "speech"):
            print("Skipping because store.mode is not defined (",repr(store.mode))
            return text

        for mode_tag, key in _TPS_PARSING_TAGS.items():
            print("I'm looking for ",repr(key))
            if store.mode == key:
                if text.startswith(mode_tag):
                    print("Skipping because the text already has the correct parsing tag (",repr(mode_tag))
                    return text
                if store.mode == "chat" and speaker == "narr":
                    print("Skipping because we're chatting but the narrator's speaking")
                    return text
                print("Returning ",repr(mode_tag+text))
                return mode_tag+text

        return text

    def detect_multiple_parsing_tags(text,is_broken):
# debug function checking that a string is not built with multiple tags in it (for instance, {chat} and {write} at the same time). If character
# is in the broken state, it overrides any other tag.
#
# args:
#           text -> the script line
#           is_broken -> special flag to tell the function whether the character is in the broken state or not
#
# usage:
#           detect_multiple_parsing_tags(text, parsing_tags,is_broken)
#
# return:
#           None. Function will throw a warning message is one or more flags are detected in the broken state; it will throw an error if multiple
#           tags are detected in a normal mood state.
        global _TPS_PARSING_TAGS

        detected = [tag for tag in _TPS_PARSING_TAGS.keys() if tag in text]

        if len(detected) > 0 and is_broken:
            print("Character's broken state is ",flag," but the following special parsing tags were input:")
            print(detected)
            print("Special parsing tags will be ignored as the broken state overrides them.")
            if len(detected) > 1:
                print("!!WARNING!! String has ",len(detected)," special parsing tags while the TPS can only accept 1. Check your code thoroughly.")
        elif len(detected) > 1:
            raise ValueError(f"TPS can only accept 1 parsing tag, {len(detected)} tags found: {detected}")

    def dict_section_selector(speaker,text,full_dict):
# simple helper function that extract the part of a dict required to properly parse the dialogue line
#
#           speaker -> the reference charID of the speaker the script line belongs to
#           text -> the script line
#           full_dict -> the complete dict for a specific character mood
#
# usage:
#           relevant_dict = dict_section_selector(speaker,text,full_dict)
#
# return:
#           function returns a dict with the information required to parse the dialogue line given the current character's mood and
#           tags found in the dialogue line
        if full_dict.get("broken",False):
            return text,full_dict["broken"]
        elif "{write}" in text:
            return text.replace("{write}",""),full_dict["write_modifiers"]
        elif "{chat" in text:
            return text,full_dict["chat_modifiers"]
            
