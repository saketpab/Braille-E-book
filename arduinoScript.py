import serial
import time

# Serial setup
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to initialize

def send_to_arduino(left_face, right_face):
    command = f"{left_face},{right_face}\n"
    print(f"Sending: {command.strip()}")
    arduino.write(command.encode())
    time.sleep(1)