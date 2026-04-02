import requests
from arduinoScript import send_to_arduino
from wheelSpinningScript import spin_wheels

#takes in the word from the user, we can adjust ther length of the word
def getWord():

    wordSizeLimit = 2
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

#converts the braille unicode character to a 2D matrix
def braille_to_matrix(char):
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
    
    return [
        [dots[0], dots[3]],
        [dots[1], dots[4]],
        [dots[2], dots[5]],
    ]

#converts a 2D matrix to the corresponding faces 
def column_to_face(top, middle, bottom):
    return (top << 2) | (middle << 1) | bottom

#converts the set of two 2D matrix to the corresponding faces for the left and right wheel
def matrix_to_faces(matrix):
    left_face = column_to_face(matrix[0][0], matrix[1][0], matrix[2][0])
    right_face = column_to_face(matrix[0][1], matrix[1][1], matrix[2][1])
    return left_face, right_face




#the main part that calls all the functions and runs the program. It gets the word from the user, sends it to the API, converts the response to the corresponding faces, and then spins the wheels accordingly
if __name__ == "__main__":
    theWord = getWord()
    listOfChar = list(theWord)
    logs = []
    result = []
    #print(f"You entered: {theWord}")
    for char in listOfChar:
        res = send_to_api(char)
        matrix = braille_to_matrix(res['response'])
        left_face, right_face = matrix_to_faces(matrix)
    
    

        # print(f"Character: {char}")
        # print(f"Braille Matrix: {matrix}")
        logs.append((char, res, matrix, left_face, right_face))
        result.append([left_face, right_face])

    spin_wheels(result)
    print(logs)
    print(result)