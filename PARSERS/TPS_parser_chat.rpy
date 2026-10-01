init -2 python:
    def rhythmize_chat(speaker,text,parser_data):
# parser processing script lines flagged with the {chat} tag
#
# args:
#           speaker -> the reference charID of the speaker the script line belongs to
#           text -> the script line
#           parser_data -> subset of the character's TPS Dictionary with the information required to properly
#                          process the text
#
# usage:
#           parsed_line = rhythmize_chat(speaker,text,parser_data)
#
# return:
#           function returns the script line properly parsed with the addition of all necessary stylizing and
#           rhythm tags, and a list of special effects the master parser will make happen when passing everything
#           back to the original Ren'Py pipeline

        starting_pause,total_time,text = parse_chat_tags(text)
                                                                                                          
        text = remove_custom_tags(text)
        output = []

        is_slow = random.random() <= parser_data["cps"]["slowdown"]["slow_start"]

        opening_tags,closing_tags = generate_nonbroken_tags(parser_data,"chat",is_slow)

        output.append("".join(opening_tags))

        if renpy.is_skipping() or persistent.dynamic_text_speed == 2:
            output.append(text)
            output.append("".join(closing_tags))
            return output

# if the speaker is not the narrator, then the reader does not get to see the message being tapped "real-time". They
# just see the "Typing..." screen and then the message pops up all at once
        if speaker != "narr":
            if starting_pause is not None:
                renpy.pause(starting_pause)
            if total_time is not None:
                if timeline > 0:
                    timeline = timeline_from_fixed(text,total_time,parser_data["pauses"])
                else:
                    output.append(text)
                    output.append("".join(closing_tags))
                    output.append(f"{{fast}}")
                    return output
            else:
                timeline = timeline_from_typing(text,parser_data,is_slow)

            speaker_char_obj = TPS_characters_register[speaker]
            store.typing_who = renpy.substitute(speaker_char_obj.name)
            store.typing_who_args = dict(getattr(speaker_char_obj,"who_args",{}))

            for index,chunk in enumerate(timeline):
                if index % 2 == 0:
                    renpy.show_screen(typing(speaker_char_obj))
                else:
                    renpy.hide_screen(typing)
    
                renpy.pause(chunk)
            
            renpy.hide_screen(typing)

            output.append(text)
            output.append("".join(closing_tags))
            output.append(f"{{fast}}")
            return output

# if the speaker is the narrator, then the message gets typed into the textbox and gets rhythmized properly, as if
# it was dialogue line - only, pauses do not follow punctuation but are scattered across the text, and cps varies
# between "fast" and "slow" tapping.
        i = 0
        if is_slow:
            clock,trigger = 0,random.randint(*parser_data["pauses"]["slow_interval"])
        else:
            clock,trigger = 0,random.randint(*parser_data["pauses"]["interval"])

        while i < len(text):
            character = text[i]

            if character == "{":                                                   # finds tag, preserves it
                end = text.find("}",i)
                if end == -1:
                    output.append(character)
                    i += 1
                else:
                    output.append(text[i:end+1])
                    i = end + 1
                continue

            if text.startswith("...",i):                                    # finds ellipsis, consider it as single character
                output.append("...")
                i += 3
                if not parser_data["pauses_chat"]["ignore_punctuation"]:
                    clock += 1
                continue

            if character in punct.map.keys():                               # finds punctuation mark
                i += 1
                output.append(character)
                if not parser_data["pauses_chat"]["ignore_punctuation"]:
                    clock += 1
                continue

            if character in " \n\t":                                        # finds space, new-line, or tab
                i += 1
                output.append(character)
                continue

            if clock >= trigger:
                if character not in " \n\t":
                    cps_switch_chance = parser_data["cps"]["slow_chance_midword"]
                else:
                    cps_switch_chance = parser_data["cps"]["slow_chance"]

                actual_pause = calculate_nonspeech_pause(parser_data["pauses"])

                if is_slow:
                    cps_switch = random.random() > cps_switch_chance
                else:
                    cps_switch = random.random() <= cps_switch_chance

                if cps_switch:
                    is_slow = not is_slow
                    output.append(f"{{/cps}}")
        
                    this_chunk_cps = calculate_cps_multiplier(parser_data["cps"],"write",is_slow)

                    output.append(f"{{w={actual_pause}}}{{cps=*{this_chunk_cps}}}{character}")
                else:
                    output.append(f"{{w={actual_pause}}}{character}")
            
                if is_slow:
                    clock,trigger = 0,random.randint(*parser_data["pauses"]["slow_interval"])
                else:
                    clock,trigger = 0,random.randint(*parser_data["pauses"]["interval"])
                i += 1
            else:
                output.append(f"{character}")
                clock +=1
                i +=1
            
        output.append("".join(closing_tags))

        return parser_data["modifiers"]["effects"],"".join(output)
