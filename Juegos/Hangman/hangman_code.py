import unicodedata
from os import system
from spellchecker import SpellChecker

def hangman(failures):
      if failures == 0:
        print("  _____ ")
        print(" |     |")
        print(" |      ")
        print(" |      ")
        print(" |      ")
        print(" |      ")
        print("=========")
      elif failures == 1:
        print("  _____ ")
        print(" |     |")
        print(" |     O")
        print(" |      ")
        print(" |      ")
        print(" |      ")
        print("=========")
      elif failures == 2:
        print("  _____ ")
        print(" |     |")
        print(" |     O")
        print(" |     |")
        print(" |      ")
        print(" |      ")
        print("=========")
      elif failures == 3:
        print("  _____ ")
        print(" |     |")
        print(" |     O")
        print(" |    /|")
        print(" |      ")
        print(" |      ")
        print("=========")
      elif failures == 4:
        print("  _____ ")
        print(" |     |")
        print(" |     O")
        print(" |    /|\\")
        print(" |      ")
        print(" |      ")
        print("=========")
      elif failures == 5:
        print("  _____ ")
        print(" |     |")
        print(" |     O")
        print(" |    /|\\")
        print(" |    / ")
        print(" |      ")
        print("=========")
      else:
        print("  _____ ")
        print(" |     |")
        print(" |     O")
        print(" |    /|\\")
        print(" |    / \\")
        print(" |      ")
        print("=========")

def guessed_letter() -> str:
      while True:
            guessed_letter = str(input("Choose a letter: "))
      
            if len(guessed_letter) == 1 and guessed_letter.isalpha():
                  break
            print("Just one letter!")
      return guessed_letter

def remove_especial_characters(texto):
    plain_text = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
    return plain_text

def game_play(word, failed_letters, coded_word, failures):
      positions = []
      guess_letter = remove_especial_characters(guessed_letter()).upper()
      # Use a loop to find every letter

      if (guess_letter in failed_letters) or (guess_letter+" " in coded_word):
            error = 100
            failures += 1
      else:
            for i in range(len(word)):
                  if remove_especial_characters(word[i]) == guess_letter:
                        positions.append(i)

      # Check if the word contains the letter and show the positions
            if positions:
                  error = 101
                  for i in positions: coded_word[i] = word[i]+" "
            else:
                  failures += 1
                  failed_letters.append(guess_letter)
                  error = 102

      return failed_letters, coded_word, failures, error, guess_letter

def ortography_corrector(texto, lang):
    # Create the corrector instance for a given language
    spell = SpellChecker(language=lang)

    words = texto.split()

    # Find and correct spelling errors
    corrections = []
    for word in words:
        # Suggested correction
        correction = spell.correction(word)
        corrections.append(correction)

    corrected_text = ' '.join(corrections)

    return corrected_text.upper()


system("clear")
print("Your word cannot include special characters like: ., !, ?, etc")

lang = {"English": "en",
        "Español": "es",
        "Français": "fr",
        "Português": "pt",
        "Deutsch": "de"}

word = input("Choose a word to find: ")
word = ortography_corrector(word, lang["English"])
total_characters = len(word)
system("clear")

coded_word = []
print("The game begins: ")
for i in range(total_characters): 
    if word[i] == " ":
        coded_word.append("  ")
    else:
        coded_word.append("_ ")
final_word = ''.join(coded_word)

failed_letters = []
failures=0
hangman(failures)
print("The word doesn't contains the following letters: ", sorted(failed_letters))
print("")
print("The actual word: " + final_word)
print("")
while (failures < 6):
    failed_letters, coded_word, failures, error, guess_letter = game_play(word, failed_letters, coded_word, failures)
    final_word = ''.join(coded_word)

    system("clear")
    if error == 100:
        print("The " + guess_letter + " letter has been used :/")
    elif error == 101:
        print("The word includes the " + guess_letter + " letter!")
    elif error == 102:
        print("The word does NOT include the " + guess_letter + " letter...")
    hangman(failures)
    print("The word doesn't contains the following letters: ", sorted(failed_letters))
    print("")
    print("The actual word: " + final_word)
    print("")
    if "_ " not in coded_word:
        break

system("clear")
if failures < 6:
    print("You win!")
    print("The word is: "+final_word)
    print("")
else:
    hangman(failures)
    print("")
    print("Game over :(")
    coded_word = []
    for i in range(total_characters): coded_word.append(word[i]+" ")
    final_word = ''.join(coded_word)
    print("The word was: "+final_word)
    print("")

