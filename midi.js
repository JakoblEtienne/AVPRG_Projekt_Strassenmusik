if (navigator.requestMIDIAccess) {
    navigator.requestMIDIAccess({sysex: false}).then(function (midiAccess) {
        midi = midiAccess;
        var inputs = midi.inputs.values();
        // loop through all inputs
        for (var input = inputs.next(); input && !input.done; input = inputs.next()) {
            // listen for midi messages
            input.value.onmidimessage = onMIDIMessage;
        }
    });
} else {
    alert("No MIDI support in your browser.");
}

function onMIDIMessage(event) {
    // event.data is an array
    // event.data[0] = on (144) / off (128) / controlChange (176)  / pitchBend (224) / ...
    // event.data[1] = midi note
    // event.data[2] = velocity

    switch (event.data[0]) {
    case 144:
        // your function startNote(note, velocity)

        fTonleiter(Tonart1, Grundton1, event.data[2] - 4);

        startNote(playNote(event.data[1]), 127);

        console.log("start", event.data[1]);
        console.log(event.data[2]);

        console.log(Oktavlage1);
        break;
    case 128:
        // your function stopNote(note, velocity)
        stopNote(playNote(event.data[1]), 127);
        console.log(playNote(event.data[1]));
        console.log("Ende", event.data[1]);
        console.log(event.data[2]);
        break;
    case 176:
        // your function controlChange(controllerNr, value)
        console.log("control", event.data[1]);
        console.log(event.data[2]);
        break;
    case 224:
        // your function pitchBend(LSB, HSB)
        pitchBend(event.data[1], event.data[2]);
        break;
    }
}
