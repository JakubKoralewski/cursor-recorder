# cursor-recorder-for-afterfx :clapper: + :movie_camera: + :computer: + :mouse: = :sparkler: 

Records mouse movement to .json file and opens it in After Effects.

## :heavy_exclamation_mark: Demo :heavy_exclamation_mark: ([vimeo.com](https://vimeo.com/289324251))

[![How it works.](https://i.vimeocdn.com/video/724944159.webp)](https://vimeo.com/289324251)

Saves the [`cursor-recorder.json`](cursor-recorder.json) (link to an example) file to the python script's directory. From there in After Effects:

1. have a compisition open,
2. run the [`cursor-recorder.jsx`](cursor-recorder.jsx) script,
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

### you can do [this][vortex-thing-video]:

[![][vortex-thing-thumbnail]][vortex-thing-video]

[vortex-thing-thumbnail]: https://i.imgur.com/J4mLmbn.png
[vortex-thing-video]: https://streamable.com/ceebw

### [this][ideas-video] can give you some ideas:

[![][ideas-thumbnail]][ideas-video]

[ideas-thumbnail]: https://i.imgur.com/NofznGx.png
[ideas-video]: https://streamable.com/zk1yi

### [this][overkill-video] may seem like an overkill but I'm supposed to advertise a product so here you go:

[![][overkill-thumbnail]][overkill-video]

btw this is from [this extension](https://github.com/JakubKoralewski/google-calendar-box-select) of mine (I'm really selling out right now)

[overkill-thumbnail]: https://i.imgur.com/HPZONha.png
[overkill-video]: https://streamable.com/rvdxr
