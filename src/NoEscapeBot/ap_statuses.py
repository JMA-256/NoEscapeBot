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

from datetime import datetime
from discord import User

ACCESS_POINTS = [
    "concourse-escalator-up",
    "concourse-escalator-down",
    "concourse-lift",
    "mquni-escalator-up",
    "mquni-escalator-down",
    "mquni-lift",
    "mqcentre-escalator-up",
    "mqcentre-escalator-down",
    "mqcentre-lift",
]

VERIFICATION_THRESHOLD = 2
DEFAULT_USER = "System"


class Statuses:

    def __init__(self) -> None:
        self._statuses = {ap: True for ap in ACCESS_POINTS}
        self._timestamp_reported = {ap: None for ap in ACCESS_POINTS}
        self._timestamp_verified = {ap: None for ap in ACCESS_POINTS}
        self._users = {ap: None for ap in ACCESS_POINTS}
        self._votes = {ap: 0 for ap in ACCESS_POINTS}

    def get_status(self, access_point: str) -> str:
        """
        Returns the following for each access point:

          "is_working": the current status,
          "reported":   the timestamp of the last update
                        (or None, if there has been no reports yet),
          "verified":   the timestamp of verification
                        (or None, if it is not verified),
          "user":       the user who reported it as a string
                        (or 'System' if there is none), and
          "votes":      the current number of votes it has.

        * Throws a KeyError if the given access point is invalid.
        """
        if access_point not in ACCESS_POINTS:
            raise KeyError(f"invalid access point: {access_point}")
        return {
            "is_working": self._statuses[access_point],
            "reported": self._timestamp_reported[access_point],
            "verified": self._timestamp_verified[access_point],
            "user": self._stringify_user(self._users[access_point]),
            "votes": self._votes[access_point],
        }

    def _stringify_user(self, user: User) -> str:
        if user is None:
            return DEFAULT_USER
        username = User.name
        discriminator = f"#{User.discriminator}" if User.discriminator != 0 else ""
        return f"{username}{discriminator}"

    def is_verified(self, access_point):
        """
        Returns True if the access point votes meet
        VERIFICATION_THRESHOLD.

        * Throws a KeyError if the given access point is invalid.
        """
        if access_point not in ACCESS_POINTS:
            raise KeyError(f"invalid access point: {access_point}")
        return self._votes[access_point] >= VERIFICATION_THRESHOLD

    def get_all_statuses(self) -> dict[str, str]:
        """
        Returns the statuses and verification timestamps of all
        access points.
        """
        return {ap: self.get_status(ap) for ap in ACCESS_POINTS}

    def set_status(
        self, access_point: str, is_working: bool, reporting_user: User
    ) -> None:
        """
        Updates the status, reported timestamp (to the current time),
        and the user, and resets verification and votes.

        * Throws a KeyError if the given access point is invalid.
        * Throws a ValueError if the target status already matches
          the stored status.
        """
        if access_point not in ACCESS_POINTS:
            raise KeyError(f"invalid access point: {access_point}")
        if self._statuses[access_point] == is_working:
            raise ValueError(
                f"{is_working} has already been reported for '{access_point}'."
            )
        current_timestamp = datetime.timestamp(datetime.now())
        self._statuses[access_point] = is_working
        self._timestamp_reported[access_point] = current_timestamp
        self._timestamp_verified[access_point] = None
        self._users[access_point] = reporting_user
        self._votes[access_point] = 0

    def update(self):
        """
        Updates the verification statuses for all access points.
        Intended mainly for internal use, but can be invoked by
        client for manual updates.

        * If the votes reach VERIFICATION_THRESHOLD, and the
          current verification status is None, it's set to
          the current timestamp.
        * else it's set to None.

        * Throws a KeyError if the given access point is invalid.
        """
        for access_point in ACCESS_POINTS:
            if self._votes[access_point] >= VERIFICATION_THRESHOLD:
                if self._timestamp_verified[access_point] is None:
                    current_timestamp = datetime.timestamp(datetime.now())
                    self._timestamp_verified[access_point] = current_timestamp
            else:
                self._timestamp_verified[access_point] = None

    def verify_status(self, access_point: str) -> bool:
        """
        Increments the vote of the access point's report by one,
        and updates verification statuses with update(self).

        * Throws a KeyError if the given access point is invalid.
        """
        if access_point not in ACCESS_POINTS:
            raise KeyError(f"invalid access point: {access_point}")
        self._votes[access_point] += 1
        self.update()

    def unverify_status(self, access_point: str):
        """
        Decrements the vote of the access point's report by one,
        and updates the verification timestamp (to None) if the
        votes do not meet VERIFICATION_THRESHOLD.

        * Throws a KeyError if the given access point is invalid.
        """
        if access_point not in ACCESS_POINTS:
            raise KeyError(f"invalid access point: {access_point}")
        self._votes[access_point] -= 1
        self.update()


def _test() -> None:
    """
    Private testing function - please do not call.
    """
    from pprint import pprint
    from time import sleep
    print("### This is a sample REPL-style usage of the ap_statuses module. ###")
    print("\n# Initialising object\n")
    print(">>> s = Statuses()")
    s = Statuses()
    print(">>> s.get_all_statuses()\n")
    pprint(s.get_all_statuses())
    print("\n# New report that mquni-lift is down")
    print("# NOTE: the User object is not properly set up for this test.\n")
    class User:
        def __init__(self):
            self.name = "Clyde"
            self.discriminator = 0
    print(">>> s.set_status('mquni-lift', False, User())")
    s.set_status("mquni-lift", False, User())
    print(">>> s.get_status('mquni-lift')\n")
    pprint(s.get_status("mquni-lift"))
    print("\n# Votes coming in\n")
    print(f">>> for i in range(0, {VERIFICATION_THRESHOLD}): # verification threshold")
    print("...     s.verify_status('mquni-lift')")
    for i in range(0, VERIFICATION_THRESHOLD):
        s.verify_status('mquni-lift')        
    print(">>> s.get_status('mquni-lift')\n")
    pprint(s.get_status("mquni-lift"))
    print("\n# Some time passes...")
    sleep(1)
    print("# Manual update\n")
    print(">>> s.update()")
    print(">>> s.get_status('mquni-lift')\n")
    pprint(s.get_status("mquni-lift"))
    print("## Notice how the update didn't re-refresh the timestamp -\n## it only does it when it's None.")
    print("\n# Someone takes away vote\n")
    print(">>> s.unverify_status('mquni-lift')")
    s.unverify_status('mquni-lift')
    print(">>> s.get_status('mquni-lift')\n")
    pprint(s.get_status("mquni-lift"))
    print()

if __name__ == "__main__":
    _test()
