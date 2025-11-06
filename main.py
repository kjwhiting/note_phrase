import string
import re
from midiutil import MIDIFile

# ===== CONFIG / CONSTANTS =====
NOTES = ["E3","F#3","G#3","A3","B3","C#4","D#4","E4","F#4","G#4", "A4","B4","C#5","D#5","E5","F#5","G#5","A5","B5","C#6", "D#6","E6","E6-E6","B3-A4-C#6","B3-F#4","C#6-C#6"]

ALPHABET = list(string.ascii_lowercase)

NOTE_TO_MIDI = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
    "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11
}


def note_name_to_number(note: str) -> int:
    """Convert 'C#4' to MIDI note number (C4 = 60)."""
    match = re.match(r"([A-G]#?)(\d)", note)
    if not match:
        raise ValueError(f"Invalid note: {note}")
    name, octave = match.groups()
    return 12 + NOTE_TO_MIDI[name] + 12 * (int(octave) - 1)


def convert_phrase(phrase: str):
    """Convert text phrase to ordered list of note names."""
    phrase = re.sub(r"\s+", "", phrase).lower()
    order_of_notes = []
    for ch in phrase:
        if ch in ALPHABET:
            idx = ALPHABET.index(ch)
            note = NOTES[idx % len(NOTES)]
            # Handle composite chords: split by "-" or "or"
            parts = re.split(r"[-\sor]+", note)
            if ch in ["w", "z"]:
                order_of_notes.append(parts)
            order_of_notes.append(parts)
    return order_of_notes


def create_midi_file(filename: str, phrase: str):
    """Create a valid MIDI file with simple timing and note mapping."""
    track = 0
    time = 0
    tempo = 120
    duration = .5
    volume = 90

    midi = MIDIFile(1)
    midi.addTempo(track, time, tempo)

    notes_from_phrase = convert_phrase(phrase)
    for chord in notes_from_phrase:
        for n in chord:
            try:
                midi_num = note_name_to_number(n)
                midi.addNote(track, channel=0, pitch=midi_num, time=time, duration=duration, volume=volume)
            except ValueError:
                pass  # skip malformed notes
        time += duration

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

    print(f"MIDI file created successfully: {filename}")


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    while True:
        phrase = input("Enter a phrase (e.g. 'C4 D4 E4 F4 G4') or blank to exit: ").strip()
        if not phrase:
            print("Goodbye!")
            break

        try:
            create_midi_file("phrase.mid", phrase)
            print("✅ MIDI file created as 'output.mid'")
        except Exception as e:
            print(f"Error: {e}")

