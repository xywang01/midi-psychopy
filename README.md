# midi-psychopy - A Python interface for asynchronous MIDI data collection

The MIDI Interface is a Python package designed to interact with MIDI devices through the 
[Mido](https://github.com/mido/mido) library. It provides functionality to receive and 
transmit MIDI data asynchronously, which is useful for real-time data collection in
PsychoPy experiments.

## Installation

You can install the MIDI Interface package using pip:

```bash
pip install midi-psychopy
```

## Usage

### Basic Usage - Collecting MIDI Data

```python
import time
import pandas as pd
from midi_controller import MidiController

# Create an instance of MidiController
controller = MidiController(device_name='UM-ONE')

# Start data collection
controller.start_data_collection()

# Let the program run for some time (e.g., 10 seconds)
time.sleep(10)

# Stop data collection
controller.stop_data_collection()

# Access the collected MIDI data
print(controller.sequence_out_full)
```

### In PsychoPy

The setup for using the MidiController in a PsychoPy experiment is similar to the basic usage. Users can follow the 
steps below to integrate the MidiController into their experiment:

1. Create a code component in the PsychoPy Builder interface inside the routine where you want to collect MIDI data.
2. Import and instantiate the MidiController object in the "Begin Experiment" tab.

```python
import os
import pandas as pd
from midi_controller import MidiController

# Create an instance of MidiController
midi_controller = MidiController(device_name='UM-ONE')

# Initialize a DataFrame to store the collected MIDI data
keypress_data = pd.DataFrame()

# Also initialize a variable to keep track of the trial number
trial_count = 0

# Define the path to save the data
# expInfo is standard PsychoPy variable. make sure to check the name of the identifying variable in your experiment 
# (i.e., participant is the default name for the participant ID defined in the "Experiment Info" section of the "Basic" 
# tab in the PsychoPy GUI's "Properties" window).
par_id = expInfo['participant']  
save_dir = os.path.abspath(f'./data_keypress')
file_name = f'par_{par_id}.csv'
save_path = f'{save_dir}/{file_name}'
```

3. Start data collection in the "Begin Routine" tab.

```python
# Start data collection
midi_controller.start_data_collection()
```

4. Stop data collection in the "End Routine" tab.

```python
# Stop data collection
midi_controller.stop_data_collection()
```

Alternatively, a conditional statement can also be used in the "Each Frame" tab to terminate data collection based 
on certain conditions.

```python
if some_condition:
    midi_controller.stop_data_collection()
```

5. Store the collected MIDI data in the "End Experiment" tab.

Because the start_data_collection() method would reset the collected data (sequence_out_full) each time it is called,
the data should be stored locally as a csv file or in a Pandas DataFrame.

```python
temp_out = midi_controller.sequence_out_full
# Add a column to store the trial number. If there are other variables to store, add them here.
temp_out['trial'] = trial_count

trial_count += 1

# Append the collected data to the keypress_data DataFrame
keypress_data = pd.concat([keypress_data, temp_out], ignore_index=True)

# Save the data to a csv file in case the experiment crashes
keypress_data.to_csv(save_path)
```
## Requirements

- Python 3.x
- Mido
- Pandas

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a 
pull request on GitHub.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## MIDI Interface
For more details about the underlying MIDI interface used by the MidiController, refer to midi_interface.py.
