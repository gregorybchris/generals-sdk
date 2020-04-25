'use strict'

let fs = require('fs')
let LZString = require('lz-string')

function deserialize(serialized) {
    let replayArray = new Uint8Array(serialized)
    let obj = JSON.parse(LZString.decompressFromUint8Array(replayArray))

	let replay = {}
	let i = 0
	replay.version = obj[i++]
	replay.id = obj[i++]
	replay.mapWidth = obj[i++]
	replay.mapHeight = obj[i++]
	replay.usernames = obj[i++]
	replay.stars = obj[i++]
	replay.cities = obj[i++]
	replay.cityArmies = obj[i++]
	replay.generals = obj[i++]
	replay.mountains = obj[i++]
	replay.moves = obj[i++].map(deserializeMove)
	replay.afks = obj[i++].map(deserializeAFK)
	replay.teams = obj[i++]
	replay.map_title = obj[i++] // only available when version >= 7

	return replay
}

function deserializeMove(serialized) {
	return {
		index: serialized[0],
		start: serialized[1],
		end: serialized[2],
		is50: serialized[3],
		turn: serialized[4],
	}
}

function deserializeAFK(serialized) {
	return {
		index: serialized[0],
		turn: serialized[1],
	}
}

function parseArgs() {
	let args = process.argv
	let inFilepath = ''
	let outFilepath = ''
	if (args.length == 2)
		throw new Error('Path to input .gior file is required')
	else if (args.length == 3) {
		inFilepath = args[2]
		if (inFilepath.endsWith('.gior'))
			outFilepath = `${inFilepath.substring(0, inFilepath.length - 5)}.json`
		else
			outFilepath = `${inFilepath}.json`
	}
	else if (args.length == 4) {
		inFilepath = args[2]
		outFilepath = args[3]
	}
	else {
		throw new Error('Too many arguments passed')
	}
	return [inFilepath, outFilepath]
}

let [inFilepath, outFilepath] = parseArgs()
let input = fs.readFileSync(inFilepath)

try {
    let replay = deserialize(input)
	fs.writeFileSync(outFilepath, JSON.stringify(replay, null, 4))
	console.log(`Successfully converted ${inFilepath} to ${outFilepath}`)
}
catch(e) {
	console.error(`Failed to convert ${inFilepath} to JSON`, e)
}
