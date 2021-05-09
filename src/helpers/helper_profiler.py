"""
helper_profiler.py
---
This file contains the Profiler class, which is used to interact with Goalie or Drill profiles.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

import csv
import os
from pathlib import Path


class Profiler():
    """Profiler.

    The Profiler class used for interacting with Goalie or Drill profiles
    """

    def __init__(self, dirname):
        """__init__.

        Initializes the Profiler object
        s
        :param dirname: Direction and name of the profile (i.e.: goalie_profiles or drill_profiles)
        """
        self.dirname = dirname

    def get_profiles(self):
        """get_profiles.

        Lists all the profiles in the directory
        """

        location = str(Path.home()) + \
            '/Documents/ball_e_profiles/' + self.dirname
        profile_names = list()
        profile_info = list()
        for r, profile_dirs, profile_infos in os.walk(location):
            for profile_dir in profile_dirs:
                profile_names.append(profile_dir)
            for each_profile_info in profile_infos:
                profile_info.append(os.path.join(r, each_profile_info))

        return {profile_names[i]: profile_info[i] for i in range(len(profile_names))}

    def get_profile_info(self, profile_path):
        """get_profile_info.

        This method retrieves all the profiles info and appropriately puts them in a dictionary object.

        :param profile_path: Profile path containing the profile's .csv file
        """
        with open(profile_path) as file:
            csv_reader = csv.reader(file, delimiter=',')
            row_count = 0
            info_dict = dict()
            if "goalie_profiles" in profile_path:
                for row in csv_reader:
                    if row_count == 0:
                        row_count += 1
                    else:
                        info_dict[row_count] = [row[0], row[1]]
                        # info_dict[row[0]] = row[1]
                        row_count += 1
            elif "drill_profiles" in profile_path:
                for row in csv_reader:
                    if row_count == 0:
                        row_count += 1
                    else:
                        info_dict[row[0]] = [row[1], row[2], row[3]]
                        row_count += 1

        return info_dict


def main():
    """Main prototype/testing area. Code prototyping and checking happens here."""

    some_profiler = Profiler("drill_profiles")
    print(some_profiler.get_profiles())
    print(some_profiler.get_profile_info(
        "/home/codeabiswas/Documents/ball_e_profiles/drill_profiles/drill_a/drill_a.csv"))


if __name__ == "__main__":
    # Run the main function
    main()
