# Sleepy Alarm
**Category:** Forensics
**Difficulty:** Medium
**Author:** Minerva.

## Description
Yuuichi woke up for his school, but the alarm audio seems to have an extra jingle in it. Maybe you can help him uncover the secret?

Hint: The flag length, including ictf and enclosing braces, is 39.

## Distribution

- `togive/morning_n_breakfast.mp3`

## Solution
Easiest way: reverse search "morning_n_breakfast.mp3" to find the audio, and then compare the two signals. 
Intended way: the audio signal has a very light "jingle" when heard at full volume. FFT analysis also shows an unusual peak at 8kHz. From here, after isolating the 8kHz wave, it appears to have three distinct amplitudes i.e. 2e-3, 5e-3, and 0. The modulating algorithm is Amplitude Shift Keying. 0 amplitude indicates completion of one byte, while 2e-3 and 5e-3 represent 0 and 1 respectively. Each bit is "transmitted" for a duration of 0.02s, or 50 baud.  
