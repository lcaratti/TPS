init -2 python:
# ------------------------------------------------------------------------
# PARSER FOR "BROKEN" CASE
# ------------------------------------------------------------------------  
    def rhythmize_broken(speaker,text,parser_data):
# parser processing script lines whenever a character is in the "broken" state
#
# args:
#           speaker -> the reference charID of the speaker the script line belongs to
#           text -> the script line
#           parser_data -> subset of the character's TPS Dictionary with the information required to properly
#                          process the text
#
# usage:
#           parsed_line = rhythmize_broken(speaker,text,parser_data)
#
# return:
#           function returns the script line properly parsed with the addition of all necessary stylizing and
#           rhythm tags, and a list of special effects the master parser will make happen when passing everything
#           back to the original Ren'Py pipeline

        text = remove_custom_tags(text)
        output = []

        opening_tags,closing_tags = generate_broken_tags(parser_data)

        output.append("".join(opening_tags))

        if renpy.is_skipping() or persistent.dynamic_text_speed == 2:
            output.append(text)
            output.append("".join(closing_tags))
            return output

        i = 0
        clock,trigger = 0,random.randint(*parser_data["pauses"]["trigger_interval"])

        while i < len(text):
            character = text[i]

            if character == "{":                                           # finds tag, preserve it
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
                if not parser_data["ignore_punctuation"]:
                    clock += 1
                continue

            if character in punct.map.keys():                               # finds punctuation mark
                i += 1
                output.append(character)
                if not parser_data["ignore_punctuation"]:
                    clock += 1
                continue

            if character in " \n\t":                                        # finds space, new-line, or tab
                i += 1
                output.append(character)
                continue

            if clock >= trigger and character not in " \n\t":
                output.append("".join(closing_tags))
                if "weighted_pauses" in parser_data:
                    pauses = list(parser_data["weighted_pauses"].keys())
                    weights = list(parser_data["weighted_pauses"].values())
                    actual_pause = random.choices(pauses,weights=weights,k=1)[0]
                else:
                    actual_pause = random.uniform(*parser_data["random_pauses"])
                output.append(f"{{w={actual_pause}}}")
                opening_tags,closing_tags = generate_broken_tags(parser_data)
                output.append("".join(opening_tags))
# introduces stuttering when text speed changes
                if random.random() > parser_data["stutter_likelihood"]:
                    i +=1
                trigger = 0,random.randint(*parser_data["trigger_interval"])
            else:
                output.append(f"{character}")
                clock +=1
                i +=1
            
            output.append("".join(closing_tags))
            return None,"".join(output)