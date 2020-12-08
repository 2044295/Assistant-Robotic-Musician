# Sheet Music Markup Language: SMML
## Notes from Mentor Meeting 2020/11/19
- HTML-like language
- Start with solo before looking into chords
- Need audio analysis: audio into data
- Some more on structure:

##### SMML Structure
- Measures are comparable to `<div>`s
- Notes are comparable to `<p>` tags
    - Define starting measure, starting beat, and length
- How much markup/articulation do we include?
    - Critical: Pitches and Timing
        - This includes staccato over notes
        - Also includes ties, but irrelevant based on style of note tag
            - Ties are created by JS not by SMML
    - Volume---human intuition---possibility, for following structure
        - How will it respond loud vs soft?---probably unimportant
        - Track explicit volume in order to compare volumes: set up an if-then
          statement for any ambiguous cases
    - In terms of performance quality---slurs, lyrics, etc.---probably unnecessary
- Sample rate?
    - Recorded music: 44.1K Hz
    - Often there is lower resolution---lower quality, lower file size
    - 44,100 Hz is probably not necessary for a fluid, responsive app
    - Figure out a way to be flexible for different input rates, and still be as
      consistent as possible
        - Maybe a manual cutoff that gives an error message when input is too
          slow---if the microphone interface is problem
    - Upper sample rates are for really high-end (expensive classical) only
    - Try to maximize efficiency
- FILE TYPE?
    - Easiest, most common, high-res uncompressed, cross-device is `.wav`
        - Industry-standard; safest
    - Anything else is a potential bonus---will need to convert

### On the Programming End of Things
- Sample rate?
    - Recorded music: 44.1K Hz
    - Often there is lower resolution---lower quality, lower file size
    - 44,100 Hz is probably not necessary for a fluid, responsive app
    - Figure out a way to be flexible for different input rates, and still be as
      consistent as possible
        - Maybe a manual cutoff that gives an error message when input is too
          slow---if the microphone interface is problem
    - Upper sample rates are for really high-end (expensive classical) only
    - Try to maximize efficiency
- FILE TYPE?
    - Easiest, most common, high-res uncompressed, cross-device is `.wav`
        - Industry-standard; safest
    - Anything else is a potential bonus---will need to convert
