import argparse
from typing import List, Mapping, Union

from common import log_error_and_exit
from wiring import ROTORS


class KeySheet:
    def __init__(self, parsed_args: argparse.Namespace) -> None:
        self.plugboard_wiring = self.__validate_and_parse_plugboard_pairs(
            parsed_args.plugboard_pairs
        )
        self.ring_settings = self.__validate_ring_settings(parsed_args.ring_settings)
        self.rotor_order = self.__validate_rotor_order(parsed_args.rotor_order)
        self.rotor_positions = self.__validate_rotor_positions(
            parsed_args.rotor_positions
        )

    def __validate_and_parse_plugboard_pairs(
        self, plugboard_pairs: Union[None, str]
    ) -> Mapping[str, str]:
        if not plugboard_pairs:
            return {}

        ERROR_MESSAGE = "Invalid plugboard pairs"
        PLUGBOARD_PAIRS_MAX = 10

        plugboard_pairs_list = plugboard_pairs.split(",")
        for pair in plugboard_pairs_list:
            # Check that the "pair" is in fact a pair of letters.
            if len(pair) != 2 or not pair.isalpha():
                log_error_and_exit(ERROR_MESSAGE)

        if len(plugboard_pairs_list) != len(set(plugboard_pairs_list)):
            log_error_and_exit(ERROR_MESSAGE)

        if len(plugboard_pairs_list) > PLUGBOARD_PAIRS_MAX:
            log_error_and_exit(ERROR_MESSAGE)

        plugboard_pairs_dict = {pair[0]: pair[1] for pair in plugboard_pairs_list}
        plugboard_pairs_dict_keys = list(plugboard_pairs_dict.keys())
        for letter in plugboard_pairs_dict_keys:
            # Connecting a letter to multiple other letters isn't physically possible
            # on the machine.
            if plugboard_pairs_dict_keys.count(letter) != 1:
                log_error_and_exit(ERROR_MESSAGE)

        plugboard_pairs_dict_reversed = {
            pair[1]: pair[0] for pair in plugboard_pairs_list
        }

        # Ensure bidirectionality of the plugboard wiring by merging the two dicts.
        return plugboard_pairs_dict | plugboard_pairs_dict_reversed

    def __validate_ring_settings(self, ring_settings: str) -> str:
        ERROR_MESSAGE = "Invalid ring settings"
        RING_SETTINGS_NUM = 3

        ring_settings_list = ring_settings.split(",")
        if len(ring_settings_list) != RING_SETTINGS_NUM:
            log_error_and_exit(ERROR_MESSAGE)

        for setting in ring_settings_list:
            # The setting is always a two-digit number, e.g. 1 is 01.
            if len(setting) != 2:
                log_error_and_exit(ERROR_MESSAGE)
            # Each number is mapped to a letter, hence the range.
            elif int(setting) < 1 and int(setting) > 26:
                log_error_and_exit(ERROR_MESSAGE)

        return ring_settings

    def __validate_rotor_order(self, rotor_order: str) -> List[str]:
        ERROR_MESSAGE = "Invalid rotor order"
        ROTORS_NUM = 3

        rotor_order_list = rotor_order.split(",")
        if len(rotor_order_list) != ROTORS_NUM:
            log_error_and_exit(ERROR_MESSAGE)

        for rotor in rotor_order_list:
            if rotor not in ROTORS.keys():
                log_error_and_exit(ERROR_MESSAGE)
            # 1 rotor per slot (duh).
            elif rotor_order_list.count(rotor) > 1:
                log_error_and_exit(ERROR_MESSAGE)

        return rotor_order_list

    def __validate_rotor_positions(self, rotor_positions: str) -> str:
        ROTOR_POSITIONS_NUM = 3

        if len(rotor_positions) != ROTOR_POSITIONS_NUM or not rotor_positions.isalpha():
            log_error_and_exit("Invalid rotor positions")

        return rotor_positions
