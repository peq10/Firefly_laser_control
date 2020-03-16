#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:58:21 2020

@author: peter
"""

import numpy as np
import matplotlib.pyplot as plt
import neo #https://neo.readthedocs.io/en/stable/
import scipy.stats

def load_ephys(path,lazy = False):
    reader = neo.io.Spike2IO(path)
    bl = reader.read(lazy = lazy)[0]
    return bl

#file in dropbox
ephys_fname = '/home/peter/Dropbox/Imperial/MScSupervision/20170208_CHO_noNR_Cell4/Cell4TCourse.smr'
calibration_fname = '/home/peter/Dropbox/Imperial/MScSupervision/20170208_CHO_noNR_Cell4/power_calibration_980nm_8um_spot.dat'

#load using python-neo
ephys = load_ephys(ephys_fname)

#plot the data
Im = ephys.segments[0].analogsignals[2][:,1]
Vm = ephys.segments[0].analogsignals[1][:,1]
print(f'Im units: {Im.units}')
print(f'Vm units: {Vm.units}')
print(f'Im sampling rate: {Im.sampling_rate}')

fig,axarr = plt.subplots(nrows = 4,sharex = True)
axarr[0].plot(Im.times,np.squeeze(Im))
axarr[0].set_ylabel(f'Membrane Current\n({Im.units})')
axarr[0].set_ylim([-1,1])

axarr[1].plot(Vm.times,np.squeeze(Vm))
axarr[1].set_ylabel(f'Membrane Voltage\n({Vm.units})')
axarr[1].set_ylim([-50,-10])

#This channel shows the command voltage sent to the pockels cell which controls the laser power
pockels = ephys.segments[0].analogsignals[0][:,0]

#this channel shows the power measurement from a beam sampler, proportional to the actual laser power in the system
#This measurement has a slow time course and so a calibration run is taken first with longer stimulation duration 
#to enable us to link the 
picker = ephys.segments[0].analogsignals[0][:,1]

axarr[2].plot(pockels.times,np.squeeze(pockels))
axarr[2].set_ylabel('Pockels cell\ncommand voltage (V)')
axarr[3].plot(picker.times,np.squeeze(picker))
axarr[3].set_ylabel('Picker power meter\nmeasurement output (V)')
axarr[3].set_xlabel('Time (s)')
plt.show()


#NOTE that sampling rates for these last two channels is different! 
#Need to use time to compare properly

print(f'Pockels cell sampling rate: {pockels.sampling_rate}')

#load the calibration file
sample_power_calibration = np.loadtxt(calibration_fname)

#plot the calibration
fig,ax = plt.subplots()
ax.plot(sample_power_calibration[0,:],sample_power_calibration[1,:])
ax.set_xlabel('Picker power (mW)')
ax.set_ylabel('Power onto cell (mW)')
plt.show()

#These two constants allow you to convert the voltage measured at the picker 
#into a mW value measured at the picker. The power meter outputs between 0 and picker_max_output Volts
#in direct proportion to the input power as a fraction of picker_max_measurement_mW.
#i.e. if the Picker outputs 1 V, it is measuring 250 mA of current.
picker_max_output_V = 2
picker_max_measurement_mW = 500
beam_spot_diameter = 8 #in micro meters


#this next variable is an array with times and labels which tells us when the calibration and stimulation occurred.
#The label key is in the following dict:
#The keys are loaded as bytes and need to be recovered as characters using the built in chr() function after converting from byte to int
label_key = {'A':'cancel','F':'calibrate','E':'stimulate'}
keyboard = ephys.segments[0].events[1]
labels = [chr(int(x)) for x in keyboard.labels]

print('Trace contains the following events:')
[print(f'Event: {label_key[chr(int(keyboard.labels[x]))]} at time {keyboard[x]:.0f}') for x in range(len(keyboard))]



#Task 1:
#turn the Pockels command measurement into optical Power density in the sample (in mW / um^2) using 
#the previous two constants, the calibration curve measured in the pockels time course,
#and the sample_power_calibration (above) which converts between power in the picker and power
#in the sample.

#Plot a curve with pockels cell command voltage (in V) on the x axis, and power density
#in the sample on the y axis.


#Task 2:
#Segment the measured current values for each stimulation power and repeat.

#Plot the Stimulation power - membrane current curve for the first stimulation

#Then plot the 'bleaching' curve: plot the decrease in evoked photocurrent with repeat number.



