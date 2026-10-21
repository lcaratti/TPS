init offset = -1

################################################################################
## TYPING SCREEN FOR THE CHAT PARSER
################################################################################
screen typing(who_name,who_color):
    #zorder 100
    window:
        style "typing_window"

        window:
            style "typing_namebox":
                color who_color
            text who_name id "typing_who"

        text "typing" + "." * store.typing_dots:
            style "typing_say_dialogue"
        timer 0.4 repeat True action SetVariable("typing_dots",(store.typing_dots % 3) + 1)

style typing_window is say_window:
    background Null()
style typing_namebox is namebox:
    background Null()
style typing_say_dialogue is say_dialogue:
    background Null()
