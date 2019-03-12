import time
import array
import RPi.GPIO as GPIO

## Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 as MCP3008lib

## In order to make CPU usage calculations.
import psutil

##Disable alarms for Pin corruption
##GPIO.setwarnings(False)

    ##PWM output configuration
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)  ##Pin 18, 50Hz
dc = 6.4 ##Leveled
pwm.start(dc)

    ##Debugging LED configuration
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH) ##LED
time.sleep(0.5)

   ## Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp3008 = MCP3008lib.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    #---------------------------#

###########GLOBAL VARIABLES##########
   ## ADC analog channel. From 0 to 7
ch = 0
   ## Sample time (in seconds)
Ts = 0.06
   ## Posizio kontsigna (cm)
kontsigna = 25

dc=6.4
   ## PID balioak
global Kp
Kp=15
global Ki
Ki=3
global Kd
Kd=25
global er
er= 0
global L
L=46
global R
R=5.65
########----------------------#########


 ##Distance Register initialization
register = array.array("l")
 ##Error Register initialization
errorea = array.array("f")
 ##Output Register initialization
irteera = array.array("f")



er=array.array("f")
er.append(1)

for i in range(0,4):
    errorea.append(0)
    irteera.append(0)
    
print (errorea)
print (irteera)

for i in range(0,10):
    register.append(mcp3008.read_adc(0))
    time.sleep(Ts)##this is what the sensor takes to make a reading 55ms



print('Reading MCP3008 values, press Ctrl-C to quit...')
time.sleep(0.5)## debugg


    


###BEGIZTA NAGUSIA###
def main():
#    cpu = psutil.cpu_percent()  ## In order to make CPU usage calculations.
#    print("%CPU=" + str(cpu))

    GPIO.output(7, GPIO.LOW) ##LED  debugg
   
    
    try:
        
        
        #time.sleep(2)
        for i in range(0,9): #register shifting
            register[i] = register[i+1]
        del register[9]
        register.insert(9,mcp3008.read_adc(ch)) #add readen last value
        suma = sum(register)
        batazbestekoa = suma/10
        
        #print(register)
        #print(suma)
        #print(format(batazbestekoa, '.3f'))
        
        adc=(batazbestekoa*3.3)/1024
       
        if adc<=2.333:
            distantzia =-17.874*pow(adc,5)+146.44*pow(adc,4)-481.93*pow(adc,3)+804.15*pow(adc,2)-696.09*adc+271.56
        elif adc>2.333:
            distantzia =-27575*pow(adc,3)+188463*pow(adc,2)-429165*adc+325617
        
        print (distantzia)

        ##doiketa
        #distantzia=distantzia-5
        
        ##Shiffting of the error array and refresh
        del errorea[0]
        errorea.append(kontsigna-distantzia)
        
               
    
        
        
        ##Shiffting of the output array and refresh. Calculation of the controller. 
        del irteera[0]
        
        #diferentziazko ekuazioa edo PIDa       
        a = -0.01*irteera[2]+irteera[1]+0.01*irteera[0]+121.827*errorea[3]-118.119*errorea[2]-121.719*errorea[1]+118.227*errorea[0]
        
                irteera.append(a)
        print ("   Errorea: ")
        print (errorea[3])

        print ("  Irteera: " + str(a))
        print ("  Angelua: " + str(b))
        
       
        #Eragingailua / actuator 
        dc=-0.0498*(-a)+6.6836
        
        if dc>=11.6:
            dc=11.6
        elif (dc<11.6) and (dc>=2.6):
            dc=dc
        elif dc<2.6:
            dc=2.6

        
        print ("duty cycle: " + str(round(dc,2)))
        
        ##ACTIVAR##
        pwm.ChangeDutyCycle(dc)
        
        
        time.sleep(Ts)  
            
    except KeyboardInterrupt:
        print(“Ctrl+C sakatu egin da. Programatik irtetzen“)
        pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    while(True):
        main()
