# cursor-recorder-for-afterfx :clapper: + :movie_camera: + :computer: + :mouse: = :sparkler: 

Records mouse movement to .json file and opens it in After Effects.

## :heavy_exclamation_mark: Demo :heavy_exclamation_mark: (image is a link to [vimeo.com](https://vimeo.com/289324251))

[![How it works.](https://i.imgur.com/nokmpUN.png)](https://vimeo.com/289324251)

Saves the [`cursor-recorder.json`](cursor-recorder.json) (link to an example) file to the python script's directory. From there in After Effects:

1. have a composition open,
2. run the [`cursor-recorder.jsx`](script\cursor-recorder.jsx) script,
3. choose the right `.json` file,
4. ??,
5. profit,
6. you currently need to sync the mouse manually :worried:

## Helpful example expressions:

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

### Build script
I chose to combine the two files for releases to make it simpler to install without having to copy the *json2.jsxinc* file.
Run to create an output file in `\release` directory.

```console
$ sh build_script.sh
```

### Python packages

```sh
$ pip install -r requirements.txt
```

# Credits

- json2.js by Douglas Crockford

# License
[Mozilla Public License Version 2.0](LICENSE)
