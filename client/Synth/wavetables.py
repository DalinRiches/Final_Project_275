import wave
import math
import struct

class wavetable:
    ''' This class allows for wav files to be parsed into a wavetable.
        All wavetables created using Serum by Xfer, specifically Serum's wavetable editor.

            Only supports single channel wav files.

        Args:
            wav: the location of the file to be parsed

        Returns:
            a list of signed 16 bytes in Little Endian form corresponding to
            a wavetable with n frames(n wavetable positions) of 2048 samples
                The list is of length n*2048
    '''

    def __init__(self,wav=None):
        if wav == None:
            return

        else:
            self.table = self.parse_wavtab(wav)


    def parse_wavtab(self, wav=None):
        '''
            This function parses wavetable data from the provided wav file

                Only supports single channel wav files.

            Args:
                wav: the location of the file to be parsed

            Returns:
                a list of signed 16 bytes in Little Endian form corresponding
                to a wavetable with n frames(n wavetable positions) of 2048
                samples
                    The list is of length n*2048
        '''
        if wav == None:
            return

        with wave.open(wav,mode='rb') as wav:

            num_frame = wav.getnframes()
            if not num_frame%2048 == 0:
                num_frame = num_frame - num_frame%2048

            frames = []

            #read all frames
            for i in range (0, num_frame):
                frame = wav.readframes(1)
                frame = struct.unpack('<H', frame)
                frames.append(frame[0])

            return frames


if __name__ == "__main__":
    table = wavetable(wav='basic.wav')
    print(table)
