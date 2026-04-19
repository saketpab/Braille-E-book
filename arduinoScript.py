import serial
import time

arduino = serial.Serial('COM3', 9600, timeout=2)
time.sleep(2)

# Wait for Arduino READY
start_time = time.time()
while True:
    line = arduino.readline().decode(errors='ignore').strip()
    if line:
        print(f"Arduino: {line}")
        if line == "READY":
            break

    if time.time() - start_time > 5:
        raise Exception("Arduino did not send READY")

def send_to_arduino(left_face, right_face):
    command = f"{left_face},{right_face}\n"
    print(f"Sending: {command.strip()}")
    arduino.write(command.encode())

    timeout_counter = 0

    while True:
        line = arduino.readline().decode(errors='ignore').strip()

        if not line:
            timeout_counter += 1
            if timeout_counter > 5:
                print("No response from Arduino")
                break
            continue

        print(f"Arduino: {line}")

        if line == "OK":
            break
        elif line.startswith("ERROR"):
            print(f"Arduino error: {line}")
            break
