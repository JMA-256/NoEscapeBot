#!/bin/env python

"""
NoEscapeBot - global access point status tracking

Authors:
    jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "NoEscapeBot"

ACCESS_POINTS = [
    "concourse-escalator-up",
    "concourse-escalator-down",
    "concourse-lift",
    "mquni-escalator-up",
    "mquni-escalator-down",
    "mquni-lift",
    "mqcentre-escalator-up",
    "mecentre-escalator-down",
    "mqcentre-lift",
]


class Statuses:

    def __init__(self) -> None:
        self._statuses = {ap: True for ap in ACCESS_POINTS}

    def get_status(self, access_point: str) -> str:
        """
        Returns the status of a given access point, either 'working' or 'broken'.
        Throws a KeyError if the given access point is invalid.
        """
        if access_point not in ACCESS_POINTS:
            raise KeyError(f"invalid access point: {access_point}")
        return "working" if self._statuses[access_point] else "broken"

    def get_all_statuses(self) -> dict[str, str]:
        """
        Returns the statuses of all access points.
        """
        return {self.get_status(ap) for ap in ACCESS_POINTS}

    def set_status(self, access_point: str, is_working: bool) -> None:
        """
        Updates the status of the given access point to the target status.
        Throws a KeyError if the given access point is invalid.
        """
        if access_point not in ACCESS_POINTS:
            raise KeyError(f"invalid access point: {access_point}")
        self._statuses[access_point] = is_working
