import mido
import time
import pandas as pd
from threading import Thread, Event

# need to make sure that the backend is set to pygame to be compatible with PsychoPy
mido.set_backend('mido.backends.pygame')

ACCEPTED_MESSAGES = ('note_on', 'note_off')


class MidiInterface:
    """
    The basic interface that receives and transmits data through MIDI.

    The setup uses Python's thread-based parallelism to collect data asynchronously. This interface is designed to
    interact with the MIDI device through the mido library directly. The higher level controller class, MidiController,
    is designed to handle the data collection process.
    """
    class MidiThread(Thread):
        """
        This is a separate class to control the thread behaviors for asynchronous data collection.
        Each time the start_streaming method is called, we will start a new thread.
        """

        def __init__(self, func):
            Thread.__init__(self)
            self.func = func
            self.daemon = True
            self.streaming = Event()
            self.streaming.set()

        def run(self):
            while self.streaming.is_set():
                self.func()

        def terminate(self):
            self.streaming.clear()

    def __init__(self,
                 device_name='UM-ONE',
                 ):
        """
        :param device_name: the name of the MIDI device that you want to connect to. This can be found by running the
        mido.get_input_names() function or the wrapper function in the functions module.
        """
        self.device_name = device_name

        try:
            self.in_port = mido.open_input(self.device_name)
        except:
            print('MIDI device not found. Please check the device name and try again.')
            return

        self.thread = None
        self._listeners = []
        self.frame_data = None

        self.start_time = None
        self.i_event = None
        self.i_note = None
        self.key_is_pressed = False
        self.sequence_out_template = pd.DataFrame({
            'order': None,
            'note': None,
            'type': None,
            'velocity': None,
            'timestamp': None,
        }, index=[0])

    def start_streaming(self):
        self.start_time = time.time()
        self.i_event = 0  # used to modulate the frame
        self.i_note = 0
        self.thread = self.MidiThread(self.update)
        self.thread.start()
        print('Midi streaming has started!')

    def stop_streaming(self):
        self.thread.terminate()
        print('Midi streaming is terminated!')

    def accept_notes(self):
        # Only let note_on and note_off messages through.
        for message in self.in_port:
            if message.type in ACCEPTED_MESSAGES:  # Only interested in note messages
                yield message

    def subscribe(self, callback):
        self._listeners.append(callback)

    def unsubscribe(self, callback):
        self._listeners.remove(callback)

    def send_data(self):
        for callback in self._listeners:
            callback(self.frame_data)

    def update(self):
        """
        This function records a specific number of notes, defined by the input
        """
        for msg in self.accept_notes():
            # keep track of the total number of notes played based on when the key was released
            if msg.type == 'note_on':
                if msg.velocity > 0:  # keypress starts
                    temp_sequence_full = self.sequence_out_template.copy()
                    temp_sequence_full['order'] = self.i_note
                    temp_sequence_full['note'] = msg.note
                    temp_sequence_full['type'] = 'key_down'
                    temp_sequence_full['velocity'] = msg.velocity
                    temp_sequence_full['timestamp'] = time.time() - self.start_time

                    # store the frame data
                    self.frame_data = temp_sequence_full
                    self.send_data()

                    self.key_is_pressed = True

                else:  # keypress is released
                    if self.key_is_pressed:
                        temp_sequence_full = self.sequence_out_template.copy()
                        temp_sequence_full['order'] = self.i_note
                        temp_sequence_full['note'] = msg.note
                        temp_sequence_full['type'] = 'key_released'
                        temp_sequence_full['velocity'] = msg.velocity
                        temp_sequence_full['timestamp'] = time.time() - self.start_time

                        # store the frame data
                        self.frame_data = temp_sequence_full
                        self.send_data()

                        self.key_is_pressed = False
                        self.i_note += 1
