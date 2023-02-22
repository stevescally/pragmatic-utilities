#!/usr/bin/env python

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

