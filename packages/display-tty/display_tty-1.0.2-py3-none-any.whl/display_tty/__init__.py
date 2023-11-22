"""
File in charge linking of the disp file ot the module so that it could be imported as a module
"""

from .my_disp import Disp

SUCCESS = 0
ERR = 84
ERROR = 84

TOML_CONF = {
    'PRETTIFY_OUTPUT': True,
    'PRETTY_OUTPUT_IN_BLOCS': True,
    'MESSAGE_CHARACTER': '@',
    'MESSAGE_ERROR_CHARACTER': '#',
    'MESSAGE_INFORM_CHARACTER': 'i',
    'MESSAGE_QUESTION_CHARACTER': '?',
    'MESSAGE_SUCCESS_CHARACTER': '/',
    'MESSAGE_WARNING_CHARACTER': '!',
    'SUB_SUB_TITLE_WALL_CHARACTER': '*',
    'SUB_TITLE_WALL_CHARACTER': '@',
    'TITLE_WALL_CHARACTER': '#',
    'TREE_COLUMN_SEPERATOR_CHAR': '│',
    'TREE_LINE_SEPERATOR_CHAR': '─',
    'TREE_NODE_CHAR': '├',
    'TREE_NODE_END_CHAR': '└',
    'MESSAGE_ANIMATION_DELAY_BLOCKY': 0.01,
    'MESSAGE_ANIMATION_DELAY': 0.01
}

SAVE_TO_FILE = False
FILE_NAME = "run_results.txt"
FILE_DESCRIPTOR = None


IDISP = Disp(
    TOML_CONF,
    SAVE_TO_FILE,
    FILE_NAME,
)

IDISPLAY = IDISP
IDISPTTY = IDISP
IDTTY = IDISP


class Display(Disp):
    """ A rebind of the class named Disp """


class DispTTY(Disp):
    """ A rebind of the class named Disp """


class DisplayTTY(Disp):
    """ A rebind of the class named Disp """
