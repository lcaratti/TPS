# ------------------------------------------------------------------------
# PUNCTUATION MARKS' MAPPING
# ------------------------------------------------------------------------  
# this section tells the TPS which punctuation marks it should look for, and how to deal with them as "groups"
#
# this defines the marks that the TPS will act upon, in the following format:
#"actual character in the script": "key found in the <<pauses>> section of the profile"
#
#To add a new mark:
#### --> 1) add it to the list following format above
#### --> 2) add it to the jitter_groups dictionary below
#### --> 3) add the corresponding "key": value pair to all dictionaries & moods
define punct_map = {
    ".": "point",
    ",": "comma",
    "!": "excl",
    "?": "qmark",
    ";": "semicol",
    ":": "ddot",
    "-": "bracket",
    "...": "ellipsis"
}

# Punctuation marks are grouped based on their "weight" and "how conscious" the corresponding pause should feel.
# - "strong" group: heavy and very conscious pauses. Ends a sentence, lets a question hang, etc.
# - "weak" group: breathers, pauses between two sentences talking about the same thing
# - "ellipsis" group: special group. Ellipsis are three marks merged into one and gets a special treatment
# this inverts the above grouping so that it's easier to find out which group corresponds to which sign
#define jitter_groups_map = {
#    mark: group for group,marks in jitter.groups.items() for mark in marks
#}
