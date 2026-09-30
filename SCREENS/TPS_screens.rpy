init offset = -1

################################################################################
## TYPING SCREEN FOR THE CHAT PARSER
################################################################################
screen typing(who):
    #zorder 100
    window:
        id "typing_window"
        style "typing_window"


        if store.typing_who is not None:

            window:
                id "typing_namebox"
                style "namebox"
                text typing_who:

                    id "typing_who"
                    style store.typing_who_args.get("style", "default")
                    color store.typing_who_args.get("color", gui.text_color)


        text "typing" + "." * store.typing_dots:
            id "typing_what"
            style "say_dialogue"
        timer 0.3 repeat True action SetVariable("typing_dots",(store.typing_dots % 3) + 1)

style typing_window is window
style typing_say is default