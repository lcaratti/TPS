# THIS FILE HOLDS DEFAULT VALUES USED BY THE TPS
init -1 python:
    _DEFAULT_PROFILE = {
#################################################################################
# DEFAULT BASE PROFILE
################################################################################# 
        "default_base_params": {
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DEFAULT SPEECH SECTION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            "speech": {
    
#--------------------------------------------------------------------------------
#           TEXT MODIFIERS SUB-SECTION
#--------------------------------------------------------------------------------
# This section defines default values for speech modifiers
#    - "mult": a multiplier applied to the character's cps. Actual cps is calculated as:
#                base_cps_from_config * profile["cps"]["multiplier"] * speech_modifier["style"]["mult"] {* jitter}
#    - "size": an increase (or reduction) in the text size with respect to the value from config
#    - "col": text colour
#    - "style": either bold ("b"), italic ("i"), underline ("u") or strikethrough ("s")
#    - "pause_mult": a multiplier applied to the character's punctuation pauses. Each pause is calculated as:
#                profile["pauses"]["puncuation mark"] * speech_modifier["style"]["pause_mult"] {* jitter}
#    - "font": self-explanatory
#    - "shader": currently not in use - will host a dict with information on text halo parameters via the OneShader shader
#
# currently applicable styles:
# - narr: base style used when the character also is the current narrator
# - base: base style used when no custom tag is applied
# - shout: gets applied when the {shout} tag is used
# - whisper: gets applied when the {whisper} tag is used
# - think: gets applied when the {think} tag is used
                "modifiers": {
                        "narr": {
                                "mult": 1.0,
                                "size": 0,
                                "col": gui.text_color,
                                "style": "",
                                "pause_mult": 1.0,
                                "font": {
                                    "path": "fonts/Rubik-VariableFont_wght.ttf",
                                    "weight": 400
                                },
                                "shader": None,
                                "effects": None
                                },
                        "base": {
                                "mult": 1.0,                             # never change this - change the cps parameter in the spoken text speed section instead!
                                "size": 0,
                                "col": gui.text_color,
                                "style": "",
                                "pause_mult": 1.0,                       # never change this - change pause parameters in the spoken text's pauses section instead!
                                "font": {
                                    "path": "fonts/Rubik-VariableFont_wght.ttf",
                                    "weight": 400
                                },
                                "shader": None,
                                "effects": None
                                },
                        "shout": {
                                "mult": 1.55,
                                "size": 4,
                                "col": gui.text_color,
                                "style": "",
                                "pause_mult": 0.65,
                                "font": {
                                    "path": "fonts/Rubik-VariableFont_wght.ttf",
                                    "weight": 500
                                },
                                "shader": None,
                                "effects": None
                                },
                        "whisper": {
                                "mult": 1.33,
                                "size": -4,
                                "col": gui.text_color,
                                "style": "",
                                "pause_mult": 0.78,
                                "font": {
                                    "path": "fonts/Rubik-VariableFont_wght.ttf",
                                    "weight": 300
                                },
                                "shader": None,
                                "effects": None
                                },
                        "think": {
                                "mult": 1.15,
                                "size": -1,
                                "col": gui.text_color,
                                "style": "i",
                                "pause_mult": 0.85,
                                "font": {
                                    "path": "fonts/Rubik-VariableFont_wght.ttf",
                                    "weight": 400
                                },
                                "shader": None,
                                "effects": None
                                }
                            },
#--------------------------------------------------------------------------------
#           TEXT SPEED SUB-SECTION
#--------------------------------------------------------------------------------
# This section defines default values for text speed (baseline values and jitter) used by the TPS' speech module
#
#    - "mult": the base multiplier applied to *all* dialogue lines
#    - "anxiety": when active, cps might change within a same dialogue line depending on how long punctuation pauses last
#        - "active": when True, anxiety module is invoked
#        - "trigger": how much longer (or shorter) than the base value a pause should be to trigger the anxiety pattern
#        - "amount": how strong the cps fluctuation should be (max. value)
#    - "jitter": parameters defining the fluctuation of text speed between different dialogue lines
#        - "pattern": the kind of noise the jitter should use ("random", "pink", "sine", "choice")
#        - additional params defining the amount of jitter to be applied (params vary depending on the pattern)
                "cps": {
                        "mult": 1.0,
                        "anxiety": {
                            "active": False,
                            "trigger": 0,
                            "amount": 0
                                },
                        "jitter": {
                            "pattern": "pink",
                            "amount": 0.04,
                            "roughness": 0.35
                                }
                            },
# ------------------------------------------------------------------------
#           TEXT PAUSES SUB-SECTION
# ------------------------------------------------------------------------ 
# This section defines punctuation pauses and their jitter patterns
#    - "pauses_speech": a dict with the basic pauses for each punctuation marks
#        - punctuation marks: base pause duration for the specific punctuation mark
#    - "jitter": parameters describing pauses variance
#        - specific group: punctuation marks are divided into three groups (strong, weak, and ellipsis). Each group gets its dedicated jitter params
#            - "pattern": the kind of noise the jitter should use ("random", "pink", "sine", "choice")
#            - additional params defining the amount of jitter to be applied (params vary depending on the pattern)
#            - "split": special parameter for ellipsis, provides weights to split the total pause duration between the three dots of the ellipsis
                "pauses": {
                    "point": 0.43,
                    "comma": 0.19,
                    "excl": 0.55,
                    "qmark": 0.5,
                    "bracket": 0.17,
                    "ellipsis": 0.8,
                    "semicol": 0.27,
                    "ddot": 0.36,
                    "jitter": {
                        "strong": {
                            "amount": 0.1,
                            "pattern": "pink",
                            "roughness": 0.3
                                },
                        "weak": {
                            "amount": 0.13,
                            "pattern": "pink",
                            "roughness": 0.35
                                },
                        "ellipsis": {
                            "amount": 0.12,
                            "pattern": "pink",
                            "roughness": 0.3,
                            "split": [1, 1.1, 1.5]
                                }
                            }
                        }
                    },
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DEFAULT WRITING SECTION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            "write": {
#--------------------------------------------------------------------------------
#           TEXT MODIFIERS SUB-SECTION
#--------------------------------------------------------------------------------
# This section defines default values for written text modifiers - currently only the main character has the chance to write something.
# Mika too might end up writing in the foreseeable future
#
#    - not describing keys this model shares with the previous section
#    - lacks "pause_mult" attribute as writing mananges pauses a different way
                "modifiers": {
                        "mult": 0.4,                         # do not change this - this is not about the character's mood, it defines the basic CPS for written text
                        "size": 2,
                        "col": gui.text_color,
                        "style": "",
                        "font": {
                                "path": "fonts/daniel.ttf",
                                "weight": 0
                            },
                        "shader": "dissolve",
                        "shader": None,
                        "effects": "writing_sound"
                            },
#--------------------------------------------------------------------------------
#           TEXT SPEED SUB-SECTION
#--------------------------------------------------------------------------------
# This section defines default values for written text speed used by the TPS' speech module
#
#    - "mult": baseline writing speed multiplier
#    - "slowdown": paramters defining the prosody of slowed-down written text
#        - "mult_slow": slow writing speed multiplier
#        - "slow_chance": likelihood for the character to abruptly slow down during writing
#        - "slow_chance_midword": likelihood for the slowdown to happen mid-word rather than at a punctuation mark or a space
#        - "slow_start": likelihood for the character to start writing in slowdown mode
#    - "jitter": parameters defining the fluctuation of text speed (both baseline and slowdown mode). Follows a random noise pattern
#        - "amount": the maximum variance (absolute value) for text speed
                "cps": {
                    "mult": 1.0,
                    "slowdown": {
                        "mult_slow": 0.67,
                        "slow_chance": 0.25,
                        "slow_chance_midword": 0.1,
                        "slow_start": 0.05
                            },
                    "jitter": {
                        "amount": 0.18
                            }
                        },
# ------------------------------------------------------------------------
#           TEXT PAUSES SUB-SECTION
# ------------------------------------------------------------------------ 
# This section defines punctuation pauses and their jitter patterns used by the TPS' writing module
#    - "interval": specifies how many characters may pass before the system checks for a change in writing speed when writing at normal speed [min,max]
#    - "slow_interval": specifies how many characters may pass before the system checks for a change in writing speed during slowdown [min,max]
#    - "ignore_punctuation": when True, the module will not count punctuation when counting how many glyphs till the next check for a change in written text speed
#    - "pause_weights": a dict of key:value items. The key specifies the pause duration, while the value specifies the likelihood for the pause to last "key" seconds
                "pauses": {
                    "showup_time": [0.5,2.0],
                    "fast_interval": [5,12],          
                    "slow_interval": [4,8],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.1,
                            0.3: 0.3,
                            0.6: 0.3,
                            1.0: 0.2,
                            1.8: 0.1
                            }
                        }
                    },
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DEFAULT CHATTING SECTION
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            "chat": {
#--------------------------------------------------------------------------------
#           TEXT MODIFIERS SUB-SECTION
#--------------------------------------------------------------------------------
# This section defines default values for text chat app
#
#    - not describing keys this model shares with the previous section
#    - lacks "pause_mult" attribute as chatting mananges pauses a different way
                "modifiers": {
                        "mult": 0.1,                         # do not change this - this is not about the character's mood, it defines the basic CPS for tapped
                        "size": -2,
                        "col": gui.text_color,
                        "style": "",
                        "font": {
                                "path": "fonts/Inter-VariableFont_opsz,wght.ttf",
                                "weight": 350
                            },
                        "shader": None,
                        "shader": None,
                        "effects": "chat_buzz"
                                },
#--------------------------------------------------------------------------------
#           TEXT SPEED SUB-SECTION
#-------------------------------------------------------------------------------- 
# This section defines default values for written text speed used by the TPS' chat module
#
#    - "mult": baseline writing speed multiplier
#    - "slowdown": paramters defining the prosody of slowed-down chat
#        - "mult_slow": slow chat speed multiplier
#        - "slow_chance": likelihood for the character to abruptly slow down during chatting
#        - "slow_chance_midword": likelihood for the slowdown to happen mid-word rather than at a punctuation mark or a space
#        - "slow_start": likelihood for the character to start chatting in slowdown mode
#    - "jitter": parameters defining the fluctuation of text speed (both baseline and slowdown mode). Follows a random noise pattern
#        - "amount": the maximum variance (absolute value) for text speed
#    - "typos": parameters used by the typo injecting and correction submodule
#        - "chance": likelihood for the character to make a typo
#        - "correct_chance": likelihood for the character to notice the typo
#        - "notice": how many glyphs the character will type before starting to roll-back [min,max]
#        - "p1": duration of the pause between the moment character stops typing and the moment it starts rolling back [min,max]
#        - "p2": duration of the pause between the moment character completes rolling back and the moment it resumes typing
                "cps": {
                    "mult": 1.0,
                    "slowdown": {
                        "mult_slow": 0.5,
                        "slow_chance": 0.33,
                        "slow_chance_midword": 0.33,
                        "slow_start": 0.08
                                },
                    "jitter": {
                        "amount": 0.24
                            },
                    "typos": {
                        "chance": 0.05,
                        "correct_chance": 0.8,
                        "notice": [1,5],
                        "p1": [0.6,1.2],
                        "p2": [0.4,0.8]
                            }
                        },
# ------------------------------------------------------------------------
#           TEXT PAUSES SUB-SECTION
# ------------------------------------------------------------------------  
# This section defines punctuation pauses and their jitter patterns used by the TPS' phone chat module
#    - "interval": specifies how many characters may pass before the system checks for a change in tapping speed when wtexting at normal speed [min,max]
#    - "slow_interval": specifies how many characters may pass before the system checks for a change in tapping speed during slowdown [min,max]
#    - "ignore_punctuation": when True, the module will not count punctuation when counting how many glyphs till the next check for a change in tapping speed
#    - "pause_weights": a dict of key:value items. The key specifies the pause duration, while the value specifies the likelihood for the pause to last "key" seconds
                "pauses": {
                    "interval": [8,16],          
                    "slow_interval": [5,10],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.1,
                            0.3: 0.25,
                            0.6: 0.35,
                            1.0: 0.15,
                            1.8: 0.15
                                }
                            }
                    }
            },
#################################################################################
# DEFAULT BROKEN PROFILE
#################################################################################
        "default_broken_params": {
# ------------------------------------------------------------------------
# DEFAULT PROSODY SYSTEM MODIFIERS - BROKEN PROFILE
# ------------------------------------------------------------------------ 
# This section defines the default "broken" profile
#    - "broken": internal flag that enables the broken module
#    - "mult": base text speed multiplier
#    - "jitter": parameters defining the fluctuation of text speed. Follows a random noise pattern
#    - "ignore_punctuation": when True, the module will not count punctuation when counting how many glyphs till the next check for a change in written text speed
#    - "stutter_likelihood": chance the character will stutter (ie. "h-hello") when the module triggers a pause and a text speed change
#    - "pause_weights": a dict of key:value items. The key specifies the pause duration, while the value specifies the likelihood for the pause to last "key" seconds
#           "modifiers":
#--------------------------------------------------------------------------------
#           TEXT MODIFIERS SUB-SECTION
#--------------------------------------------------------------------------------
# add descritption
                "modifiers": {
                    "font": {
                            "path": "fonts/Rubik-VariableFont_wght.ttf",
                            "weight": [300,700]
                        },
                    "size": [-3,3],
                    "col": [0.6,1.0],
                    "shader": None
                    },
#--------------------------------------------------------------------------------
#           TEXT SPEED SUB-SECTION
#--------------------------------------------------------------------------------
# add descritption
                "cps": {
                    "mult": 1.1,
                    "jitter": {
                        "amount": 0.7
                            }
                        },
# ------------------------------------------------------------------------
#           TEXT PAUSES SUB-SECTION
# ------------------------------------------------------------------------  
# add descritption
                "pauses": {
                    "trigger_interval": [4,18],
                    "ignore_punctuation": True,
                    "stutter_likelihood": 0.4,
                    "weighted_pauses": {
                            0.1: 0.2,
                            0.3: 0.25,
                            0.6: 0.25,
                            0.9: 0.2,
                            1.7: 0.1
                                    }
                        }
                    }
                }
