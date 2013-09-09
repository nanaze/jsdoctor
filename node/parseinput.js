#!/usr/bin/env node

var esprima = require('esprima');

function log(msg) {
    process.stderr.write(msg + '\n');
}

function main() {

    var stdin = process.stdin;

    var content = '';

    stdin.on('data', function (data) {
	content += data;
    });

    stdin.on('end', function () {
	log('Source read from standard input.');
	var obj = processScript(content);

	log('Writing resulting JSON to standard output');
	var jsonStr = JSON.stringify(obj);
	process.stdout.setEncoding('utf8');
	process.stdout.write(jsonStr);
    });

    stdin.resume();
}

function processScript(script) {
    log('Parsing...');
    return esprima.parse(script, {
	'loc': true,
	'range': true,
	'comment': true
    });
}


main();
