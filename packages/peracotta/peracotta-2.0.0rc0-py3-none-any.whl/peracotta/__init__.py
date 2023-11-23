import os
import signal
import sys
from pathlib import Path

from dotenv import load_dotenv
from peracotta.commons import env_to_bool
from peracotta.constants import logdir_path
from peracotta.gui import GUI
from peracotta.logger import excepthook, logger
from PyQt6 import QtWidgets


def main_gui():
    sys.excepthook = excepthook
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # makes CTRL+C work

    logdir = Path(logdir_path)
    if not logdir.exists():
        os.mkdir(logdir)

    stdout_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "WARNING"
    file_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "INFO"

    log_format = "{time}\t{message}"
    logger.remove()
    logger.add(sys.stdout, format=log_format, level=stdout_level, colorize=True, backtrace=True, diagnose=True)
    logger.add(logdir.joinpath("peracotta.log"), format=log_format, level=file_level)

    # noinspection PyBroadException
    load_dotenv()
    tarallo_url = os.environ["TARALLO_URL"]
    tarallo_token = os.environ["TARALLO_TOKEN"]
    app = QtWidgets.QApplication(sys.argv)
    # This is EXTREMELY IMPORTANT, DON'T TACH [sic], DO NOT REMOVE IT EVER
    # noinspection PyUnusedLocal
    window = GUI(app, tarallo_url, tarallo_token)
    app.exec()


def main_cli():
    print("Sorry, peracruda isn't implemented in v2 yet! Use the old one at https://github.com/WEEE-Open/peracotta")
