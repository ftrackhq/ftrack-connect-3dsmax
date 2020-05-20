import pymxs

class MaxHelper(object):
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
        menu = MaxHelper.menu_exists(menu_name)
        if not menu:
            return

        result = pymxs.runtime.execute(
        '''
        menuMan.unRegisterMenu  {}
        '''.format(menu))
        if result:
            MaxHelper.refresh_menu()

    @staticmethod
    def create_menu(menu_name):
        result = pymxs.runtime.execute(
        '''
        menuMan.createMenu  "{}"
        '''.format(menu_name))
        return result

    @staticmethod
    def add_separator(menu_item):
        result = pymxs.runtime.execute(
        '''
        separator = menuMan.createSeparatorItem()
       {}.addItem separator -1
        '''.format(menu_item))
        return result

    @staticmethod
    def add_action(callback, menu, action_name):
        sub_menu = MaxHelper.create_menu(menu_name)
        result = pymxs.runtime.execute(
        '''
        menu_sub_item = menuMan.createSubMenuItem "{}" {}
        {}.addItem menu_sub_item -1
        '''.format(menu_name,sub_menu, menu_item)
        )