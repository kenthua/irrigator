import RPi.GPIO as GPIO,time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)

print('on')
GPIO.output(16,GPIO.LOW)

time.sleep(2)

print('off')
GPIO.output(16,GPIO.HIGH)