from typing import cast, Mapping, Union

from common import logger
from key_sheet import KeySheet
from wiring import REFLECTOR, ROTORS


class Machine:
    def __init__(self, key_sheet: KeySheet) -> None:
        self.letter = ""
        self.name = "Enigma I"
        self.plugboard_wiring = key_sheet.plugboard_wiring
        self.ring_settings = key_sheet.ring_settings
        self.rotor_order = key_sheet.rotor_order
        self.rotor_positions = key_sheet.rotor_positions
        self.scrambled_letter = ""

        logger.debug(f"Initialized {self.name} machine")

        self.rotor_r = Rotor(
            "right",
            self.rotor_positions[2],
            ROTORS[self.rotor_order[2]],
        )
        self.rotor_m = Rotor(
            "middle",
            self.rotor_positions[1],
            ROTORS[self.rotor_order[1]],
        )
        self.rotor_l = Rotor(
            "left",
            self.rotor_positions[0],
            ROTORS[self.rotor_order[0]],
        )
        self.plugboard = Plugboard(self.plugboard_wiring)
        self.reflector = Reflector(REFLECTOR["wiring"])

    def _scramble_letter(self) -> None:
        self.scrambled_letter = self.plugboard.scramble_letter(self.scrambled_letter)

        if self.rotor_r.is_notch_aligned:
            self.rotor_m.step(1)
            self.rotor_r.step(1)
        elif self.rotor_m.is_notch_aligned:
            self.rotor_l.step(1)
            # "Double stepping" the middle rotor.
            self.rotor_m.step(1)
            self.rotor_r.step(1)
        else:
            self.rotor_r.step(1)

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
    def __init__(self, slot: str, position: str, wiring: Mapping[str, str]) -> None:
        self.is_notch_aligned = cast(bool, None)
        self.notch = wiring["notch"]
        self.slot = slot
        self.wiring = wiring["wiring"]
        self.position = self.wiring[0]

        self.step(position)

    def step(self, value: Union[int, str]) -> None:
        if isinstance(value, str):
            # Calculate the distance between the letters in the wiring.
            value = self.wiring.find(value) - self.wiring.find(self.position)

        for i in range(value):
            # Move the first letter to the end.
            self.wiring += self.wiring[0]
            self.wiring = self.wiring[1:]

        self.position = self.wiring[0]
        self.is_notch_aligned = True if self.position == self.notch else False

    def scramble_letter(self, letter: str) -> str:
        # Subtracting 65 gives the letter's position in the alphabet.
        return self.wiring[ord(letter) - 65]

    def unscramble_letter(self, letter: str) -> str:
        # Adding 65 to the scrambled letter's position in the wiring gives the original letter.
        return chr(self.wiring.find(letter) + 65)
