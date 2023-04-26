import serial
importos, time
importRPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
port = serial.Serial(“/dev/ttyS0”, baudrate=9600, timeout=1)
port.write(b’AT\r’)
rcv = port.read(10)
print(rcv)
time.sleep(1)
port.write(b”AT+CMGF=1\r”)
print(“Text Mode Enabled…”)
time.sleep(3)
port.write(b’AT+CMGS=”9166873301″\r’)
msg = “! EMERGENCY ALERT !
If you are receiving this message, then I might be in a medical emergency or casualty right now. Please track me with the below location tracker. Thank you.
print(“sending message….”)
time.sleep(3)
port.reset_output_buffer()
time.sleep(1)
port.write(str.encode(msg+chr(26)))
time.sleep(3)
print("message sent")