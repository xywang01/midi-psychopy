from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='midi-psychopy',
    version='0.0.1',
    description='A Python interface for asynchronous MIDI data collection using PsychoPy',
    url='https://github.com/xywang01/midi-psychopy',
    download_url='https://github.com/xywang01/midi-psychopy/archive/refs/tags/0.0.1.tar.gz',
    author='X. Michael Wang, Centre for Motor Control, University of Toronto, Faculty of Kinesiology and Physical Education',
    author_email='michaelwxy.wang@utoronto.ca',
    license='MIT',
    packages=['midi_psychopy', ],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'mido',
        'numpy',
        'pandas',
        'matplotlib',
    ]
)
