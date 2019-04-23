/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/. 
 * All comments and write lines are removed from this file */

var helpFromTwoText = "You need to select an even amount of items in your project panel.\nEach pair must consist of a data (.txt) file and a video file. The names of the video and data files (disregarding the extension) have to be the same!\nThey will be unless you changed them.\n\n1. Select the video, data pairs in the project panel.\n2. Click this button.\n3. Your composition(s) will be created.";
var helpFromFileText = "This will ask you to select a file from your drive.\nCompared to the 'From Two' button above, you do not have to import the .txt file in your project.\n\n1. Have a composition open.\n2. Click this button.\n3. Select a .txt file.\n4. You have a null.";
var helpTipHelpTip = 'Get more info.';
var repositoryLink = 'https://github.com/JakubKoralewski/cursor-recorder';
var about = "`Cursor Recorder for After Effects` is only a part of the `cursor-recorder` project.\nThe other half is the script - `Cursor Recroder for OBS` that lets you exactly time the start and stop of the cursor recording by getting the cursor data only when you record in OBS Studio.\n\nThe project is open-source on Github at " + repositoryLink + ".";
var copyrightHelpTip = "Mozilla Public License 2.0 \nIf a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/";
var FILE;
(function (FILE) {
    FILE[FILE["TXT"] = 0] = "TXT";
    FILE[FILE["VIDEO"] = 1] = "VIDEO";
})(FILE || (FILE = {}));
var PROPERTIES;
(function (PROPERTIES) {
    PROPERTIES["ANCHOR_POINT"] = "anchorPoint";
    PROPERTIES["POSITION"] = "position";
    PROPERTIES["X_POSITION"] = "xPosition";
    PROPERTIES["Y_POSITION"] = "yPosition";
    PROPERTIES["Z_POSITION"] = "zPosition";
    PROPERTIES["SCALE"] = "scale";
    PROPERTIES["ORIENTATION"] = "orientation";
    PROPERTIES["ROTATION"] = "rotation";
    PROPERTIES["X_ROTATION"] = "xRotation";
    PROPERTIES["Y_ROTATION"] = "yRotation";
    PROPERTIES["Z_ROTATION"] = "zRotation";
    PROPERTIES["OPACITY"] = "opacity";
})(PROPERTIES || (PROPERTIES = {}));
;
var EXPRESSIONS = [
    {
        name: "Cursor always in center",
        expressions: {
            video: [{
                    property: PROPERTIES.ANCHOR_POINT,
                    expression: function (nullName) {
                        return "thisComp.layer(\"" + nullName + "\").transform.position;";
                    }
                }]
        }
    },
    {
        name: "Smooth Follow",
        optional_args: [
            {
                title: "Multiplier",
                id: "multiplier",
                "default": 2
            }
        ],
        expressions: {
            video: [{
                    property: PROPERTIES.POSITION,
                    expression: function (nullName, opts) {
                        var width = opts.width || 1920;
                        var height = opts.height || 1080;
                        var multiplier = parseFloat(opts.multiplier.text) || 2;
                        var multiplier100 = 100 * multiplier;
                        return "thisLayerScale = transform.scale;\ncursorX = thisComp.layer(\"" + nullName + "\").transform.position[0];\ncursorY = thisComp.layer(\"" + nullName + "\").transform.position[1];\nxvalue = linear(thisLayerScale[0], 100, " + multiplier100 + ", cursorX + " + width / multiplier + ", " + width + ");\nyvalue = linear(thisLayerScale[0], 100, " + multiplier100 + ", cursorY + " + height / multiplier + ", " + height + ");\n[xvalue - cursorX, yvalue - cursorY];";
                    }
                },
                {
                    property: PROPERTIES.SCALE,
                    expression: function (_nullName, opts) {
                        var multiplier = parseFloat(opts.multiplier.text) || 2;
                        var multiplier100 = 100 * multiplier;
                        return [multiplier100, multiplier100];
                    }
                }]
        }
    }
];
var currentOptionalArgs = [];
{
    function cursorRecorderPanel(thisObj) {
        function buildUI(thisObj) {
            var myPanel = thisObj instanceof Panel
                ? thisObj
                : new Window("palette", "Cursor Recorder For After Effects", undefined, {
                    resizeable: true,
                    closeButton: true
                });
            myPanel.alignment = ['center', 'center'];
            myPanel.alignChildren = 'center';
            myPanel.preferredSize = [400, 200];
            myPanel.helpTip = about;
            var pCreateNull = myPanel.add("panel", undefined, "Create Null");
            pCreateNull.orientation = 'column';
            pCreateNull.alignment = 'center';
            var gfromTwo = pCreateNull.add("group", undefined, { name: "fromTwo" });
            gfromTwo.orientation = 'row';
            var fromTwoButton = gfromTwo.add("button", undefined, "Create Comp from video and data", { name: "fromTwo" });
            fromTwoButton.alignment = 'fill';
            var helpFromTwo = gfromTwo.add("button", undefined, "?", { name: "helpFromTwo" });
            helpFromTwo.helpTip = helpTipHelpTip;
            helpFromTwo.alignment = "right";
            helpFromTwo.maximumSize = [30, 20];
            fromTwoButton.onClick = function () {
                fromTwoButtonClicked();
            };
            helpFromTwo.onClick = function () {
                displayHelp('How to use the From Two import', helpFromTwoText);
            };
            var gfromFile = pCreateNull.add("group", undefined, { name: "fromFile" });
            gfromFile.orientation = 'row';
            var fromFileButton = gfromFile.add("button", undefined, "Import .txt file from file", { name: "fromFile" });
            fromFileButton.alignment = 'fill';
            var helpFromFile = gfromFile.add("button", undefined, "?", { name: "helpFromFile" });
            helpFromFile.alignment = "right";
            helpFromFile.maximumSize = [30, 20];
            helpFromFile.helpTip = helpTipHelpTip;
            fromFileButton.onClick = fromFileButtonClicked;
            helpFromFile.onClick = function () {
                displayHelp('How to use the From File import', helpFromFileText);
            };
            var pExpressions = myPanel.add("panel", undefined, "Add Expressions");
            pExpressions.orientation = 'column';
            pExpressions.alignment = 'fill';
            var gTVWithOptArgs = pExpressions.add("group");
            gTVWithOptArgs.orientation = 'column';
            gTVWithOptArgs.alignment = 'fill';
            var tvExpressions = gTVWithOptArgs.add("treeview", undefined, undefined, { name: "Expression List" });
            tvExpressions.alignment = 'fill';
            var createdExpressions = [];
            for (var i = 0; i < EXPRESSIONS.length; i++) {
                var createdExpression = tvExpressions.add("item", EXPRESSIONS[i].name, i);
                createdExpression.onActivate = function () {
                    alert("expression activated");
                };
                createdExpressions.push(createdExpression);
            }
            tvExpressions.onChange = function () {
                var opt_args = EXPRESSIONS[tvExpressions.selection.index].optional_args;
                if (opt_args) {
                    for (var _i = 0, opt_args_1 = opt_args; _i < opt_args_1.length; _i++) {
                        var arg = opt_args_1[_i];
                        var newOptionalArg = gTVWithOptArgs.add("edittext", undefined, arg["default"], { name: arg.title });
                        newOptionalArg.preferredSize = [80, 20];
                        newOptionalArg.justify = 'center';
                        newOptionalArg.helpTip = arg.title;
                        currentOptionalArgs.push({ name: arg.id, element: newOptionalArg });
                    }
                    myPanel.layout.layout(true);
                }
                else {
                    if (currentOptionalArgs) {
                        for (var _a = 0, currentOptionalArgs_1 = currentOptionalArgs; _a < currentOptionalArgs_1.length; _a++) {
                            var arg = currentOptionalArgs_1[_a];
                            gTVWithOptArgs.remove(arg.element);
                        }
                        currentOptionalArgs = [];
                    }
                    myPanel.layout.layout(true);
                }
            };
            var addExpressionButton = pExpressions.add("button", undefined, "Add Expression");
            addExpressionButton.onClick = function () {
                var selectedExpression = tvExpressions.selection;
                addExpression(selectedExpression.index, currentOptionalArgs ? currentOptionalArgs : null);
            };
            var copyright = myPanel.add("edittext", undefined, "Copyright MPL-2.0 (c) 2019 by Jakub Koralewski");
            copyright.helpTip = about + '\n\n' + copyrightHelpTip;
            var link = myPanel.add("button", undefined, repositoryLink);
            link.onClick = function () {
                openURL(repositoryLink);
            };
            myPanel.onResizing = myPanel.onResize = myPanel.onShow = function () {
                this.layout.resize();
            };
            myPanel.layout.layout(true);
            return myPanel;
        }
        var UI = buildUI(thisObj);
        if (UI != null && UI instanceof Window) {
            UI.center();
            UI.show();
        }
    }
    cursorRecorderPanel(this);
}
function openURL(address) {
    try {
        var URL = new File("cursor-recorder-shortcut.html");
        URL.open("w");
        URL.writeln('<html><HEAD><meta HTTP-EQUIV="REFRESH" content="0; url=' + address + '"></HEAD></HTML>');
        URL.close();
        URL.execute();
    }
    catch (err) {
        alert("Error at line# " + err.line.toString() + "\r" + err.toString());
    }
}
function addExpression(selectedExpressionNumber, currentOptionalArgs) {
    try {
        var activeComp = getActiveComp();
        var selectedExpression = EXPRESSIONS[selectedExpressionNumber];
        var neededFiles = [];
        if (selectedExpression.expressions["null"]) {
            neededFiles.push(FILE.TXT);
        }
        if (selectedExpression.expressions.video) {
            neededFiles.push(FILE.VIDEO);
        }
        var null_layer = void 0;
        var video_layers = [];
        for (var i = 1, len = activeComp.numLayers; i <= len; i++) {
            var layer = activeComp.layers[i];
            if (layer.nullLayer) {
                null_layer = layer;
            }
            else {
                if (layer.hasVideo) {
                    video_layers.push(layer);
                }
            }
        }
        if (neededFiles.indexOf(FILE.VIDEO) !== -1) {
            if (video_layers.length === 0) {
                alert("Video not found in this composition!");
            }
            var video_layer = void 0;
            var foundSameName = false;
            for (var _i = 0, video_layers_1 = video_layers; _i < video_layers_1.length; _i++) {
                var layer = video_layers_1[_i];
                if (getStringWithoutExtension(layer.name) === getStringWithoutExtension(null_layer.name)) {
                    foundSameName = true;
                    video_layer = layer;
                    break;
                }
            }
            if (!foundSameName) {
                video_layer = video_layers[0];
            }
            var optionalArgs = { width: video_layer.width, height: video_layer.height };
            for (var _a = 0, currentOptionalArgs_2 = currentOptionalArgs; _a < currentOptionalArgs_2.length; _a++) {
                var optArg = currentOptionalArgs_2[_a];
                optionalArgs[optArg.name] = optArg.element;
            }
            for (var _b = 0, _c = selectedExpression.expressions.video; _b < _c.length; _b++) {
                var expression = _c[_b];
                var expressionResult = expression.expression(null_layer.name, optionalArgs);
                setExpression(video_layer, expression.property, expressionResult);
            }
        }
        if (neededFiles.indexOf(FILE.TXT) !== -1) {
            for (var _d = 0, _e = selectedExpression.expressions["null"]; _d < _e.length; _d++) {
                var expression = _e[_d];
                setExpression(null_layer, expression.property, expression.expression(null_layer.name));
            }
        }
    }
    catch (err) {
        alert("Error at line# " + err.line.toString() + "\r" + err.toString());
    }
}
function setExpression(layer, property, expressionResult) {
    if (typeof expressionResult == "string") {
        layer.transform[property].expression = expressionResult;
    }
    else {
        layer.transform[property].setValue(expressionResult);
    }
}
function displayHelp(title, helpText) {
    alert(helpText, title);
}
function fromTwoButtonClicked() {
    try {
        var selection = app.project.selection;
        if (selection.length == 0) {
            alert("You must select something first!");
            return;
        }
        else if (selection.length % 2 !== 0) {
            alert("You did not select an even number of elements!");
            return;
        }
        var cursorRecorderDataFileFound = false;
        var fileMappings = {};
        for (var i = 0, len = selection.length; i < len; i++) {
            if (!(selection[i] instanceof FootageItem)) {
                alert(getName(selection[i]).concat(" is not a valid file. Please select a video and a text file."));
                return;
            }
            var withoutExtension = getStringWithoutExtension(selection[i].file.name);
            if (!(withoutExtension in fileMappings)) {
                fileMappings[withoutExtension] = { txt: null, video: null };
            }
            if (selection[i].file.name.endsWith('txt')) {
                cursorRecorderDataFileFound = true;
                fileMappings[withoutExtension].txt = selection[i];
            }
            else {
                fileMappings[withoutExtension].video = selection[i];
            }
            selection[i].selected = false;
        }
        if (!cursorRecorderDataFileFound) {
            alert("None of the selected items was a .txt file!");
            return;
        }
        for (var name in fileMappings) {
            var mapping = fileMappings[name];
            var newComp = createCompFromFootage(mapping.video);
            addCursorRecorderNull(newComp, mapping.txt.file);
            newComp.openInViewer();
        }
    }
    catch (err) {
        alert("Error at line# " + err.line.toString() + "\r" + err.toString());
    }
}
function fromFileButtonClicked() {
    try {
        var fromFileAlertTitle = 'Importing From File Error.';
        var activeComposition = getActiveComp();
        if (!activeComposition) {
            if (!app.project.activeItem || app.project.activeItem === undefined) {
                alert("You neither have a composition opened in the viewer nor selected in the project panel!", fromFileAlertTitle);
                return;
            }
            if (app.project.activeItem.typeName != "Composition") {
                alert("You did not select a composition, but a " + app.project.activeItem.typeName + "!", fromFileAlertTitle);
                return;
            }
        }
        var file = File.openDialog("Choose a file containing the cursor movement data.", "Text files: *.txt", true);
        if (!file) {
            return;
        }
        addCursorRecorderNull(app.project.activeItem, new File(file));
    }
    catch (err) {
        alert("Error at line# " + err.line.toString() + "\r" + err.toString());
    }
}
function addCursorRecorderNull(comp, dataFile) {
    try {
        var times = [];
        var positions = [];
        var myNull = void 0;
        if (dataFile.open("r")) {
            myNull = comp.layers.addNull();
            myNull.name = dataFile.name;
            var last_time = void 0;
            var line = void 0;
            while (true) {
                line = dataFile.readln();
                var splitLine = line.split(" ");
                if (!line) {
                    myNull.outPoint = parseFloat(last_time);
                    break;
                }
                last_time = splitLine[0];
                times.push(splitLine[0]);
                positions.push([splitLine[1], splitLine[2]]);
            }
            myNull.outPoint = parseFloat(last_time);
            dataFile.close();
        }
        else {
            alert("There was an error opening the file!");
            return;
        }
        myNull.transform.position.setValuesAtTimes(times, positions);
    }
    catch (err) {
        alert("Error at line# " + err.line.toString() + "\r" + err.toString());
    }
}
function createCompFromFootage(footage) {
    var fileNameOnly = getStringWithoutExtension(footage.name);
    var newComp = app.project.items.addComp(fileNameOnly, footage.width, footage.height, footage.pixelAspect, footage.duration, footage.frameRate);
    newComp.layers.add(footage);
    return newComp;
}
function getName(obj) {
    return ((obj.file && obj.file.name) || obj.name);
}
function getStringWithoutExtension(str) {
    var dotPosition = str.lastIndexOf(".");
    return str.substring(dotPosition, 0);
}
function getActiveComp() {
    var comp;
    var X = app.project.activeItem;
    var selComp = app.project.selection.length === 1 && app.project.selection[0].typeName === "Composition" ? app.project.selection[0] : null;
    var temp;
    function activateCompViewer() {
        var A = (app.activeViewer && app.activeViewer.type === ViewerType.VIEWER_COMPOSITION);
        if (A)
            app.activeViewer.setActive();
        return A;
    }
    ;
    if (X instanceof CompItem) {
        if (selComp === null) {
            comp = X;
        }
        else if (selComp !== X) {
            comp = null;
        }
        else {
            X.selected = false;
            temp = app.project.activeItem;
            X.selected = true;
            if (temp === null) {
                comp = (activateCompViewer() && app.project.activeItem === X) ? X : null;
            }
            else {
                comp = X;
            }
            ;
        }
        ;
    }
    else {
        comp = activateCompViewer() ? app.project.activeItem : null;
    }
    ;
    return comp;
}
;
if (!String.prototype.endsWith) {
    String.prototype.endsWith = function (search, this_len) {
        if (this_len === undefined || this_len > this.length) {
            this_len = this.length;
        }
        return this.substring(this_len - search.length, this_len) === search;
    };
}
