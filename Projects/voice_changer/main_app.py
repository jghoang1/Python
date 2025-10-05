from typing import Any
import mido
import kivy
import pyaudio

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot, MeshStemPlot
from kivy.graphics import *
import matplotlib.pyplot as plt

import numpy as np
import logging
import itertools
from common import *
from oscillator import SineOscillator, SquareOscillator, SawtoothOscillator
import time
from scipy.signal import butter, lfilter, freqz, hilbert
from collections import deque
import random



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)


Window.size = (1200, 1000)

def freq_from_key(key) -> int:
    return 440 * 2 ** ((key - A4)/12)

def add_without_clipping(a, b, upper = np.iinfo(np.int16).max, lower = np.iinfo(np.int16).min):
    return min(max(a + b, lower), upper)

add_no_clip = np.vectorize(add_without_clipping)


class Envelope():
    def __init__(self, attack_duration=0.05, decay_duration=0.05, sustain_level=0.8, release_duration=0.1) -> None:
        self.attack_duration = attack_duration
        self.decay_duration = decay_duration
        self.sustain_level = sustain_level
        self.release_duration = release_duration

    def get_ads_stepper(self):
        steppers = []
        if self.attack_duration > 0:
            steppers.append(itertools.count(start=0, \
                step= 1 / (self.attack_duration * SR)))
        if self.decay_duration > 0:
            steppers.append(itertools.count(start=1, \
            step=-(1 - self.sustain_level) / (self.decay_duration  * SR)))
        while True:
            l = len(steppers)
            if l > 0:
                val = next(steppers[0])
                if l == 2 and val > 1:
                    steppers.pop(0)
                    val = next(steppers[0])
                elif l == 1 and val < self.sustain_level:
                    steppers.pop(0)
                    val = self.sustain_level
            else:
                val = self.sustain_level
            yield val
    
    def get_r_stepper(self):
        val = 1
        if self.release_duration > 0:
            release_step = - self.val / (self.release_duration * SR)
            stepper = itertools.count(self.val, step=release_step)
        else:
            val = -1
        while True:
            if val <= 0:
                self.ended = True
                val = 0
            else:
                val = next(stepper)
            yield val
    
    def __iter__(self):
        self.val = 0
        self.ended = False
        self.stepper = self.get_ads_stepper()
        return self
    
    def __next__(self):
        self.val = next(self.stepper)
        return self.val
        
    def trigger_release(self):
        self.stepper = self.get_r_stepper()


class ActiveNote():
    OSCILLATORS = {"sine": SineOscillator,
                   "square": SquareOscillator,
                   "saw": SawtoothOscillator}

    def __init__(self, note, velocity, waveform="sine") -> None:
        self.triggered = False
        self.note = note 
        self.frequency = freq_from_key(self.note)
        self.velocity = velocity
        self.waveform = waveform

        self.oscillator = self.OSCILLATORS[self.waveform](freq=self.frequency, 
                                                          amp=DEFAULT_AMP,
                                                          wave_range=(np.iinfo(np.int16).min * (127 + self.velocity)/254, 
                                                                      np.iinfo(np.int16).max * (127 + self.velocity)/254))
        iter(self.oscillator)

        self.envelope = Envelope()
        iter(self.envelope)
    
    def get_n_env_steps(self, n):
        return np.array([next(self.envelope) for i in range(n)])
    
    def get_n_osc_steps(self, n):
        
        return np.array([next(self.oscillator) for i in range(n)])

    
    def set_waveform(self, waveform):
        if waveform == self.waveform:
            return
        if waveform not in self.OSCILLATORS:
            logger.error(f"{waveform} not a valid waveform. Valid waveforms: {self.OSCILLATORS.keys()}")
            return
        self.waveform = waveform
        self.oscillator = self.OSCILLATORS[self.waveform](freq=self.frequency, 
                                                          amp=DEFAULT_AMP,
                                                          wave_range=(np.iinfo(np.int16).min * (127 + self.velocity)/254, 
                                                                      np.iinfo(np.int16).max * (127 + self.velocity)/254))
        iter(self.oscillator)
    
    def trigger_release(self):
        self.triggered = True
        self.envelope.trigger_release()
    
    def reactivate(self):
        self.triggered = False
        iter(self.envelope)


class Beep():
    def __init__(self) -> None:
        self.frames = np.array([])
        self.ended = True

    def get_n_frames(self, n):
        pass

    def generate_frames(self):
        pass


class ToneBeep(Beep):
    OSCILLATORS = {"sine": SineOscillator,
                   "square": SquareOscillator,
                   "saw": SawtoothOscillator}
    
    def __init__(self, waveform="sine") -> None:
        super().__init__()
        self.oscillator = self.OSCILLATORS[waveform](amp=DEFAULT_AMP, wave_range=(np.iinfo(np.int16).min, 
                                                                      np.iinfo(np.int16).max))
        self.envelope = Envelope()
        self.freq = random.randrange(100,200)
        self.triggered = False
        iter(self.oscillator)
        iter(self.envelope)
    
    def get_n_env_steps(self, n):
        return np.array([next(self.envelope) for i in range(n)])
    
    def get_n_osc_steps(self, n):
        return np.array([next(self.oscillator) for i in range(n)])
    
    def update(self, n, value, control):
        f_range = max(0.01, control[0] /127 * 5)
        f_step = max(0.01, control[1] / 127)
        self.oscillator.freq = self.freq * 2 ** ((f_range/f_step * value)//127 * f_step)

        tone = self.get_n_osc_steps(n)
        env = self.get_n_env_steps(n)
        return (tone * env).astype(np.int16)

    def trigger_release(self):
        self.triggered = True
        self.envelope.trigger_release()
    
    def reset(self):
        self.triggered = False
        self.freq = random.randrange(100,500)
        iter(self.oscillator)
        iter(self.envelope)


class MidiInputManager():
    def __init__(self, root, input_name=None) -> None:
        self.root = root
        self.input_name = input_name if input_name in mido.get_input_names() else None
        self.midi_stream = None
        self.active_notes = {}
        self.active_pads = {}
        self.pitchwheel = 0
        self.controls = {x:0 for x in range(70,78)}
        self.aftertouch = 0

        self.open_input()   

    def open_input(self):
        self.midi_stream = mido.open_input()
    
    def iter_pending(self):
        if self.midi_stream is not None:
            return self.midi_stream.iter_pending()
    
    def make_label(self):
        return f"""
        Acttive Notes: {[note for note in self.active_notes]}  Active Pads: {[note for note in self.active_pads]} 
        Pitch: {self.pitchwheel} Controls: {self.controls}
        """
    
    
    def update(self, dt):
        for msg in self.iter_pending():
            logger.info(msg)

            if msg.type == "note_on" and msg.channel == 0:
                self.active_notes[msg.note] = msg.velocity
            if msg.type == "note_on" and msg.channel == 9:
                self.active_pads[msg.note] = msg.velocity
            if msg.type == "note_off" and msg.channel == 0:
                if msg.note in self.active_notes:
                    del self.active_notes[msg.note]
            if msg.type == "note_off" and msg.channel == 9:
                self.aftertouch = 0
                if msg.note in self.active_pads:
                    del self.active_pads[msg.note]
            if msg.type == "pitchwheel":
                self.pitchwheel = msg.pitch
            if msg.type == "control_change":
                self.controls[msg.control] = msg.value
            if msg.type == "aftertouch":
                self.aftertouch = msg.value


        self.root.midi_label.text = self.make_label()
            

class AudioInputManager():
    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()
        self._start_stream()
        
    def read(self):
        if self.stream.is_active:
            return self.stream.read(self.stream.get_read_available())
    
    def write(self, data):
        self.stream.write(data)

    def _start_stream(self):
        self.stream = self.p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SR,
                    input=True,
                    output=True,
                    # output_device_index=9, # Comment to debug
                    frames_per_buffer=FRAMES_PER_BUFFER)
        
    def reset_stream(self):
        self.stream.close()
        self._start_stream()


class FXManager():
    def __init__(self) -> None:
        pass


class AudioVisualizer(GridLayout):
    def __init__(self, y_factor=1, fft_y_factor=10, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.y_factor = y_factor
        self.fft_y_factor = fft_y_factor
        self.graph = Graph(x_ticks_major=100, y_ticks_major=10000 * self.y_factor, padding=5,
                           x_grid=True, y_grid=True, xmin=-0, xmax=1000, ymin=-30000 * self.y_factor, ymax=np.iinfo(np.int16).max * self.y_factor)
        self.add_widget(self.graph)
        
        self.plot = MeshLinePlot(color=[0, 0.5, 0, 1])
        self.graph.add_plot(self.plot)

        self.fft_graph = Graph(x_ticks_major=0.1, y_ticks_major=10000 * self.fft_y_factor, padding=5,
                               x_grid_label = True, xlog = True,
                               x_grid=True, y_grid=True, xmin=1, xmax=1000, ymin=0, ymax=np.iinfo(np.int16).max * self.fft_y_factor)
        self.add_widget(self.fft_graph)
        self.fft_plot = MeshStemPlot(color=[0, 0.5, 0.5, 1])
        self.fft_graph.add_plot(self.fft_plot)
        

    def update(self, dt, data):
        # Get mic frames
        if len(data) > 0:
        # Update graph plot
            self.plot.points = enumerate(data)
            fft = np.abs(np.fft.fft(data , n=1024))
            self.fft_plot.points = enumerate(fft, start=1)


class AudioModule(GridLayout):
    def __init__(self, root, active=True, incoming_modules = None,  **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.active = active
        with self.canvas.before:
            color = COLOR_MODULE_BG if self.active else COLOR_MODULE_BG_INACTIVE
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.button = Button(text="Active" if self.active else "Inactive", background_color=COLOR_BTN_ACTIVE if self.active else COLOR_BTN_INACTIVE, size_hint=(None,0.4))
        self.button.bind(on_press = self.activate_callback)
        self.add_widget(self.button)
        self.incoming_modules = incoming_modules

        self.root = root

        self.out = None
                        
    def on_pos(self, *args):
        self.rect.pos = self.pos

    def on_size(self, *args):
        self.rect.size = self.size

    def set_active(self, active):
        self.active = active
    
    def toggle_active(self):
        self.active = not self.active

    def process_audio(self, dt, data):
        self.out = data
        return data
    
    def activate_callback(self, instance):
        self.toggle_active()
        self.button.background_color = COLOR_BTN_ACTIVE if self.active else COLOR_BTN_INACTIVE
        self.button.text="Active" if self.active else "Inactive"
        with self.canvas.before:
            color = COLOR_MODULE_BG if self.active else COLOR_MODULE_BG_INACTIVE
            Color(*color)
            del self.rect
            self.rect = Rectangle(pos=self.pos, size=self.size)
    

class PassThrough(AudioModule):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        assert len(self.incoming_modules) == 1
        self.cols = 1
        self.label = Label(text="Empty")
        self.add_widget(self.label)

    def process_audio(self, dt, data):
        self.out = self.incoming_modules[0].out
        return self.out
    

class ToneGenerator(AudioModule):

    def __init__(self, root, waveform="sine", gain = 0.8, **kwargs):
        super().__init__(root, **kwargs)
        self.cols = 1
        self.active_notes = {}
        self.waveform = waveform

        # Widget Title Label
        self.label = Label(text = "Tone Generator")
        self.add_widget(self.label)

        # Gain slider
        self.gain = gain
        self.gain_label = Label(text=f"Gain: {self.gain}")
        self.add_widget(self.gain_label)
        self.gain_slider = Slider(min=0, max=2, value=self.gain)
        def on_gain_change(_, value):
            self.gain_label.text = f"Gain: {value:.02f}"
            self.gain = value
        self.gain_slider.bind(value=on_gain_change)
        self.add_widget(self.gain_slider)

        # Pitch slider
        self.pitch = 0
        self.pitch_label = Label(text="Pitch: +0")
        self.add_widget(self.pitch_label)
        self.pitch_slider = Slider(min=-12, max=12, value=0)
        def on_pitch_change(_, value):
            self.pitch_label.text = f"Pitch: {value:+.02f}"
            self.pitch = value
        self.pitch_slider.bind(value=on_pitch_change)
        self.add_widget(self.pitch_slider)

        # Octave slider
        self.octave = 0
        self.octave_label = Label(text="Octave: +0")
        self.add_widget(self.octave_label)
        self.octave_slider = Slider(min=-4, max=4, step = 1, value=0)
        def on_octave_change(_, value):
            self.octave_label.text = f"Octave: {value:+d}"
            self.octave = value
        self.octave_slider.bind(value=on_octave_change)
        self.add_widget(self.octave_slider)

        # Buttons
        self.buttons = GridLayout(rows=3, cols=2)
        self.button_list = [Button(text="sine"), Button(text="square"), Button(text="saw")]
        for btn in self.button_list:
            btn.bind(on_press=self.button_callback)
            self.buttons.add_widget(btn)
        self.add_widget(self.buttons)
        for btn in self.button_list:
            if btn.text == self.waveform:
                self.button_callback(btn)


    def process_audio(self, dt, data): 
        if not self.active:
            self.out =  np.zeros(len(data), dtype=np.int16)
            return self.out
        
        data = self.root.mic_frames
        

        # Check for ended envelopes
        self.active_notes = {k:v for k,v in self.active_notes.items() if not v.envelope.ended}

        # Add any new notes:
        for note in self.root.midi.active_notes:
            if note not in self.active_notes:
                self.active_notes[note] = ActiveNote(note, self.root.midi.active_notes[note])
            elif note in self.active_notes and self.active_notes[note].triggered:
                self.active_notes[note].reactivate()
        for note in self.active_notes:
            if note not in self.root.midi.active_notes and not self.active_notes[note].triggered:
                self.active_notes[note].trigger_release()
        # If triggered and re-activated, set stepper back to ads


        out = self.get_carrier_tone(len(data))
        self.out = out
        return out

    def produce_tone(self, active_note, num_frames):
        freq = active_note.frequency
        # modulate from pitch and octave setting
        freq *= 2**((12*self.octave + self.pitch)/12)
        # modulate from pitch wheel
        freq *= 2**((2 * self.root.midi.pitchwheel) / (8191 * 12))

        active_note.oscillator.freq = freq
        active_note.set_waveform(self.waveform)
        tone = active_note.get_n_osc_steps(num_frames)
        env = active_note.get_n_env_steps(num_frames)
        return (tone * env * self.gain_slider.value).astype(np.int16)
        
    def get_carrier_tone(self, num_frames):
        out = np.zeros(num_frames, dtype=np.int16)
        for note in self.active_notes.values():
            out = add_no_clip(out, self.produce_tone(note, num_frames))
        return out
    
    def set_waveform(self, waveform):
        self.waveform = waveform

    def button_callback(self, instance):
        for btn in self.button_list:
            btn.background_color = COLOR_BTN_INACTIVE
        instance.background_color = COLOR_BTN_ACTIVE
        self.set_waveform(instance.text)


class Add(AudioModule):
    def __init__(self, root, gain=0.8, **kwargs):
        super().__init__(root, **kwargs)
        self.cols = 1
        assert len(self.incoming_modules) > 0
        # Widget Title Label
        self.label = Label(text = "Adder")
        self.add_widget(self.label)

        # Gain slider
        self.gain = gain
        self.gain_label = Label(text=f"Gain: {self.gain}")
        self.add_widget(self.gain_label)
        self.gain_slider = Slider(min=0, max=2, value=self.gain)
        def on_gain_change(_, value):
            self.gain_label.text = f"Gain: {value:.02f}"
            self.gain = value
        self.gain_slider.bind(value=on_gain_change)
        self.add_widget(self.gain_slider)

    def process_audio(self, dt, data):
        n_modules = len(self.incoming_modules)
        out = np.zeros(len(self.incoming_modules[0].out))
        for module in self.incoming_modules:
            out = (out + module.out * 1/n_modules * self.gain_slider.value)
        out = out.astype(np.int16)
        self.out = out
        return out


class Vocoder(AudioModule):
    def __init__(self, root, active=True, **kwargs):
        super().__init__(root, active, **kwargs)
        assert len(self.incoming_modules) == 1

        self.n_1_incoming = None
        self.n_1_mic = None

        self.n_channels = 4
        self.max_freq = 10_000
        self.min_freq = 100
        self.q = 0.9
        self.filter_order = 3

        self.calculate_filters()


        # Widget Title Label
        self.label = Label(text = "Vocoder")
        self.add_widget(self.label)

        # Channels slider
        self.ch_label = Label(text=f"Channels: {self.n_channels}")
        self.add_widget(self.ch_label)
        self.ch_slider = Slider(min=2, max=12, step = 1, value=self.n_channels)
        def on_ch_change(_, value):
            self.n_channels = value
            self.ch_label.text = f"Channels: {self.n_channels}"
            self.calculate_filters()
        self.ch_slider.bind(value=on_ch_change)
        self.add_widget(self.ch_slider)

        # Q slider
        self.q_label = Label(text=f"Q: {self.q}")
        self.add_widget(self.q_label)
        self.q_slider = Slider(min=0.01, max = 1,  value=self.q)
        def on_q_change(_, value):
            self.q = value
            self.q_label.text = f"Q: {self.q}"
            self.calculate_filters()
        self.q_slider.bind(value=on_q_change)
        self.add_widget(self.q_slider)

        # Min Freq slider
        self.min_f_label = Label(text=f"min_freq: {self.min_freq:0.0f}")
        self.add_widget(self.min_f_label)
        self.min_freq_slider = Slider(min=1.5, max = 4.2, value=float(np.log10(self.min_freq)))
        def on_min_freq_change(_, value):
            self.min_freq = 10**value
            self.min_f_label.text = f"min_freq: {self.min_freq:0.0f}"
            self.calculate_filters()
        self.min_freq_slider.bind(value=on_min_freq_change)
        self.add_widget(self.min_freq_slider)

        # Max Freq slider
        self.max_f_label = Label(text=f"max_freq: {self.max_freq:0.0f}")
        self.add_widget(self.max_f_label)
        self.max_freq_slider = Slider(min=1.5, max = 4.2, value=float(np.log10(self.max_freq)))
        def on_max_freq_change(_, value):
            self.max_freq = 10**value
            self.max_f_label.text = f"max_freq: {self.max_freq:0.0f}"
            self.calculate_filters()
        self.max_freq_slider.bind(value=on_max_freq_change)
        self.add_widget(self.max_freq_slider)

        # filter order slider
        self.order_label = Label(text=f"Filter Order: {self.filter_order}")
        self.add_widget(self.order_label)
        self.order_slider = Slider(min=1, max=4, step = 1, value=self.filter_order)
        def on_order_change(_, value):
            self.filter_order = value
            self.order_label.text = f"Filter Order: {self.filter_order}"
            self.calculate_filters()
        self.order_slider.bind(value=on_order_change)
        self.add_widget(self.order_slider)

    def calculate_filters(self):
        base_freq = (self.max_freq/self.min_freq)**(1/(self.n_channels-1))
        base_channel = np.log(self.min_freq) / np.log(base_freq)
        self.boost = 3 * np.sqrt(self.n_channels)


        self.filters = []
        self.fcs = []
        for k in range(self.n_channels):
            fc = base_freq ** (base_channel + k)
            self.fcs.append(fc)
            if k == 0:
                # First channel is low pass
                b, a = butter(self.filter_order, fc, "lowpass", fs=SR)
                self.filters.append((b,a))
            elif k == self.n_channels - 1:
                # Last channel is high pass
                b, a = butter(self.filter_order, fc, "highpass", fs=SR)
                self.filters.append((b,a))
            else:
                # Middle channels are band pass
                b, a = butter(self.filter_order, (base_freq ** (base_channel + k - self.q), base_freq ** (base_channel + k + self.q)), "bandpass", fs=SR)
                self.filters.append((b,a))


    def process_audio(self, dt, data):
        if not self.active:
            self.out = data
            return data
        
        n_0_incoming = self.incoming_modules[0].out
        n_0_mic = self.root.mic_frames
        if all(x is not None for x in (self.n_1_incoming,
                                       self.n_1_mic)): 
            
            all_incoming = np.concatenate((self.n_1_incoming, n_0_incoming))
            all_mic = np.concatenate((self.n_1_mic, n_0_mic))
            # Split modulator (mic)
            mic_data = self.root.mic_frames
            channel_amplitudes = self._get_channel_amplitudes(all_mic)
            # Split carrier (from tone gen)
            channel_carriers = self._get_channel_carriers(all_incoming)
            
            # Modulate the carrier per channel
            out = np.zeros(len(all_mic))
            for amp, carr in zip(channel_amplitudes, channel_carriers):
                out = add_no_clip(out, amp * carr)
                # out = add_no_clip(out, carr)

            out = out[len(self.n_1_mic):]


        else:
            out = np.zeros(len(data))
        

        self.n_1_incoming = n_0_incoming
        self.n_1_mic = n_0_mic
        self.out = out
        return out.astype(np.int16)
    
    def _get_channel_amplitudes(self, modulator):
        out = []
        for b,a in self.filters:
            filtered = lfilter(b, a, modulator)
            filtered = filtered * self.boost / np.iinfo(np.int16).max
            
            out.append(abs(hilbert(filtered)))
        return out

    def _get_channel_carriers(self, carrier):
        out = []
        for b,a in self.filters:
            filtered = lfilter(b, a, carrier)
            filtered *= self.boost
            out.append(filtered)
        return out


class MicInput(AudioModule):
    def __init__(self, root, delay=0, active=True, incoming_modules=None, gain=0.8, **kwargs):
        super().__init__(root, active, incoming_modules, **kwargs)
        self.frames = None

        # Widget Title Label
        self.label = Label(text = "MicInput")
        self.add_widget(self.label)

        # Gain slider
        self.gain = gain
        self.gain_label = Label(text=f"Gain: {self.gain}")
        self.add_widget(self.gain_label)
        self.gain_slider = Slider(min=0, max=2, value=self.gain)
        def on_gain_change(_, value):
            self.gain_label.text = f"Gain: {value:.02f}"
            self.gain = value
        self.gain_slider.bind(value=on_gain_change)
        self.add_widget(self.gain_slider)


    def process_audio(self, dt, data):
        if not self.active:
            self.out =  np.zeros(len(data), dtype=np.int16)
            return self.out
        frames = self.root.mic_frames
        self.out = frames * self.gain
        return self.out
 

class Beeps(AudioModule):
    def __init__(self, root, gain=0.8, **kwargs):
        super().__init__(root, **kwargs)
        self.cols = 1
        self.active_pads = []
        self.velocity = 0

        # Widget Title Label
        self.label = Label(text = "Beep Generator")
        self.add_widget(self.label)

        # Gain slider
        self.gain = gain
        self.gain_label = Label(text=f"Gain: {self.gain}")
        self.add_widget(self.gain_label)
        self.gain_slider = Slider(min=0, max=2, value=self.gain)
        def on_gain_change(_, value):
            self.gain_label.text = f"Gain: {value:.02f}"
            self.gain = value
        self.gain_slider.bind(value=on_gain_change)
        self.add_widget(self.gain_slider)

        self.pads = {40: ToneBeep(waveform="sine"),
                     41: ToneBeep(waveform="square"),
                     42: ToneBeep(waveform="saw"),
                     43: ToneBeep(),
                     44: ToneBeep(),
                     45: ToneBeep(),
                     46: ToneBeep(),
                     47: ToneBeep()}

        # Active Pads Label
        self.pad_label = Label(text = f"Active Pads: {self.active_pads}")
        self.add_widget(self.pad_label)

    def process_audio(self, dt, data): 
        if not self.active:
            self.out =  np.zeros(len(data), dtype=np.int16)
            return self.out
        data = self.root.mic_frames


        # Check for ended envelopes
        self.active_pads = [pad for pad in self.active_pads if not self.pads[pad].envelope.ended]
        
        # Add any new notes:
        for note in self.root.midi.active_pads:
            if note not in self.active_pads:
                self.active_pads.append(note)
                self.velocity = self.root.midi.active_pads[note]
                self.pads[note].reset()
            elif note in self.active_pads and self.pads[note].triggered:
                self.pads[note].reset()
                self.velocity = self.root.midi.active_pads[note]
        for note in self.active_pads:
            if note not in self.root.midi.active_pads and not self.pads[note].triggered:
                self.pads[note].trigger_release()

        if self.active_pads:
            note = self.active_pads[-1]
            beep = self.pads[note]
            if self.root.midi.aftertouch:
                self.velocity = self.root.midi.aftertouch
            control = [self.root.midi.controls[x] for x in range(70,78)]
            out = beep.update(len(data), self.velocity, control)
        else:
            out = np.zeros(len(data))

        self.pad_label.text = f"Active Pads: {self.active_pads} {[self.pads[pad].envelope.ended for pad in self.active_pads]}"
        out = out * self.gain
        self.out = out
        return out
    

class ModuleWidget(GridLayout):
    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.cols = 4
        self.root = root
        self.modules = [None for _ in range(7)]
        self.active = True

        self.button = Button(text="Active" if self.active else "Inactive", background_color=COLOR_BTN_ACTIVE if self.active else COLOR_BTN_INACTIVE)
        self.button.bind(on_press = self.activate_callback)
        self.add_widget(self.button)

        self.modules[0] = MicInput(root, gain=0.2)
        self.modules[1] = ToneGenerator(root, waveform="sine")
        self.modules[2] = ToneGenerator(root, waveform="saw", active=False, gain=0.5)
        self.modules[3] = Add(root, incoming_modules=self.modules[1:3], gain=1.5)
        self.modules[4] = Vocoder(root, incoming_modules=self.modules[3:4])
        self.modules[5] = Beeps(root)
        self.modules[6] = Add(root, incoming_modules=[self.modules[0],self.modules[4],self.modules[5]], gain=1.5)

        # self.modules[0] = MicInput(root, gain=1.0)
        # self.modules[1] = ToneGenerator(root, waveform="sine")
        # self.modules[2] = ToneGenerator(root, waveform="sine",  gain=0.5)
        # self.modules[3] = ToneGenerator(root, waveform="saw", gain=0.2)
        # self.modules[4] = Add(root, incoming_modules=self.modules[0:4], gain=1.5)

        # for i in range(5,):
        #     self.modules[i] = PassThrough(root, incoming_modules=[self.modules[i-1]])
  

        for module in self.modules:
            self.add_widget(module)

    def update(self, dt, data):
        if self.active:
            for module in self.modules:
                data = module.process_audio(dt, data)
        else:
            data = self.root.mic_frames
        self.root.output_vis.update(dt, data)
        data = data.tobytes()
        self.root.audio.write(data)

    def activate_callback(self, _):
        self.active = not self.active
        self.button.background_color = COLOR_BTN_ACTIVE if self.active else COLOR_BTN_INACTIVE
        self.button.text="Active" if self.active else "Inactive"
        with self.canvas.before:
            color = COLOR_MODULE_BG if self.active else COLOR_MODULE_BG_INACTIVE
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.midi = MidiInputManager(self)
        self.audio = AudioInputManager()
        self.fx = FXManager()
        self.mic_frames = None

        # Top
        self.top_section = BoxLayout(orientation = "horizontal", size_hint=(1,0.1))
        self.add_widget(self.top_section)
        # Top: Mic gain
        self.gain_slider_with_label = BoxLayout(orientation = "vertical", size_hint=(1,1))
        self.top_section.add_widget(self.gain_slider_with_label)
        self.gain = 16
        self.gain_label = Label(text=f"Mic Gain: {self.gain:.02f}")
        self.gain_slider_with_label.add_widget(self.gain_label)
        self.gain_slider = Slider(min=0, max=32, value=self.gain)
        def on_gain_change(_, value):
            self.gain_label.text = f"Mic Gain: {value:.02f}"
            self.gain = value
        self.gain_slider.bind(value=on_gain_change)
        self.gain_slider_with_label.add_widget(self.gain_slider)

        # Top low pass 
        self.lowpass_slider_with_label = BoxLayout(orientation = "vertical", size_hint=(1,1))
        self.top_section.add_widget(self.lowpass_slider_with_label)
        self.lowpass = 10000
        self.lowpass_label = Label(text=f"Mic lowpass: {self.lowpass:.0f}")
        self.lowpass_slider_with_label.add_widget(self.lowpass_label)
        self.lowpass_slider = Slider(min=50, max=20000, step=1,value=self.lowpass)
        def on_lowpass_change(_, value):
            self.lowpass_label.text = f"Mic lowpass: {value:.0f}"
            self.lowpass = value
        self.lowpass_slider.bind(value=on_lowpass_change)
        self.lowpass_slider_with_label.add_widget(self.lowpass_slider)
        # Top : MIDI label
        self.midi_label = Label()
        self.top_section.add_widget(self.midi_label)


        # Modules
        self.modules = ModuleWidget(self)
        self.add_widget(self.modules)

        # Bottom
        self.bottom = BoxLayout(orientation = "horizontal", size_hint=(1.0, 0.3))
        self.add_widget(self.bottom)
        # Bottom: Input Vis
        self.audio_vis = AudioVisualizer(y_factor=0.3, fft_y_factor=30)
        self.bottom.add_widget(self.audio_vis)
        # Bottom : Output Vis
        self.output_vis = AudioVisualizer(y_factor=0.3, fft_y_factor=30)
        self.bottom.add_widget(self.output_vis)

        # Reset Button
        self.reset_button = Button(text = "Reset Stream", size_hint=(1.0, 0.1))
        def reset_callback(_):
            self.audio.reset_stream()
            self.midi.midi_stream.close()
            self.midi = MidiInputManager(self)
        self.reset_button.bind(on_press=reset_callback)
        self.add_widget(self.reset_button)


    def update(self, dt):
        # Read audio data since last update
        audio_data = self.audio.read()
        if audio_data: 
            signal_array = np.frombuffer(audio_data, np.int16) * self.gain
            b, a = butter(3, (10, self.lowpass), "bandpass", fs=SR)
            signal_array = lfilter(b, a, signal_array)
            self.mic_frames = signal_array.astype(np.int16)
            self.audio_vis.update(dt, signal_array)
            self.modules.update(dt, signal_array)

        # Read MIDI changes since last update
        self.midi.update(dt)

        logger.debug(f"{dt:.03f}")   


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_widget = MainWidget()
        

    def build(self): 
        Clock.schedule_interval(self.update, APP_FRAMERATE)
        return self.main_widget
    
    def update(self, dt):
        self.main_widget.update(dt)

    


if __name__ == '__main__':
    MyApp().run()

