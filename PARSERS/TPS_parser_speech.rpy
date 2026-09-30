init -2 python:
    def rhythmize_speech(speaker,text,parser_data):
# parser processing script lines un-tagged script lines
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

        actual_modifier = detect_modifier(speaker,text)

        text = remove_custom_tags(text)
        output = []
        
        opening_tags,closing_tags = generate_nonbroken_tags(speaker,parser_data,actual_modifier)

        output.append("".join(opening_tags))

        if renpy.is_skipping() or persistent.dynamic_text_speed == 2:
            output.append(text)
            output.append("".join(closing_tags))
            return None,"".join(output)

        i = 0
        how_much_anxious = False

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

            if character in store.punct_map.keys():
                if text.startswith("...", i):
                    this_mark = "..."
                else:
                    this_mark = character

                this_mark_name = store.punct_map[this_mark]
                this_mark_pause = calculate_pause(speaker,parser_data["pauses"],this_mark_name)

                if text.startswith("...", i):
                    for val in parser_data["pauses"]["jitter"]["ellipsis"].get("split",[1,1,1]):
                        ell_pause = this_mark_pause * val / sum(parser_data["pauses"]["jitter"]["ellipsis"].get("split",[1,1,1]))
                        output.append(".")
                        output.append(f"{{w={ell_pause}}}")
                else:
                        output.append(character)
                        output.append(f"{{w={this_mark_pause}}}")

                if parser_data["cps"]["anxiety"]["active"]:
                    how_much_anxious = anxiety_check(how_much_anxious,this_mark_name,this_mark_pause,parser_data)
                if how_much_anxious:
                    output.append(f"{{/cps}}")
                    this_chunk_cps = calculate_cps_multiplier(speaker,parser_data,actual_modifier,is_slow=False,anxiety = how_much_anxious)
                    output.append(f"{{cps=*{this_chunk_cps}}}")
                if text.startswith("...", i):
                    i += 3
                else:
                    i += 1
            else:
                output.append(character)
                i += 1

        output.append("".join(closing_tags))
        return parser_data["modifiers"][actual_modifier]["effects"],"".join(output)





