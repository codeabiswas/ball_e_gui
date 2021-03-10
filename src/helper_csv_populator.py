import csv
import datetime
import os
from pathlib import Path


def main(dirname):
    location = str(Path.home()) + \
        '/Documents/ball_e_profiles/' + dirname

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


if __name__ == "__main__":
    main("goalie_profiles")
