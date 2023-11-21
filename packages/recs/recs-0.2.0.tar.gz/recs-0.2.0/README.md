#  🎬 recs: the Universal Recorder 🎬

## Why should there be a record button at all?

A long time ago, I asked myself, "Why is there a record button and the possibility
of missing a take? Why not record everything?"

I sometimes play music, and I have mixed bands live, and I wanted a program that would
simply record everything at all times which I didn't have to stop and start, that I
could run completely separately from my other music programs.

Separately, I wanted to digitize a huge number of cassettes and LPs, so I wanted
a program that ran in the background and recorded everything except silence, so I just
play the music into the machine, and have it divided into pieces

Nothing like that existed so I wrote it.

## `recs`:  the Universal Recorder

`recs` records any or every audio input on your machine, intelligently filters
out quiet, and stores the results in named, organized files.

Free, open-source, configurable, light on CPU and memory, and bulletproof

### Bulletproof?

It's not difficult to record some audio. Writing a program that runs continuously and
records audio even as real-world things happen is considerably harder.

It is impossible to prevent all loss, but considerable ingenuity and pulling of cables
has been used to mitigate and minimize this through software.  See Appendix A.

### Universal?

It is a "Universal Recorder" because I plan to be able to record all streams of data in
some coherent way.

I have already [written code](https://github.com/rec/litoid) to do this for
MIDI and DMX and I'll be folding that in in due time, but most of the difficulty
and most of the value in this first step is the audio, so I have focused on just audio
for this first release!

It might be that video is also incorporated in the far future, but the tooling is just
not there for Python yet, and it would be much too heavy to sit in the background all
the time and almost be forgotten about, so you could call it an Almost Universal
Recorder if you liked.

### Installation

Use

### Usage





#### Appendix A: Failure modes

1. Hardware crash or power loss
2. Segfault or similar C/C++ errors


The aim is to be as bulletproof as possible. The pre-beta existing as I write this
(2023/11/19) seems to handle harder cases like hybernation well, and can
detect if a  device goes offline and report it.

The holy grail is reconnecting to a device that comes back online: this is an
[unsolved problem](https://github.com/spatialaudio/python-sounddevice/issues/382)
in Python, I believe, but I am on my way to solving it.
