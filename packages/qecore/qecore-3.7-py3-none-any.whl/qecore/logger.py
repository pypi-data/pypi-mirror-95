#!/usr/bin/env python3
import logging
import inspect

# Solution provided by https://stackoverflow.com/a/54209647

class Singleton(type):
    """
    Singletop class used as metaclass by :py:class:`logger.QELogger`.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class QELogger(metaclass=Singleton):
    logger = None

    def __init__(self):
        """
        Initiating logger class with some basic logging setup.
        """

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[logging.StreamHandler()])

        self.logger = logging.getLogger("desktopqe")


    @staticmethod
    def __get_call_info():
        """
        Inspecting stack to find the exact place to pass as location of the logger called.

        :rtype: tuple
        :return: Tuple with filename and line number the logger was called from.
        """

        stack = inspect.stack()

        file_name = stack[2][1].split("/")[-1]
        line_length = stack[2][2]

        return file_name, line_length


    def info(self, message, *args):
        """
        Inspecting stack to find the exact place to pass as location of the logger called.

        :rtype: tuple
        :return: Tuple with filename and line number the logger was called from.
        """
        message = "[{}:{:3}] {}".format(*self.__get_call_info(), message)
        self.logger.info(message, *args)
