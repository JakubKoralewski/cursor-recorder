/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. 
 * 
 * Copyright 2019 (c) Jakub Koralewski
 * */

main();
function main() {
	if (!app.project.activeItem) {
		alert("A composition must be open and selected!");
		return;
	}

	var file = new File(
		File.openDialog("Choose a cursor recorder json.", "Text files: *.txt", true)
	);
	
	if(!file) {
		/* User cancelled */
		return;
	}

	if (file.open("r")) {
		file.encoding = "UTF-8";
		var myNull = app.project.activeItem.layers.addNull();
		myNull.name = file.name;
		while(1){
			var line = file.readln();
			$.writeln(line);
			if (!line) {
				break;
			}
			
			line = line.split(" ");
			
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
