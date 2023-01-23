import os
import shutil
import sys

import pytest
from cologs import COLOGS_FILE, COLOGS_FOLDER, get_cologs

STDOUT_FILE = "stdout.log"


def test_levels_stdout():
    errors = []

    levels = ("Debug", "Info", "Warning", "Error", "Critical")

    log_path = os.path.join(COLOGS_FOLDER, STDOUT_FILE)

    cologs = get_cologs()
    cologs.debug("")
    cologs.info("")
    cologs.warning("")
    cologs.error("")
    cologs.critical("")

    with open(log_path, "r") as f:
        lines = f.readlines()
        for level, line in zip(levels, lines):
            level_ = level.lower()
            line_ = line.strip().lower()
            if level_ not in line_:
                errors.append(f"{level_} level not found in {line_}.")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_levels_file():
    errors = []

    levels = ("Debug", "Info", "Warning", "Error", "Critical")

    log_path = os.path.join(COLOGS_FOLDER, COLOGS_FILE)

    cologs = get_cologs()
    cologs.debug("")
    cologs.info("")
    cologs.warning("")
    cologs.error("")
    cologs.critical("")

    with open(log_path, "r") as f:
        lines = f.readlines()
        for level, line in zip(levels, lines):
            level_ = level.lower()
            line_ = line.strip().lower()
            if level_ not in line_:
                errors.append(f"{level_} level not found in {line_}.")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_messages_stdout():
    errors = []

    messages = ("Check", "My", "Testing", "Message", "Out")

    log_path = os.path.join(COLOGS_FOLDER, STDOUT_FILE)

    cologs = get_cologs()
    cologs.debug(messages[0])
    cologs.info(messages[1])
    cologs.warning(messages[2])
    cologs.error(messages[3])
    cologs.critical(messages[4])

    with open(log_path, "r") as f:
        lines = f.readlines()
        for message, line in zip(messages, lines):
            line_ = line.strip()
            if message not in line_:
                errors.append(f"{message} level not found in {line_}.")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_messages_file():
    errors = []

    messages = ("Check", "My", "Testing", "Message", "Out")

    log_path = os.path.join(COLOGS_FOLDER, COLOGS_FILE)

    cologs = get_cologs()
    cologs.debug(messages[0])
    cologs.info(messages[1])
    cologs.warning(messages[2])
    cologs.error(messages[3])
    cologs.critical(messages[4])

    with open(log_path, "r") as f:
        lines = f.readlines()
        for message, line in zip(messages, lines):
            line_ = line.strip()
            if message not in line_:
                errors.append(f"{message} level not found in {line_}.")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_same_outputs():
    messages = ("Check", "My", "Testing", "Message", "Out")

    log_file_path = os.path.join(COLOGS_FOLDER, COLOGS_FILE)
    log_stdout_path = os.path.join(COLOGS_FOLDER, STDOUT_FILE)

    cologs = get_cologs()
    cologs.debug(messages[0])
    cologs.info(messages[1])
    cologs.warning(messages[2])
    cologs.error(messages[3])
    cologs.critical(messages[4])

    with open(log_file_path, "r") as f:
        file_lines = f.readlines()
    with open(log_stdout_path, "r") as f:
        stdout_lines = f.readlines()

    for file_line, stdout_line in zip(file_lines, stdout_lines):
        assert file_line == stdout_line


@pytest.fixture(autouse=True)
def test_folder_fixture():
    if not os.path.exists(COLOGS_FOLDER):
        os.makedirs(COLOGS_FOLDER)
    with open(os.path.join(COLOGS_FOLDER, STDOUT_FILE), "w") as sys.stdout:
        yield
    shutil.rmtree(COLOGS_FOLDER)
