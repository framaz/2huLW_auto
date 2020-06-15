# importing the automator
from lwautomation import LWAutomation

# Emu window title, maybe this one even works for you
title = "Qt5QWindowIcon22, (LOST WORD) ahk_class Qt5QWindowIcon ahk_exe MEmu.exe"

# Measured width and heigth of the window you measured before.
width = 751
heigth = 434

# creating automation object
automator = LWAutomation(title, width, heigth)

# creating a script
# for example, we have only one character in the middle with a swap char
# let's do a level 5 times in a loop
# notice that only code wich starts with four spaces is looped
with automator.loop(5):
    # it's our turn
    automator.swap_char()  # swap out the char
    automator.power_up(1)  # use one power
    automator.graze(3)  # use three grazes
    automator.use_spellcard(4)  # use spellcard number 4(LW), notice that numeration starts with 0

    # after we did our, we have to wait till every animation is played
    # for it we call end_turn function
    # we pass two arguments to it: max_enemy_attacks and max_enemy_spells
    # you shoud try to predict it correctly to reduce the waiting time
    # if you can't predict it, you may hust call it without arguments like this:
    # automator.end_turn() - this implies the longes scenario: enemy will do 3 spells
    automator.end_turn(max_enemy_attacks=2, max_enemy_spells=1)

    # next turn
    # use skills
    # this uses first and third spells of the middle character
    automator.use_skills(3, 5)

    # use right attack
    automator.use_attack(1)

    # end turn, we expect all enemies to be dead, so noone attacks
    automator.end_turn(max_enemy_attacks=0, max_enemy_spells=0)

    # then we finish the stage and restart the battle
    automator.restart_after_battle()
# loop ends as there are no more spaces before code

# the following line will create a file "myscript.ahk" with resulting script
# in the app's directory
# call automator.create_script AFTER you wrote you all actions you needed
automator.create_script("myscript.ahk")
