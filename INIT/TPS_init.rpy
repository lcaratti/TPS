init -50 python:
# Cry "Havoc," and let slip the dogs of war!
    initialize_TPS()

init python:

# this makes sure I use the rhythmic_say function when it's time to invoke renpy.exports.say
    renpy.exports.say = TPS_say                                # this is ****CRITICAL**** !!!!!!!!!!!!!!!!!

# required by the TPS parser even if fonts are NOT variable
    if not hasattr(gui,"text_axis"):
        gui.text_axis = {}
    if "weight" not in gui.text_axis:
        gui.text_axis["weight"] = None

    TPS_charprofiles_checkin()