#!/usr/bin/env node

const fs = require('file-system');

// Reading the data synchronously so it's available whenever we need it
const freqData = JSON.parse(fs.readFileSync('04_PitchFreq.json'));

function getPitchExact(freq) {
  // Comparing indeces of frequency and specific pitch in respective lists
  console.log(`Finding Pitch ${freq}`);
  let freqIndex = freqData.frequencies.indexOf(freq);
  let pitch = freqData.pitches[freqIndex];

  // Backup for if there is an indexing error in the lists
  if (freqData[pitch] == freq) {
    // Indeces matched -- expected frequency returns
    console.log('Pitch found using index-matching!');
    return(pitch);
  } else {
    // Indeces did not match -- brute-force test all possible pitches
    console.log('Indices did not line up...');
    for (i = 0; i < freqData.pitches.length; i++) {
      pitch = freqData.pitches[i];
      if (freqData[pitch] == freq) {
        console.log('Pitch found by discrete-testing method!');
        return(pitch);
      }
    }
    console.log('Pitch not found');
    return(null);
  }
}

function getPitchEstimate(freq) {
  // Trying frequency to see if it is exact
  let new_freq = freq
  let pitch = getPitchExact(new_freq);

  // Backup for if (when) the frequency is not exact
  if (pitch == null) {
    let errors = [null, null];

    // Looping over all dicrete frequencies to measure error
    for (i = 0; i < freqData.frequencies.length; i++) {
      errors[0] = errors[1];
      errors[1] = Math.abs(freq - freqData.frequencies[i]);

      // Turning point detected when error increases -- use previous value
      if (errors[1] > errors[0] && errors[0] != null) {
        new_freq = freqData.frequencies[i - 1];
        i = freqData.frequencies.length; // stop the loop
      }
    }

    // And lastly, finding the exact pitch
    pitch = getPitchExact(new_freq);
  }

  let error = Math.abs(freq - new_freq) / new_freq
  return([pitch, error]);
}

console.log(getPitchExact(16.351597831287414));
console.log()
console.log(getPitchExact(439.99999999999994));
console.log()
console.log(getPitchExact(6644.875161279121));
console.log()
console.log(getPitchExact(440));
console.log()
console.log(getPitchEstimate(440));
console.log()
console.log(getPitchEstimate(1250));
console.log()
console.log(getPitchEstimate(6644.875161279121));
console.log()
