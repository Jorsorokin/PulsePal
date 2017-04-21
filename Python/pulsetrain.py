"""
pulsetrain.py

A script for the PulsePal that initiates a continuous pulse train at a user-specified pulse frequency. 
The stimulus is indefinite until the user presses "enter" on the terminal to end the protocol.

By default, the pulse sent through the PulsePal is 5V, and the pulse width and inter-pulse widths are 
equal to one another, and are determined by the pulse frequency as:
            1/2 * (1 / pulseFrequency)

Dependencies:
    - PulsePal python package

Known issues:
    - there is a physical constraint on the pulse frequency determined by the capacitive properties 
    of your stimulus generator. For instance, setting the pulse frequency to 1000 Hz would result in 
    a pulse width of .0005 ms, which may be too fast for the stimulus generator to send a reliable pulse.
    For typical frequencies between 1 & 100 Hz, this shouldn't be an issue.

Written by Jordan Sorokin, 4/6/2017
"""

# imports
import thread, time
from PulsePal import PulsePalObject # import PulsePalObject

# function for checking keypress
def input_thread(key):
    raw_input()
    key.append(None)

# Initializing PulsePal
pp = PulsePalObject() # Create a new instance of a PulsePal object
pp.connect('COM3') # <-- check this for MAC
pp.setDisplay('Connected to:','Python')
print('Connected to PulsePal, version ' + str(pp.firmwareVersion))
time.sleep(2)

# set up the pulse train for ch. 1
pulseFreq = float(input('pulse frequency (Hz): '))
#pulseWidth = 1 / pulseFreq / 2; # here we set the pulse width and inter-pulse width equal to one another
pulseWidth = float(input('pulse width (s): '))
interPulseWidth = 1.0 / pulseFreq - pulseWidth
pulseOn = [0.0,1/pulseFreq]
pulseVoltages = [5,5]

# create the custom pulse train and set to Channel 1 of the PulsePal
pp.interPulseInterval[1] = interPulseWidth
pp.sendCustomPulseTrain(1,pulseOn,pulseVolages) # create custom pulse train # 1
pp.programOutputChannelParam('customTrainID',1,1) # set channel 1 of the PulsePal to output the pulse train
pp.programOutputChannelParam("isBiphasic",1,0) # only positive, monophasic step pulses
pp.setContinuousLoop(1,1) # sets the output of the pulse to be continuous, thus the pulse stimulus will continue indefinitely

# initialize the pulse train. Set "key" to respond to the user pressing "enter" on the keyboard to stop the pulses
key = []
thread.start_new_thread(input_thread, (key,))
pp.setDisplay('Starting program:', str(pulseFreq) + ' Hz')
time.sleep(2)

# trigger the pulse train
print('Press ENTER to end the electroplating program')
pp.triggerOutputChannels()

# check if "enter" is pressed
if key:

    # terminate
    pp.abortPulseTrains() # terminate the pulse output
    pp.setContinuousLoop(1,0) # terminates the continuous loop (for future use since parameters are saved internally)
    print('disconnected from PulsePal')
    pp.setDisplay('disconnected from', 'Python')
    pp.disconnect()