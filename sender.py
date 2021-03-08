import serial
import time

# Open grbl serial port ==> CHANGE THIS BELOW TO MATCH YOUR USB LOCATION
s = serial.Serial('/dev/cu.usbserial-14110',115200) # GRBL operates at 115200 baud. Leave that part alone.

# Wake up grbl
s.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

# Stream g-code to grbl
while True:
    l = input('>>>')
    l = line.strip() # Strip all EOL characters for consistency
    if l == 'stop':
        break
    s.write(l + '\n') # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print(' : ' + grbl_out.strip())

# Close file and serial port
s.close()