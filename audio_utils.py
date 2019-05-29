import pyaudio as pa
import sampler as s
import struct
import wave

# Default values
SAMPLE_RATE = 24000 # Times per second
NUM_CHANNELS = 1
DEFAULT_FILENAME = "audio.wav"
FORMAT = pa.paFloat32

def _get_sample(fn, sample_rate = SAMPLE_RATE):
    xy_vals = s.sample_fn(fn, sample_rate * fn.dur)

    y_vals = []
    for xy in xy_vals:
        y_val = float(xy[1]) # The y-value from the sample as float
        y_bytes = struct.pack("f", y_val) # The float converted to bits
        for b in y_bytes:
            y_vals.append(b)

    return bytes(y_vals)

def save_sine(fn, sample_rate = SAMPLE_RATE, name = DEFAULT_FILENAME):
    y_vals = _get_sample(fn, sample_rate)

    if not name.endswith(".wav"):
        name = name + ".wav"

    wv = wave.open(name, 'wb')
    wv.setframerate(8000)
    wv.setnchannels(NUM_CHANNELS)
    wv.setsampwidth(pa.get_sample_size(FORMAT))
    wv.writeframes(y_vals)
    wv.close()

def play_sine(fn, sample_rate = SAMPLE_RATE):
    y_vals = _get_sample(fn, sample_rate)

    p =  pa.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=NUM_CHANNELS, # Does not handle stereo yet
        rate=sample_rate,
        output=True
    )

    # TODO: FIGURE OUT HOW FRAMES WORK
    # What do frames mean, really?
    stream.write(y_vals, len(y_vals) // 4)
    stream.stop_stream()
    stream.close()
    p.terminate()