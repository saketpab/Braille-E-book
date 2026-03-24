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



if __name__ == "__main__":
    theWord = getWord()
    print(f"You entered: {theWord}")