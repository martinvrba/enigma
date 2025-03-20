#!python3

import argparse
import logging
import sys

from enigma import Machine
from key_sheet import KeySheet

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Enigma I Cipher Device Simulator")
    arg_parser.add_argument("plaintext", help="text to process", type=str)
    arg_parser.add_argument(
        "-g",
        "--rotor-positions",
        default="EAB",
        help="Grundstellung (e.g. ABC)",
        type=str,
    )
    arg_parser.add_argument(
        "--rotor-order", default="I,II,III", help="Walzenlage (e.g. I,II,III)", type=str
    )
    arg_parser.add_argument(
        "--ring-settings",
        default="01,01,01",
        help="Ringstellung (e.g. 01,13,26)",
        type=str,
    )
    arg_parser.add_argument(
        "--plugboard-pairs",
        help="Steckerbrett (e.g. AZ,BY,CX... up to 10 pairs)",
        type=str,
    )
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug mode"
    )
    parsed_args = arg_parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if parsed_args.debug else logging.INFO)

    key_sheet = KeySheet(parsed_args)
    enigma_machine = Machine(key_sheet)

    ciphertext = ""
    for letter in "".join(
        [char.upper() for char in parsed_args.plaintext if char.isalpha()]
    ):
        enigma_machine.keyboard(letter)
        ciphertext += enigma_machine.lampboard()

    i = 0
    for letter in ciphertext:
        print(letter, end="")
        i += 1
        if i % 5 == 0:
            print(" ", end="")
    print()

    sys.exit(0)
