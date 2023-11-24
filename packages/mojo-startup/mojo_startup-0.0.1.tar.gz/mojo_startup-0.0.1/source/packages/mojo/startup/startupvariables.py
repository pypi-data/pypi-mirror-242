"""
.. module:: startupvariables
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the most basic variables required to begin the startup
               of a customized mojo environment.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


import os

class MOJO_STARTUP_VARIABLES:

    MJR_NAME = "mjr"
    if "MJR_NAME" in os.environ:
        MJR_NAME = os.environ["MJR_NAME"]

    MJR_HOME_DIRECTORY = os.path.expanduser(os.path.join("~", MJR_NAME))
    if "MJR_HOME_DIRECTORY" in os.environ:
        MJR_HOME_DIRECTORY = os.environ["MJR_HOME_DIRECTORY"]
        MJR_HOME_DIRECTORY = os.path.abspath(os.path.expandvars(os.path.expanduser(MJR_HOME_DIRECTORY)))

    MJR_STARTUP_SETTINGS = os.path.join(MJR_HOME_DIRECTORY, "settings.ini")
    if "MJR_STARTUP_SETTINGS" in os.environ:
        MJR_STARTUP_SETTINGS = os.environ["MJR_STARTUP_SETTINGS"]
        MJR_STARTUP_SETTINGS = os.path.abspath(os.path.expandvars(os.path.expanduser(MJR_STARTUP_SETTINGS)))
