# CUSTOM PYTHON CLASSES THE TPS USES TO STORE STUFF IN AN ELEGANT WAY...

init -10 python:
############################################################################################################################
#
# these are the TPSCharacter classes that basically handles a character's profile within Ren'Py's standard Character object
#
############################################################################################################################
    class TPSADVCharacter(ADVCharacter):
        def __init__(self,*args,profile="generic",**kwargs):
            super(TPSADVCharacter,self).__init__(*args,**kwargs)
            self.profile = profile                                  # this tells the TPS which character profile to use
            TPS_character_checkin(self)

    class TPSNVLCharacter(NVLCharacter):
        def __init__(self,*args,profile="generic",**kwargs):
            super(TPSNVLCharacter,self).__init__(*args,**kwargs)
            self.profile = profile                                  # this tells the TPS which character profile to use

    class TPSCharacter(object):
        def __init__(self,name=NotSet,*args,**kwargs):
            self.profile = kwargs.pop("profile","generic")

# fallback for lazy users who forget to use the correct params when instancing the TPSCharacter ;)
            if "what_suffix" in kwargs.keys() and not "what_speech_suffix" in kwargs.keys():
                self.what_speech_prefix = kwargs.pop("what_suffix")
            else:
                self.what_speech_suffix = kwargs.pop("what_speech_suffix",_TPS_SUFFIXES["speech"])
            if "what_prefix" in kwargs.keys() and not "what_speech_suffix" in kwargs.keys():
                self.what_speech_prefix = kwargs.pop("what_prefix")
            else:
                self.what_speech_prefix = kwargs.pop("what_speech_prefix",_TPS_PREFIXES["speech"])

            self.what_think_prefix = kwargs.pop("what_think_prefix",_TPS_PREFIXES["think"])
            self.what_think_suffix = kwargs.pop("what_think_suffix",_TPS_SUFFIXES["think"])
            self.nick = kwargs.pop("nick",name)

# initialize all TPS parameters for this character
            TPS_character_checkin(self)

# build character objects
            self.adv = ADVCharacter(name,*args,**kwargs)
            self.nvl = NVLCharacter(name,kind=nvl,*args,**kwargs)

# this allows the TPSCharacter object to inherit methods from the active character
        def __getattr__(self, name):
            return getattr(
                getattr(self, store.presentation_mode),
                name
            )

# this makes the TPSCharacter callable so that say.execute won't complain about me passing a non-callable object
        def __call__(self, *args, **kwargs):
            return getattr(
                self,
                store.presentation_mode
            )(*args, **kwargs)

############################################################################################################################
#
# this class handles grouping characters into different shared_state groups, each group transitioning independently
#
############################################################################################################################
    class SharedGroup:
        def __init__(self, *params):                        # input: a set of (character,mood,lines) triplets
            self.triplets = []                              # initializes the triplets array
            for t in params:
                if len(t) == 2:
                    self.triplets.append((t[0],t[1],0))
                else:
                    self.triplets.append(t)
            self.shared = True                              # use it only when sharing transition state across multiple character
            if _DEBUG:
# debugging step: check the SharedGroup's actual content
                for triplet in self.triplets:
                    print("SharedGrouup has: ",repr(triplet))

############################################################################################################################
#
# this class is used by the TPS phone suite to store a text message data **** WIP WIP WIP WIP WIP ****
#
############################################################################################################################
    class PhoneMsg:
        def __init(self, text, sender, timestamp="11:26"):
            self.text = text
            self.sender = sender
            self.timestamp = timestamp
            self.state = "sent"                 # accepted states: "sent", "received", "read"
            self.height = Text(self.text,style="phone_text",xmax=_DEFAULT_PHONE_BUBBLE_WIDTH).size()[1]