#include "json2.jsxinc"

main();
function main() {
	if (!app.project.activeItem) {
		alert("A composition must be open and selected!");
		return;
	}

	var file = new File(
		File.openDialog("Choose a cursor recorder json.", "Files:*.json", true)
	);

	var parsedData;
	if (file.open("r")) {
		file.encoding = "UTF-8";
		parsedData = JSON.parse(file.read());
		file.close();
	}

	var myNull = app.project.activeItem.layers.addNull();
	myNull.name = file.name;

	myNull.transform.position.setValuesAtTimes(
		parsedData.times,
		parsedData.positions
	);
}
