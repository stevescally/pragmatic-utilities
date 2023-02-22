#!/usr/bin/env python

''' 
GPLv3 License

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see https://www.gnu.org/licenses/.

Copyright (C) 2022 Stephen Scally
'''

'''
This script is provided with a dictionary mapping of ripped episodes and 
their expected Plex name.  The script runs through the specified folder
and renames the files accordingly.

For each season the track mappings will have to be provided.
'''

import os
import sys
import argparse


def build_dict(mapping_file):
    d = {}
    with open(mapping_file) as f:
        for line in f:
            (key,val) = line.split(",")
            d[key] = val.strip()
    return d


def rename_files(episode_data, file_dir, file_prefix):
    os.chdir(file_dir)
    for key,val in episode_data.items():
        new_file=(file_prefix + "_E" + val + ".mkv")
        os.rename(key, new_file)
        print("Rename " + key + " -> " + new_file) 


def main():

    parser = argparse.ArgumentParser(description='Rename DVD filenames for Plex.')
    parser.add_argument('-d', '--dir',\
                        dest='directory',\
                        required=True,\
                        help='Directory with files to be renamed')
    parser.add_argument('-m', '--map',\
                        dest='mapping',\
                        required=True,\
                        help='File mapping DVD rip to expected episode')
    parser.add_argument('-p', '--prefix',\
                        dest='prefix',\
                        required=True,\
                        help='The new prefix the dvd file should have\
                        i.e NAME_OF_SERIES_S03')

    args = parser.parse_args()


    ''' Build dictionary of episode info'''
    episode_info = build_dict(args.mapping)


    ''' Rename espisode files for Plex format'''
    rename_files(episode_info, args.directory, args.prefix)


if __name__ == "__main__":
    main()

