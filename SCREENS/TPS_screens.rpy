init offset = -1

################################################################################
## TYPING SCREEN FOR THE CHAT PARSER
################################################################################
screen typing(chat_who_name,chat_who_color):
    zorder 100
    window:
        style "typing_window"

        window:
            id "typing_namebox"
            style "typing_namebox"    
            text chat_who_name:
                style "typing_label"
                color chat_who_color
            
        text "typing" + "." * store.typing_dots:
            style "typing_dialogue"
        timer 0.4 repeat True action SetVariable("typing_dots",(store.typing_dots +1) % 4)

style typing_window is window:
    background Null()

style typing_namebox is namebox:
    background Null()

style typing_label is say_label

style typing_dialogue is say_dialogue