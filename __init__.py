import nuke
import sys
import time
module_path = '/home/shrimo/project'
if module_path not in sys.path:
    sys.path.append(module_path)

from amg_system import qt
# from amg.system import qt

import switch_menubar


def add_callback():
    nuke.addOnCreate(switch_menubar.on_node_create, nodeClass='Switch')
    nuke.addOnDestroy(switch_menubar.on_node_create, nodeClass='Switch')
    nuke.addKnobChanged(switch_menubar.on_node_rename, nodeClass='Switch')


def remove_callback():
    nuke.removeOnCreate(switch_menubar.on_node_create, nodeClass='Switch')
    nuke.removeOnDestroy(switch_menubar.on_node_create, nodeClass='Switch')
    nuke.addKnobChanged(switch_menubar.on_node_rename, nodeClass='Switch')


def set_menu():
    sys.stderr.write('AMG Switch start\n')
    nuke.addOnCreate(add_callback, nodeClass='Root')
    nuke.addOnDestroy(remove_callback, nodeClass='Root')
