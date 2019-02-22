rm -r release
mkdir release
sed -n '/include/!p' afterfx-script/cursor-recorder.jsx > release/cursor-recorder.jsx
sed -i '/* *\// r afterfx-script/json2.jsxinc' release/cursor-recorder.jsx
