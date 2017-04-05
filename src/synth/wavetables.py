import wave
import math
import struct

class wavetable:

    #TODO: Get wave table's from WAV files - this allows umlimited possibilites
    #        will also make it so we don't have to type 700,000 numbers
    #        will also allow the use of seperate wave tables for each octave
    #           -Prevents nasty aliasing at high frequency's

    def __init__(self,wav=None, wtpos=0):
        if wav == None:
            return

        else:
            self.table = self.parse_wavtab(wav, wtpos)

    # This is mostly to test the osc
    def square(self):
        return [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
                255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
                255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
                255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
                255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
                255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255]

    def parse_wavtab(self, wav=None,wtpos=0):
        if wav == None:
            return

        with wave.open(wav,mode='rb') as wav:
            channels = wav.getnchannels()
            data_size = wav.getsampwidth()
            samplerate = wav.getframerate()

            num_frame = wav.getnframes()
            print(data_size)
            print(wav.getcompname())
            print(num_frame)
            pos = 2048*wtpos
            wav.setpos(pos)

            frames = []

            #read all frames
            for i in range (0, 2048):
                frame = wav.readframes(1)
                frame = struct.unpack('<H', frame)
                frames.append(frame[0])

            return frames


if __name__ == "__main__":
    table = wavetable(wav='Basic Shapes.wav')
