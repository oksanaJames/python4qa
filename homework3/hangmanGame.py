import datetime
import traceback
import collections
from itertools import *
import re
from functools import reduce

filename = 'wordlist.txt'


def replace_to_regex(stringInput):
    # This function replaces all symbols entered to regex letter match
    return stringInput.replace('-', '\w')


def regex_find_all_words(pattern, stringInput):
    # This function finds all words based on pattern
    return re.findall(pattern, stringInput)


def transform_list_to_string(listInput):
    # This function transforms list to string for future regex search
    return reduce((lambda x, y: x + " " + y), listInput)


def reduce_words_by_not_matched_letter(list1, list2):
    # This function filters all words which doesn't contain the letter
    return reduce(set.difference, [set(item) for item in [list1, list2]])


def word_length():
    # This function takes user input
    print("\nPlease choose a WORD from a file 'wordlist.txt'...")
    wordLength = input("How many letters in your word? \n")
    wordLength = int(wordLength)
    return wordLength


def extract_all_words(wordLength):
    # This function extract all words based on specified length
    extractedWords = set()
    with open(filename) as f:
        for word in f:
            word = word.strip().lower()
            if len(word) != wordLength:
                continue
            extractedWords.add(word)
    return sorted(extractedWords)


def letter_popularity(count, letters):
    return round(count * 100 / len(letters), 2)


def print_word(wordLength):
    # This function prints word letters with - symbols
    hiddenWord = ''.join(['-' for i in range(wordLength)])
    return hiddenWord.strip()


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False
    return input('\nDo you want to play again? (yes or no)\n').lower().startswith('y')


def gamePlay():
    wrongLetters = []
    showedLetters = []
    wordPattern = ''
    lettersCount = word_length()  # how many letters in a word
    print("Word pattern is: \n{}".format(print_word(lettersCount)))
    lengthBasedWords = extract_all_words(lettersCount)  # sort all words based on the letters count

    def recursive_check(recursiveList):
        global wordPattern
        if len(recursiveList) == 1:
            if type(recursiveList) == set:
                if input("Matching word is '{}'? (yes or no)".format(next(iter(recursiveList)))).lower().startswith('y'):
                    print("Congratulations! Word '{}' guessed with {} attempts".format(next(iter(recursiveList)),
                                                                                       len(showedLetters) + len(
                                                                                           wrongLetters)))
                    return next(iter(recursiveList))
                else:
                    print("Something went wrong...Please try again")
                    return next(iter(recursiveList))

        letters = list(chain.from_iterable(recursiveList))  # transform words to letters
        lettersDictionary = collections.Counter(letters)  # put a letter and it's count in a dict, sorted by count

        for letter, count in lettersDictionary.most_common():
            if letter not in showedLetters and letter not in wrongLetters:
                print("\nLetter '{}' with popularity {} %".format(letter, letter_popularity(count, letters)))
                if input('Is it present in a word? (yes or no)\n').lower().startswith('y'):
                    if len(showedLetters) == lettersCount - 1:
                        wordPattern = wordPattern.replace('-', letter)
                        if input("Matching word is '{}' (yes or no)? ".format(wordPattern)).lower().startswith('y'):
                            print("Congratulations! Word '{}' guessed with {} attempts".format(wordPattern,
                                                                                               len(showedLetters) + len(
                                                                                                   wrongLetters)))
                            return wordPattern
                        else:
                            print("Something went wrong...Please try again")
                            return wordPattern

                    wordPattern = input('Please show me a position of a letter...\n')
                    showedLetters.append(letter)
                    if len(wrongLetters) > 0:
                        print("\tWrong letters: {}\n".format(' '.join(wrongLetters)))

                    # regex reduce a list with words which doesn't contain a letter on a position specified
                    # replace '---e-' to '\w\w\we\w'
                    rgx = replace_to_regex(wordPattern)
                    wordString = transform_list_to_string(recursiveList)
                    matchedWords = regex_find_all_words(rgx, wordString)

                    # print(matchedWords)
                    # print(len(matchedWords))
                    return recursive_check(matchedWords)
                else:
                    # reduce a list with words without a letter specified
                    wrongLetters.append(letter)
                    print("\tWrong letters: {}\n".format(' '.join(wrongLetters)))
                    # pattern for a letter existense in a word
                    rgx = r'\w*[{}]\w*'.format(letter)
                    wordString = transform_list_to_string(recursiveList)
                    matchedWords = regex_find_all_words(rgx, wordString)

                    reducedList = reduce_words_by_not_matched_letter(recursiveList, matchedWords)
                    # print(reducedList)
                    # print(len(reducedList))
                    return recursive_check(reducedList)
    recursive_check(lengthBasedWords)


if __name__ == '__main__':
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        start = datetime.datetime.now()
        print('Welcome to a Hangman Game!\n')
        while True:
            gamePlay()
            if not playAgain():
                break
    except Exception as e:
        print("\nError")
        print(e)
        traceback.print_exc()
    finally:
        duration = str(datetime.datetime.now() - start)  # print the time taken for script execution
        print('\n')
        print('game complete in duration: %s' % duration)
        print('-----end-----')
