import requests
import serial
import time

#Serial setup
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  


#Get character input
def get_character():
    while True:
        user_input = input("Enter ONE character: ")
        if len(user_input) == 1:
            return user_input
        print("Invalid input. Enter exactly 1 character.\n")


#Call Braille API
def send_to_api(char):
    res = requests.post(
        "http://localhost:5000/translate",
        json={"translate": char}
    )
    return res.json()['response']


#Convert from Braille to dot matrix
def braille_to_matrix(char):
    code = ord(char) - 0x2800

    dots = [
        (code >> 0) & 1,  # dot 1
        (code >> 1) & 1,  # dot 2
        (code >> 2) & 1,  # dot 3
        (code >> 3) & 1,  # dot 4
        (code >> 4) & 1,  # dot 5
        (code >> 5) & 1,  # dot 6
    ]

    return [
        [dots[0], dots[3]],
        [dots[1], dots[4]],
        [dots[2], dots[5]],
    ]


#Map from dot matrix to octagon face
def column_to_face(top, middle, bottom):
    # Convert 3 bits → number (0–7)
    return (top << 2) | (middle << 1) | bottom


def matrix_to_faces(matrix):
    # Left column (dots 1,2,3)
    left_face = column_to_face(
        matrix[0][0],
        matrix[1][0],
        matrix[2][0]
    )

    # Right column (dots 4,5,6)
    right_face = column_to_face(
        matrix[0][1],
        matrix[1][1],
        matrix[2][1]
    )

    return left_face, right_face


#Send to Arduino
def send_to_arduino(left_face, right_face):
    command = f"{left_face},{right_face}\n"
    print(f"Sending: {command.strip()}")
    arduino.write(command.encode())
    time.sleep(1)


if __name__ == "__main__":
    char = get_character()

    braille_char = send_to_api(char)
    matrix = braille_to_matrix(braille_char)
    left_face, right_face = matrix_to_faces(matrix)

    print(f"\nInput: {char}")
    print(f"Braille char: {braille_char}")
    print(f"Matrix: {matrix}")
    print(f"Left wheel face: {left_face}")
    print(f"Right wheel face: {right_face}")

    send_to_arduino(left_face, right_face)