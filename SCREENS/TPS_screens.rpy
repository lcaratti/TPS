init offset = -1

################################################################################
## TYPING SCREEN FOR THE CHAT PARSER
################################################################################
screen typing(who_color,what_color):
    #zorder 100
    window:
        id "typing_window"
        style "typing_window"


        if store.typing_who is not None:

            window:
                id "typing_namebox"
                style "namebox":
                    color who_color
                text typing_who id "typing_who"


        text "typing" + "." * store.typing_dots:
            id "typing_what"
            style "say_dialogue":
                color what_color
        timer 0.4 repeat True action SetVariable("typing_dots",(store.typing_dots % 3) + 1)

style typing_window is window:
    background None
style typing_say is default:
    background None