# special screen for the TPS's text effects WYSIWYG editor

################################################################################
## Initialization
################################################################################

init offset = -1

################################################################################
## The actual screen
################################################################################
style wysisyg_slider is mmorpg_slider:
    xmaximum 200
    ymaximum 20
screen TPS_editor():
    frame:
        xalign 0.02
        yalign 0.02
        hbox:
            spacing 15
            vbox:
                text "{u}{b}Base text params{/b}{/u}"
                hbox:
                    spacing 14
                    text "Text size: "
                    textbutton "-" action(SetVariable("text_size", max(text_size-1,-12)))
                    text " [text_size] "
                    textbutton "+" action(SetVariable("text_size", min(text_size+1,12)))
                vbox:
                    hbox:
                        spacing 13
                        text "{i}Text color{/i}"
                        frame:
                            background Solid(rgb2hex(text_col_r,text_col_g,text_col_b,text_col_a))
                            xsize 24
                            ysize 24
                    hbox:
                        text "R:"
                        bar:
                            style "wysisyg_slider"
                            value VariableValue("text_col_r",255)
                    hbox:
                        text "G:"
                        bar:
                            style "wysisyg_slider"
                            value VariableValue("text_col_g",255)
                    hbox:
                        text "B:"
                        bar:
                            style "wysisyg_slider"
                            value VariableValue("text_col_b",255)
                    hbox:
                        text "A:"
                        bar:
                            style "wysisyg_slider"
                            value VariableValue("text_col_a",255)
            vbox:
                hbox:
                    spacing 14
                    text "Glow radius: "
                    textbutton "-" action(SetVariable("glow_radius", max(glow_radius-1,0)))
                    text " [glow_radius] "
                    textbutton "+" action(SetVariable("glow_radius", min(glow_radius+1,20)))
                hbox:
                    spacing 14
                    text "Glow sigma: "
                    textbutton "-" action(SetVariable("glow_sigma", max(glow_sigma-0.1,0)))
                    text " [glow_sigma] "
                    textbutton "+" action(SetVariable("glow_sigma", min(glow_sigma+0.1,15)))
                hbox:
                    spacing 13
                    text "{i}Glow color{/i}"
                    frame:
                        background Solid(rgb2hex(glow_grad1_r,glow_grad1_g,glow_grad1_b,glow_grad1_a))
                        xsize 24
                        ysize 24
                hbox:
                    text "R:"
                    bar:
                        style "wysisyg_slider"
                        value VariableValue("glow_grad1_r",255)
                hbox:
                    text "G:"
                    bar:
                        style "wysisyg_slider"
                        value VariableValue("glow_grad1_g",255)
                hbox:
                    text "B:"
                    bar:
                        style "wysisyg_slider"
                        value VariableValue("glow_grad1_b",255)
                hbox:
                    text "A:"
                    bar:
                        style "wysisyg_slider"
                        value VariableValue("glow_grad1_a",255)
    text build_test_line():
        yalign 0.5
        xalign 0.5