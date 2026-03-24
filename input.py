import requests

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

def send_to_api(word):
    res = requests.post(
        "http://localhost:5000/translate",
        json={"translate": word}
    )
    
    return res.json()

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



if __name__ == "__main__":
    theWord = getWord()
    #print(f"You entered: {theWord}")
    result = send_to_api(theWord)
    matrix = braille_to_matrix(result['response'])
    print(f"API Response: {result}")
    print(f"Braille Matrix: {matrix}")