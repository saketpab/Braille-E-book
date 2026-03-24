import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', None)

lt_brailleData = pd.read_csv(r'letters_braille.csv')
df_lt_brailleData = pd.DataFrame(lt_brailleData)

numData = dict(digits=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def translate(string):
    unicode_string = ''

    list_letter = list(string)

    isNum = False

    for i in list_letter:
        if i.isupper():
            capital_char = chr(10272)
            unicode_string += capital_char
            i = i.lower()

        idx = 0
        for elem in df_lt_brailleData['letter']:
            idx += 1

            if elem == i:
                letter_unicode = df_lt_brailleData.iloc[idx - 1, 1]

                unicode_string += chr(int(letter_unicode))

    unicode_string += chr(10240)

    return unicode_string