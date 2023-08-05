
# -*- coding: utf-8 -*-
from subprocess import check_output  # call command line
import shutil          # move and delete files/folders
from slurm.files import rm, find


def run(cmd):
    # given a command string, it runs it
    cmd = cmd.split()
    return check_output(cmd).decode("utf8")


def rmdir(path):
    if not isinstance(path, list):
        path = [path]
    for p in path:
        try:
            shutil.rmtree(p)
            # print(p)
        except FileNotFoundError:
            # folder was already deleted or doesn't exist ... it's ok
            pass
    # exit(0)

def cleanup(path, files, folders):
    cup = []
    for f in files:
        cup += find(path, f)
    rm(cup)

    cup = []
    for f in folders:
        cup += find(path, f)
    rmdir(cup)
