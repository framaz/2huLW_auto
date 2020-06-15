class LWAutomation:
    def __init__(self, title: str, screen_width: int,
                 screen_heigth: int, script_path: str = "lwauto.ahk"):
        self._title = title
        self._screen_width = screen_width
        self._screen_heigth = screen_heigth
        self._script_path = script_path
        self._result = []
        self._result.append(header.format(title))
        self._spells_this_turn = 0
        self._attacks_this_turn = 0

    def _click(self, x, y, radius, min_time, max_time):
        self._result.append(f"RRclick({x}, {y}, {radius})")
        self._result.append(f"randsleep({min_time}, {max_time})")

    def _translate_coords(self, x, y, radius):
        return (x * self._screen_width / _mesurements_taken_x,
                y * self._screen_heigth / _mesurements_taken_y,
                radius * self._screen_width / _mesurements_taken_x)

    def _relative_click(self, x, y, radius, min_time, max_time):
        x, y, radius = self._translate_coords(x, y, radius)
        self._click(x, y, radius, min_time, max_time)

    def _open_spell_menu(self):
        self._relative_click(47, 339, 10, 1, 2)

    def use_spellcard(self, spellcard_num: int):
        self._open_spell_menu()
        self._spells_this_turn += 1
        x, y = _spell_card_points_coords[spellcard_num]
        self._relative_click(x, y, 30, 1, 2)

    def use_attack(self, attack_num: int):
        self._attacks_this_turn += 1
        x, y = _attack_coords[attack_num]
        self._relative_click(x, y, 30, 1, 2)


_mesurements_taken_x = 960.
_mesurements_taken_y = 550.
_spell_card_points_coords = [(155, 273),
                             (298, 180),
                             (440, 140),
                             (585, 170),
                             (725, 160)
                             ]
_attack_coords = [(240, 460),
                  (550, 460)]

header = """#NoEnv
; #Warn
SendMode Input
SetWorkingDir %A_ScriptDir%
RRClick(pointx, pointy, radius)
{{
    ranmin := pointx-radius
    ranmax := pointx+radius
    Random, OutX, %ranmin%, %ranmax%
    VarY := (radius**2-(OutX-pointx)**2)**(1/2)+pointy
    VarY := Round(varY)
    YDist := VarY-PointY
    YDist := 2*YDist
    Random, Subval, 0, %Ydist%
    OutY :=PointY-Subval
    ControlClick, {0} Left, 1,  x%OutX% y%OutY% NA
    Sleep, 10
}}
randsleep(min, max)
{{
    min := min * 1000
    max := max * 1000
    Random, rand, min, max
    sleep, rand
}}"""
