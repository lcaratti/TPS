init -9 python:
    store.character_profiles["insecure"] = {
# ------------------------------------------------------------------------
# 1. BASE - Everyday use
# ------------------------------------------------------------------------
        "base": {
            "speech": {
                "modifiers": {
                    "narr": {
                        "size": -1,
                        "col": "#fefefefb",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 350
                                }
                            },
                    "base": {
                        "size": -2,
                        "col": "#fafafad9",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 300
                                }
                            },
                    "shout": {
                        "size": 3,
                        "col": "#fdfdfffd",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 380
                                }
                            },
                    "whisper": {
                        "size": -5,
                        "col": "#fefaffce",
                            },
                    "think": {
                        "mult": 1.2,
                        "pause_mult": 0.8,
                        "col":  "#fdfdfe",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 350
                                }
                            }
                        },
                "cps": {
                    "mult": 0.85,
                    "anxiety": {
                        "active": True,
                        "trigger": 0.08,
                        "amount": 0.2
                            },
                    "jitter": {
                        "pattern": "pink",
                        "amount": 0.05,
                        "roughness": 0.35
                            }
                        },
                "pauses": {
                    "point": 0.45,
                    "comma": 0.325,
                    "excl": 0.4,
                    "qmark": 0.48,
                    "bracket": 0.3,
                    "ellipsis": 0.95, 
                    "semicol": 0.3,
                    "ddot": 0.3,
                    "jitter": {
                        "strong": {
                            "pattern": "choice",
                            "amount": [0.04,0.03,0.09,0.02,0.0,0.0,0.06,0.03],
                            "with_sign": False
                                },
                        "weak": {
                            "pattern": "choice",
                            "amount": [0.055,0.02,0.11,0.045,0.06,0.0,0.075,0.045],
                            "with_sign": False
                                },
                        "ellipsis": {
                            "pattern": "pink",
                            "amount": 0.15,
                            "roughness": 0.5,
                            "split": [1.0,2.0,3.5]
                                }
                            }
                        }
                    },
            "write": {    
                    },
            "chat": {    
                    }
                },
# ------------------------------------------------------------------------
# 2. EASYGOING - With Close Friends
# ------------------------------------------------------------------------
        "easygoing": {
            "speech": {
                "modifiers": {
                    "narr": {
                        "size": 1,
                        "col": "#fefffdfe"
                            },
                    "base": {
                        "size": 1,
                        "col": "#fffefdf1"
                            },
                    "shout": {
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 470
                                },
                        "mult": 1.65,
                        "pause_mult": 0.5,
                        "col": "#fffdfc"
                            },
                    "whisper": {
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 370
                                },
                        "pause_mult": 0.75,
                        "col": "#fffbfde4"
                            },
                    "think": {
                        "mult": 1.25,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 400
                                },
                        "col": "#fbfffb"
                            },
                        },
                "cps": {
                    "multiplier": 1.1,
                    "anxiety": {
                        "active": False
                            },
                    "jitter": {
                        "pattern": "pink",
                        "amount": 0.09,
                        "roughness": 0.45,
                            }
                        },
                "pauses": {
                    "point": 0.32,
                    "comma": 0.22,
                    "excl": 0.4,
                    "qmark": 0.35,
                    "bracket": 0.2,
                    "ellipsis": 0.69, 
                    "semicol": 0.2,
                    "ddot": 0.22,
                    "jitter": {
                        "strong": {
                            "pattern": "pink",
                            "amount": 0.15,
                            "roughness": 0.25,
                                },
                        "weak": {
                            "pattern": "pink",
                            "amount": 0.2,
                            "roughness": 0.4,
                                },
                        "ellipsis": {
                            "pattern": "pink",
                            "amount": 0.3,
                            "roughness": 0.5,
                            "split": [1.0,1.3,1.6]
                                }
                            }
                        }
                    },
            "write": {
                "modifiers": {
                    "mult": 0.51,
                    "size": 3
                        },
                "cps": {
                    "mult": 1.15,
                    "slowdown": {
                        "mult_slow": 0.72,
                        "slow_chance": 0.15,
                        "slow_chance_midword": 0.3,
                        "slow_start": 0.02
                            },
                    "jitter": {
                        "amount": 0.25
                            }
                        },
                "pauses": {
                    "showup_time": [0.5,1.6],
                    "fast_interval": [7,16],          
                    "slow_interval": [3,8],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.25,
                            0.3: 0.25,
                            0.6: 0.25,
                            1.0: 0.15,
                            1.8: 0.1
                            }
                        }
                    },
            "chat": {
                "modifiers": {
                    "mult": 0.13,
                    "effects": "chat_chirp"
                        },
                "cps": {
                    "mult": 1.2,
                    "slowdown": {
                        "mult_slow": 0.65,
                        "slow_chance": 0.23,
                        "slow_chance_midword": 0.4,
                        "slow_start": 0.02
                            },
                    "jitter": {
                        "amount": 0.31
                            },
                    "typos": {
                        "chance": 0.15,
                        "correct_chance": 0.65,
                        "notice": [2,7],
                        "p1": [0.3,0.9],
                        "p2": [0.4,0.9]
                            }
                        },
                "pauses": {
                    "interval": [6,18],          
                    "slow_interval": [4,12],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.17,
                            0.3: 0.3,
                            0.6: 0.3,
                            1.0: 0.12,
                            1.8: 0.11
                            }
                        }
                    }
                },
    # ------------------------------------------------------------------------
    # 3. AWKWARD - Socially Difficult Situations
    # ------------------------------------------------------------------------
        "awkward": {
            "speech": {
                "modifiers": {
                    "narr": {
                        "size": -2,
                        "col": "#fff5fed2",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 320
                                }
                            },
                    "base": {
                        "size": -3,
                        "col": "#ffeffdd0",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 300
                                }
                            },
                    "shout": {
                        "size": 4,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 490
                                },
                        "mult": 1.8,
                        "pause_mult": 0.55,
                        "col": "#ffeefcff"
                            },
                    "whisper": {
                        "size": -7,
                        "mult": 1.3,
                        "pause_mult": 0.85,
                        "col": "#ecfbffc6"
                            },
                    "think": {
                        "mult": 1.15,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 460
                                },
                        "pause_mult": 0.9,
                        "col": "#fff5fdd3"
                            }
                        },
                "cps": {
                    "multiplier": 0.65,
                    "anxiety": {
                        "active": True,
                        "trigger": 0.04,
                        "amount": 0.25
                            },
                    "jitter": {
                        "pattern": "random",
                        "amount": 0.17,
                            }
                        },
                "pauses": {
                    "point": 0.6,
                    "comma": 0.35,
                    "excl": 0.45,
                    "qmark": 0.75,
                    "bracket": 0.35,
                    "ellipsis": 1.1,
                    "semicol": 0.35,
                    "ddot": 0.45,
                    "jitter": {
                        "strong": {
                            "pattern": "sine",
                            "period": 6,
                            "amount": 0.15
                                },
                        "weak": {
                            "pattern": "random",
                            "amount": 0.27
                                },
                        "ellipsis": {
                            "pattern": "random",
                            "amount": 0.3,
                            "split": [0.9,1.1,1.9]
                                }
                            }
                        }
                    },
            "write": {
                "modifiers": {
                    "mult": 0.34
                        },
                "cps": {
                    "mult": 0.86,
                    "slowdown": {
                        "mult_slow": 0.57,
                        "slow_chance": 0.4,
                        "slow_chance_midword": 0.4,
                        "slow_start": 0.12
                            },
                    "jitter": {
                        "amount": 0.27
                            }
                        },
                "pauses": {
                    "showup_time": [1.0,2.6],
                    "fast_interval": [5,13],          
                    "slow_interval": [6,12],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.15,
                            0.3: 0.25,
                            0.6: 0.3,
                            1.0: 0.18,
                            1.8: 0.12
                            }
                        }
                    },
            "chat": {
                "modifiers": {
                    "mult": 0.075,
                    "effects": "chat_chirp"
                        },
                "cps": {
                    "mult": 0.76,
                    "slowdown": {
                        "mult_slow": 0.55,
                        "slow_chance": 0.35,
                        "slow_chance_midword": 0.4,
                        "slow_start": 0.2
                            },
                    "jitter": {
                        "amount": 0.28
                            },
                    "typos": {
                        "chance": 0.3,
                        "correct_chance": 0.85,
                        "notice": [1,4],
                        "p1": [0.8,1.9],
                        "p2": [0.6,1.6]
                            }
                        },
                "pauses": {
                    "interval": [5,15],          
                    "slow_interval": [4,10],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.1,
                            0.3: 0.3,
                            0.6: 0.33,
                            1.0: 0.15,
                            1.8: 0.12
                            }
                        }
                    }
                },
# ------------------------------------------------------------------------
# 4. PANIC - extreme anxiety / situation clearly getting off-hand
# ------------------------------------------------------------------------
        "panic": {
            "speech": {
                "modifiers": {
                    "narr": {
                        "size": -2,
                        "col": "#fdfdffa0",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 340
                                }
                            },
                    "base": {
                        "size": -1,
                        "font": "fonts/Rubik-Light.ttf",
                        "col": "#fdfcffef",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 330
                                }
                            },
                    "shout": {
                        "size": 7,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 520
                                },
                        "mult": 1.9,
                        "pause_mult": 0.25,
                        "col": "#fefdfff0",
                            },
                    "whisper": {
                        "size": -8,
                        "mult": 1.7,
                        "pause_mult": 0.35,
                        "col": "#fbfbffdd"
                            },
                    "think": {
                        "mult": 0.85,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 420
                                },
                        "pause_mult": 1.15,
                        "col": "#fafbff8e"
                            }
                        },
                "cps": {
                    "multiplier": 1.2,
                    "anxiety": {
                        "active": True,
                        "trigger": 0.025,
                        "amount": 0.25
                            },
                    "jitter": {
                        "pattern": "sine",  
                        "amount": 0.2,
                        "period": 5
                            }
                        },
                "pauses": {
                    "point": 0.4,  
                    "comma": 0.3,
                    "excl": 0.35,
                    "qmark": 0.7,
                    "bracket": 0.2,
                    "ellipsis": 0.95,   
                    "semicol": 0.28,
                    "ddot": 0.5,
                    "jitter": {
                        "strong": {
                            "pattern": "choice",  
                            "amount": [0.02,0.28,0.03,0.0,0.26,0.02,0.05,0.0,0.22,0.09],
                            "with_sign": False
                                },
                        "weak": {
                            "pattern": "random", 
                            "amount": 0.2
                                },
                        "ellipsis": {
                            "pattern": "sine", 
                            "amount": 0.25,
                            "period": 8,
                            "split": [1.4, 0.5, 1.8]
                                }
                            }
                        }
                    },
            "write": {
                "modifiers": {
                    "mult": 0.34
                        },
                "cps": {
                    "mult": 0.86,
                    "slowdown": {
                        "mult_slow": 0.57,
                        "slow_chance": 0.4,
                        "slow_chance_midword": 0.4,
                        "slow_start": 0.12
                            },
                    "jitter": {
                        "amount": 0.27
                            }
                        },
                "pauses": {
                    "showup_time": [1.0,2.6],
                    "fast_interval": [5,13],          
                    "slow_interval": [6,12],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.15,
                            0.3: 0.25,
                            0.6: 0.3,
                            1.0: 0.18,
                            1.8: 0.12
                            }
                        }
                    },
            "chat": {
                "modifiers": {
                    "mult": 0.16,
                    "effects": "chat_chirp"
                        },
                "cps": {
                    "mult": 1.15,
                    "slowdown": {
                        "mult_slow": 0.53,
                        "slow_chance": 0.37,
                        "slow_chance_midword": 0.6,
                        "slow_start": 0.05
                            },
                    "jitter": {
                        "amount": 0.22
                            },
                    "typos": {
                        "chance": 0.4,
                        "correct_chance": 0.55,
                        "notice": [2,8],
                        "p1": [0.7,1.7],
                        "p2": [0.5,1.5]
                            }
                        },
                "pauses": {
                    "interval": [7,19],          
                    "slow_interval": [4,16],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.14,
                            0.3: 0.24,
                            0.6: 0.34,
                            1.0: 0.18,
                            1.8: 0.12
                            }
                        }
                    }
                },
# ------------------------------------------------------------------------
# 5. OBSESSIVE-COMPULSIVE - Ritualistic Control
# ------------------------------------------------------------------------
        "ocd": {
            "speech": {
                "modifiers": {
                    "narr": {
                        "col": "#d8d6e9f5"
                            },
                    "base": {
                        "col": "#fff5faff"
                            },
                    "shout": {
                        "size": 5,
                        "mult": 1.6,
                        "pause_mult": 0.62,
                        "col": "#dcfff9ff"
                            },
                    "whisper": {
                        "size": -5,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 400
                                },
                        "mult": 1.5,
                        "pause_mult": 0.68,
                        "col": "#ffe2f5ff"
                            },
                    "think": {
                        "size": 3,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 650
                                },
                        "mult": 1.5,
                        "pause_mult": 0.4,
                        "col": "#fbe5ffff"
                            }
                        },
                "cps": {
                    "multiplier": 0.9,
                    "anxiety": {
                        "active": True,
                        "trigger": 0.18,
                        "amount": 0.3,
                            },
                    "jitter": {
                        "pattern": "choice",   
                        "amount": [0.0,0.25,-0.15,0.0,-0.15,0.25,0.0,0.15,-0.25,0.0,-0,25,0.15]
                            }
                        },
                "pauses": {
                    "point": 0.5,
                    "comma": 0.25,      
                    "excl": 0.5,
                    "qmark": 0.5,      
                    "bracket": 0.25,
                    "ellipsis": 0.75,          
                    "semicol": 0.375,
                    "ddot": 0.375,        
                    "jitter": {
                        "strong": {
                            "pattern": "choice",   
                            "amount": [0.0,0.01,0.0,0.2,0.028,0.0,0.0,0.15,0.0,0.0,0.02,0.027],
                            "with_sign": False
                                },
                        "weak": {
                            "pattern": "choice",   
                            "amount": [0.2,0.028,0.0,0.0,0.23,0.0,0.19,0.02,0.027,0.19,0.01,0.0],
                            "with_sign": False
                                },
                        "ellipsis": {
                            "pattern": "random",   
                            "amount": 0.23,
                            "split": [0.6, 1.2, 2.4]  
                                }
                            }
                        }
                    },
            "write": {
                "modifiers": {
                    "mult": 0.4,
                    "size": 2
                        },
                "cps": {
                    "slowdown": {
                        "mult_slow": 0.7,
                        "slow_chance": 0.15,
                        "slow_chance_midword": 0.3,
                        "slow_start": 0.01
                            },
                    "jitter": {
                        "amount": 0.1
                            }
                        },
                "pauses": {
                    "showup_time": [1.0,2.0],
                    "fast_interval": [8,16],          
                    "slow_interval": [4,8],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.22,
                            0.3: 0.33,
                            0.6: 0.3,
                            1.0: 0.08,
                            1.8: 0.07
                            }
                        }
                    },
            "chat": {
                "modifiers": {
                    "mult": 0.1,
                    "effects": "chat_mute"
                        },
                "cps": {
                    "slowdown": {
                        "mult_slow": 0.7,
                        "slow_chance": 0.15,
                        "slow_chance_midword": 0.2,
                        "slow_start": 0.02
                            },
                    "jitter": {
                        "amount": 0.1
                            },
                    "typos": {
                        "chance": 0.05,
                        "correct_chance": 0.98,
                        "notice": [1,3],
                        "p1": [0.5,3.0],
                        "p2": [0.7,2.0]
                            }
                        },
                "pauses": {
                    "interval": [5,15],          
                    "slow_interval": [3,9],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.22,
                            0.3: 0.33,
                            0.6: 0.3,
                            1.0: 0.08,
                            1.8: 0.07
                            }
                        }
                    }
                },
    # ------------------------------------------------------------------------
    # 6. TIRED - Mental/Physical Exhaustion
    # ------------------------------------------------------------------------
        "tired": {
            "speech": {
                "text_modifiers": {
                    "narr": {
                        "size": -1,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 310
                                },
                        "col": "#f5f9ffab"
                            },
                    "base": {
                        "size": -2,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 310
                                },
                        "col": "#fafafad0"
                            },
                    "shout": {
                        "size": 4,
                        "mult": 1.4,
                        "pause_mult": 0.8,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 390
                                },
                        "col": "#f5f5f5bb"
                            },
                    "whisper": {
                        "size": -7,
                        "mult": 1.25,
                        "pause_mult": 0.7,
                        "col": "#faf2f18c"
                            },
                    "think": {
                        "size": -2,
                        "mult": 0.87,
                        "pause_mult": 1.2,
                        "col": "#edf4f89d",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 340
                                }
                            }
                        }, 
                "cps": {
                    "multiplier": 0.89,
                    "anxiety": {
                        "active": False
                            },
                    "jitter": {
                        "pattern": "sine",
                        "amount": 0.18,
                        "period": 11
                            }
                        },
                "pauses": {
                    "point": 0.52,
                    "comma": 0.42,
                    "excl": 0.45,
                    "qmark": 0.48,
                    "bracket": 0.25,
                    "ellipsis": 1.1, 
                    "semicol": 0.37,
                    "ddot": 0.33,
                    "jitter": {
                        "strong": {
                            "pattern": "choice",   
                            "amount": [0.03,0.05,-0.02,0.11,-0.04,0.0,0.0,-0.18,0.07,0.0,-0.03,-0.04,0.2,0.0]
                                },
                        "weak": {
                            "amount": 0.27,
                            "pattern": "random"
                                },
                        "ellipsis": {
                            "amount": 0.28,
                            "pattern": "random",
                            "split": [1.9, 1.2, 3]
                                }
                            }
                        }
                    },
            "write": {
                "modifiers": {
                    "mult": 0.33,
                    "size": 1
                        },
                "cps": {
                    "slowdown": {
                        "mult_slow": 0.45,
                        "slow_chance": 0.5,
                        "slow_chance_midword": 0.5,
                        "slow_start": 0.2
                            },
                    "jitter": {
                        "amount": 0.33
                            }
                        },
                "pauses": {
                    "showup_time": [1.5,3.0],
                    "fast_interval": [5,12],          
                    "slow_interval": [6,14],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.12,
                            0.3: 0.3,
                            0.6: 0.35,
                            1.0: 0.13,
                            1.8: 0.1
                            }
                        }
                    },
            "chat": {
                "modifiers": {
                    "mult": 0.75,
                    "effects": "chat_mute"
                        },
                "cps": {
                    "slowdown": {
                        "mult_slow": 0.55,
                        "slow_chance": 0.4,
                        "slow_chance_midword": 0.5,
                        "slow_start": 0.16
                            },
                    "jitter": {
                        "amount": 0.3
                            },
                    "typos": {
                        "chance": 0.4,
                        "correct_chance": 0.55,
                        "notice": [5,14],
                        "p1": [1.5,3.0],
                        "p2": [1.2,2.5]
                            }
                        },
                "pauses": {
                    "interval": [5,15],          
                    "slow_interval": [5,12],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.12,
                            0.3: 0.3,
                            0.6: 0.35,
                            1.0: 0.13,
                            1.8: 0.1
                            }
                        }
                    }
                },
    # ------------------------------------------------------------------------
    # 7. VERY EMBARRASSED - Romantic/Comedic Flustered
    # ------------------------------------------------------------------------
        "embarrassed": {
            "speech": {
                "text_modifiers": {
                    "narr": {
                        "size": -3,
                        "col": "#fce2fdf1",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 300
                                }
                            },
                    "base": {
                        "size": -2,
                        "col": "#ffd2dfe0",
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 300
                                }
                            },
                    "shout": {
                        "size": 5,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 550
                                },
                        "mult": 1.5,
                        "pause_mult": 0.7,
                        "col": "#fdb3c3d0"
                            },
                    "whisper": {
                        "size": -5,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 480
                                },
                        "mult": 1.2,
                        "pause_mult": 0.95,
                        "col": "#e6cad0"
                            },
                    "think": {
                        "size": -3,
                        "mult": 0.8,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 560
                                },
                        "pause_mult": 1.35,
                        "col": "#d5cfddd2"
                            }
                        },
                "cps": {
                    "multiplier": 1.17,
                    "anxiety": {
                        "active": True,
                        "trigger": 0.07,
                        "amount": 0.23
                            },
                    "jitter": {
                        "pattern": "pink",
                        "amount": 0.26,
                        "roughness": 0.65
                            }
                        },
                "pauses": {
                    "point": 0.28,
                    "comma": 0.14,
                    "excl": 0.32,
                    "qmark": 0.38,
                    "bracket": 0.19,
                    "ellipsis": 0.79,
                    "semicol": 0.22,
                    "ddot": 0.24,
                    "jitter": {
                        "strong": {
                            "amount": 0.25,
                            "pattern": "random"
                                },
                        "weak": {
                            "amount": 0.3,
                            "pattern": "random"
                                },
                        "ellipsis": {
                            "amount": 0.33,
                            "pattern": "random",
                            "split": [3, 1, 2]
                                }
                            }
                        }
                    },
            "write": {
                "modifiers": {
                    "mult": 0.53,
                    "size": 3
                        },
                "cps": {
                    "slowdown": {
                        "mult_slow": 0.57,
                        "slow_chance": 0.33,
                        "slow_chance_midword": 0.4,
                        "slow_start": 0.03
                            },
                    "jitter": {
                        "amount": 0.27
                            }
                        },
                "pauses": {
                    "showup_time": [0.7,2.5],
                    "fast_interval": [4,18],          
                    "slow_interval": [4,14],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.23,
                            0.3: 0.26,
                            0.6: 0.25,
                            1.0: 0.14,
                            1.8: 0.12
                            }
                        }
                    },
            "chat": {
                "modifiers": {
                    "mult": 0.14,
                    "effects": "chat_chirp"
                        },
                "cps": {
                    "slowdown": {
                        "mult_slow": 0.65,
                        "slow_chance": 0.25,
                        "slow_chance_midword": 0.35,
                        "slow_start": 0.04
                            },
                    "jitter": {
                        "amount": 0.31
                            },
                    "typos": {
                        "chance": 0.27,
                        "correct_chance": 0.65,
                        "notice": [1,7],
                        "p1": [0.5,2.5],
                        "p2": [0.3,2.0]
                            }
                        },
                "pauses": {
                    "interval": [5,16],          
                    "slow_interval": [4,14],
                    "ignore_punctuation": False,  # will *not* ignore punctuation when counting characters
                    "weighted_pauses": {
                            0.1: 0.25,
                            0.3: 0.26,
                            0.6: 0.24,
                            1.0: 0.14,
                            1.8: 0.12
                            }
                        }
                    }
                },
    # ------------------------------------------------------------------------
    # 9. DISSOCIATED - flatline
    # ------------------------------------------------------------------------
        "flatline": {
            "speech": {
                "modifiers": {
                    "narr": {
                        "size": -1
                            },
                    "base": {
                        "size": -1
                            },
                    "shout": {
                        "size": 3,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 400
                                },
                        "mult": 1.25,
                        "pause_mult": 0.7
                            },
                    "whisper": {
                        "size": -3,
                        "font": {
                                "path": "fonts/Rubik-VariableFont_wght.ttf",
                                "weight": 400
                                },
                        "mult": 1.15,
                        "pause_mult": 0.8
                            },
                    "think": {
                        "size": -1,
                        "style": "i"
                            }
                        }, 
                "cps": {
                    "multiplier": 0.75,
                    "anxiety": {
                        "active": False
                            },
                    "jitter": {
                        "pattern": "none",
                            }
                        },
                "pauses": {
                    "point": 0.45, 
                    "comma": 0.24,  
                    "excl": 0.45,   
                    "qmark": 0.45,  
                    "bracket": 0.24,    
                    "ellipsis": 0.9,  
                    "semicol": 0.24,
                    "ddot": 0.24,
                    "jitter": {
                        "strong": {
                            "pattern": "none"
                                },
                        "weak": {
                            "pattern": "none"
                                },
                        "ellipsis": {
                            "pattern": "none",
                            "split": [1, 1, 1] 
                                }
                            }
                        }
                    },
            "write": {    
                    },
            "chat": {    
                    }
                },
    # ------------------------------------------------------------------------
    # 8. BROKEN - Fragmented, randomized mind pattern
    # ------------------------------------------------------------------------
        "broken": {
            "modifiers": {
                    },
            "cps": {
                    },
            "pauses": {
                    }
                }
        }
