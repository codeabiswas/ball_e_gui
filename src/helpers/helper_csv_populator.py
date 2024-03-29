"""
helper_csv_populator.py
---
This is a helper file that is not used by the GUI. Its sole purpose is top populate goalie and drill profiles for tessting.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

import csv
import datetime
import os
import random
from pathlib import Path


def main(dirname):
    """main.

    Main prototype/testing area. Code prototyping and checking happens here. 

    :param dirname: String with either Goalie or Drill Profiles
    """
    location = str(Path.home()) + \
        '/Documents/ball_e_profiles/' + dirname

    if dirname == "goalie_profiles":
        # Go through each directory in the goalie_profiles directory and populate with a .csv file
        for r, _, profile_infos in os.walk(location):
            for each_profile_info in profile_infos:
                with open(os.path.join(r, each_profile_info), 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow(
                        ["Drill Name", "Date Completed (Most recent prioritized)"])
                    for counter in range(50):
                        curr_date = datetime.datetime.today() - datetime.timedelta(days=counter)
                        format_date = curr_date.strftime('%m/%d/%Y')
                        writer.writerow(
                            ["Drill {}".format(counter+1), format_date])

    elif dirname == "drill_profiles":
        location_choices = ["TL", "TM", "TR",
                            "CL", "CR", "CM", "BL", "BM", "BR"]
        speed_choices = [i for i in range(30, 101, 5)]

        # Go through each directory in the drill_profiles directory and populate with a .csv file
        for r, _, profile_infos in os.walk(location):
            for each_profile_info in profile_infos:
                with open(os.path.join(r, each_profile_info), 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow(
                        ["Ball #", "Targeted Area", "Speed", "Rate of Fire"])
                    for counter in range(36):
                        writer.writerow(
                            [counter+1, random.choice(location_choices), random.choice(
                                speed_choices), "10"]
                        )


if __name__ == "__main__":
    # Run the main function
    # main("goalie_profiles")
    main("drill_profiles")
