"""
electroplate.py

A script for the PulsePal that initiates a continuous pulse train for electroplating electrodes.
The pulse train is composed of 0.5s pulses of 5V and inter-pulse durations of 2s to provide enough time
to move the stimulating electrode to the proper leads on your EIB.

Two different tones are played...a short, high-frequency tone that signifies the start of a pulse
and a longer, lower-frequency tone that signifies the end of the pulse.

When you are finished electroplating, highlight the terminal that was used to call the script and
press "enter" on the keyboard to end the continuous pulse.

By Jordan Sorokin, 3/13/2017
"""

# imports
import thread, time, winsound
from PulsePal import PulsePalObject # Import PulsePalObject

# Initializing PulsePal
pp = PulsePalObject() # Create a new instance of a PulsePal object
pp.connect('COM3') # Connect to PulsePal on port COM3 (open port, handshake and receive firmware version)
pp.setDisplay("Connected to:","Python")
print('Connected to PulsePal, version ' + str(pp.firmwareVersion))
winsound.PlaySound('SystemExclamation',winsound.SND_ALIAS)
time.sleep(2)

# set up the pulse train for ch. 1
pulsewidth = input("pulse width (s): ")
pp.programOutputChannelParam("phase1Voltage",1,5.0) # 5V pulse
pp.programOutputChannelParam("isBiphasic",1,0) # only positive, monophasic

# function for checking keypress
def input_thread(key):
    raw_input()
    key.append(None)

# initialize loop
key = []
thread.start_new_thread(input_thread, (key,))
pp.setDisplay("Starting program:",str(pulsewidth) +" sec pulses")
time.sleep(2)
print('Press ENTER to end the electroplating program')

# loop indefinitely
pp.setContinuousLoop(1,1)
while True:
    # check if "enter" is pressed
    if key:
        break

    # send a pulse and warning tone
    pp.setContinuousLoop(1,1)
    winsound.Beep(660,250) # high freq beep
    pp.triggerOutputChannels(1,0,0,0) # send a pulse through ch. 1

    # send a low-freq tone indicating the end
    time.sleep(pulsewidth-0.5) # takes about 1/2 second to turn off output
    pp.setContinuousLoop(1,0)
    time.sleep(0.5)
    winsound.Beep(220,500) # low freq beep
    time.sleep(2) # rest-period for changing leads

# terminate
pp.setContinuousLoop(1,0)
print('disconnected from PulsePal')
pp.setDisplay("God speed,","Mr. Mouse")
time.sleep(2)
pp.disconnect()
