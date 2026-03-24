import pandas as pd
import string

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)

lt_brailleData = pd.read_csv(r'alternate meanings - lettersnumbers.csv')
df_lt_brailleData = pd.DataFrame(lt_brailleData)

partial_brailleData = pd.read_csv(
    r'alternate meanings - partial_and_connected.csv')
df_partial_brailleData = pd.DataFrame(partial_brailleData)

whole_brailleData = pd.read_csv(r'alternate meanings - all_abrs.csv')
df_whole_brailleData = pd.DataFrame(whole_brailleData)

isolated_brailleData = pd.read_csv(
    r'alternate meanings - isolated_words.csv')
df_isolated_brailleData = pd.DataFrame(isolated_brailleData)

single_brailleData = pd.read_csv(
    r'alternate meanings - single_words.csv')
df_single_brailleData = pd.DataFrame(single_brailleData)

numData = dict(digits=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def wholeStrUpperCase(string, unicode_string):
    capital_char = chr(10272)
    unicode_string += capital_char
    unicode_string += capital_char
    string = string.lower()

    return string, unicode_string


def arrayWordOrSign(string):
    # define and init vars
    arr = []
    i = 0
    currentWord = ""
    currentTuple = (True, "")
    wordCheck = False
    if string[0].isalpha():
        wordCheck = True
    count = 0

    # separate words and punctuation/digits
    while i < len(string):
        if string[i] == '\'' or string[i].isalpha():
            if wordCheck:
                currentWord += string[i]
            else:
                currentTuple = (False, currentWord)
                arr.append(currentTuple)  # append the word
                wordCheck = True
                count += 1
                currentWord = string[i]
        else:
            if wordCheck:
                currentTuple = (True, currentWord)
                arr.append(currentTuple)  # append the word
                wordCheck = False
                count += 1
                currentWord = string[i]
            else:
                currentWord += string[i]
        if i == len(string) - 1:
            currentTuple = (wordCheck, currentWord)
            arr.append(currentTuple)  # append the word
        i += 1
    return arr


def getPartialWord(string):
    idx = 0
    isFound = False
    found_unicode_string = ''
    found_elem = ''
    for elem in df_partial_brailleData['partial_word']:
        idx += 1

        if elem == string:
            length_partial = df_partial_brailleData.iloc[idx - 1, 1]

            for x in range(length_partial):
                col = int(x + 2)
                a = df_partial_brailleData.iloc[int(idx - 1), col]
                partialWord = chr(int(a))
                found_unicode_string += partialWord
            found_elem = elem
            isFound = True
            break

    ans = [isFound, found_unicode_string, found_elem]
    return ans


def getWholeWord(string):
    idx = 0
    isFound = False
    found_unicode_string = ''
    found_elem = ''
    for elem in df_whole_brailleData['word']:
        idx += 1

        if elem == string:
            length_whole = df_whole_brailleData.iloc[idx - 1, 1]

            for x in range(length_whole):
                col = int(x + 2)
                a = df_whole_brailleData.iloc[int(idx - 1), col]
                wholeWord = chr(int(a))
                found_unicode_string += wholeWord
            found_elem = elem
            isFound = True
            break

    ans = [isFound, found_unicode_string, found_elem]
    return ans


def getIsolatedWord(string):
    idx = 0
    isFound = False
    found_unicode_string = ''

    if string.isupper():
        string, found_unicode_string = wholeStrUpperCase(string, found_unicode_string)

    listStr = list(string)

    for s in range(len(listStr)):
        if listStr[s].isupper():
            capital_char = chr(10272)
            found_unicode_string += capital_char
            listStr[s] = listStr[s].lower()
            string = ''.join(listStr)

    for elem in df_isolated_brailleData['isolated words']:
        idx += 1

        if elem == string:
            unicode = df_isolated_brailleData.iloc[idx - 1, 1]
            found_unicode_string += chr(unicode)
            isFound = True
            break

    ans = [isFound, found_unicode_string]
    return ans


def getSingleWord(string):
    idx = 0
    isFound = False
    found_unicode_string = ''

    if string.isupper():
        string, found_unicode_string = wholeStrUpperCase(string, found_unicode_string)

    listStr = list(string)

    for s in range(len(listStr)):
        if listStr[s].isupper():
            capital_char = chr(10272)
            found_unicode_string += capital_char
            listStr[s] = listStr[s].lower()
            string = ''.join(listStr)

    temp = df_single_brailleData['single_words']
    for elem in temp:
        idx += 1

        if elem == string:
            unicode = df_single_brailleData.iloc[idx - 1, 1]
            found_unicode_string += chr(unicode)
            isFound = True
            break

    ans = [isFound, found_unicode_string]
    return ans


def translate_word(word):
    unicode_string = ''  # the unicode braille
    pointer = 0  # point to current char

    if word.isupper():
        word, unicode_string = wholeStrUpperCase(word, unicode_string)

    while pointer < len(word):
        isWhole = False
        isPartial = False

        # 1. look for whole
        windowLength = min(len(word) - pointer, 10)
        while windowLength >= 2:
            testStr = word[pointer: pointer + windowLength]

            # uncapitalize word
            if word[pointer].isupper():
                capital_char = chr(10272)
                unicode_string += capital_char
                listStr = list(testStr)
                listStr[pointer] = listStr[pointer].lower()
                listWord = list(word)
                listWord[pointer] = listWord[pointer].lower()
                word = ''.join(listWord)
                testStr = ''.join(listStr)

            isFound, unicode_whole, elem = getWholeWord(testStr)
            if isFound:
                unicode_string += unicode_whole
                pointer += len(elem)
                isWhole = True
                break
            else:
                windowLength -= 1

        # 2. look for partial
        # if not isWhole, then we will look for partial
        if not isWhole and pointer != 0:
            windowLength_partial = min(len(word) - pointer, 5)
            while windowLength_partial >= 2:
                partial_testStr = word[pointer: pointer + windowLength_partial]
                isFound, unicode_partial, elem = getPartialWord(partial_testStr)
                if isFound:
                    unicode_string += unicode_partial
                    pointer += len(elem)
                    isPartial = True
                    break
                else:
                    windowLength_partial -= 1

        # 3. if not whole and not partial, then translate the current char, and move the point to next position
        if not isWhole and not isPartial:
            letterBooleanList = df_lt_brailleData['letter'] == word[pointer]
            letter_data = df_lt_brailleData.loc[letterBooleanList]
            letter_unicode = letter_data['unicode']
            braille_char = chr(letter_unicode.values[0])
            unicode_string += braille_char
            pointer += 1

    return unicode_string


def translateSignAndNum(sign):
    unicode_ans = ''
    alreadyNumSign = False
    list_sign = list(sign)
    for i in range(len(list_sign)):
        if list_sign[i] in numData['digits']:
            if alreadyNumSign == False:
                numSign_char = chr(10300)
                unicode_ans += numSign_char
                alreadyNumSign = True

            letterBooleanList = df_lt_brailleData['letter'] == list_sign[i]
            letter_data = df_lt_brailleData.loc[letterBooleanList]
            letter_unicode = letter_data['unicode']
            braille_char = chr(letter_unicode.values[0])
            unicode_ans += braille_char

        else:
            letterBooleanList = df_lt_brailleData['letter'] == list_sign[i]
            letter_data = df_lt_brailleData.loc[letterBooleanList]
            letter_unicode = letter_data['unicode']
            braille_char = chr(letter_unicode.values[0])
            unicode_ans += braille_char
            alreadyNumSign = False

    return unicode_ans


def getNextWord(arr):
    ans = ''
    isPunctuation = False
    for i in range(len(arr)):
        if arr[i][0]:
            string_before = list(arr[max(i - 1, 0)][1])
            string_after = list(arr[min(i + 1, len(arr) - 1)][1])
            if string_before != list(arr[0][1]):
                if string_before[len(string_before) - 1] in string.punctuation:
                    isPunctuation = True

            if string_after[0] in string.punctuation:
                isPunctuation = True

            if isPunctuation:
                # print("normal words")
                isFound_single, unicode_single = getSingleWord(arr[i][1])
                if isFound_single:
                    ans += unicode_single
                else:
                    wordBraille = translate_word(arr[i][1])
                    ans += wordBraille
                    isPunctuation = False

            else:
                # print("Isolation!")
                isFound, unicode_isolated = getIsolatedWord(arr[i][1])
                isFound_single, unicode_single = getSingleWord(arr[i][1])
                if isFound:
                    ans += unicode_isolated
                elif isFound_single:
                    ans += unicode_single
                else:
                    wordBraille = translate_word(arr[i][1])
                    ans += wordBraille

        else:
            # print("punctuation treatment")
            signsBraille = translateSignAndNum(arr[i][1])
            ans += signsBraille

    return ans


# arrayInput = arrayWordOrSign(str(input()))

# print(getNextWord(arrayInput))

# print(translate_word('CHARACTERISTICS'))
# print(chr(10288) + chr(10269))

# character,2,10256,10273
# print(chr(10256) + chr(10273))
# print(chr(10259) + chr(10257) + chr(10301) + chr(10262))  # hey!

# print(chr(10246))  # isolate be
# print(chr(10273))  # ch
# print(chr(10259))  # have
