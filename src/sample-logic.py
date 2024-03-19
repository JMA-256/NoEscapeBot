#!/bin/env python

"""
NoEscapeBot - preliminary logic for core functionality

Authors:
    jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from pprint import pprint

_ACCESS_POINTS = [
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

_is_online = {ap: True for ap in _ACCESS_POINTS}


def get_access_points():
    """
    Returns a list of available access points.
    """
    return _ACCESS_POINTS


def get_status(access_point: str) -> str:
    """
    Returns 'working' or 'broken' for the given
    access point, or raises a ValueError if the
    access point is invalid.
    """
    if access_point not in _ACCESS_POINTS:
        raise ValueError(f"Invalid access point: {access_point}")
    return "working" if _is_online[access_point] else "broken"


if __name__ == "__main__":
    print("Just some code for now -- no main function yet!")
    exit
