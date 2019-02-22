-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this
-- file, You can obtain one at http://mozilla.org/MPL/2.0/. 
-- 
-- Copyright 2019 (c) Jakub Koralewski


local obs = _G.obslua
local cachedSettings = {}

function script_description()
    return "<h1>OBS Cursor Recorder</h1><b>Lets you save your cursor movement to a JSON formatted file.</b><br/><br/>©2019 Jakub Koralewski. Open-source on GitHub.<hr />"
end

function _G.script_properties()
    local props = obs.obs_properties_create()
    obs.obs_properties_add_bool(props, "enabled", "Enabled")
    obs.obs_properties_add_path(props, "file", "Directory to save JSON file", obs.OBS_PATH_DIRECTORY, nil, script_path())
    return props
end

function _G.script_update(settings)
    cachedSettings.file = obs.obs_data_get_string(settings, "file")
    print("file directory: ".. cachedSettings.file)
    cachedSettings.enabled = obs.obs_data_get_int(settings, "enabled")
end

-- A function named script_defaults will be called to set the default settings
function _G.script_defaults(settings)
    local config = obs.obs_frontend_get_profile_config()
    
    obs.obs_data_set_default_bool(settings, "enabled", true)
end

function _G.script_tick(seconds)
    print(GetCursorPosition())
    if obs.obs_frontend_recording_active() then
        print("script tick")
        
    end

end

--[[ To save JSON: https://obsproject.com/docs/reference-settings.html?highlight=obs_data_create_from_json_file_safe ]]