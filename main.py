from lwautomation import LWAutomation

kek = LWAutomation("Qt5QWindowIcon22, (LOST WORD) ahk_class Qt5QWindowIcon ahk_exe MEmu.exe,,", 960, 550)
with kek.loop(5):
    kek.use_attack(0)
    kek.use_attack(1)
    kek.use_attack(1)
    kek.end_turn(max_attacks_expected=1)

kek.create_script()
