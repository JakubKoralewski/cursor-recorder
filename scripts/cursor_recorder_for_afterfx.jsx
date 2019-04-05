/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. 
 * 
 * Copyright 2019 (c) Jakub Koralewski
 * */

/* Use $.writeln('lol') to log data. 
 * Remember not to use in production as it opens the ExtendScript toolkit when runnning the script. 
 */

main();
function main() {
	if (!app.project.activeItem || app.project.activeItem === 'undefined') {
		alert("A composition must be open and selected!");
		return;
	}

	var file = new File(
		File.openDialog("Choose a file containing the cursor movement data.", "Text files: *.txt", true)
	);
	
	if(!file) {
		/* User cancelled */
		return;
	}

	if (file.open("r")) {
		file.encoding = "UTF-8";
		var myNull = app.project.activeItem.layers.addNull();
		myNull.name = "cursor-recorder";
		var last_time = 0;
		while (1) {
			var line = file.readln();
			if (!line) {
				myNull.outPoint = parseFloat(last_time);
				break;
			}
			line = line.split(" ");
			last_time = line[0];
			myNull.transform.position.setValueAtTime(
				line[0],
				[line[1], line[2]]
			);
		}
		file.close();
	} else {
		alert("There was an error opening the file!");
		return;
	}
}
