# Overview

When we download books they come with the names formatted as the publisher or
site determines.  This isn't always the best format or easily searchable. Thus
we want to have a small program that is giving a file directory and list of
book name mappings from the directory and what they should be named.

# Expected Final Format

1. Every words first letter is capitalized
2. Underscores between all words, editions, and volumes
3. Journals append the conference initials, year and volume
   ```
   Cybersecurity For Computer Science ITCS 2023 Volume 1
   ```
4. Editions are referenced with (2nd), (3rd), (5th), etc
   __First editions do not need to be identified__

# Workflow

1. Generate an index for the location of files to be renamed.
   ```
   ebook_rename.py -ed directory_of_ebooks
   ```
2. This will generate an ebook_index.csv file, unless -eio value was specified.
3. Edit the ebook_index file
    - Replace the CSV header with New_Filename
    - Remove any quotes, dashes, apostrophes
    - Remove the first and second columns, leaving you only with the existing filename
    - Edit the filenames to their expected values
    - Save these changes to another file, such as ebook_index_modified.csv
    - Do not save the current changes made to ebook_index.csv
4. Use the paste command to append the modified file to the original ebook_index.csv
   ```
   paste -d ',' ebook_index.csv ebook_index_modified.csv > ebook_index_final.csv
   ```
5. Remove the newlines (^M) that the paste command adds. (Vim command)
   ```
   %s/^M//g
   ```
6. Import the new final index which should have the Secure Hash, Directory Location, 
   Filename, New_Filename headers. Debug (-d) can be specified to see the process.
   ```
   ebook_rename.py -ei ebook_index_final.csv
   ```
7. A rename log is generated which will produce an index with the newly named file.
   This is done so that you can fix any renames by simply importing the rename index
   file and the old name will be re-applied.

## Options

To see all options available you can provide the (-h) flag.

```
usage: ebook_rename.py [-h] [--debug] [--ebook-directory [EBOOK_DIRECTORY]] [--ebook-index-output [EBOOK_INDEX_OUTPUT]]
                       [--ebook-index-input [EBOOK_INDEX_INPUT]] [--quiet]

Index and rename ebooks to formatted filenames.

optional arguments:
  -h, --help            show this help message and exit
  --debug, -d           Enable debug logging output.
  --ebook-directory [EBOOK_DIRECTORY], -ed [EBOOK_DIRECTORY]
                        Directory where ebooks to be indexed and renamed are located on the local system.
  --ebook-index-output [EBOOK_INDEX_OUTPUT], -eio [EBOOK_INDEX_OUTPUT]
                        Name of ebook index output file to be modified for file rename.
  --ebook-index-input [EBOOK_INDEX_INPUT], -ei [EBOOK_INDEX_INPUT]
                        Name of index to be used for checking duplicates or source index for renaming filename.
  --quiet, -q           Only outputs index progress
```

## Vim Commands

*Disclaimer:* This may not be the most efficient use of commands but they will accomplish what you need.

### Remove Commas, Quotes, Underscores, Extra spaces

#### Commas

```
%s/,//g
```
#### Quotes 

Remove quotes.
```
%s/"//g
```
#### Underscores 

Underscores removed.
```
%s/_//g
```

Underscores remove and replaced with space.
```
%s/_/ /g
```

#### Extra spaces 

Any combination of two spaces is replaced with a single space.
```
%s/  / /g
```

#### Remove the secure hash and file directory entries

This matches the secure hash and the current directory structure that you are in.
You can modify the the forward slashes(/) and word(``\w*``) combinations to match
the directory structure as there could be more depth or less. 

```
%s/\v^([a-z]|\d).*,\/\w*\/\w*\/\w*.\w*\/\w*\/\w*\,//gc
```

#### Capitalize the first letter of each word.

This works best if you have removed all other underscores, commas, etc so that the
filename resembles something similar to ``This is the Books current Filename.pdf``
Underscores and dashes can change how the individual words are interpreted causing
first letters to be skipped.

```
%s/\v<(.)(\w*) /\u\1\L\2 /g
```
