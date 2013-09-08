#!/usr/bin/env node

var path = require('path');
var esprimaPath = path.resolve(__dirname, '../third_party/esprima/esprima.js');
var esprima = require(esprimaPath);

function main() {
    process.stdin.resume();
    process.stdin.setEncoding('utf8');

    console.log('Waiting for standard input...');
    process.stdin.on('end', handleStdInEnd);
}

function handleStdInEnd() {
    console.log('Standard input ended.');
    var source = process.stdin.read();
    console.log('Source read from standard input.');

    console.log('Parsing...');
    var obj = esprima.parse(source, {
	'loc': true,
	'range': true,
	'comment': true
    });

    console.log('Parsing complete.');

    console.log('Writing resulting JSON to standard output');
    process.stdout.write(JSON.stringify(obj))
}

main();
