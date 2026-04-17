import serial
import time

# Serial setup — dtr must be set BEFORE opening to prevent reset-on-connect
arduino = serial.Serial()
arduino.port = 'COM4'
arduino.baudrate = 9600
arduino.timeout = 1
arduino.dtr = False
arduino.open()
time.sleep(0.5)
arduino.reset_input_buffer()

print("Arduino ready.")

def send_to_arduino(left_face, right_face):
    command = f"{left_face},{right_face}\n"
    print(f"Sending: {command.strip()}")
    arduino.write(command.encode())
    while True:
        line = arduino.readline().decode().strip()
        if not line:
            continue
        print(f"Arduino: {line}")
        if line == "OK":
            break
        elif line.startswith("ERROR"):
            print(f"Arduino error: {line}")
            break