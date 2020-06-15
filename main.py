from lwautomation import LWAutomation

kek = LWAutomation("Qt5QWindowIcon22, (LOST WORD) ahk_class Qt5QWindowIcon ahk_exe MEmu.exe", 960, 550)
with kek.loop(2):
    kek.use_attack(0)
    kek.graze(1)
    kek.swap_char()
    kek.use_spellcard(0)
    kek.graze(1)
    kek.use_attack(0)
    kek.end_turn(max_attacks_expected=1)
    kek.use_attack(1)
    kek.use_skills(3, 4, 5)
    kek.use_spellcard(4)
    kek.use_attack(0)
    kek.end_turn()
    kek.restart_after_battle()

kek.create_script()
