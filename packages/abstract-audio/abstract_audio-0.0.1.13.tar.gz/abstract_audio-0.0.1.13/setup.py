from time import time
from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='abstract_audio',
    version='0.0.1.13',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='This module provides functionalities to capture and manipulate audio input from a microphone and save them into a text file. It uses an abstract GUI to display the state of audio recording and playback..',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_audio',
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.11'],
    install_requires=['playsound>=1.3.0', 'gtts>=2.3.2', 'pydub>=0.25.1', 'PySimpleGUI>=4.60.5', 'abstract_utilities>=0.2.2.32', 'abstract_gui>=0.0.61.71'],
    python_requires='>=3.6',
    setup_requires=['wheel'],
)