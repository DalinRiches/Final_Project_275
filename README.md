# CMPUT 275 Final Project:  Digital Synthesizer
April 14, 2017  
Made by:  Dalin Riches and John Dorn

# Overview
This project is a two-oscillator digital synthesizer. It includes a graphical
sequencer interface as well as the basic synthesizer module. The GUI can
be run from the client directory by:

    python3 seq_interface.py

The synthesizer can also be used without the GUI as a Python module, by
importing Synth.


The Synth module and thus the graphical synthesizer support audio playback
through the computer speakers using ALSA, with the python module `alsaaudio`.
Direct playback is thus only supported on Linux. Recording to a .wav file,
however, should work on all platforms.


# Dependencies
For direct playback, `alsaaudio` is required.


Alsaaudio home page: https://larsimmisch.github.io/pyalsaaudio/  
PyPI: https://pypi.python.org/pypi/pyalsaaudio


The module can be installed manually (see:
https://larsimmisch.github.io/pyalsaaudio/pyalsaaudio.html#installation)
or from PyPI (`pip install pyalsaaudio` - note that the package name is not `alsaaudio`).


PIL is also required to run the graphical interface. PyPI package `pillow`
provides this dependency, or it may already be installed.


# Synth
The Synth module is built around two wavetable oscillators that generate the
initial audio stream. The oscillators are capable of loading arbitrary wave
forms from .wav files. Several such files are included for demonstration.


## Wavetables
A wavetable is a three dimensional array of data. The "x-axis" is the sample
number (time); the "y-axis" the amplitude (signal); and the "z-axis" the
wave-table position. An oscillator normally holds one wavetable position
(frame) at a time, and generates its signal by looping through the samples
in that frame. However, the frame can be changed during playback using
modulation. (See LFOs, below.) Wave-tables are loaded from .wav files where each
block of 2048 samples in the file constitutes one frame. Thus any .wav file
can be used as a wavetable, even one that was not intended to be used this
way. The only requirement is that the file must contain at least 2048 samples.


### Note on included wavetables
Wavetables included in this program were all either generated mathematically
or created within Xfer's Serum using the wave table editor. No wavetables
included were created by a third party.


Information on serum and how the wavetable editor works is here:
https://www.xferrecords.com/products/serum


## Oscillators
The oscillator is the only synthesizer component that directly producees
a signal. An oscillator has the following numeric parameters:

1. Detune
2. Volume
3. Wavetable Postion
4. Phase Offset

An Oscillator also has one selectable parameter: the current wavetable.

#### Detune
Allows you to offset the frequency of the oscillator from the root note
(the note being provided by the sequencer) by up to 24 semitones
(where 12 semitones is one octave).


#### Volume
Allows you to change the volume of the oscillator.


#### Wavetable Position
Allows you to select a frame from the current wavetable.


#### Phase Offset
Allows you to set the initial phase (starting position within the frame).
(Note that this parameter cannot be set from the GUI.)


## Envelopes
Envelopes shape the sound of each note with amplification modulation. The
envelope controllers in the synthesizer modules have an ADSR shape:
consisting of Attack, Decay, Sustain, and Release phases. When a note is
played, the Attack and Decay phases of the envelope occur immediately:
the amplitude increases from 0% to 100% and then decreases to the sustain
level. The Sustain phase continues until a specified time before the end
of the note, at which point the Release phase occurs and the amplitude
decreases from the sustain level back to 0%. The end result is a continuous
amplitude curve. An envelope has the following numeric parameters:

1. Attack Time
2. Decay Time
3. Sustain Level
4. Release Time

#### Attack Time
Determines the amount of time the input signal will take to rise from 0 to 100%
amplification in seconds.


#### Decay Time
Determines the amount of time the input signal will take to fall from 100% to
the sustain level in seconds.


#### Sustain Level
Determines the amplification during the Sustain phase. The length of the
Sustain phase automatically scales to fill the time the other three phases
do not cover.


#### Release Time
Determines the amount of time the input signal will take to fall from the
sustain level back to 0% amplification, in seconds.


## Filters
The filters are frequency-domain components that will attenuate certain
frequencies. A filter can be set to one of two modes, eiter Low-Pass or
High-Pass. Both of these filter modes function as first-order RC filters -
they attenuate frequencies either above (Low-Pass) or below(High-Pass)
the cut-off frequency with a slope of -20dB/dec in the magnitude-frequency
Bode-Plot. The filters have the following numeric parameters:

1. Cutoff

A Filter also has one toggleable parameter: its filter type.


#### Cutoff
Allows you to change the cutoff frequency of the filter.


## LFOs
The LFO or low frequency oscillator generates a value from -1 to 1 using
a classical oscillator waveform. It can be configured to a sine, square, or saw
waveform. The LFO can be used to to oscillate (modulate) numeric parameters of
other components. An LFO can be set to modulate any component (including
itself, though this is not very useful.) An LFO has the following
numeric parameters:

1. Speed (Frequency)
2. Amount (Range)
3. Offset
4. Wavetype

An LFO also has two selectable parameters: the device and parameter to
modulate, and one toggle parameter: it can be set either to Retrigger,
in which case the waveform will 'reset' every time a new note begins
(thus each note will receive identical modulation); or Continue, in
which case the waveform will not 'reset' (thus the modulation will
be continuous through the entire sequence).

#### Speed (Frequency)
Determines the frequency the LFO operates at.

#### Amount (Range)
Determines the amount of output that is passed into the control. Larger
values produce stronger modulation.

#### Offset
Offsets the output of the LFO additively.

#### Wavetype
Determines which waveform the LFO uses. (Though this is technically a
numeric parameter, it selects between the Sine, Square, and Saw wavetypes.)


## Voicing
The Synth module is theoretically capable of generating multiple voices,
producing a polyphonic audio system. However, the mixing of multiple voices
is not fully functional, and the GUI provides no ability to control this
feature. All output from the GUI uses only one voice.


## Structure
The two oscillators generate simultaneously, the output from each of which
feeds into its own envelope. These two audio streams are then mixed and passed
through the filters in series (this allows you to create a bandpass filter by
combining low and high pass.) The three LFOs run independently of this stream,
and modify their target parameter at the beginning of every sample generation.
The update order for each sample is as follows:

1. LFOs; update modulated parameters
2. Oscillators (produces two streams)
3. Envelopes
4. Mix audio streams
5. Filter 1
6. Filter 2
7. Output to playback or file


# GUI
The GUI is a panel-based interface allowing direct control of almost all of
the settings of the Synth module. Every panel has an ON/OFF switch, which can
be toggled to completely remove a component from the audio pathway, and dials
controlling the numeric parameters of each component (described above).
Toggleable parameters are presented as buttons -- pressing the button switches
the value of the parameter. Selectable parameters appear in the upper-right
corner of a component's panel. Clicking on the button for a parameter will
open a new window presenting the possible choices for that parameter. Note
that for LFOs the Parameter menu updates dynamically based on what Component
is currently selected, so the Component must be set first. An LFO can also
be set to the component 'None', which effectively disables it.


## Step Sequencer
The GUI also contains a step sequencer that can be used to enter a sequence
of notes. The range of the sequencer is two octaves, from C2 to B4. A range
of two octaves greater can be obtained by setting the Detune parameter on
the oscillators appropriately. The y-axis of the sequencer, top to bottom,
corresponds to the pitch of the note (higher is higher-pitched) and the x-axis
corresponds to time. Step time is controlled by the "Speed" dial to the right
of the sequencer, which can be used to set the length of each note in seconds.


Notes can be placed and removed by left (button 1) clicking in the sequencer.
Longer notes can be created by clicking and dragging to the right -- the note
will be held continuously from the start to the end of the resulting area.
Clicking on an existing note and dragging either direction will clear the
area that is dragged across of all notes. Clicking in a long note or causing
it to be split will result in two notes.


## Generating Output
To generate output, click the Render button to the right of the sequencer.
The kind of output generated depends on the current settings of the Playback
and Record buttons. (Light gray indicates enabled, dark gray disabled.) If
Playback is enabled, the rendered audio will be played through the speakers
via ALSA when rendering finishes. If Record is enabled, the rendered audio
will be written to `output.wav` in the current directory. If a file of this
name already exists, it will be overwritten.
