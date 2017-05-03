# :copyright: Copyright (c) 2016 ftrack

import functools

import MaxPlus
import ftrack
import os
from PySide import QtCore
from ftrack_connect.ui.widget.asset_manager import FtrackAssetManagerDialog
from ftrack_connect.ui.widget.import_asset import FtrackImportAssetDialog
from ftrack_connect_3dsmax.legacy.connector import Connector
from ftrack_connect_3dsmax.legacy.connector.maxcallbacks import *
from ftrack_connect_3dsmax.legacy.ui.publisher import PublishAssetDialog
from ftrack_connect_3dsmax.legacy.ui.tasks import FtrackTasksDialog

from ftrack_connect_3dsmax.legacy.ui.info import FtrackMaxInfoDialog

try:
    ftrack.setup()
except Exception:
    pass

class LegacyFtrackMenuBuilder(object):
    '''Build the Ftrack menu.'''
    MENU_NAME = 'Ftrack'

    def __init__(self):
        '''Initialize the menu builder.'''
        if MaxPlus.MenuManager.MenuExists(self.MENU_NAME):
             MaxPlus.MenuManager.UnregisterMenu(self.MENU_NAME)

        self.__menu_builder = MaxPlus.MenuBuilder(self.MENU_NAME)

    def add_separator(self):
        '''Add a separator between menu items.'''
        self.__menu_builder.AddSeparator()

    def add_item(self, action):
        '''Add a menu item.'''
        self.__menu_builder.AddItem(action)

    def create(self):
        '''Create the Ftrack menu.'''
        self.__menu_builder.Create(MaxPlus.MenuManager.GetMainMenu())

    def __del__(self):
        '''Unregister the Ftrack menu.'''
        MaxPlus.MenuManager.UnregisterMenu(self.MENU_NAME)

class LegacyDisableMaxAcceleratorsEventFilter(QtCore.QObject):
    """An event filter that disables the 3ds Max accelerators while a widget is
    visible. This class is used when running in Max 2016, where widgets cannot
    be parented to Max's main window, and as a result they don't get the
    keyboard focus unless Max accelerators are disabled.
    """
    def eventFilter(self, obj, event):
        '''Enable / disable Max accelerators when a widget is shown / hidden.'''
        if event.type() == QtCore.QEvent.Show:
            MaxPlus.Core.EvalMAXScript('enableAccelerators = false')
        elif event.type() == QtCore.QEvent.Close:
            MaxPlus.Core.EvalMAXScript('enableAccelerators = true')
        elif event.type() == QtCore.QEvent.Hide:
            MaxPlus.Core.EvalMAXScript('enableAccelerators = true')

        return False

connector = Connector()
legacyFtrackMenuBuilder = None

currentEntity = ftrack.Task(
    os.getenv('FTRACK_TASKID',
    os.getenv('FTRACK_SHOTID')))

# Dialogs.
legacyImportAssetDialog = None
legacyPublishAssetDialog = None
legacyAssetManagerDialog = None
legacyInfoDialog = None
legacyTasksDialog = None

def __isMax2017():
    '''Return True if the 3ds Max version is 2017'''
    vers = MaxPlus.Core.EvalMAXScript('getFileVersion "$max/3dsmax.exe"').Get()
    return vers.startswith('19')

def __createAndInitFtrackDialog(Dialog):
    '''Create an instance of a dialog and initialize it for use in 3ds Max'''
    dialog = Dialog(connector=connector)

    try:
        # AttachQWidgetToMax is only available in Max 2017 and newer.
        MaxPlus.AttachQWidgetToMax(dialog, isModelessDlg=True)
    except AttributeError:
        # If running 2016, the dialog cannot be parented to Max's window.
        dialog.installEventFilter(
            LegacyDisableMaxAcceleratorsEventFilter(dialog))

    # Make the dialog initial size bigger, as in Max by default they appear too small.
    dialog.resize(dialog.width(), 1.7 * dialog.height())
    return dialog

def __legacyCreateDialogAction(actionName, callback):
    '''Create an action and add it to the menu builder if it is valid'''
    global legacyFtrackMenuBuilder

    action = MaxPlus.ActionFactory.Create(
        'ftrack_legacy_' + actionName, actionName, callback)
    if action._IsValidWrapper():
        legacyFtrackMenuBuilder.add_item(action)
        return action

def showImportAssetDialog():
    '''Create the import asset dialog if it does not exist and show it'''
    global legacyImportAssetDialog

    if not legacyImportAssetDialog:
        legacyImportAssetDialog = __createAndInitFtrackDialog(FtrackImportAssetDialog)

    # Add some extra margins to the import asset dialog under 3ds Max 2017.
    if __isMax2017():
        legacyImportAssetDialog.mainLayout.setContentsMargins(5, 5, 5, 5)

    legacyImportAssetDialog.show()

def showPublishAssetDialog():
    '''Create the publish asset dialog if it does not exist and show it'''
    global legacyPublishAssetDialog

    if not legacyPublishAssetDialog:
        legacyPublishAssetDialog = __createAndInitFtrackDialog(functools.partial(
            PublishAssetDialog, currentEntity=currentEntity))

    # Add some extra margins to the import asset dialog under 3ds Max 2017.
    if __isMax2017():
        legacyPublishAssetDialog.mainLayout.setContentsMargins(5, 5, 5, 5)

    legacyPublishAssetDialog.show()

def showAssetManagerDialog():
    '''Create the asset manager dialog if it does not exist and show it'''
    global legacyAssetManagerDialog

    if not legacyAssetManagerDialog:
        legacyAssetManagerDialog = __createAndInitFtrackDialog(FtrackAssetManagerDialog)

        # Make some columns of the asset manager dialog wider to compensate
        # for the buttons appearing very small with Max's 2017 custom Qt stylesheet.
        tableWidget = legacyAssetManagerDialog.assetManagerWidget.ui.AssertManagerTableWidget
        tableWidget.setColumnWidth(0, 25)
        tableWidget.setColumnWidth(9, 35)
        tableWidget.setColumnWidth(11, 35)
        tableWidget.setColumnWidth(15, 35)

    legacyAssetManagerDialog.show()

def showInfoDialog():
    '''Create the info dialog if it does not exist and show it'''
    global legacyInfoDialog

    if not legacyInfoDialog:
        legacyInfoDialog = __createAndInitFtrackDialog(FtrackMaxInfoDialog)

    legacyInfoDialog.show()

def showTasksDialog():
    '''Create the tasks dialog if it does not exist and show it'''
    global legacyTasksDialog

    if not legacyTasksDialog:
        legacyTasksDialog = __createAndInitFtrackDialog(FtrackTasksDialog)

    legacyTasksDialog.show()


def initFtrackLegacy():
    '''Initialize Ftrack, register assets and build the Ftrack menu.'''
    connector.registerAssets()

    global legacyFtrackMenuBuilder
    legacyFtrackMenuBuilder = LegacyFtrackMenuBuilder()

    __legacyCreateDialogAction("Import Asset", showImportAssetDialog)
    __legacyCreateDialogAction("Publish Asset", showPublishAssetDialog)
    legacyFtrackMenuBuilder.add_separator()

    # Save the showAssetManagerAction for later use.
    showAssetManagerAction = __legacyCreateDialogAction(
        "Asset Manager", showAssetManagerDialog)

    legacyFtrackMenuBuilder.add_separator()
    __legacyCreateDialogAction("Info", showInfoDialog)
    __legacyCreateDialogAction("Tasks", showTasksDialog)

    # Create the Ftrack menu.
    legacyFtrackMenuBuilder.create()

    registerMaxOpenFileCallbacks(showAssetManagerAction)

    # Send usage event.
    from ftrack_connect_3dsmax.legacy.connector import usage
    usage.send_event('USED-FTRACK-CONNECT-3DS-MAX')

initFtrackLegacy()
