import logging

from typing import Mapping, Union

import wiring

logger = logging.getLogger(__name__)

class Machine:
    def __init__(self, settings: Mapping[str, str]) -> None:
        self.name = "Enigma I"
        logger.debug(f"Initializing {self.name} machine ...")
        # Ensure bidirectionality of the plugboard wiring by merging the two dicts.
        self.plugboard_wiring = {
            item[0]: item[1] for item in settings["plugboard_wiring"].split(",")
        } | {item[1]: item[0] for item in settings["plugboard_wiring"].split(",")}
        self.rotor_start_pos = settings["rotor_start_pos"].split(",")
        self.rotor_order = settings["rotor_order"].split(",")

        self.letter = ""
        self.scrambled_letter = ""

        self.rotor_r = Rotor(
            wiring.ROTORS[self.rotor_order[2]]["notch_pos"],
            "right",
            self.rotor_start_pos[2],
            wiring.ROTORS[self.rotor_order[2]]["wiring"],
        )
        self.rotor_m = Rotor(
            wiring.ROTORS[self.rotor_order[1]]["notch_pos"],
            "middle",
            self.rotor_start_pos[1],
            wiring.ROTORS[self.rotor_order[1]]["wiring"],
        )
        self.rotor_l = Rotor(
            wiring.ROTORS[self.rotor_order[0]]["notch_pos"],
            "left",
            self.rotor_start_pos[0],
            wiring.ROTORS[self.rotor_order[0]]["wiring"],
        )
        self.plugboard = Plugboard(self.plugboard_wiring)
        self.reflector = Reflector(wiring.REFLECTOR["wiring"])

    def _scramble_letter(self) -> None:
        self.scrambled_letter = self.plugboard.scramble_letter(self.scrambled_letter)

        if self.rotor_r.is_notch_aligned:
            self.rotor_m.shift_position(1)
            self.rotor_r.shift_position(1)
        elif self.rotor_m.is_notch_aligned:
            self.rotor_l.shift_position(1)
            # "Double stepping" the middle rotor.
            self.rotor_m.shift_position(1)
            self.rotor_r.shift_position(1)
        else:
            self.rotor_r.shift_position(1)

        self.scrambled_letter = self.rotor_r.scramble_letter(self.scrambled_letter)
        self.scrambled_letter = self.rotor_m.scramble_letter(self.scrambled_letter)
        self.scrambled_letter = self.rotor_l.scramble_letter(self.scrambled_letter)

        self.scrambled_letter = self.reflector.scramble_letter(self.scrambled_letter)

        self.scrambled_letter = self.rotor_l.unscramble_letter(self.scrambled_letter)
        self.scrambled_letter = self.rotor_m.unscramble_letter(self.scrambled_letter)
        self.scrambled_letter = self.rotor_r.unscramble_letter(self.scrambled_letter)

        self.scrambled_letter = self.plugboard.unscramble_letter(self.scrambled_letter)

    def keyboard(self, key: str) -> None:
        self.letter = key
        self.scrambled_letter = self.letter

        self._scramble_letter()

    def lampboard(self) -> str:
        return self.scrambled_letter


class Plugboard:
    def __init__(self, wiring: Mapping[str, str]) -> None:
        self.wiring = wiring

    def scramble_letter(self, letter: str) -> str:
        return self.wiring[letter] if letter in self.wiring.keys() else letter

    def unscramble_letter(self, letter: str) -> str:
        return self.scramble_letter(letter)


class Reflector:
    def __init__(self, wiring: Mapping[str, str]) -> None:
        self.wiring = wiring

    def scramble_letter(self, letter: str) -> str:
        return self.wiring[letter]


class Rotor:
    def __init__(self, notch_pos: str, slot: str, start_pos: str, wiring: str) -> None:
        self.is_notch_aligned = False
        self.notch_pos = notch_pos
        self.slot = slot
        self.wiring = wiring
        self.position = self.wiring[0]
        self._set_starting_position(start_pos)

    def _set_starting_position(self, start_pos: str) -> None:
        self.shift_position(start_pos)

    def shift_position(self, value: Union[int, str]) -> None:
        if isinstance(value, str):
            # Calculate the distance between the letters in the wiring.
            value = self.wiring.find(value) - self.wiring.find(self.position)
        for i in range(value):
            # Move the first letter to the end.
            self.wiring += self.wiring[0]
            self.wiring = self.wiring[1:]
            self.position = self.wiring[0]
            self.is_notch_aligned = True if self.position == self.notch_pos else False

    def scramble_letter(self, letter: str) -> str:
        # Subtracting 65 gives the letter's position in the alphabet.
        return self.wiring[ord(letter) - 65]

    def unscramble_letter(self, letter: str) -> str:
        # Adding 65 to the scrambled letter's position in the wiring gives the original letter.
        return chr(self.wiring.find(letter) + 65)
