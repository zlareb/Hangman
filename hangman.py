# Problem Set 2, hangman.py
import random
import string

WORDLIST_FILENAME = "words.txt"
letters_guessed = []

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# Load the list of words into the variable wordlist
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter not in letters_guessed:
            return False 
    return True
            

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    cursor = -1
    wordstatus = ""
    letters = []

    for letter in secret_word:
        letters.append(letter)
        cursor+=1
        if letter not in letters_guessed:
            letters[cursor] = '_ '

    for i in range(len(letters)):
        wordstatus = wordstatus[:] + letters[i]

    return wordstatus


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabets = []
    total_alpha = string.ascii_lowercase
    cursor = -1
    cursor2 = -1
    remaining_words = ""

    for alphabet in total_alpha:
        alphabets.append(alphabet)
        cursor += 1

    for alphabet in alphabets:
        cursor2 += 1
        if alphabet in letters_guessed:
            alphabets.remove(alphabets[cursor2])

    for i in range(len(alphabets)):
        remaining_words = remaining_words + alphabets[i]       

    return remaining_words
    
  
def hangman(secret_word):
  '''
  secret_word: string, the secret word to guess.
  
  Starts up an interactive game of Hangman.

  * At the start of the game, let the user know how many 
    letters the secret_word contains and how many guesses s/he starts with.
    
  * The user should start with 6 guesses

  * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.
  
  * Ask the user to supply one guess per round. Remember to make
    sure that the user puts in a letter!
  
  * The user should receive feedback immediately after each guess 
    about whether their guess appears in the computer's word.

  * After each guess, you should display to the user the 
    partially guessed word so far.
  
  Follows the other limitations detailed in the problem write-up.
  '''
  # At the start of the game, let the user know how many letters the secret_word contains
  guesses_remaining = 6
  warnings_remaining = 3
  numofletters = len(secret_word)
  vowels = ['a', 'e', 'i', 'o', 'u']

  print("Welcome to the game Hangman!")
  print("I am thinking of a word that is", numofletters, "letters long.")
  print(secret_word)
  print("-------------")


  while guesses_remaining>0:

    print("You now have", guesses_remaining, "guesses left.")
    print("Available letters:", get_available_letters(letters_guessed))

    user_input = input("Please guesss a letter: ").lower()

    if user_input not in string.ascii_lowercase:
        if warnings_remaining > 0:
            warnings_remaining -= 1
        else:
            guesses_remaining -= 1    
        print("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left:", get_guessed_word(secret_word, letters_guessed))
    
    elif user_input not in secret_word and user_input not in letters_guessed:
        if user_input in vowels:
            guesses_remaining -= 2 
        else:
            guesses_remaining -= 1
        letters_guessed.append(user_input)
        print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))

    elif user_input not in secret_word and user_input in letters_guessed:
        if warnings_remaining > 0:
            warnings_remaining -= 1
            print("Oops! You've alreaedy guessed that letter. You now have", warnings_remaining, "warnings left:", get_guessed_word(secret_word, letters_guessed))
        else:
            guesses_remaining -= 1
            print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))

    else:
        letters_guessed.append(user_input)
        print("Good guess:", get_guessed_word(secret_word, letters_guessed))

    print("-------------")

    if get_guessed_word(secret_word, letters_guessed) == secret_word:
          break
    else:
        continue


  Total_score = guesses_remaining * len(unique_letters)    

  if get_guessed_word(secret_word, letters_guessed) != secret_word:
      print("Sorry, you ran out of guesses. The word was", secret_word)
  else:
      print("Congratulations, you won!")
      print("Your total score for this game is:", Total_score) 


def match_with_gaps(my_word, other_word, letters_guessed):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_stripped = my_word.replace(" ", "")

    if len(my_word_stripped) != len(other_word):
        return False
    
    i=0
    for letter in my_word_stripped:
        if letter != "_":
            if letter != other_word[i]:
                return False
                # return false if letter is neither a _ nor other_word[i]
        else: 
            if other_word[i] in letters_guessed:
                return False
            # return false if letter is an underscore but the corresponding letter in other_word has been guessed
        i += 1
    return True
                
    
def show_possible_matches(my_word,letters_guessed):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    word_matches = ""
    for word in wordlist:
        if match_with_gaps(my_word,word,letters_guessed):
            word_matches += word + " "

    if len(word_matches) == 0:
      print("No matches found.")
    else:
      print("Possible word matches:")
      print(word_matches)


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    numofletters = len(secret_word)
    vowels = ['a', 'e', 'i', 'o', 'u']

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", numofletters, "letters long.")
    print(secret_word)
    print("-------------")


    while guesses_remaining>0:

      print("You now have", guesses_remaining, "guesses left.")
      print("Available letters:", get_available_letters(letters_guessed))

      user_input = input("Please guesss a letter: ").lower()

      if user_input not in string.ascii_lowercase:
          if user_input == "*":
              show_possible_matches(get_guessed_word(secret_word, letters_guessed),letters_guessed)
          
          else: 
            if warnings_remaining > 0:
                warnings_remaining -= 1
            else:
                guesses_remaining -= 1    
            print("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left:", get_guessed_word(secret_word, letters_guessed))
      
      elif user_input not in secret_word and user_input not in letters_guessed:
          if user_input in vowels:
              guesses_remaining -= 2 
          else:
              guesses_remaining -= 1
          letters_guessed.append(user_input)
          print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))

      elif user_input not in secret_word and user_input in letters_guessed:
          if warnings_remaining > 0:
              warnings_remaining -= 1
              print("Oops! You've alreaedy guessed that letter. You now have", warnings_remaining, "warnings left:", get_guessed_word(secret_word, letters_guessed))
          else:
              guesses_remaining -= 1
              print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))

      else:
          letters_guessed.append(user_input)
          print("Good guess:", get_guessed_word(secret_word, letters_guessed))

      print("-------------")

      if get_guessed_word(secret_word, letters_guessed) == secret_word:
            break
      else:
          continue


    Total_score = guesses_remaining * len(unique_letters)    

    if get_guessed_word(secret_word, letters_guessed) != secret_word:
        print("Sorry, you ran out of guesses. The word was", secret_word)
    else:
        print("Congratulations, you won!")
        print("Your total score for this game is:", Total_score) 
 

if __name__ == "__main__":
    # pass

    # To run hangman(secret_word)
    # uncomment the following 8 lines and comment the 8 lines following "##############"
    
    #secret_word = choose_word(wordlist)
    # unique_letters = []
    # for letter in secret_word:
    #   if letter in unique_letters:
    #     continue
    #   else:
    #     unique_letters.append(letter)  
    #hangman(secret_word)

###############
    
    secret_word = choose_word(wordlist)
    unique_letters = []
    for letter in secret_word:
      if letter in unique_letters:
        continue
      else:
        unique_letters.append(letter)  
    hangman_with_hints(secret_word)
