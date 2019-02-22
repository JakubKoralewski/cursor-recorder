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
    --[[ local profileName = obs.obs_frontend_get_current_profile()
    print("profileName: ".. profileName)
    local programDataPath = obs.os_get_program_data_path()
    print("programDataPath: ".. programDataPath)
    local configPath = programDataPath ..  ]]
    --local defaultFilePath = obs.config_get_string('RecFilePath')
    local config = obs.obs_frontend_get_profile_config()
    --[[ local recFilePath = obs.config_get_string(config, "RecFilePath") ]]
    print(recFilePath)
    obs.obs_data_set_default_string(settings, "file", script_path())
    --[[ _G.util.config_get_string() ]]
    -- C:\Users\Admin\AppData\Roaming\obs-studio\basic\profiles\Bez tytułu\basic.ini
end