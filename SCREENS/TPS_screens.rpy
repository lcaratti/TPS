init offset = -1

################################################################################
## TYPING SCREEN FOR THE CHAT PARSER
################################################################################
screen typing():
    #zorder 100
    window:
        id "typing_window"
        style "typing_window"

        window:
            id "typing_namebox"
            style "typing_namebox"    
            text store.chat_who_name:
                id "chat_who"
                style say
                color store.chat_who_color
            
        text "typing" + "." * store.typing_dots:
            id "fake_what"
            style "typing_dialogue"
        timer 0.4 repeat True action SetVariable("typing_dots",(store.typing_dots % 3) + 1)

style typing_window is window:
    background Null()

style typing_namebox is namebox:
    background Null()

style typing_dialogue is say_dialogue