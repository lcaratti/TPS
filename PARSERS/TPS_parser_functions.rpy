init -2 python:
# ------------------------------------------------------------------------
# FUNCTIONS USED BY THE "BROKEN" PARSER
# ------------------------------------------------------------------------  
    def generate_broken_tags(parser_data):
# function generating opening and closing style tags for the "broken" parser
#
# args:
#       parser_data --> source dictionary with all information about style and text speed
#
# returns:
#       Function returns the list of opening and closing tags in the correct order as to avoid errors
#       due to wrong tag opening/closing order
        opening_tags = []
        closing_tags = []

        size = random.randint(*parser_data["modifiers"]["size"])
        if parser_data["modifiers"]["font"]["variable"]:
            font = parser_data["modifiers"]["font"]["path"]
            font_weight = random.randint(*parser_data["modifiers"]["font"]["weight"])
        else:
            font = random.choice(*parser_data["modifiers"]["font"]["path"])
            font_weight = None
        alpha = round(random.uniform(*parser_data["modifiers"]["col"]) * 255)
        color = f"#ffffff{alpha:02x}"
        shader = parser_data["modifiers"]["shader"]

        cps_multiplier = calculate_cps_multiplier(parser_data["cps"],"broken")

        if size > 0:
            opening_tags.append(f"{{size=+{size}}}")
        elif size < 0:
            opening_tags.append(f"{{size=-{abs(size)}}}")
        if font != gui.text_font:
            opening_tags.append(f"{{font={font}}}")
        if font_weight is not None and font_weight != gui.text_axis["weight"]:
            opening_tags.append(f"{{axis:width={font_weight}}}")
        if color != None:
            opening_tags.append(f"{{color={color}}}")
# cps should always be the last tag to open and the first to be closed
        opening_tags.append(f"{{cps=*{cps_multiplier}}}")
        closing_tags.append("{/cps}")

        if color != None:
            closing_tags.append("{/color}")
        if font_weight is not None and font_weight != gui.text_axis["weight"]:
            closing_tags.append("{/axis}")
        if font != gui.text_font:
            closing_tags.append("{/font}")
        if size != 0:
            closing_tags.append("{/size}")

        return opening_tags,closing_tags

# ------------------------------------------------------------------------
# FUNCTIONS USED BY THE "SPEECH" PARSER
# ------------------------------------------------------------------------  
    def detect_modifier(speaker,text):
        global _TPS_MODIFIER_TAGS

        if speaker == "narr":
            return "narr"
        
        modifier = None

        for tag in _TPS_MODIFIER_TAGS.keys():
            if tag in text:
                modifier = _TPS_MODIFIER_TAGS[tag]
                break

        if modifier is None:
            return "base"
        else:
            return modifier

    def anxiety_check(how_much_anxious,mark,pause_value,parser_data):
# Function that check whether a pause triggers a character's anxious reaction (ie. forces re-calculation of text speed)
#
# args:
#       how_much_anxious --> residual anxiety (if any) from a previous trigger
#       mark --> the specific punctuation mark the pause has been evaluated for
#       pause_value --> the actual value in seconds of the pause
#       parser_data --> the dictionary the function is supposed to take all the required information from
#
# usage:
#       is_anxious = anxiety_check(pause_value,parser_data)
#
# returns:
#       function returns +1 if the pause was too long; -1 if the pause was too short; False otherwise
        base_pause = parser_data["pauses"][mark]

        deviation = (pause_value - base_pause) / base_pause

        if abs(deviation) > parser_data["cps"]["anxiety"]["trigger"]:
            return deviation / abs(deviation) * (1 + how_much_anxious)
        elif how_much_anxious:
            return how_much_anxious * random.uniform(0.35,0.85)
        else:
            return False

# ------------------------------------------------------------------------
# FUNCTIONS USED BY THE "CHAT" PARSER
# ------------------------------------------------------------------------  
    def parse_chat_tags(text):

        start = None
        total = None

        if text.startswith("{"):
            tag_ends = text.index("}")
            tag = text[:tag_ends + 1]

            start_match = re.search(r"\bstart=([0-9]+(?:\.[0-9]+)?)",tag)
            total_match = re.search(r"\btotal=([0-9]+(?:\.[0-9]+)?)",tag)

            if start_match:
                start = float(start_match.group(1))

            if total_match:
                total = float(total_match.group(1))

            text = text[tag_ends+1:]

        return start,total,text

    def timeline_from_fixed(text,time,pauses_data):
# function that builds a chat message tapping timeline ("Typing..." screen appearing and disappearing) considering a fixed
# time span
#
# args:
#       text --> the dialogue line
#       time --> fixed time required to tap the dialogue line
#       pauses_data --> character-specific dictionary housing data to calculate for how long the "Typing..." screen is supposed
#                       to disappear
#
# usage:
#       timeline = timeline_from_fixed(text,time,pauses_data)
#
# returns:
#       Function returns a list of floats
        remaining_characters = len(text)
        n_pauses = 0
        timeline = []

        n_chunks = ceil(len(text) / random.uniform(8,16))
        n_pauses = n_chunks - 1

        if pauses_data.get("weighted_pauses",False):
            pauses_lenght = list(pauses_data["weighted_pauses"].keys())
            pauses_weights = list(pauses_data["weighted_pauses"].values())
            pauses = [random.choices(pauses_lenght,weights=pauses_weights,k=1)[0] for _ in range(n_pauses)]
        else:
            pauses = [random.uniform(*pauses_data["random_pause"]) for _ in range(n_pauses)]

        if sum(pauses) > 0.4 * time:
            correction_factor = 0.4 * time / sum(pauses)
            pauses = [pause * correction_factor for pause in pauses]

        spare_time = time - sum(pauses)

        typing_times = [random.uniform(1,3) for _ in range(n_chunks)]
        typing_times = [spare_time * tap_tap_tap / sum(typing_times) for tap_tap_tap in typing_times]

        for i in range(n_chunks):
            timeline.append(typing_times[i])
            if i < n_pauses:
                timeline.append(pauses[i])

        return timeline

    def timeline_from_typing(text,parser_data,is_slow):
# function that builds a chat message tapping timeline ("Typing..." screen appearing and disappearing) calculating how long the
# character is supposed to take to type the message itself
#
# args:
#       text --> the dialogue line
#       parser_data --> source dictionary with all information about style and text speed
#       pauses_data --> character-specific dictionary housing data to calculate for how long the "Typing..." screen is supposed
#                       to disappear
#       is_slow --> flag telling the tag generator that character is starting its line in the "slowdown" mode (ie. slow 
#                   tapping/writing speed)
#                   
# usage:
#       timeline = timeline_from_typing(text,parser_data,is_slow)
#
# returns:
#       Function returns a list of floats
        timeline = []
        characters_left = len(text)

        while characters_left > 0:
    
            cps_multiplier = calculate_cps_multiplier(parser_data,"chat",is_slow)

            if is_slow:
                typed_this_round = min(characters_left,random.randint(*parser_data["pauses"]["slow_interval"]))
            else:
                typed_this_round = min(characters_left,random.randint(*parser_data["pauses"]["fast_interval"]))

# the "Typing..." screen keeps the reader busy - they see something, and somethings the time it takes for a message to appear IS
# the message itself. Hence in this case typing speed is multiplied by a chat-specific cps modifier
            typing_speed = preferences.text_cps * cps_multiplier * parser_data["modifiers"]["mult"]
            timeline.append(typed_this_round / typing_speed)

            characters_left =- typed_this_round

            if characters_left > 0:
                if pauses_data.get("weighted_pauses",False):
                    pauses = list(parser_data["pauses"]["weighted_pauses"].keys())
                    weights = list(parser_data["pauses"]["weighted_pauses"].values())
                    timeline.append(random.choices(pauses,weights=weights,k=1)[0])
                else:
                    timeline.append(random.uniform(*parser_data["pauses"]["random_pause"]))

        return timeline

# ------------------------------------------------------------------------
# FUNCTIONS SHARED BY TWO OR MORE PARSERS
# ------------------------------------------------------------------------
    def generate_nonbroken_tags(speaker,parser_data,mode,is_slow=False):
# function generating opening and closing style tags for all parsers except the "broken" parser
#
# args:
#       speaker --> the charID corresponding to the character the dialogue line belongs to
#       parser_data --> source dictionary with all information about style and text speed
#       mode --> a string specifying the system which sub-section of the parser_data dict the function has to
#                look into
#       is_slow --> flag from "chat" and "write" parsers, telling the tag generator that character is starting
#                   its line in the "slowdown" mode (ie. slow tapping/writing speed)
#
# usage:
#       opening_tags,closing_tags = generate_nonbroken_tags(speaker,parser_data,mode,is_slow=False)
#
# returns:
#       Function returns two lists of fully-formed tags which are then added to the parser's output string
        opening_tags = []
        closing_tags = []

        if mode in ["narr","base","shout","think","whisper"]:
            size = parser_data["modifiers"][mode]["size"]
            color = parser_data["modifiers"][mode]["col"]
            style = parser_data["modifiers"][mode]["style"]
            font = parser_data["modifiers"][mode]["font"]["path"]
            if parser_data["modifiers"][mode]["font"]["variable"]:
                font_weight = parser_data["modifiers"][mode]["font"]["weight"]
                if "b" in style:
                    font_weight += 100
                    style = style.replace("b","")
            else:
                font_weight = None
            shader = parser_data["modifiers"][mode]["shader"]
        else:
            size = parser_data["modifiers"]["size"]
            color = parser_data["modifiers"]["col"]
            style = parser_data["modifiers"]["style"]
            font = parser_data["modifiers"]["font"]["path"]
            if parser_data["modifiers"]["font"]["variable"]:
                font_weight = parser_data["modifiers"]["font"]["weight"]
            else:
                font_weight = None
            shader = parser_data["modifiers"]["shader"]
            
        cps_multiplier = calculate_cps_multiplier(speaker,parser_data,mode,is_slow)

        if shader != None:
            opening_tags.append(f"{{shader={shader}}}")
        if size > 0:
            opening_tags.append(f"{{size=+{size}}}")
        elif size < 0:
            opening_tags.append(f"{{size=-{abs(size)}}}")
        if font != gui.text_font:
            opening_tags.append(f"{{font={font}}}")
        if font_weight is not None and font_weight != gui.text_axis["weight"]:
            opening_tags.append(f"{{axis:weight={font_weight}}}")
        if color != None:
            opening_tags.append(f"{{color={color}}}")
        if style != None:
            for tag in style:
                opening_tags.append(f"{{{tag}}}")

# cps should always be the last tag to open and the first to be closed
        opening_tags.append(f"{{cps=*{cps_multiplier}}}")
        closing_tags.append("{/cps}")

        if style != None:
            for tag in reversed(style):
                closing_tags.append(f"{{/{tag}}}")
        if color != None:
            closing_tags.append("{/color}")
        if font_weight is not None and font_weight != gui.text_axis["weight"]:
            closing_tags.append("{/axis}")
        if font != gui.text_font:
            closing_tags.append("{/font}")
        if size != 0:
            closing_tags.append("{/size}")
        if shader != None:
            closing_tags.append("{/shader}")

        return opening_tags,closing_tags

    def remove_custom_tags(string):
# helper function to remove custom tags used inside the rhythmic_say function. Prevents hard crashes from unknown tags
#
# args:
#       string --> the string that must be cleaned
#
# usage:
#       clean_string = remove_custom_tags(string)
#
# returns:
#       function returns a string stripped of custom tags
        global _TPS_PARSING_TAGS, _TPS_MODIFIER_TAGS

        clean_string = str(string)

# first step - removes the {norhythm} tag
        if clean_string.startswith("{norhythm}"):                            # special tag to skip parsing & pause addition
            clean_string = clean_string[len("{norhythm}"):]

# ADD MORE PARSING TAGS TO INIT LIST AS REQUIRED
        for parsing_tag in _TPS_PARSING_TAGS.keys():
            if clean_string.startswith(parsing_tag):
                clean_string = clean_string[len(parsing_tag):]

# ADD MORE MODIFIER TAGS TO INIT LIST AS REQUIRED
        for modifier_tag in _TPS_MODIFIER_TAGS.keys():
            if clean_string.startswith(modifier_tag):
                clean_string = clean_string[len(modifier_tag):]
            
        return clean_string

    def calculate_cps_multiplier(speaker,parser_data,section,is_slow,anxiety = False):
# helper function calculating the cps multiplier that goes into the {cps} tag
#
# args:
#       speaker --> the charID corresponding to the character the dialogue line belongs to
#       parser_data --> source dictionary with all information about style and text speed
#       section --> string telling the function into which part of the parser_data dict to look
#       is_slow --> flag from "chat" and "write" parsers, telling the tag generator that character is starting
#                   its line in the "slowdown" mode (ie. slow tapping/writing speed)
#
# usage:
#       cps_mult = calculate_cps_multiplier(parser_data,section,is_slow)
#
# returns:
#       Function returns a float
        if section == "broken":
            cps_base_multiplier = parser_data["mult"]
            jitter = random.uniform(-parser_data["jitter"]["amount"], parser_data["jitter"]["amount"])
            return cps_base_multiplier * (1 + jitter)

        if section in ["narr","base","shout","whisper","think"]:
            cps_base_multiplier = parser_data["cps"]["mult"] * parser_data["modifiers"][section]["mult"]
        elif is_slow:
            cps_base_multiplier = parser_data["cps"]["slowdown"]["mult_slow"]
        else:
            cps_base_multiplier = parser_data["cps"]["mult"]

        cps_jitter = calculate_jitter(speaker,parser_data["cps"]["jitter"],jitter_group = "cps")

        if parser_data["cps"].get("anxiety",False) and parser_data["cps"]["anxiety"]["active"]:
            cps_anxious_jitter = abs(calculate_jitter(speaker,parser_data["cps"]["anxiety"])) * anxiety
        else:
            cps_anxious_jitter = 0

        return cps_base_multiplier * (1 + cps_jitter) * (1 + cps_anxious_jitter)

    def calculate_jitter(speaker,parser_data,jitter_group = None):
# very simple helper function to generate a variable's (such as pause duration or cps) jitter value
#
# args:
#       speaker --> the charID corresponding to the character the dialogue line belongs to
#       parser_data --> the dictionary the function is supposed to take all the required information from
#       jitter_group --> the specific sub-section in the jitter pauses dict, corresponding to a group of
#                        punctuation marks sharing the same jitter pattern
#
# usage:
#       jitter = calculate_jitter(parser_data,jitter_group)
#
# returns:
#       Function returns a float
        global _TPS_JITTER_FUNCTIONS

        if not parser_data.get("pattern",False) or parser_data.get("pattern",False) == "random":
            return random.uniform(-parser_data["amount"],parser_data["amount"])
        elif parser_data.get("pattern") is None:
            return 0
        else:
            return _TPS_JITTER_FUNCTIONS[parser_data.get("pattern")](speaker,parser_data,jitter_group)
            
    def calculate_jitter_pink(speaker,parser_data,jitter_group):
# calculates jitter value for a pink noise based jitter
#
# args:
#       speaker --> the charID corresponding to the character the dialogue line belongs to
#       parser_data --> the dictionary the function is supposed to take all the required information from
#       jitter_group --> the specific sub-section in the jitter pauses dict, corresponding to a group of
#                        punctuation marks sharing the same jitter pattern
#
# usage:
#       jitter = calculate_jitter_pink(parser_data,jitter_group)
#
# returns:
#       Function returns a float
        prev_jitter = store.jitter_states[speaker][jitter_group]
        roughness = parser_data["roughness"]
        if prev_jitter == 0:
            next_jitter = random.uniform(-parser_data["amount"],parser_data["amount"])
        else:
            next_jitter = random.uniform(-parser_data["amount"],parser_data["amount"]) * roughness + prev_jitter * (1 - roughness)

        store.jitter_states[speaker][jitter_group] = next_jitter

        return next_jitter

    def calculate_jitter_sine(speaker,parser_data,jitter_group):
# calculates jitter value for a sine-shaped jitter
#
# args:
#       speaker --> the charID corresponding to the character the dialogue line belongs to
#       parser_data --> the dictionary the function is supposed to take all the required information from
#       jitter_group --> the specific sub-section in the jitter pauses dict, corresponding to a group of
#                        punctuation marks sharing the same jitter pattern
#
# usage:
#       jitter = calculate_jitter_sine(parser_data,jitter_group)
#
# returns:
#       Function returns a float
        period = parser_data.get("period",13)
        phase = int(store.jitter_states[speaker][jitter_group]) % parser_data.get("period",13)
        amount = parser_data.get("amount",0)
        store.jitter_states[speaker][jitter_group] += 1
        return amount * math.sin(2 * math.pi * phase / period)

    def calculate_jitter_choice(speaker,parser_data,jitter_group):
# calculates jitter value for a jitter defined by a user-defined sequence
#
# args:
#       speaker --> the charID corresponding to the character the dialogue line belongs to
#       parser_data --> the dictionary the function is supposed to take all the required information from
#       jitter_group --> the specific sub-section in the jitter pauses dict, corresponding to a group of
#                        punctuation marks sharing the same jitter pattern
#
# usage:
#       jitter = calculate_jitter_pink(parser_data,jitter_group)
#
# returns:
#       Function returns a float
        jitter_sequence = parser_data["amount"]
        index = int(store.jitter_states[speaker][jitter_group]) % len(jitter_sequence)
        store.jitter_states[speaker][jitter_group] += 1
        if parser_data["with_sign"]:
            return jitter_sequence[index]
        else:
            return jitter_sequence[index] * random.choice([-1,1])

    def calculate_pause(speaker,parser_data, punct_mark):
# function that calculates the pause value for the corresponding punctuation mark
#
# args:
#       speaker --> the charID corresponding to the character the dialogue line belongs to
#       parser_data --> the dictionary the function is supposed to take all the required information from
#       punct_mark --> the specific punctuation mark the pause should be evaluated for. Corresponds to a key
#                      in the parser_data dictionary
#
# usage:
#       pause_value = calculate_pause(punct_mark,punct_mark)
#
# returns:
#       function returns a float

        pause_group = store.jitter_groups_map[punct_mark]

        base_pause_value = parser_data[punct_mark]

        pause_jitter = calculate_jitter(speaker,parser_data["jitter"][pause_group],pause_group)

        return base_pause_value * (1 + pause_jitter)