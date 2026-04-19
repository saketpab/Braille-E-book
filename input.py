import requests
import time
from arduinoScript import send_to_arduino, arduino


#takes in the word from the user, we can adjust ther length of the word
def getWord():

    wordSizeLimit = 1

    user_input = ""
    while len(user_input) != wordSizeLimit:
        user_input = input(f"Enter a word with a limit of {wordSizeLimit} character(s): ")
        
        if len(user_input) == wordSizeLimit:
            return user_input
        else:
            print(f"Invalid input. Please enter exactly {wordSizeLimit} character(s).\n")
    
    return user_input

#sends ther word character by character to the open source API, which returns the braille unicode character for the inputted character. Then we convert the braille unicode character to a 2D matrix, and then we convert the 2D matrix to the corresponding faces for the left and right wheel. Finally, we send the faces to the arduino to spin the wheels.
def send_to_api(word):
    res = requests.post(
        "http://localhost:5000/translate",
        json={"translate": word}
    )
    
    return res.json()

motor1_map = {
    "000": 0,
    "111": 1,
    "011": 2,
    "101": 3,
    "110": 4,
    "100": 5,
    "010": 6,
    "001": 7
}

motor2_map = {
    "000": 0,
    "100": 1,
    "010": 2,
    "001": 3,
    "011": 4,
    "101": 5,
    "110": 6,
    "111": 7
}

#converts the braille unicode character to a 2D matrix
def braille_to_faces(char):
    code = ord(char) - 0x2800  # Braille Unicode starts here
    
    # Each bit corresponds to a dot
    dots = [
        (code >> 0) & 1,  # dot 1
        (code >> 1) & 1,  # dot 2
        (code >> 2) & 1,  # dot 3
        (code >> 3) & 1,  # dot 4
        (code >> 4) & 1,  # dot 5
        (code >> 5) & 1,  # dot 6
    ]
    
    # build 3-dot columns
    left_pattern = f"{dots[0]}{dots[1]}{dots[2]}"
    right_pattern = f"{dots[3]}{dots[4]}{dots[5]}"

    # lookup (safe fallback to 0 if missing)
    left_face = motor1_map.get(left_pattern, 0)
    right_face = motor2_map.get(right_pattern, 0)

    return left_face, right_face



#the main part that calls all the functions and runs the program. It gets the word from the user, sends it to the API, converts the response to the corresponding faces, and then spins the wheels accordingly
# if __name__ == "__main__":
#     theWord = getWord()
#     listOfChar = list(theWord)
#     logs = []
#     result = []
#     #print(f"You entered: {theWord}")
#     for char in listOfChar:
#         res = send_to_api(char)
#         matrix = braille_to_matrix(res['response'])
#         left_face, right_face = matrix_to_faces(matrix)
    
    

#         # print(f"Character: {char}")
#         # print(f"Braille Matrix: {matrix}")
#         logs.append((char, res, matrix, left_face, right_face))
#         result.append([left_face, right_face])

#     for left_face, right_face in result:
#         send_to_arduino(left_face, right_face)
#     print(logs)
#     print(result)
#     arduino.close()


if __name__ == "__main__":
    theWord = getWord()
    listOfChar = list(theWord)

    logs = []
    result = []

    for char in listOfChar:
        res = send_to_api(char)

        braille_char = res['response']

        left_face, right_face = braille_to_faces(braille_char)

        logs.append({
            "char": char,
            "braille": braille_char,
            "left_face": left_face,
            "right_face": right_face
        })

        result.append((left_face, right_face))

    # send to Arduino
    for left_face, right_face in result:
       send_to_arduino(left_face, right_face)

    print(logs)
    print(result)

    #arduino.close()
