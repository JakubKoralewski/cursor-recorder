rm -r release
mkdir release
sed -n '/include/!p' script/cursor-recorder.jsx > release/cursor-recorder.jsx
sed -i '/* *\// r script/json2.jsxinc' release/cursor-recorder.jsx
