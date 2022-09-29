#!/usr/bin/env python3

from pathlib import Path
import os
from distutils.dir_util import copy_tree
from argparse import ArgumentParser
from configparser import ConfigParser


def backup(pathSource: Path, pathArchive: Path):
    status = False
    while True:
        pathArchiveRecord = pathArchive / input("Name: ")
        if pathArchiveRecord.exists():
            print("There is an existing directory with the same name!")
            op = input("Overwrite/abort/rename? ([o]/a/r)").lower()
            if op.startswith('a'):
                break
            elif op.startswith('r'):
                continue
        else:
            pathArchiveRecord.mkdir(parents=True)
        copy_tree(str(pathSource), str(pathArchiveRecord))
        status = True
        break
    return status


def restore(pathSource: Path, pathArchive: Path):
    records = list(filter(
        lambda subdir: os.path.isdir(pathArchive / subdir),
        os.listdir(pathArchive)
    ))
    if len(records) == 0:
        print("No backups available!")
        return
    print("Existing backups:\nID\tName")
    for i, record in enumerate(records):
        print("%d\t%s" % (i, record))
    while True:
        recordID = int(input("ID: "))
        if recordID < 0 or recordID >= len(records):
            print("Invalid ID!")
        else:
            break
    pathArchiveRecord = pathArchive / str(records[recordID])
    copy_tree(str(pathArchiveRecord), str(pathSource))


def reset(pathSource: Path, pathTemplate: Path):
    copy_tree(str(pathTemplate), str(pathSource))


def archive(pathSource: Path, pathArchive: Path, pathTemplate: Path):
    if backup(pathSource, pathArchive):
        reset(pathSource, pathTemplate)


COMMAND = "command"


class Command:
    BACKUP = "backup"
    RESTORE = "restore"
    RESET = "reset"
    ARCHIVE = "archive"


class Argument:
    ARCHIVE = "archive"
    SOURCE = "source"
    TEMPLATE = "template"


class Config:
    archive = Path("archive/default")
    source = Path("source")
    template = Path("template")

    def __str__(self):
        return f"(archive: {self.archive}, source: {self.source}, template: {self.template})"


def parse_args(config: Config) -> str:
    parser = ArgumentParser(description="The Archiver.")
    parser.add_argument(
        COMMAND, type=str, metavar="<command>",
        choices=[Command.BACKUP, Command.RESTORE, Command.RESET, Command.ARCHIVE]
    )
    parser.add_argument(
        "--source", type=Path, metavar="<source directory>", dest=Argument.SOURCE
    )
    parser.add_argument(
        "--archive", type=Path, metavar="<archive directory>", dest=Argument.ARCHIVE
    )
    parser.add_argument(
        "--template", type=Path, metavar="<template directory>", dest=Argument.TEMPLATE
    )
    args = vars(parser.parse_args())
    if args.get(Argument.SOURCE) is not None:
        config.source = args.get(Argument.SOURCE)
    if args.get(Argument.TEMPLATE) is not None:
        config.template = args.get(Argument.TEMPLATE)
    if args.get(Argument.ARCHIVE) is not None:
        config.archive = args.get(Argument.ARCHIVE)
    return args.get(COMMAND)


SECTION_PATHS = "Paths"


def load_config() -> Config:
    config = Config()
    parser = ConfigParser()
    if len(parser.read("archiver.ini", "utf-8")) == 0:
        return config
    if not parser.has_section(SECTION_PATHS):
        return config
    paths = parser[SECTION_PATHS]
    if paths.get(Argument.SOURCE) is not None:
        config.source = Path(paths.get(Argument.SOURCE))
    if paths.get(Argument.TEMPLATE) is not None:
        config.template = Path(paths.get(Argument.TEMPLATE))
    if paths.get(Argument.ARCHIVE) is not None:
        config.archive = Path(paths.get(Argument.ARCHIVE))
    return config


def main():
    config = load_config()
    command = parse_args(config)
    if command == Command.BACKUP:
        backup(config.source, config.archive)
    elif command == Command.RESTORE:
        restore(config.source, config.archive)
    elif command == Command.RESET:
        reset(config.source, config.template)
    elif command == Command.ARCHIVE:
        archive(config.source, config.archive, config.template)
    else:
        print("Unknown command: " + command)
        return


if __name__ == '__main__':
    main()
