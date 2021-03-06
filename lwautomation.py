class LWAutomation:
    def __init__(self, title: str, screen_width: int,
                 screen_heigth: int):
        self._title = title
        self._screen_width = screen_width
        self._screen_heigth = screen_heigth
        self._result = []
        self._spells_this_turn = 0
        self._attacks_this_turn = 0

    @property
    def result(self):
        return self._result

    def _click(self, x, y, radius, min_time, max_time):
        self._result.append(f"RRclick({x}, {y}, {radius})")
        self._result.append(f"randsleep({min_time}, {max_time})")

    def _translate_coords(self, x, y, radius):
        return (x * self._screen_width / _mesurements_taken_x,
                (y) * self._screen_heigth / _mesurements_taken_y,
                radius * self._screen_width / _mesurements_taken_x)

    def _relative_click(self, x, y, radius, min_time, max_time):
        x, y, radius = self._translate_coords(x, y, radius)
        self._click(x, y, radius, min_time, max_time)

    def _open_spell_menu(self):
        self._relative_click(47, 339, 15, 1, 2)

    def use_spellcard(self, spellcard_num: int):
        self._open_spell_menu()
        self._spells_this_turn += 1
        x, y = _spell_card_points_coords[spellcard_num]
        self._relative_click(x, y, 40, 1, 2)

    def use_attack(self, attack_num: int):
        self._attacks_this_turn += 1
        x, y = _attack_coords[attack_num]
        self._relative_click(x, y, 40, 1, 2)

    def _format_output_string(self):
        res = header.format(self._title)
        for string in self._result:
            res = res + "\n" + string
        return res

    def create_script(self, script_path="script.ahk"):
        result = self._format_output_string()
        with open(script_path, "w") as file:
            file.write(result)

    def power_up(self, n):
        for _ in range(n):
            self._relative_click(765, 415, 40, 1, 2)

    def graze(self, n):
        for _ in range(n):
            self._relative_click(825, 290, 40, 1, 2)

    def use_skills(self, *args):
        self._relative_click(875, 380, 10, 1, 2)
        for arg in args:
            self._relative_click(_skills[arg], 430, 10, 1, 2)
            self._relative_click(555, 400, 10, 1, 2)
        self._relative_click(875, 380, 10, 2, 3)

    def restart_after_battle(self):
        self._sleep(5, 10)
        self._relative_click(130, 470, 10, 3, 4)
        self._relative_click(130, 470, 10, 5, 10)

    def swap_char(self):
        self._relative_click(805, 51, 10, 4, 6)

    def _sleep(self, min, max):
        self._result.append(f"randsleep({min}, {max})")

    def end_turn(self, max_enemy_attacks=None, max_enemy_spells=3):

        min = (self._attacks_this_turn + max_enemy_attacks) * 6  # wait for all attacks
        min += (self._spells_this_turn + max_enemy_spells) * 12  # wait for all spells
        max = min * 1.2
        self._sleep(min, max)

    def loop(self, n):
        return _Loop(n, self)


class _SyntaxOperation():
    def __init__(self, target: LWAutomation):
        self._target = target
        self._start_pos = len(target.result) + 1

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i in range(self._start_pos, len(self._target.result)):
            self._target.result[i] = "    " + self._target.result[i]
        self._target.result.append("}")


class _Loop(_SyntaxOperation):
    def __init__(self, n, target: LWAutomation):
        super().__init__(target)
        self._n = n

    def __enter__(self):
        self._target.result.append(f"loop, {self._n} {{")


_mesurements_taken_x = 960.
_mesurements_taken_y = 550.
_spell_card_points_coords = [(155, 273),
                             (298, 180),
                             (440, 140),
                             (585, 170),
                             (725, 160)
                             ]
_attack_coords = [(240, 430),
                  (550, 430)]
_skills = [144, 208, 276, 390, 457, 525, 640, 706, 775]
header = """#NoEnv
; #Warn
SendMode Input
SetWorkingDir %A_ScriptDir%
RRClick(pointx, pointy, radius)
{{
    double_rad := radius * radius
    Random, rad, 0, %double_rad%
    Random, Angle, 0, 6
    
    rad := Sqrt(rad)
    OutX := Sin(Angle) * rad + pointx
    OutY := Cos(Angle) * rad + pointy
    ControlClick, {},, Left, 1,  x%OutX% y%OutY% NA
    Sleep, 10
}}
randsleep(min, max)
{{
    min := min * 1000
    max := max * 1000
    Random, rand, min, max
    sleep, rand
}}"""
