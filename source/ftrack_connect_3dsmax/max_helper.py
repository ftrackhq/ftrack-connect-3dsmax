import pymxs
import uuid

class MaxMenuHelper(object):
    #https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__files_GUID_1374EDCA_CC8B_4B43_81A5_6ED98DBE01D3_htm

    @staticmethod
    def menu_exists(menu_name):
        result = pymxs.runtime.execute(
        '''
        menuMan.findMenu {}
        '''.format(menu_name))
        return result

    @staticmethod
    def refresh_menu():
        pymxs.runtime.execute(
        '''menuMan.updateMenuBar()'''
        )

    @staticmethod
    def unregister_menu(menu_name):
        menu = MaxMenuHelper.menu_exists(menu_name)
        if not menu:
            return

        result = pymxs.runtime.execute(
        '''
        menuMan.unRegisterMenu  {menu_name}
        '''.format(menu_name=menu_name))
        if result:
            MaxMenuHelper.refresh_menu()

    @staticmethod
    def create_menu(menu_name):
        result = pymxs.runtime.execute(
        '''
        menuMan.createMenu  "{menu_name}"
        '''.format(menu_name=menu_name))
        return result

    @staticmethod
    def add_separator(menu_item):
        result = pymxs.runtime.execute(
        '''
        separator = menuMan.createSeparatorItem()
        {menu_item}.addItem separator -1
        '''.format(
            menu_item=menu_item
        ))
        return result

    @staticmethod
    def add_action(callback, menu_item, action_name):
        macro_name = uuid.uuid4().hex

        result = pymxs.runtime.execute(
        '''
        -- macro script
        macroScript {macro_name}
        category: "ftrack"
        tooltip: "{action_name}"
        (
            on execute do
            (
                python.execute "{callback}"
            )
        )
        
        -- register action
        action = menuMan.createActionItem "{macro_name}" "ftrack"
        action.setUseCustomTitle true
        action.setTitle("{action_name}")
        {menu_item}.addItem action -1
        '''.format(
            macro_name=macro_name,
            menu_item=menu_item,
            action_name=action_name,
            callback=callback)
        )