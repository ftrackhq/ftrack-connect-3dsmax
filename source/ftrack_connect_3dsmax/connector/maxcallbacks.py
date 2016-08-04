
import ftrack

import MaxPlus

showAssetManagerAction = None
checkForNewAssetsAndRefreshCallbackId = None

def checkForNewAssetsAndRefreshAssetManager(code=None):
    '''Check whether there is any new asset and
    refresh the asset manager dialog'''
    from ftrack_connect_3dsmax.connector.assethelper import getFtrackAssetVersionsInfo
    versions = getFtrackAssetVersionsInfo()

    message = ''
    for (assetId, assetVersion, assetTake, helperNodeName) in versions:
        assetversion = ftrack.AssetVersion(assetId)
        asset = assetversion.getAsset()
        versions = asset.getVersions(componentNames=[assetTake])
        latestVersion = versions[-1].getVersion()
        if latestVersion != assetVersion:
            message = '- {0} can be updated from v:{1} to v:{2}'.format(
                helperNodeName, assetVersion, latestVersion
            )

    if message != '':
        cmd = 'queryBox "{0}. Open Asset Manager?" title:"{1}"'.format(
            message, "New assets")
        if MaxPlus.Core.EvalMAXScript(cmd).Get():
            showAssetManagerAction.Execute()

    from ftrack_connect.connector import panelcom
    panelComInstance = panelcom.PanelComInstance.instance()
    panelComInstance.refreshListeners()

def registerMaxOpenFileCallbacks(showAssetManagerDialogAction=None):
    '''Register File Open callbacks, used for refreshing the asset manager
    and updating assets.'''
    if showAssetManagerDialogAction:
        global showAssetManagerAction
        showAssetManagerAction = showAssetManagerDialogAction

    global checkForNewAssetsAndRefreshCallbackId
    checkForNewAssetsAndRefreshCallbackId = MaxPlus.NotificationManager.Register(
        MaxPlus.NotificationCodes.FilePostOpenProcess,
        checkForNewAssetsAndRefreshAssetManager)

def unregisterMaxOpenFileCallbacks():
    '''Unregister File Open callbacks'''
    global checkForNewAssetsAndRefreshCallbackId
    if checkForNewAssetsAndRefreshCallbackId:
        MaxPlus.NotificationManager.Unregister(checkForNewAssetsAndRefreshCallbackId)
        checkForNewAssetsAndRefreshCallbackId = None


class DisableOpenFileCallbacks(object):
    '''Class that disables the File Open callbacks and re-enables them when used
    with Python's with statement.
    '''
    def __enter__(self):
        unregisterMaxOpenFileCallbacks()
        return self

    def __exit__(self, type, value, traceback):
        registerMaxOpenFileCallbacks()
