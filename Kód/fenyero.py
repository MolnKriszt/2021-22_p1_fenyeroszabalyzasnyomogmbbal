import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

#36. tüske legyen kimenet
pin = 24
GPIO.setup(pin, GPIO.OUT)
pingomb1 = 18
GPIO.setup(pingomb1, GPIO.IN)
frequency = 50
fill = 100
delta = 5
#A pin PWM üzemmódba kapcsolása
p = GPIO.PWM(pin, frequency)
#indítás
p.start(fill)

print("villogás: f={0} Hz kitöltés: {1} % Leállítás: Ctrl-C" .format(frequency, fill))


#kapcsoló

pinSIO = 15
pinSUp = 18
pinSDown = 14
GPIO.setup(pinSIO, GPIO.IN)
GPIO.setup(pinSUp, GPIO.IN)
GPIO.setup(pinSDown, GPIO.IN)

# Our function on what to do when the button is pressed

io = False


def SIO(channel):
    global fill
    global io
    global pin
    global p
    io = not io
    if io:
        #bekapcs
        fill = 100
        p
        p.start(fill)       
    else:
        #kikapcs
        fill = 0
        p.stop()
    print(fill)
    print(io)
    
def SUP(channel):
    global fill
    global p
    fill = fill + delta
    if fill >= 100:
        fill = 100
    p.ChangeDutyCycle(fill)    
    print(fill)
    
def SD(channel):
    global p
    global fill
    fill = fill - delta
    if fill <= 0:
        fill = 0
    p.ChangeDutyCycle(fill)
    print(fill)        
    

# Add our function to execute when the button pressed event happens

#GPIO.add_event_detect(pin, GPIO.RISING, callback=Shutdown, bouncetime=1000)
#GPIO.add_event_detect(pin, GPIO.FALLING, callback=Shutdown, bouncetime=2000)
GPIO.add_event_detect(pinSIO, GPIO.FALLING, callback=SIO, bouncetime=500)
GPIO.add_event_detect(pinSUp, GPIO.FALLING, callback=SUP, bouncetime=500)
GPIO.add_event_detect(pinSDown, GPIO.FALLING, callback=SD, bouncetime=500)

def upindit():
    global fill
    
    fill += delta
    if fill >= 100:
        fill = 0
    p.ChangeDutyCycle(fill)
    print(fill)
    
def downindit():
    global fill
    
    fill = fill - delta
    if fill <= 0:
        fill = 100
    p.ChangeDutyCycle(fill)
    print(fill) 

try:
    while True:
        inUp = GPIO.input(pinSUp)
        inDown = GPIO.input(pinSDown)
        if inUp == 0:
            upindit()
            
        if inDown == 0:
            downindit()
            
        time.sleep(0.1)     
        
except KeyboardInterrupt:
    print("Pinek lekapcsolva")
    GPIO.cleanup()
