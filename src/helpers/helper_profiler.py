import csv
import os
from pathlib import Path


class Profiler():
    def __init__(self, dirname):
        self.dirname = dirname

    def get_profiles(self):

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
        with open(profile_path) as file:
            csv_reader = csv.reader(file, delimiter=',')
            row_count = 0
            info_dict = dict()
            if "goalie_profiles" in profile_path:
                for row in csv_reader:
                    if row_count == 0:
                        row_count += 1
                    else:
                        info_dict[row[0]] = row[1]
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
    some_profiler = Profiler("drill_profiles")
    print(some_profiler.get_profiles())
    print(some_profiler.get_profile_info(
        "/home/codeabiswas/Documents/ball_e_profiles/drill_profiles/drill_a/drill_a.csv"))


if __name__ == "__main__":
    main()
