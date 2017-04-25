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

ftrack.setup()

class FtrackMenuBuilder(object):
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

class DisableMaxAcceleratorsEventFilter(QtCore.QObject):
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
ftrackMenuBuilder = None

currentEntity = ftrack.Task(
    os.getenv('FTRACK_TASKID',
    os.getenv('FTRACK_SHOTID')))

# Dialogs.
importAssetDialog = None
publishAssetDialog = None
assetManagerDialog = None
infoDialog = None
tasksDialog = None

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
            DisableMaxAcceleratorsEventFilter(dialog))

    # Make the dialog initial size bigger, as in Max by default they appear too small.
    dialog.resize(dialog.width(), 1.7 * dialog.height())
    return dialog

def __createDialogAction(actionName, callback):
    '''Create an action and add it to the menu builder if it is valid'''
    global ftrackMenuBuilder

    action = MaxPlus.ActionFactory.Create(
        actionName, actionName, callback)
    if action._IsValidWrapper():
        ftrackMenuBuilder.add_item(action)
        return action

def showImportAssetDialog():
    '''Create the import asset dialog if it does not exist and show it'''
    global importAssetDialog

    if not importAssetDialog:
        importAssetDialog = __createAndInitFtrackDialog(FtrackImportAssetDialog)

    # Add some extra margins to the import asset dialog under 3ds Max 2017.
    if __isMax2017():
        importAssetDialog.mainLayout.setContentsMargins(5, 5, 5, 5)

    importAssetDialog.show()

def showPublishAssetDialog():
    '''Create the publish asset dialog if it does not exist and show it'''
    global publishAssetDialog

    if not publishAssetDialog:
        publishAssetDialog = __createAndInitFtrackDialog(functools.partial(
            PublishAssetDialog, currentEntity=currentEntity))

    # Add some extra margins to the import asset dialog under 3ds Max 2017.
    if __isMax2017():
        publishAssetDialog.mainLayout.setContentsMargins(5, 5, 5, 5)

    publishAssetDialog.show()

def showAssetManagerDialog():
    '''Create the asset manager dialog if it does not exist and show it'''
    global assetManagerDialog

    if not assetManagerDialog:
        assetManagerDialog = __createAndInitFtrackDialog(FtrackAssetManagerDialog)

        # Make some columns of the asset manager dialog wider to compensate
        # for the buttons appearing very small with Max's 2017 custom Qt stylesheet.
        tableWidget = assetManagerDialog.assetManagerWidget.ui.AssertManagerTableWidget
        tableWidget.setColumnWidth(0, 25)
        tableWidget.setColumnWidth(9, 35)
        tableWidget.setColumnWidth(11, 35)
        tableWidget.setColumnWidth(15, 35)

    assetManagerDialog.show()

def showInfoDialog():
    '''Create the info dialog if it does not exist and show it'''
    global infoDialog

    if not infoDialog:
        infoDialog = __createAndInitFtrackDialog(FtrackMaxInfoDialog)

    infoDialog.show()

def showTasksDialog():
    '''Create the tasks dialog if it does not exist and show it'''
    global tasksDialog

    if not tasksDialog:
        tasksDialog = __createAndInitFtrackDialog(FtrackTasksDialog)

    tasksDialog.show()


def initFtrack():
    '''Initialize Ftrack, register assets and build the Ftrack menu.'''
    connector.registerAssets()

    global ftrackMenuBuilder
    ftrackMenuBuilder = FtrackMenuBuilder()

    __createDialogAction("Import Asset", showImportAssetDialog)
    __createDialogAction("Publish Asset", showPublishAssetDialog)
    ftrackMenuBuilder.add_separator()

    # Save the showAssetManagerAction for later use.
    showAssetManagerAction = __createDialogAction(
        "Asset Manager", showAssetManagerDialog)

    ftrackMenuBuilder.add_separator()
    __createDialogAction("Info", showInfoDialog)
    __createDialogAction("Tasks", showTasksDialog)

    # Create the Ftrack menu.
    ftrackMenuBuilder.create()

    registerMaxOpenFileCallbacks(showAssetManagerAction)

    # Send usage event.
    from ftrack_connect_3dsmax.legacy.connector import usage
    usage.send_event('USED-FTRACK-CONNECT-3DS-MAX')

initFtrack()
