-- Copyright (c) 2016 ftrack

-- Load the FtrackAssetHelperPlugin
include "ftrackassethelper.ms"

-- Initialize ftrack if the 3ds Max version is supported.
fn initFtrack = (
    local versionString = getFileVersion "$max/3dsmax.exe"
    local versionTokens = (filterString versionString ",")
    local majorVersion = versionTokens[1] as integer
    local servicePack = versionTokens[2] as integer

    if majorVersion < 18 or (majorVersion == 18 and servicePack < 7) then (
        messageBox "This version of 3ds Max is not supported.\nPlease use 3ds Max 2016 SP3 or newer." title: "Ftrack connect 3ds Max"
    )
    else if majorVersion == 18 then ( -- 2016 SP3+.
        python.ExecuteFile("initftrack_legacy.py");
    )
    else ( -- 2017 and newer.
        python.ExecuteFile("initftrack_publish.py");
        python.ExecuteFile("initftrack_legacy.py");
    )
)

initFtrack()
