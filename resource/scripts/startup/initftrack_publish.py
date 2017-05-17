# :copyright: Copyright (c) 2016 ftrack

import functools

import MaxPlus
import ftrack
import os
from PySide import QtCore

import ftrack_connect_3dsmax.publish.plugin
import ftrack_connect_pipeline
import ftrack_connect_pipeline.publish
import ftrack_connect_pipeline.global_context_switch

try:
    ftrack.setup()
except Exception:
    pass

class FtrackPublishMenuBuilder(object):
    '''Build the Ftrack menu.'''
    MENU_NAME = 'Ftrack publish'

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


ftrackMenuBuilder = None
# Dialogs.
publishAssetDialog = None
changeContextDialog = None
max_plugin = None


def __isMax2017():
    '''Return True if the 3ds Max version is 2017'''
    vers = MaxPlus.Core.EvalMAXScript('getFileVersion "$max/3dsmax.exe"').Get()
    return vers.startswith('19')


def __createDialogAction(actionName, callback):
    '''Create an action and add it to the menu builder if it is valid'''
    global ftrackMenuBuilder

    action = MaxPlus.ActionFactory.Create(
        actionName, actionName, callback)
    if action._IsValidWrapper():
        ftrackMenuBuilder.add_item(action)
        return action


def get_max_plugin():
    '''Return the max publish plugin.'''
    global max_plugin
    if not max_plugin:
        plugin = ftrack_connect_3dsmax.publish.plugin.MaxPlugin(
            context_id=os.environ['FTRACK_CONTEXT_ID']
        )
        ftrack_connect_pipeline.register_plugin(plugin)
        max_plugin = plugin

    return max_plugin


def showPublishAssetDialog():
    '''Create the publish asset dialog if it does not exist and show it'''
    global publishAssetDialog

    if not publishAssetDialog:
        publishAssetDialog = ftrack_connect_pipeline.publish.Publish(plugin=get_max_plugin())

    publishAssetDialog.open()


def showGlobalContextSwitch():
    '''Create the context dialog if it does not exist and show it.'''
    global changeContextDialog

    if not changeContextDialog:
        changeContextDialog =ftrack_connect_pipeline.global_context_switch.GlobalContextSwitch(
                plugin=get_max_plugin()
        )

    changeContextDialog.open()


def initFtrack():
    '''Initialize Ftrack, register assets and build the Ftrack menu.'''

    global ftrackMenuBuilder
    ftrackMenuBuilder = FtrackPublishMenuBuilder()

    __createDialogAction("Publish Asset", showPublishAssetDialog)
    ftrackMenuBuilder.add_separator()

    __createDialogAction('Change Context', showGlobalContextSwitch)
    # Create the Ftrack menu.
    ftrackMenuBuilder.create()

    # Send usage event.
    # Currently commented because we already send the event when initializing
    # the legacy integration.
    # todo: uncomment when the legacy integration is removed.

    # from ftrack_connect_3dsmax.connector import usage
    # usage.send_event('USED-FTRACK-CONNECT-3DS-MAX')

initFtrack()
