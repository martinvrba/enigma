import argparse
import logging
import sys
from typing import List, Mapping, Union

import wiring

logger = logging.getLogger(__name__)


class KeySheet:
    def __init__(self, parsed_args: argparse.Namespace) -> None:
        self.plugboard_wiring = self._validate_and_parse_plugboard_pairs(
            parsed_args.plugboard_pairs
        )
        self.ring_settings = self._validate_ring_settings(parsed_args.ring_settings)
        self.rotor_order = self._validate_rotor_order(parsed_args.rotor_order)
        self.rotor_positions = self._validate_rotor_positions(
            parsed_args.rotor_positions
        )

    def _log_error_and_exit(self, error_message: str):
        logger.error(error_message)
        sys.exit(1)

    def _validate_and_parse_plugboard_pairs(
        self, plugboard_pairs: Union[None, str]
    ) -> Mapping[str, str]:
        if not plugboard_pairs:
            return {}

        error_message = "Invalid plugboard pairs"

        plugboard_pairs_list = plugboard_pairs.split(",")

        for pair in plugboard_pairs_list:
            if len(pair) != 2:
                self._log_error_and_exit(error_message)

        if len(plugboard_pairs_list) > 10:
            self._log_error_and_exit(error_message)

        if len(plugboard_pairs_list) != len(set(plugboard_pairs_list)):
            self._log_error_and_exit(error_message)

        plugboard_pairs_dict = {pair[0]: pair[1] for pair in plugboard_pairs_list}
        plugboard_pairs_dict_keys = list(plugboard_pairs_dict.keys())

        for letter in plugboard_pairs_dict_keys:
            if plugboard_pairs_dict_keys.count(letter) != 1:
                self._log_error_and_exit(error_message)

        plugboard_pairs_dict_reversed = {
            pair[1]: pair[0] for pair in plugboard_pairs_list
        }

        # Ensure bidirectionality of the plugboard wiring by merging the two dicts.
        return plugboard_pairs_dict | plugboard_pairs_dict_reversed

    def _validate_ring_settings(self, ring_settings: str) -> str:
        error_message = "Invalid ring settings"

        setting_count = 0

        for setting in ring_settings.split(","):
            if setting_count > 3:
                self._log_error_and_exit(error_message)
            elif len(setting) != 2:
                self._log_error_and_exit(error_message)
            elif int(setting) < 1 and int(setting) > 26:
                self._log_error_and_exit(error_message)

        return ring_settings

    def _validate_rotor_order(self, rotor_order: str) -> List[str]:
        error_message = "Invalid rotor order"

        rotor_order_list = rotor_order.split(",")

        if len(rotor_order_list) != 3:
            self._log_error_and_exit(error_message)

        for rotor in rotor_order_list:
            if rotor not in wiring.ROTORS.keys():
                self._log_error_and_exit(error_message)
            elif rotor_order_list.count(rotor) > 1:
                self._log_error_and_exit(error_message)

        return rotor_order_list

    def _validate_rotor_positions(self, rotor_positions: str) -> str:
        if len(rotor_positions) == 3 and rotor_positions.isalpha():
            return rotor_positions
        else:
            self._log_error_and_exit("Invalid rotor positions")
