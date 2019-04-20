# cursor-recorder :clapper: + :movie_camera: + :computer: + :mouse: = :sparkler: 

<img src="docs/img/logo.png" width="80" align="left" />

Records mouse movement to a file and opens it in After Effects. Use with [OBS Studio](https://github.com/obsproject/obs-studio) as an [external Python script][cursor_recorder_for_obs] or if you prefer a more manual approach, using the [standalone Python script][cursor_recorder_standalone]. Then use the [After Effects script][cursor_recorder_for_afterfx] to import the generated cursor movement data.


## How to use

### With OBS (manually)
1. #### Import the [cursor_recorder_for_obs.py][cursor_recorder_for_obs] in OBS. (You need to do this just once).
   1. Go to `Tools -> Scripts`.
   2. Make sure you have a Python interpreter installed and its path set in OBS' settings (`Scripts -> Python Settings`).
   3. Click the :heavy_plus_sign: icon (Add Scripts) and select the [cursor_recorder_for_obs.py][cursor_recorder_for_obs].
   4. Make sure the script is enabled. (It is by default).
   5. Click `Install Python modules` if you don't have `pyautogui` and/or `keyboard` packages installed.

2. You're ready to start recording. The *.txt will be saved in the same place as your video with the same name.
3. Stop the recording.
4. #### Import the [cursor_recorder_for_afterfx.jsx][cursor_recorder_for_afterfx] in After Effects. (You need to do this just once).
   1. Go to the folder you installed After Effects.
   2. To be exact, go here `Adobe After Effects CC 2019\Support Files\Scripts\ScriptUI Panels`.
   3. Place the scripts/[cursor_recorder_for_afterfx.jsx][cursor_recorder_for_afterfx] file in the `ScriptUI Panels` folder.
   
5. #### Run the [cursor_recorder_for_afterfx.jsx][cursor_recorder_for_afterfx] script.
   1. Open After Effects.
   2. Go to `Window -> ` scroll down to the `cursor_recorder_for_afterfx.jsx` script and run it.
   3. Click the help buttons for more info. 
   
6. Do whatever you want with it from here. Check out the [**Examples**](#examples-with-after-effects-expressions) section below! 
   
### Standalone
1. Use the [cursor_recorder_standalone.py][cursor_recorder_standalone].
2. Specify `refresh_rate` variable inside the code for your needs.
3. File with the cursor movement should get saved to the same directory as your script.
4. [Import to After Effects.](#run-the-cursor_recorder_for_afterfxjsx-script)
    
[cursor_recorder_for_obs]: ./scripts/cursor_recorder_for_obs.py
[cursor_recorder_for_afterfx]: ./scripts/cursor_recorder_for_afterfx.jsx
[cursor_recorder_standalone]: ./scripts/cursor_recorder_standalone.py

## Examples (with After Effects expressions):

### SMOOTH FOLLOW (that's from the demo)

```javascript
thisLayerScale = transform.scale;
cursorX = thisComp.layer("cursor-recorder-movement").transform.position[0];
cursorY = thisComp.layer("cursor-recorder-movement").transform.position[1];
xvalue = linear(thisLayerScale[0], 100, 200, cursorX + 960, 1920);
yvalue = linear(thisLayerScale[0], 100, 200, cursorY + 540, 1080);
[xvalue - cursorX, yvalue - cursorY];
```

### CURSOR IN CENTER

```javascript
// Expression set on video's anchor point
thisComp.layer("cursor-recorder-movement").transform.position;
```

## Weird things you can do with this
*The images are links to streamable.com*

### You can do [this][vortex-thing-video]:

[<img src="https://i.imgur.com/J4mLmbn.png" height="200" />][vortex-thing-video]

[vortex-thing-video]: https://streamable.com/ceebw

### [This][ideas-video] can give you some ideas:

[<img src="https://i.imgur.com/NofznGx.png" height="200" />][ideas-video]

[ideas-video]: https://streamable.com/zk1yi

### [This][overkill-video] may seem like an overkill but I'm supposed to advertise a product so here you go:

[<img src="https://i.imgur.com/HPZONha.png" height="200" />][overkill-video]

[overkill-video]: https://streamable.com/rvdxr

BTW this is from [this browser extension](https://github.com/JakubKoralewski/google-calendar-box-select) of mine (I'm really selling out right now)

## Development

### Python packages

The script requires: `pyautogui` and `keyboard`. Install them yourself or using this command:

```sh
$ pip install -r requirements.txt
```

# License
[Mozilla Public License Version 2.0](LICENSE)
