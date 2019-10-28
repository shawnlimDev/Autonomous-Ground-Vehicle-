import RPi.GPIO as IO
from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
import time 
IO.setwarnings(False)
IO.setmode(IO.BCM)


#coloursensor
s2 = 22
s3 = 4
signal = 16
NUM_CYCLES = 10

#IO.setup(6,IO.OUT) #GPIO 2 -> Red LED as output
#IO.setup(5,IO.OUT) #GPIO 3 -> Green LED as output
IO.setup(20,IO.IN) #GPIO 14 -> IR sensor as input #sensor3black
IO.setup(25,IO.IN)#switch
IO.setup(17,IO.IN) #sensor4white
IO.setup(12,IO.IN) #sensor2white
IO.setup(27,IO.IN) #sensor1split
IO.setup(23,IO.IN) #sensor5marker
#coloursensor
IO.setup(signal,IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(22,IO.OUT)
IO.setup(4,IO.OUT)


# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT= 21
FORWARD_LEFT_PIN = 26
REVERSE_LEFT_PIN = 19
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 5
FORWARD_RIGHT_PIN = 13
REVERSE_RIGHT_PIN = 6




driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT,True,0,1000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT,True,0,1000)
forwardLeft = PWMOutputDevice(FORWARD_LEFT_PIN)
reverseLeft = PWMOutputDevice(REVERSE_LEFT_PIN)
forwardRight = PWMOutputDevice(FORWARD_RIGHT_PIN)
reverseRight = PWMOutputDevice(REVERSE_RIGHT_PIN)
Flag = 0
Flag2 = 0



def stop():

                forwardLeft.value = False
                reverseLeft.value = False
                forwardRight.value = False
                reverseRight.value = False
                driveLeft.value = 0
                driveRight.value = 0

                
def forward():


                forwardLeft.value = True
                reverseLeft.value = False
                forwardRight.value = True
                reverseRight.value = False
                driveLeft.value = 1
                driveRight.value = 1

def forwardSlow():


                forwardLeft.value = True
                reverseLeft.value = False
                forwardRight.value = True
                reverseRight.value = False
                driveLeft.value = 0.5
                driveRight.value = 0.5


   
def back():

                forwardLeft.value = False
                reverseLeft.value = True
                forwardRight.value = False
                reverseRight.value = True 
                driveLeft.value = 1.0
                driveRight.value = 1.0


     
def left():

                forwardLeft.value = False
                reverseLeft.value = True
                forwardRight.value = True
                reverseRight.value = False
                driveLeft.value = 0.2
                driveRight.value = 0.2

         
def right():

                forwardLeft.value = True
                reverseLeft.value = False
                forwardRight.value = False
                reverseRight.value = True
                driveLeft.value = 1.0
                driveRight.value = 1.0


while 1:

    IO.output(s2,IO.LOW)
    IO.output(s3,IO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      IO.wait_for_edge(signal, IO.FALLING)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration
    #print('red: %d\n' % red) 
   
    IO.output(s2,IO.LOW)
    IO.output(s3,IO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      IO.wait_for_edge(signal, IO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    #print('blue: %d\n' % blue) 

    IO.output(s2,IO.HIGH)
    IO.output(s3,IO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      IO.wait_for_edge(signal, IO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    #print('green: %d\n\n\n' % green)
    
    print ('%d/n' % IO.input(20))
 
    if(IO.input(27)==False): #when not split path
        if(IO.input(12)==False and IO.input(20)== True): #both while move forward
             #if ((green<15000 and green>10500 and red<18000 and red>13000 and blue <16500 and blue > 13000) or Flag == 1): #green-7000 blue - 7000 
             # if(red >9000 and red < 15000 and green <15000 and green > 10500):
              if(green < 13000):
                print("red")
                forwardSlow()
                #Flag = 1
                
            # elif (green<17000 and green > 14000 and red<14000 and red > 10000 and blue<17500 and blue>13500): #green - 7000 red -7000
              else:
                print("blue")
                forward()
                #Flag = 0
   
        elif(IO.input(17)==False and IO.input(20)==False and IO.input(12) == True): # AGV veering to right -> turn left  
            left()

        elif(IO.input(12)==False and IO.input(20)==False and IO.input(17) == True): #AGV veering to left -> turn right
            right()

        
        elif(IO.input(23) == True): #hujjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
            stop()

    if(IO.input(27)==True):#enter split path mode
            if(IO.input(20)== True):
                Flag = 1
                
                left()
            if(IO.input(17) == True and IO.input(12) == True):
                Flag2 = 1
    while(Flag2 == 1 and IO.input(27) == False):
            forwardSlow()
            if(IO.input(27) == True):
                Flag2= 0 
    if(Flag == 1):
        Flag2 = 0
            
    while(Flag == 1 or IO.input(23) == False):
            left()
            if(IO.input(23) == True):
                Flag = 0
             

    









           # if(IO.input(12)==False and IO.input(20) == True): # perfect - forward
                
            #    forward()

           # elif(IO.input(12) ==False and IO.input(20) ==False): #too left - error correction right
            #    right()

            #elif(IO.input(20) ==True and IO.input(12) ==True): #too left - error correction left
             #   left()

   

 

