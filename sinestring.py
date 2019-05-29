from expr_utils import Expr

# Default Values 
START = 0
END = 100
DURATION = 1 # Seconds

class SineBase:

    def __init__(self, var = "x", frequency = 1, amplitude = 1, dur = DURATION):
        self.set_amplitude(amplitude)
        self.set_frequency(frequency)
        self.set_dur(dur)
        self.set_var(var)

    def set_dur(self, dur):
        self.dur = dur

    def get_span(self):
        return END - START

    def _get_units_per_second(self):
        return self.get_span() / self.dur

    def set_var(self, var):
        self.var = "2*pi*{}/{}".format(var, self._get_units_per_second())

    # General loudness
    def set_amplitude(self, amplitude):
        self.amp = amplitude
    
    # General pitch
    def set_frequency(self, frequency):
        self.freq = frequency

    def __str__(self):
        return "({})*sin(({})*{})".format(self.amp, self.freq, self.var)
    

class SineFull(SineBase):

    def __init__(self, var = "x", frequency = 1, amplitude = 1, dur = DURATION):
        # Sets the main sine function
        super().__init__(var, frequency, amplitude, dur)

        # Overtones are handled seperately and added to the main sine function
        self.overtones = []
        self.overtone_data = []

        # Adds initial overtone data for main sine
        self.overtone_data.append((1,1))

        # Initial ampltitude of the main sine without overtone interference
        self.backup_amp = self.amp

    # Sets the overtones
    # Relative loudness and relative pitch
    def set_overtones(self, function = "1", num_overtones = 5):
        self.overtone_data.clear()
        weights = Expr(function)

        # All overtone data will be relative to the largest
        biggest = 0
        for i in range(1, num_overtones + 2):
            weight = weights(i)
            if abs(weight) > biggest:
                biggest = abs(weight)
            self.overtone_data.append((i, weight))

        # Dividing all overtone weights to be relative to the largest
        if biggest > 0:
            for i in range(len(self.overtone_data)):
                self.overtone_data[i] = (
                    self.overtone_data[i][0], 
                    self.overtone_data[i][1] / biggest)

    # Initializes the overtones
    def _create_overtones(self):
        self.overtones.clear()

        # If length is just 1, then its just the main sine 
        # Amplitude will be x 1 and frequency will be x 1
        if len(self.overtone_data) == 1:
            return # Return

        for ovd in self.overtone_data[1:]:
            self.overtones.append(SineBase(
                var = self.var, 
                frequency = "{}*({})".format(ovd[0], self.freq), 
                amplitude= "{}*({})".format(ovd[1], self.amp)))


    def __str__(self):
        self._create_overtones()

        # Updates amplitude of main sine based on overtone function at x = 1
        self.backup_amp = self.amp
        main_tone = self.overtone_data[0]
        self.amp = "{}*({})".format(main_tone[1], self.amp)

        # Combines all of the overtones to the main sine
        comb = super().__str__()
        for ov in self.overtones:
            comb = "{} + {}".format(comb, ov)
        
        # Resets to original amp incase overtone function ever changes
        self.amp = self.backup_amp

        return comb
