import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import thinkdsp
import numpy as np

def corrcoef(xs, ys):
    return np.corrcoef(xs, ys, ddof=0)[0, 1]

def serial_corr(wave, lag=1):
    N = len(wave)
    y1 = wave.ys[lag:]
    y2 = wave.ys[:N-lag]
    corr = corrcoef(y1, y2)
    return corr

def autocorr(wave):
    """Computes and plots the autocorrelation function.

    wave: Wave
    """
    lags = range(len(wave.ys)//2)
    corrs = [serial_corr(wave, lag) for lag in lags]
    return lags, corrs

def turnLED(number):
    for i in range(len(guitar)):
        if number == i:
            GPIO.output(notes[i], GPIO.HIGH) # notes[i] = on
        else:
            GPIO.output(notes[i], GPIO.LOW) # notes[i] = off

ADC.setup()
GPIO.setup("P9_23",GPIO.IN)
GPIO.add_event_detect("P9_23", GPIO.FALLING)

GPIO.setup("P8_11", GPIO.OUT) # E4
GPIO.setup("P8_12", GPIO.OUT) # B3
GPIO.setup("P8_13", GPIO.OUT) # G3
GPIO.setup("P8_14", GPIO.OUT) # D3
GPIO.setup("P8_15", GPIO.OUT) # A2
GPIO.setup("P8_16", GPIO.OUT) # E2
GPIO.setup("P8_17", GPIO.OUT) # green
GPIO.setup("P8_18", GPIO.OUT) # sharp
GPIO.setup("P8_21", GPIO.OUT) # flat

guitar = [329, 246, 196, 146, 110, 82] 
# notes = [E4, B3, G3, D3, A2, E2]
notes = ["P8_11", "P8_12", "P8_13", "P8_14", "P8_15", "P8_16"]
#your amazing code here
#detect wherever:
while True:
	sampleArray = []
	# DO all the stuff in here
	if GPIO.event_detected("P9_23"):
		print "event detected!"
		time.sleep(.5)
		for i in range(2000):
			sampleArray.append(ADC.read("P9_39"))
		writeArray = np.asarray(sampleArray)
		np.set_printoptions(suppress=True)
		np.savetxt("test.csv",writeArray,delimiter=',',fmt='%.4f')
		print "DONE GETTING DATA"
		wave = thinkdsp.Wave(np.asarray(sampleArray),framerate=833)
		wave.apodize()
		lags, corrs = autocorr(wave)
		wave2 = thinkdsp.Wave(corrs,framerate=1)
		period = 1.0/wave2.make_spectrum().peaks()[0][1]
		#hs = np.fft.rfft(corrs)
		#amps = np.absolute(hs)
		#n = len(hs)
		#old_freq = 883/2.0
		#old_freq = 1/2.0
		#if n%2 == 0:
		#	max_freq = old_freq
		#else:
		#	max_freq = old_freq * (n-1) / n
            
		#fs = np.linspace(0, max_freq, n)
		#t = zip(amps, fs)
		#t.sort(reverse=True)
		#period = 1.0/t[0][1]
		freq = 1.0/(period*(1/833.0))
		print freq, " FREQUENCY IS"


		# GPIO.cleanup()
		if freq > 329:
		    turnLED(0)
		    GPIO.output("P8_17", GPIO.LOW) # green = off
		    GPIO.output("P8_18", GPIO.HIGH) # sharp = on
		    GPIO.output("P8_21", GPIO.LOW) # flat = off
		       
		    
		elif freq < 82:
		    turnLED(5)
		    GPIO.output("P8_17", GPIO.LOW) # green = off
		    GPIO.output("P8_18", GPIO.LOW) # sharp = off
		    GPIO.output("P8_21", GPIO.HIGH) # flat = on
		else:
		    for i in range(len(guitar)):
		        if abs(freq - guitar[i]) > 3:
		            turnLED(i)
		            GPIO.output("P8_17", GPIO.HIGH) # green = on
		            GPIO.output("P8_18", GPIO.LOW) # sharp = off
		            GPIO.output("P8_21", GPIO.LOW) # flat = off

		        elif freq > (guitar[i] + guitar[i+1])/2:
		            turnLED(i)
		            GPIO.output("P8_17", GPIO.LOW) # green = off
		            GPIO.output("P8_18", GPIO.HIGH) # sharp = on
		            GPIO.output("P8_21", GPIO.LOW) # flat = off
		        else:
		            turnLED(i+1)
		            GPIO.output("P8_17", GPIO.LOW) # green = off
		            GPIO.output("P8_18", GPIO.LOW) # sharp = off
		            GPIO.output("P8_21", GPIO.HIGH) # flat = on







