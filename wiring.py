from types import MappingProxyType

REFLECTOR = MappingProxyType(
    {
        # Type B
        "wiring": {
            "A": "Y",
            "B": "R",
            "C": "U",
            "D": "H",
            "E": "Q",
            "F": "S",
            "G": "L",
            "H": "D",
            "I": "P",
            "J": "X",
            "K": "N",
            "L": "G",
            "M": "O",
            "N": "K",
            "O": "M",
            "P": "I",
            "Q": "E",
            "R": "B",
            "S": "F",
            "T": "Z",
            "U": "C",
            "V": "W",
            "W": "V",
            "X": "J",
            "Y": "A",
            "Z": "T",
        }
    }
)

ROTORS = MappingProxyType(
    {
        "I": {"notch": "Q", "wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ"},
        "II": {"notch": "E", "wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE"},
        "III": {"notch": "V", "wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO"},
        "IV": {"notch": "J", "wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB"},
        "V": {"notch": "Z", "wiring": "VZBRGITYUPSDNHLXAWMJQOFECK"},
    }
)
