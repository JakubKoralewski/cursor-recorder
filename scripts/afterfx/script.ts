/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/. 
 * All comments and write lines are removed from this file */

/// <reference path="./typings/ae.d.ts"/>

const helpFromTwoText = `You need to select an even amount of items in your project panel.
Each pair must consist of a data (.txt) file and a video file. The names of the video and data files (disregarding the extension) have to be the same!
They will be unless you changed them.

1. Select the video, data pairs in the project panel.
2. Click this button.
3. Your composition(s) will be created.`;

const helpFromFileText = `This will ask you to select a file from your drive.
Compared to the 'From Two' button above, you do not have to import the .txt file in your project.

1. Have a composition open.
2. Click this button.
3. Select a .txt file.
4. You have a null.`;

const helpTipHelpTip = 'Get more info.';

const repositoryLink = 'https://github.com/JakubKoralewski/cursor-recorder';

const about = `\`Cursor Recorder for After Effects\` is only a part of the \`cursor-recorder\` project.
The other half is the script - \`Cursor Recroder for OBS\` that lets you exactly time the start and stop of the cursor recording by getting the cursor data only when you record in OBS Studio.

The project is open-source on Github at ${repositoryLink}.`;

const copyrightHelpTip = `Mozilla Public License 2.0 
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/`;


enum FILE {
	TXT,
	VIDEO
}

enum PROPERTIES {
	ANCHOR_POINT = 'anchorPoint',
	POSITION = 'position',
	X_POSITION = 'xPosition',
	Y_POSITION = 'yPosition',
	Z_POSITION = 'zPosition',
	SCALE = 'scale',
	ORIENTATION = 'orientation',
	ROTATION = 'rotation',
	X_ROTATION = 'xRotation',
	Y_ROTATION = 'yRotation',
	Z_ROTATION = 'zRotation',
	OPACITY = 'opacity',
};

interface IExpressionProperty {
	property: PROPERTIES;
	expression: (nullName?: string, optional_args?: any) => string | number[];
}

interface INullExpression {
	null: IExpressionProperty;
}
interface IVideoExpression {
	video: IExpressionProperty;
}

interface IExpression {
	name: string;
	optional_args?: [
		{
			title: string;
			id: string;
			default: any;
		},
	];
	expressions: {
		null: IExpressionProperty[];
		video?: IExpressionProperty[];
	} | {
		null?: IExpressionProperty[];
		video: IExpressionProperty[];
	};
}

const EXPRESSIONS: IExpression[] = [

	/* Cursor will be always in center. You can scale the video up. */
	{
		name: "Cursor always in center",
		expressions: {
			video: [{
				property: PROPERTIES.ANCHOR_POINT,
				expression: function (nullName) {
					return "thisComp.layer(\"" + nullName + "\").transform.position;";
				},
			}]
		}
	},

	/** The video will smoothly follow the cursor. You need to set the scale manually.
	  * The maximum value is the. */
	{
		name: "Smooth Follow",
		optional_args: [
			{
				title: "Multiplier",
				id: "multiplier",
				default: 2,
			}
		],
		expressions: {
			video: [{
				/* TODO: Add a list of properties with each its own expression! */
				property: PROPERTIES.POSITION,
				expression: function (nullName, opts) {
					let width = opts.width || 1920;
					let height = opts.height || 1080;
					let multiplier = parseFloat((opts.multiplier as EditText).text) || 2;
					let multiplier100 = 100 * multiplier;
					return `thisLayerScale = transform.scale;
cursorX = thisComp.layer("`+ nullName + `").transform.position[0];
cursorY = thisComp.layer("`+ nullName + `").transform.position[1];
xvalue = linear(thisLayerScale[0], 100, `+ multiplier100 + `, cursorX + ` + width / multiplier + `, ` + width + `);
yvalue = linear(thisLayerScale[0], 100, `+ multiplier100 + `, cursorY + ` + height / multiplier + `, ` + height + `);
[xvalue - cursorX, yvalue - cursorY];`
				}
			},
			{
				property: PROPERTIES.SCALE,
				expression: function(_nullName, opts) {
					let multiplier = parseFloat((opts.multiplier as EditText).text) || 2;
					let multiplier100 = 100 * multiplier;
					return [multiplier100, multiplier100];
				}
			}]
		}
	}
];

interface IcurrentOptionalArg {
	name: string;
	element: EditText
}

let currentOptionalArgs: IcurrentOptionalArg[] = [];

{
	/** Create the ScriptUI Panel  */
	function cursorRecorderPanel(thisObj) {
		/** Build the UI  */
		function buildUI(thisObj) {
			let myPanel =
				thisObj instanceof Panel
					? thisObj
					: new Window("palette", "Cursor Recorder For After Effects", undefined, {
						resizeable: true,
						closeButton: true,
					});
			myPanel.alignment = ['center', 'center'];
			myPanel.alignChildren = 'center';
			myPanel.preferredSize = [400,200];
			myPanel.helpTip = about;

			/** Panel create Null  */
			let pCreateNull = myPanel.add("panel", undefined, "Create Null");
			pCreateNull.orientation = 'column';
			pCreateNull.alignment = 'center';

			/* From Two */

			/** Group from Two  */
			let gfromTwo = pCreateNull.add("group", undefined, { name: "fromTwo" });
			gfromTwo.orientation = 'row';

			let fromTwoButton = gfromTwo.add("button", undefined, "Create Comp from video and data", { name: "fromTwo" });
			fromTwoButton.alignment = 'fill';
			let helpFromTwo = gfromTwo.add("button", undefined, "?", { name: "helpFromTwo" });
			helpFromTwo.helpTip = helpTipHelpTip;
			helpFromTwo.alignment = "right";
			helpFromTwo.maximumSize = [30, 20];

			fromTwoButton.onClick = function () {
				fromTwoButtonClicked();
			};

			helpFromTwo.onClick = function () {
				displayHelp('How to use the From Two import', helpFromTwoText);
			};

			/* From File */

			/* Group from File */
			let gfromFile = pCreateNull.add("group", undefined, { name: "fromFile" });
			gfromFile.orientation = 'row';

			let fromFileButton = gfromFile.add("button", undefined, "Import .txt file from file", { name: "fromFile" });
			fromFileButton.alignment = 'fill';
			let helpFromFile = gfromFile.add("button", undefined, "?", { name: "helpFromFile" });
			helpFromFile.alignment = "right";
			helpFromFile.maximumSize = [30, 20];
			helpFromFile.helpTip = helpTipHelpTip;

			fromFileButton.onClick = fromFileButtonClicked;

			helpFromFile.onClick = function () {
				displayHelp('How to use the From File import', helpFromFileText);
			};

			/* Expressions */

			let pExpressions = myPanel.add("panel", undefined, "Add Expressions");
			pExpressions.orientation = 'column';
			pExpressions.alignment = 'fill';

			/** This group allows to put the optional arguments right after the TreeView. */
			let gTVWithOptArgs = pExpressions.add("group");
			gTVWithOptArgs.orientation = 'column';
			gTVWithOptArgs.alignment = 'fill';

			/** Tree view of Expressions */
			let tvExpressions = gTVWithOptArgs.add("treeview", undefined, undefined, { name: "Expression List" });
			tvExpressions.alignment = 'fill';

			let createdExpressions: ListItem[] = [];

			for (let i = 0; i < EXPRESSIONS.length; i++) {
				let createdExpression = tvExpressions.add("item", EXPRESSIONS[i].name, i);
				createdExpression.onActivate = function () {
					alert("expression activated");
				}
				createdExpressions.push(createdExpression);
			}

			tvExpressions.onChange = function () {
				let opt_args = EXPRESSIONS[tvExpressions.selection.index].optional_args;
				if (opt_args) {
					/* Add optional arguments dialogs */
					for (let arg of opt_args) {
						let newOptionalArg = gTVWithOptArgs.add("edittext", undefined, arg.default, { name: arg.title });
						newOptionalArg.preferredSize = [80, 20];
						newOptionalArg.justify = 'center';
						newOptionalArg.helpTip = arg.title;
						currentOptionalArgs.push({ name: arg.id, element: newOptionalArg });
					}
					myPanel.layout.layout(true);
				} else {
					if (currentOptionalArgs) {
						/* Remove optional arguments dialogs if they exist */
						for (let arg of currentOptionalArgs) {
							gTVWithOptArgs.remove(arg.element);
						}
						currentOptionalArgs = [];
					}
					myPanel.layout.layout(true);
				}
			}

			/* Add Expression button */
			let addExpressionButton = pExpressions.add("button", undefined, "Add Expression");

			
			addExpressionButton.onClick = function () {
				let selectedExpression = tvExpressions.selection;
				
				/* If there are currently set optional arguments
				*  addExpression with the optional arguments else don't.
				*/
				addExpression(selectedExpression.index, currentOptionalArgs ? currentOptionalArgs : null);
			}

			let copyright = myPanel.add(
				"edittext",
				undefined,
				"Copyright MPL-2.0 (c) 2019 by Jakub Koralewski"
			); 
			copyright.helpTip = about + '\n\n' + copyrightHelpTip;

			let link = myPanel.add(
				"button",
				undefined,
				repositoryLink,
			);

			link.onClick = function() {
				openURL(repositoryLink);
			}

			myPanel.onResizing = myPanel.onResize = myPanel.onShow = function() {  
				this.layout.resize();  
			}

			myPanel.layout.layout(true);
			return myPanel;
		}

		let UI = buildUI(thisObj);
		if (UI != null && UI instanceof Window) {
			UI.center();
			UI.show();
		}
	}
	cursorRecorderPanel(this);
}

/** https://forums.adobe.com/thread/1295455 
 * @author https://forums.adobe.com/people/JJMack 
 */
function openURL(address: string) {
	try{
		var URL = new File("cursor-recorder-shortcut.html");
		URL.open("w");
		URL.writeln('<html><HEAD><meta HTTP-EQUIV="REFRESH" content="0; url='+address+'"></HEAD></HTML>');
		URL.close();
		URL.execute();
	}catch (err) {
		alert("Error at line# " + err.line.toString() + "\r" + err.toString());
	}
}

/** Triggered when the `Add Expression` button is clicked.
 *
 *  @param {number} selectedExpressionNumber - the index of the expression in the expression list.
 *  @param {any} currentOptionalArgs - optional arguments to use when setting the expression
 *  e.g.: the multiplier of the zoom
 */
function addExpression(selectedExpressionNumber: number, currentOptionalArgs?: IcurrentOptionalArg[]) {
	try {
		$.writeln("Adding expression");
		let activeComp = getActiveComp();
		let selectedExpression = EXPRESSIONS[selectedExpressionNumber];

		/* Get the files needed for this expression to work. */
		let neededFiles: FILE[] = [];

		if (selectedExpression.expressions.null) {
			$.writeln("Null layer is needed for this expression.");
			neededFiles.push(FILE.TXT);
		}
		if (selectedExpression.expressions.video) {
			$.writeln("Video layer is needed for this expression.");
			neededFiles.push(FILE.VIDEO);
		}

		$.writeln("Needed files: ", neededFiles);

		let null_layer: AVLayer;
		let video_layers: AVLayer[] = [];
		for (let i = 1, len = activeComp.numLayers; i <= len; i++) {
			/* Loop over every layer in the active composition. */
			let layer = activeComp.layers[i];

			if (layer.nullLayer) {
				$.writeln("Found the null layer");
				null_layer = layer as AVLayer;
			} else {
				if (layer.hasVideo) {
					$.writeln("Found the video layer");
					video_layers.push(layer as AVLayer);
				}
			}
		}

		/* If this expression needs a video to work
		 * find one. */

		if (neededFiles.indexOf(FILE.VIDEO) !== -1) {
			$.writeln("Executing video layer logic.");

			if (video_layers.length === 0) {
				alert("Video not found in this composition!");
			}
			let video_layer: AVLayer;

			let foundSameName = false;
			for (let layer of video_layers) {
				if (getStringWithoutExtension(layer.name) === getStringWithoutExtension(null_layer.name)) {
					foundSameName = true;
					video_layer = layer;
					break;
				}
			}

			if (!foundSameName) {
				video_layer = video_layers[0];
				$.writeln("Found multiple files, so I select the first one!");
			}
			/* Assigning optional arguments for the function */
			let optionalArgs = { width: video_layer.width, height: video_layer.height };
			for (let optArg of currentOptionalArgs) {
				optionalArgs[optArg.name] = optArg.element;
			}

			for (let expression of selectedExpression.expressions.video){
				let expressionResult = expression.expression(
					null_layer.name,
					optionalArgs
				);
				setExpression(video_layer, expression.property, expressionResult);
			}
		}
		if (neededFiles.indexOf(FILE.TXT) !== -1) {
			$.writeln("Executing null layer logic.");
			for (let expression of selectedExpression.expressions.null){
				setExpression(null_layer, expression.property, expression.expression(null_layer.name));
			}
		}


	} catch (err) {
		alert("Error at line# " + err.line.toString() + "\r" + err.toString());
	}
}

/** Once you get the expression's result e.g.: a string to set an expression
 *  or a raw value to set directly. This function takes care of detecting
 *  whether the return value is:
 * 
 *  a string => expression
 *  anything else => a direct value
 * 
 *  @param {AVLayer} layer - the layer to set the value to
 *  @param {string} property - e.g.: position, rotation
 *  @param {any} expressionResult - any return value set in the expression's function
 */
function setExpression(layer: AVLayer, property: string, expressionResult: any) {
	if (typeof expressionResult == "string") {
		layer.transform[
			property
		].expression = expressionResult;
	} else {
		layer.transform[
			property
		].setValue(expressionResult as any);
	}
}

/** Triggered when the `?` button is clicked next to the corresponding `Create Null` button.  */
function displayHelp(title: string, helpText: string) {
	alert(helpText, title);
}

interface IFileMapping {
	[name: string]: { txt: FootageItem; video: FootageItem };
}

/** Triggered when the `fromTwo` button is clicked.
 *  It looks for pairs of text files and video files in the selected items in the project panel.
 *  It finds those pairs and creates the corresponding compositions and opens these newly created compositions. 
 */
function fromTwoButtonClicked() {
	try {
		$.writeln("From two clicked.");
		let selection = app.project.selection as FootageItem[];
		if (selection.length == 0) {
			alert("You must select something first!");
			return;
		} else if (selection.length % 2 !== 0) {
			alert("You did not select an even number of elements!");
			return;
		}
		let cursorRecorderDataFileFound = false;

		/** It creates a mapping, where the key is the name of the either pair of the files without the extension.
		 *  
		 *  The txt property is the text FootageItem.
		 *  The video property is the video FootageItem.
		 *  
		 *  This allows for any even number of selected items.
		 *  You can create 2, 4, 6 compositions... 
		 */
		let fileMappings: IFileMapping = {};
		for (let i = 0, len = selection.length; i < len; i++) {
			if (!(selection[i] instanceof FootageItem)) {
				/* Both a text file and a movie are a FootageItem. */
				alert(getName(selection[i]).concat(" is not a valid file. Please select a video and a text file."));
				return;
			}

			let withoutExtension = getStringWithoutExtension(selection[i].file.name);

			if (!(withoutExtension in fileMappings)) {
				$.writeln('creating empty object');
				fileMappings[withoutExtension] = { txt: null, video: null };
				$.writeln('created empty object');
			}

			if (selection[i].file.name.endsWith('txt')) {
				/* File is a txt! */
				cursorRecorderDataFileFound = true;
				$.writeln('addign txt file');
				fileMappings[withoutExtension].txt = selection[i];
				$.writeln('added txt file');
			} else {
				/* File is a video file! */
				$.writeln('addign video file');
				fileMappings[withoutExtension].video = selection[i];
				$.writeln('added video file');
			}

			/* This is done so, when a file is selected later
			 *  you can be sure it's the only selected one! */
			selection[i].selected = false;
		}
		if (!cursorRecorderDataFileFound) {
			alert("None of the selected items was a .txt file!");
			return;
		}

		for (let name in fileMappings) {
			let mapping = fileMappings[name];
			let newComp = createCompFromFootage(mapping.video);
			addCursorRecorderNull(newComp, mapping.txt.file);
			newComp.openInViewer();
		}
	} catch (err) {
		alert("Error at line# " + err.line.toString() + "\r" + err.toString());
	}
}

/** Triggered when the `fromFile` button is clicked.
 *  It triggers a file dialog. You need to select the cursor-recorder .txt file.
 *  It then interprets the data using the `addCursorRecorderNull()` function.
 *  It adds the null to the composition selected in the project panel.
 */
function fromFileButtonClicked() {
	try {
		let fromFileAlertTitle = 'Importing From File Error.';
		let activeComposition = getActiveComp();
		if (!activeComposition) {
			$.writeln(`A composition was not open in the viewer.
Looking for a selected composition in the project panel.`);
			if (!app.project.activeItem || app.project.activeItem === undefined) {
				alert(
					"You neither have a composition opened in the viewer nor selected in the project panel!",
					fromFileAlertTitle
					);
				return;
			}
			if (app.project.activeItem.typeName != "Composition") {
				alert(
					"You did not select a composition, but a " + app.project.activeItem.typeName + "!",
					fromFileAlertTitle
				);
				return;
			}
		}
		
		let file = File.openDialog("Choose a file containing the cursor movement data.", "Text files: *.txt", true);

		if (!file) {
			/* User cancelled */
			return;
		}

		$.writeln(file);
		addCursorRecorderNull(app.project.activeItem as CompItem, new File(file as any));

	} catch (err) {
		alert("Error at line# " + err.line.toString() + "\r" + err.toString());
	}
}

/** The logic behind interpreting a cursor recorder data txt file.
 *  
 *  @param {CompItem} comp - the composition to add the null to
 *  @param {File} dataFile - the file containg the data
 */
function addCursorRecorderNull(comp: CompItem, dataFile: File) {
	try {
		let times = [];
		let positions = [];
		let myNull: Layer;
		if (dataFile.open("r")) {
			myNull = comp.layers.addNull();
			myNull.name = dataFile.name;
			let lines = dataFile.read().split('\n');
			dataFile.close();
			let last_time: string;
			$.writeln("lines: ", lines);
			for (let line of lines) {
				let splitLine = line.split(" ");
				if (!splitLine[2]) {
					continue;
				}
				last_time = splitLine[0];
				times.push(splitLine[0]);
				positions.push([splitLine[1], splitLine[2]])
			}
			$.writeln("last_time: ", last_time);
			myNull.outPoint = parseFloat(last_time);
			dataFile.close();
		} else {
			alert("There was an error opening the file!");
			return;
		}

		myNull.transform.position.setValuesAtTimes(times, positions);
	} catch (err) {
		alert("Error at line# " + err.line.toString() + "\r" + err.toString());
	}
}

/** Emulates the behavior of dragging a video FootageItem onto the `New Compostion` button.  */
function createCompFromFootage(footage: FootageItem) {
	let fileNameOnly = getStringWithoutExtension(footage.name);
	let newComp = app.project.items.addComp(fileNameOnly, footage.width, footage.height, footage.pixelAspect, footage.duration, footage.frameRate);
	newComp.layers.add(footage);
	return newComp;    //Adds file to comp
}

function getName(obj: Item) {
	return (((obj as FootageItem).file && (obj as FootageItem).file.name) || obj.name);
}

/** Gets everything before the dot in the string.  */
function getStringWithoutExtension(str: string) {
	let dotPosition = str.lastIndexOf(".");
	return str.substring(dotPosition, 0);
}

/** Finds active composition. IMHO better than selecting a composition in the project panel.
 * 
 *  @author Function by UQg https://forums.adobe.com/thread/2341455  
 *  @returns {CompItem | null} If found a composition returns the composition, else null.
 * */
function getActiveComp(): CompItem {
	var comp: Item; // the returned quantity
	var X = app.project.activeItem; // the initial activeItem  
	var selComp = app.project.selection.length === 1 && app.project.selection[0].typeName === "Composition" ? app.project.selection[0] : null; // the unique selected comp, or null  
	var temp: Item;

	function activateCompViewer() {
		var A = (app.activeViewer && app.activeViewer.type === ViewerType.VIEWER_COMPOSITION);
		if (A) app.activeViewer.setActive();
		return A;
	};

	if (X instanceof CompItem) {
		if (selComp === null) {
			comp = X;
		}
		else if (selComp !== X) {
			comp = null; // ambiguity : the timeline panel is active, X is the front comp, but another comp is selected  
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
			};
		};
	}
	else {
		comp = activateCompViewer() ? app.project.activeItem : null;
	};
	return comp as CompItem;
};

/* Polyfills */

interface String {
	/** Official polyfill from MDN  */
	endsWith: (search: string, this_len?: number) => boolean;
}

if (!String.prototype.endsWith) {
	String.prototype.endsWith = function (search: string, this_len?: number) {
		if (this_len === undefined || this_len > this.length) {
			this_len = this.length;
		}
		return this.substring(this_len - search.length, this_len) === search;
	};
}

