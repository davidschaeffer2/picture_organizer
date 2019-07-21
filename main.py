import datetime
import shutil
import sys
from pathlib import Path

import os


def main():
    """
    Runs the script.
    """
    file_blacklist = ['desktop.ini', '.dropbox']
    __USAGE__ = f'Usage: main.py <dir_to_sort> <dir_to_move_sorted_pics>'
    if len(sys.argv) != 3:
        sys.exit(f'Missing directory:\n{__USAGE__}')
    dir_to_sort = sys.argv[1]
    dir_to_move_sorted_pics = sys.argv[2]
    if ensure_dest_dir_exists(dir_to_move_sorted_pics):
        try:
            with os.scandir(dir_to_sort) as files:
                for entry in files:
                    if entry.is_file() and entry.name not in file_blacklist:
                        sort_file(entry, dir_to_move_sorted_pics)
        except FileNotFoundError as e:
            sys.exit(f'Could not find the directory.\n{e}')
    else:
        sys.exit(f'Error when creating source directory.')
    return


def ensure_dest_dir_exists(dir_to_move_sorted_pics):
    """
    If the destination directory does not exists, creates it and returns True.
    If the destination directory exists, returns True.
    If the destination directory cannot be created, returns False and prints error.
    """
    try:
        os.mkdir(f'{dir_to_move_sorted_pics}')
        return True
    except FileExistsError:
        return True
    except Exception as e:
        # Catching generic exception here as I don't know what else it'll possibly
        # fail for. But I need to catch it and return False so I can handle the file
        # manually.
        sys.stderr.write('Exception occurred when trying to make source directory:\n'
                         f'{e}')
        return False


def sort_file(picture: os.DirEntry, dir_to_move_to: str):
    """
    Grabs date from name of file, calls methods to ensure path is created, moves file
    to destination directory.
    :param picture: The os.DirEntry object of the file to be moved.
    :param dir_to_move_to: The destination directory.
    :return: None
    """
    date_of_picture = picture.name.split('_')[0]
    try:
        year = date_of_picture[:4]  # [:N] = items beginning to N-1
        #print(f'Year: {year}')
        month = date_of_picture[4:6]
        #print(f'Month: {month}')
        day = date_of_picture[6:]
        #print(f'Day: {day}')
        date_obj = datetime.date(int(year), int(month), int(day))
        picture_destination = f'{dir_to_move_to}\\{year}\\{date_obj.strftime("%B")}'
        if (ensure_year_dir_exists(dir_to_move_to, year) and
                ensure_month_dir_exists(dir_to_move_to, year, date_obj.strftime("%B"))):
            shutil.move(picture.path, picture_destination)
    except ValueError as e:
        sys.stderr.write(f'Error when getting date of file:\n{e}\n'
                         f'File: {picture.path}\n')
        return  # Just skip to next file.

    return


def ensure_year_dir_exists(dir_to_move_to, year):
    """
    If the year directory does not exists, creates it and returns True.
    If the year directory exists, returns True.
    If the year directory cannot be created, returns False and prints error.
    """
    try:
        os.mkdir(f'{dir_to_move_to}\\{year}')
        return True
    except FileExistsError:
        return True
    except Exception as e:
        # Catching generic exception here as I don't know what else it'll possibly
        # fail for. But I need to catch it and return False so I can handle the file
        # manually.
        sys.stderr.write('Exception occurred when trying to make directory for year:\n'
                         f'{e}')
        return False


def ensure_month_dir_exists(dir_to_move_to, year, month):
    """
    If the month directory does not exists, creates it and returns True.
    If the month directory exists, returns True.
    If the month directory cannot be created, returns False and prints error.
    """
    try:
        os.mkdir(f'{dir_to_move_to}\\{year}\\{month}')
        return True
    except FileExistsError:
        return True
    except Exception as e:
        # Catching generic exception here as I don't know what else it'll possibly
        # fail for. But I need to catch it and return False so I can handle the file
        # manually.
        sys.stderr.write('Exception occurred when trying to make directory for year:\n'
                         f'{e}')
        return False


if __name__ == '__main__':
    main()
