# Audio-driven mouth rig

This adds audio amplitude control to the approved coupled-torso rig at commit 48c976a. Existing artwork, expression registrations and the deformation shader are unchanged.

## Try it
- Press L to play/stop the included synthetic tone fixture. It contains separated low/medium/loud pulse groups and silence, not speech.
- Pass `--audio-file /absolute/path/to/file.wav` after Godot's `--` separator to play an uncompressed 8-bit or 16-bit PCM WAV.
- Send `apply_controls({"audio_level": 0.0})` through the local API for normalized amplitude input. This does not capture the microphone or open a network listener.
- Send `audio_stop: true` or press R to stop and restore the expression's resting mouth. Explicit mouth commands take priority and stop audio control.

Loudness is sampled in 10 ms RMS windows with fast attack, slower release and hysteresis. Three existing mouth openings are selected by amplitude. Silence releases the speech override. This is not phoneme recognition: A/E/I are existing texture names, not detected vowels. No new expressions are made.

Normal WAV playback follows Godot's audio playback clock with output-latency compensation. Movie capture uses deterministic elapsed time. The 16-second proof includes initial silence, soft/medium/loud pulses, held body posture, and recovery; its sound comes from the actual Godot audio player.

## Tests
`godot --headless --path . --script res://test_audio_mouth.gd`

Tests cover WAV loading/duration, normalized bounds, silence release, opening levels, end-of-file, invalid numeric values, manual override, combined controls and reset. Existing motion and expression suites remain available.

Approved by the user on 2026-11-05. Published with the existing body rig and artwork unchanged.
