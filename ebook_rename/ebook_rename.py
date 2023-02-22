#!/usr/bin/env python
'''
Imports
-------
os:       Module used for directory structure, file input/output.
csv:      Module used for read/write CSV formatted files.
logging:  Python logging handler for debug, info, warning messages.
hashlib:  Module to generate sha256 hashes
argparse: Module providing option input values and help output.
rich.*:   Module used to provide status feedback and functionality
          to the script.


'''

import os
import csv
import logging
import hashlib
import argparse
from rich.progress import track
from rich.logging import RichHandler


def write_index(_index_filename, _index_headers, _index):
    '''
    Write generated index data containing the secure hash,
    directory path and filename. This CSV can then be read 
    in to perform the specified renaming of the current 
    filename to the new filename.

    Parameters
    ----------

    _index_filename: Default or user provided filename to
                     write out index in CSV format.

    _index: Generated index from the build_index function.

    '''

    LOG.info('Writing index to output file in CSV format\n')
    #index_fields = ['SHA256', 'Path', 'Filename']

    with open(_index_filename, 'w') as f:
        write = csv.writer(f)
        write.writerow(_index_headers)
        write.writerows(_index)


def gen_sha256(_file):

    '''
    Generate sha256 secure hash for passed file.
    Return generated secure hash value.

    Parameters
    ----------

    _file: absolute file path to object being hashed.

    '''

    LOG.debug('Generating secure hashes')
    with open(_file, 'rb') as f:
        data = f.read()
        sha256hash = hashlib.sha256(data).hexdigest()

    return sha256hash


def build_input_index(_index_filename):
    ''' 
    Read in passed CSV formatted file that serves as index file to build.

    Parameters:
    -----------

    _index_filename: Specified index from command line input

    '''

    LOG.debug('Reading in provided index file %s', _index_filename)
    with open(_index_filename, 'r') as f:
        csv_reader = csv.reader(f)
        index = list(csv_reader)

    # Remove CSV header from the new index.
    index.pop(0)

    return index 


def build_index(_ebook_dir):

    '''
    Create index of current ebooks with their directory path,
    filename and generated sha256 secure hash value.

    Parameters
    ----------

    _ebook_dir: The absolute directory path where the items to
                be indexed are located. This specified by the
                user with the -fd argument flag.
    '''

    index = []

    LOG.info("File Scanning, secure hash, index generation.")
    for dirpath, dirnames, filename in track(os.walk(_ebook_dir)):
        for f in filename:
            if '.DS_Store' in f:
                LOG.debug('Removing .DS_Store directory')
            else:
                absolute_f_path = os.path.join(dirpath, f)
                index_values = []
                LOG.debug('Creating absolute file path.')
                LOG.debug('Building local file list.')
                index_values.append(gen_sha256(absolute_f_path))
                index_values.append(dirpath)
                index_values.append(f)
                LOG.debug('Generating secure hash(SHA256): %s', index_values[1])
                LOG.debug('Logged index value is: %s', index_values)
                index.append(index_values)
                LOG.debug('New index length: %d', len(index))
                LOG.debug('Adding index values to list main list: %s', index)
                # print(f'{os.path.join(dirpath, f)}')
    LOG.info('Index Build Completed. (%d Files)', len(index))

    return index


def file_rename(_index, _ebook_index_input_filename):

    '''
    For the files in the index rename them to the value found in the new_filename 
    column. Write out a reverse index of the renamed file and its previous filename.
    '''

    rename_index = []

    for sh,path,filename,new_filename in track(_index):
        LOG.debug('Secure Hash: \t%s',sh)
        LOG.debug('Path: \t%s', path)
        LOG.debug('Filename: \t%s', filename)
        LOG.debug('New Filename: %s', new_filename)

        # Test if filename exists before renaming it.
        LOG.info('Checking if %s exists', filename)
        if os.path.isfile(os.path.join(path,filename)):
            LOG.info('Filename exists, renaming')
            os.rename(os.path.join(path,filename),os.path.join(path,new_filename))
            if gen_sha256(os.path.join(path,new_filename)) == sh:
                LOG.info('Secure hashes match. Adding entry to rename index')
                # Build reverse index of secure hash, path, filename, old_filename
                index_values = []
                index_values.append(sh)
                index_values.append(path)
                index_values.append(new_filename)
                index_values.append(filename)
                rename_index.append(index_values)
                LOG.debug(rename_index)

        elif os.path.isfile(os.path.join(path,new_filename)):
            LOG.info('%s has already been renamed.', new_filename)

        else:
            LOG.info('%s does not exist.', filename)


    return rename_index


def main():

    parser = argparse.ArgumentParser(
             description="Index and rename ebooks to formatted filenames.")

    parser.add_argument('--debug', '-d', action='store_true',
                        help='Enable debug logging output.')

    parser.add_argument('--ebook-directory', '-ed',
                        nargs='?',
                        help='Directory where ebooks to be indexed and renamed\
                              are located on the local system.')

    parser.add_argument('--ebook-index-output', '-eio',
                        nargs='?',
                        default='ebook_index.csv',
                        help='Name of ebook index output file to be modified \
                              for file rename.')

    parser.add_argument('--ebook-index-input', '-ei',
                        nargs='?',
                        help='Name of index to be used for checking duplicates or \
                              source index for renaming filename.')

    parser.add_argument('--quiet', '-q', action='store_true', default=False,
                        help='Only outputs index progress')

    args = parser.parse_args()

    # Logging Handler
    global LOG
    log_format = "%(asctime)s - %(message)s"
    log_level = logging.INFO

    if args.debug and not args.quiet:
        log_level = logging.DEBUG

    if args.quiet:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level, format=log_format, datefmt=None, handlers=[RichHandler(show_time=False)])
    LOG = logging.getLogger("rich")
    LOG.debug("Global logger configured.")
    LOG.debug(LOG)

    # Verify provided arguments
    LOG.debug('Provided command-line arguments: %s', args)

    '''
    Scenarios:

    1. If ebook_index_input is specified we don't want to scan for files and build and index as
       one has already been provided. Read in the provided file and build the index then proceed
       to renaming files.
    2. If the ebook_directory is provided, we want to scan the provided directory location and
       build an index of the found files. Then write out the files to a CSV formatted file.
    '''

    LOG.debug('Checking if index input provided')
    if args.ebook_index_input:
        LOG.debug('Building index from provided CSV file.')
        index = build_input_index(args.ebook_index_input)
        LOG.debug(index)
        LOG.debug('Calling file renaming function.')
        rename_index = file_rename(index,args.ebook_index_input)
        if len(rename_index) > 0: 
            LOG.debug('Rename Index Size: %d, writing index.', len(rename_index))
            index_headers = ['SHA256', 'Path', 'Filename', 'Old_Filename']
            write_index('rename_record_' + args.ebook_index_input, index_headers, rename_index)

    else:
        LOG.debug('Index file not provided, building index from os.walk.')
        # Build index file
        index = build_index(args.ebook_directory)

        # Write index to CSV file to add new file names
        LOG.debug('Input index file not specified, writing new index output.')
        LOG.info('Writing ebook index file.')
        index_headers = ['SHA256', 'Path', 'Filename']
        write_index(args.ebook_index_output, index_headers, index)
    

if __name__ == "__main__":
    main()
