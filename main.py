#!python3

import argparse
import logging
import sys

import enigma

# TODO: Load the settings from a YAML file.
SETTINGS = {
    "plugboard_wiring": "AZ,BY,CX",
    "rotor_order": "I,II,III",
    "rotor_start_pos": "E,A,B",
}


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Enigma I Cipher Device Simulator")
    arg_parser.add_argument("plaintext", help="the input text to process")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug mode"
    )
    args = arg_parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    em = enigma.Machine(SETTINGS)

    ciphertext = ""
    for letter in "".join([char.upper() for char in args.plaintext if char.isalpha()]):
        em.keyboard(letter)
        ciphertext += em.lampboard()

    i = 0
    for letter in ciphertext:
        print(letter, end="")
        i += 1
        if i % 5 == 0:
            print(" ", end="")
    print()

    sys.exit(0)
