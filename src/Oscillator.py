class oscillator:

    def __init__(self, wave_table="Triangle", wave_table_pos=0, voices=1, sync_pos=0, level=75):
        self.wave_table = wave_table
        self.wave_table_pos = wave_table_pos
        self.voices = voices
        self.sync_pos = sync_pos
        self.level = level

        self.generate_next_bit()

    def generate_next_bit(self):
        if self.wave_table_pos < 255:
            self.wave_table_pos += 1
        else:
            self.wave_table_pos = 0
        return self.wave_table[self.wave_table_pos]

    def

    # TODO: Make a proper  wave_table oscillator class
