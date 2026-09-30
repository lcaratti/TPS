# THIS FILE HOLDS GLOBAL VARIABLES USED BY FUNCTIONS AND THE LIKES OF THAT
# ------------------------------------------------------------------------
# DEBUGGING & PREFERENCES MENU
# ------------------------------------------------------------------------
# Enables debugging mode that will print information on the TPS activity in Ren'Py console
define _DEBUG = False
# Use this to give player the option to turn the TPS ON or OFF from the Preferences Menu
# 0 --> fully disabled
# 1 --> fully enabled
# 2 --> apply text speed only, do not inject pauses
default persistent.dynamic_text_speed = 1