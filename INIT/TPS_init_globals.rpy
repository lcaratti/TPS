init -100 python:
# ------------------------------------------------------------------------
# PRELIMINARY STEPS
# ------------------------------------------------------------------------  
# import basic packages used by the script
    import random,math,re
# import renpy store *after* the init function has populated it
    import renpy.store as store
# import NotSet flag to perfectly mimic Ren'Py Character object within my TPSCharacter class
    from renpy.character import NotSet

    _TPS_DATA_SKELETON = {
        "TPS_characters_register": {},
        "character_profiles": {},
        "moods": {
        "start": {},
        "target": {}
        },
        "jitter_states": {},
        "transition_states": {},
        "shared_states": {},
        "current_speaker": "",
        "current_narrator": "",
        "_group_id_counter": 0,
        "mode": "speech",
        "presentation_mode": "adv"
    }

    _JITTER_GROUPS = {
        "strong": ["point", "excl", "qmark"],
        "weak": ["comma", "ddot", "bracket", "semicol"],
        "ellipsis": ["ellipsis"]
    }

    jitter_groups_map = {
        mark: group for group,marks in _JITTER_GROUPS.items() for mark in marks
    }

    _TPS_PREFIXES = {
        "think": "",
        "speech": ""
    }

    _TPS_SUFFIXES = {
        "think": "",
        "speech": ""
    }

    store.presentation_mode = "adv"

init -1 python:
    _TPS_PARSERS = {
        "broken": rhythmize_broken,
        "write": rhythmize_write,
        "chat": rhythmize_chat,
        "speech": rhythmize_speech
        }

    _TPS_PARSING_TAGS = {
        "{write}": "write",
        "{speech}": "speech",
        "{chat}": "chat"
    }

    _TPS_MODIFIER_TAGS = {
        "{shout}": "shout",
        "{whisper}": "whisper",
        "{think}": "think"
    }

    _TPS_JITTER_FUNCTIONS = {
        "pink": calculate_jitter_pink,
        "sine": calculate_jitter_sine,
        "choice": calculate_jitter_choice
    }

    _TPS_PARSING_EFFECTS = {
        "writing_sound": {
            "function": play_sound_effect,
            "args": ["audio/sfx/write.mp3"]
        },
        "chat_buzz": {
            "function": play_sound_effect,
            "args": ["audio/sfx/phone_buzz.mp3"]
        },
        "chat_chirp": {
            "function": play_sound_effect,
            "args": ["audio/sfx/phone_chirp.mp3"]
        }
    }