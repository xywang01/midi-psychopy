import time
import pandas as pd
from midi_interface import MidiInterface

class MidiController:
    """
    The controller class that handles the data collection process.

    Users should instantiate this class in their PsychoPy experiment script to collect MIDI data asynchronously.
    """
    def __init__(self, device_name='UM-ONE'):
        self.sequence_out = None
        self.sequence_out_full = None

        self.midi = MidiInterface(device_name)
        self.midi.subscribe(self.receive_from_midi)

        self.is_streaming = False

        self.psychopy_global_timer = None

    def add_global_timer(self, global_timer):
        """
        A method to add the global timer from PsychoPy to the controller. This is useful for timestamping the data based
        on the global time of the experiment.
        :param global_timer:
        """
        self.psychopy_global_timer = global_timer

    def start_data_collection(self):
        """
        Start the data collection process.
        """
        self.sequence_out_full = pd.DataFrame()  # a df for more detailed output
        self.midi.start_streaming()
        self.is_streaming = True

    def stop_data_collection(self):
        """
        Stop the data collection process.
        """
        self.midi.stop_streaming()
        self.is_streaming = False

    def receive_from_midi(self, frame_data):
        """
        A callback function that receives data from the MIDI interface. This function is called every time a MIDI event
        is detected.
        """
        if self.psychopy_global_timer is not None:
            # add the global time to the frame data
            frame_data['global_time'] = self.psychopy_global_timer.getTime()

        self.sequence_out_full = pd.concat((self.sequence_out_full, frame_data), ignore_index=True)


if __name__ == '__main__':
    controller = MidiController()

    controller.start_data_collection()

    time.sleep(10)

    controller.stop_data_collection()

    print(controller.sequence_out_full)
