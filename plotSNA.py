#Silje Skeide Fuglerud
#April 2015 
#Originally: Weerapat Pittayakanchit
# Date: July 26, 2014
#
# Best tutorials and examples:
#	 Mahesh Venkitachalam
# 		https://gist.github.com/electronut/d5e5f68c610821e311b0
#		He writes a python code to continuously read the data from arduino
# 		and plot the graph. Pretty close to what I want to do.
#
#	 Jake Vanderplas
#		http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
#		He explains how to use animatio in matplotlib with
#		four different examples.

import sys, serial
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# To make main() less complicated, I separate the part where I setup variables
# with Arduino in this function setArguments
def setArguments():
    # expect 4 args
    # arg 1: serial port string
    # arg 2: starting frequency in MHz
    # arg 3: stopping frequency in MHz
    # arg 4: number of steps between starting and stopping frequencies
    if(len(sys.argv) != 5):
        print '\nYou are running using the default parameters.'
        print 'Example Usage: python plotSNA.py "COM3" 25 45 300'
        strPort = "COM3"
        start = 25
        stop = 45
        steps = 300
    elif(len(sys.argv) == 2):
    # One argument for port name
        strPort = sys.argv[1]
        start = 1
        stop = 70
        steps = 100
    else:
    # Setup variable according to the input arguments
        strPort = sys.argv[1]
        start = int(sys.argv[2])
        stop = int(sys.argv[3])
        steps = int(sys.argv[4])
    # Connect with arduino
    ser = serial.Serial(strPort, 9600, timeout = 1)
    
    # I decide to send the string of numbers instead of the bytes because
    # the original code in arduino can already read string
    for i in range(len(str(start))):
        ser.write(str(start)[i])
        
    # Tell arduino that those previous numbers are for the starting frequency
    ser.write('A')
    # Ex: if start = 123 then 
    # it will run:  ser.write('1')
    #				   ser.write('2')
    #				   ser.write('3')
    
    for i in range(len(str(stop))):
        ser.write(str(stop)[i])
    # Tell arduino that those previous numbers are for the stopping frequency
    ser.write('B')
    
    for i in range(len(str(steps))):
        ser.write(str(steps)[i])
    # Tell arduino that those previous numbers are for the number of steps
    ser.write('N')
    
    data = ser.readline()
    if data:
        print data.rstrip('\n') #strip out the new lines for now
		# (better to do .read() in the long run for this reason 
    #ser.write('s')
    return start, stop, steps, ser

	
# Read arguments, sweep through different frequencies, and animate graph
def main():
    start, stop, steps, ser = setArguments()
    # setup all the variables appear in the plot here - the appearance
    fig = plt.figure()
    fig.suptitle('Finding The Resonance Frequency of The Testing Device')
    ax = plt.axes(xlim=(start,stop), ylim=(0,125))
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Reflected Power (%)')
    ax.grid()
    line, = ax.plot([], [], lw=2)
    # Resonance stands for the resonance frequency
    resonance_text = ax.text(0.02, 0.95, ' ', transform = ax.transAxes)
    # qFactor stands for Quality factor: Q = f/df where f is the resonance freq
    # and df is the half-power bandwidth
    qFactor_text = ax.text(0.02,0.90, ' ', transform = ax.transAxes)
    # Gamma in this context means the reflected power
    gamma_text = ax.text(0.02, 0.85, ' ', transform = ax.transAxes)
    # initialization function: plot the background of each frame
    def init():
        line.set_data([], [])
        #time.sleep(.1)
        #print('I am in init')
        return line, resonance_text, qFactor_text, gamma_text
        
    # animation function.  This is called sequentially
    def update(n):
        #print('I am in update')
        #print "frame number: " + str(n)
        dataFreq = []
        dataGamma = []
        ser.write('s')
        for i in range(steps + 1):
            inputStr = ser.readline()
            #print(inputStr, len(inputStr))
            time.sleep(.01) # Delay for one hundred of a second

            # See arduino file - SNA - for more info
            nspaces=inputStr.count(" ")
            if nspaces<1:
                print("Not enough data")
                quit
            strValues=[float(x) for x in inputStr.split()]
            
            #freq, gamma, fwd, rev, dump = inputStr.split(" ")
            #dataFreq.append(float(freq))
            #dataGamma.append(float(gamma))
            dataFreq.append(float(strValues[0]))
            dataGamma.append(float(strValues[1]))
        # Find the resonance frequency
        minGamma = min(dataGamma)
        resonanceIndex = dataGamma.index(minGamma)
        resonanceFreq = dataFreq[resonanceIndex]
        # Find the quality factor by finding the freq just outside
        # the half-max bandwidth (1/2 max power)
        # When we can't find the freq outside the bandwidth
        # we use
        highF = stop
        lowF = start
        # Find the highest freq of the bandwidth
        for k in range(resonanceIndex, steps):
            if (dataGamma[k] > 100 - float(100-minGamma)/2):
                highF = dataFreq[k]
                break
        # Find the lowest freq in the bandwidth
        for k in range(resonanceIndex, 0, -1):
            if (dataGamma[k] > 100 - float(100-minGamma)/2):
                lowF = dataFreq[k]
                break
        if (highF == lowF):
            Q = float("inf")
        else:
            Q = resonanceFreq / (highF - lowF)
            
        resonance_text.set_text('Resonance Freq is %.2f MHz' % resonanceFreq)
        qFactor_text.set_text('Quality Factor is %.2f (%.2f MHz, %.2f MHz)' % (Q, lowF, highF))
        gamma_text.set_text('Minimum Reflected Power is %.4f %%' % minGamma)
        # update the line
        line.set_data(np.asarray(dataFreq), np.asarray(dataGamma))
        return line, resonance_text, qFactor_text, gamma_text
        
    anim= animation.FuncAnimation(fig, update, init_func=init,fargs=None, blit=True)							    
    plt.show()
    fig= plt.figure()
    return anim
    
	
if __name__ == "__main__": 
    anim =main()
    #plt.show()
    #fig =plt.figure()
