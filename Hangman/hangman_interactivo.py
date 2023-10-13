import json
import unicodedata
from tkinter import *
from tkinter import ttk
from spellchecker import SpellChecker

# Upload the different language strings
with open('strings_lang.json', 'r', encoding='utf-8') as archivo:
      recursos = json.load(archivo)

def game_strings():
      labelRules.config(text=obtain_string("RULES"))
      labelTextToPlay.config(text=obtain_string("CHOOSE_WORD"))
      currentWord.config(text=obtain_string("CURRENT_WORD"))
      labelGessedLetter.config(text=obtain_string("CHOOSE_LETTER"))
      correctlabelGessedLetter.config(text=obtain_string("JUST_LETTER"))
      labelFailedLetters.config(text=obtain_string("FAILED_LETTERS"))

def hangman(failures):
      if failures == 0:
            hangman_print.config(text="  _____ \n |        |\n |         \n |         \n |         \n |         \n=========")
      elif failures == 1:
            hangman_print.config(text="  _____ \n |        |\n |       O\n |         \n |         \n |         \n=========")
      elif failures == 2:
            hangman_print.config(text="  _____ \n |        |\n |       O\n |         |\n |         \n |         \n=========")
      elif failures == 3:
            hangman_print.config(text="  _____ \n |        |\n |       O\n |       /|\n |         \n |         \n=========")
      elif failures == 4:
            hangman_print.config(text="  _____ \n |        |\n |       O\n |       /|\\\n |         \n |         \n=========")
      elif failures == 5:
            hangman_print.config(text="  _____ \n |        |\n |       O\n |       /|\\\n |       / \n |         \n=========")
      else:
            hangman_print.config(text="  _____ \n |        |\n |       O\n |       /|\\\n |        / \\\n |         \n=========")

def code_text(textToPlayGet):
      totalCharacters = len(textToPlayGet)
      codedText = []
      for i in range(totalCharacters): 
            if textToPlayGet[i] == " ":
                  codedText.append("  ")
            else:
                  codedText.append("_ ")
      finalWord = ''.join(codedText)
      return finalWord, codedText

def correct_ortography(text, lang):
      # Call the corrector
      spell = SpellChecker(language=lang)

      words = text.split()

      # Find and correct
      corrections = []
      for palabra in words:
            # Obtain the suggested correction
            correccion = spell.correction(palabra)
            corrections.append(correccion)

      # Join the words again
      corrected_text = ' '.join(corrections)

      # Return to the upper case
      return corrected_text.upper()

def quitar_acentos(texto):
      texto_sin_acentos = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
      return texto_sin_acentos


def collect_guessedLetter(event=None):
      global failures
      global failedLetters
      global finalWord
      guessedLetterTry = quitar_acentos(guessedLetter.get()).upper()
      guessedLetter.delete(0, "end")
      posiciones = []
      
      if guessedLetterTry.isalpha() and len(guessedLetterTry) == 1:
            error_label.config(text="")
            if (guessedLetterTry in failedLetters) or (guessedLetterTry+" " in codedText):
                  failures +=1
                  hangman(failures)
                  hangman_print.grid(column=0, row=0)
            else:
                  for i in range(len(textToPlayGet)):
                        if quitar_acentos(textToPlayGet[i]) == guessedLetterTry:
                              posiciones.append(i)
                  if posiciones:
                        for i in posiciones: codedText[i] = textToPlayGet[i]+" "
                        finalWord = ''.join(codedText)
                  else:
                        failures += 1
                        hangman(failures)
                        hangman_print.grid(column=0, row=0)
                        failedLetters.append(guessedLetterTry)
                        labelFailedLetters.config(text=obtain_string("FAILED_LETTERS"))
                        labelFailedLettersText.config(text=str(failedLetters))

            currentWord.config(text=obtain_string("CURRENT_WORD") + finalWord)
            currentWord.grid(column=0, row=1)
            
            if failures>=6:
                  currentWord.grid_forget()
                  youLose.config(text=obtain_string("YOU_LOSE") + textToPlayGet)
                  youLose.grid(column=0, row=1)
                  labelGessedLetter.grid_forget()
                  guessedLetter.grid_forget()
                  labelFailedLetters.grid_forget()
                  labelFailedLettersText.grid_forget()
            if "_ " not in codedText:
                  currentWord.grid_forget()
                  youLose.config(text=obtain_string("YOU_WIN") + finalWord)
                  youLose.grid(column=0, row=1)
                  labelGessedLetter.grid_forget()
                  guessedLetter.grid_forget()
                  labelFailedLetters.grid_forget()
                  labelFailedLettersText.grid_forget()
      else:
            error_label.config(text=obtain_string("JUST_LETTER"))
            return False
      labelFailedLetters.grid(column=0, row=2)
      labelFailedLettersText.grid(column=1, row=2)


def collect_textToPlay(event=None):
      global textToPlayGet
      global finalWord
      global codedText
      textToPlayGet = textToPlay.get()
      textToPlay.grid_forget()
      textToPlayGet = correct_ortography(textToPlayGet, language)
      labelRules.grid_forget()
      labelTextToPlay.grid_forget()
      finalWord, codedText = code_text(textToPlayGet)
      
      hangman(failures)
      hangman_print.grid(column=0, row=0)
      currentWord.config(text=obtain_string("CURRENT_WORD") + finalWord)
      currentWord.grid(column=0, row=1)
      labelGessedLetter.grid(column=0, row=3)
      guessedLetter.grid(column=1, row=3)


def button_lang():
      global language
      language = lang[language_var.get()]
      game_strings()
      language_menu.grid_forget()
      labelLang.grid_forget()
      buttonLang.grid_forget()
      labelRules.grid(column=0, row=0)
      labelTextToPlay.grid(column=0, row=1)
      textToPlay.grid(column=1, row=1)

# Obtain the adecuate language string 
def obtain_string(key):
      return recursos.get(language, {}).get(key, f'[{key}]')

# This will be the language options at the beggining of the game
languages = ["English",
      "Español",
      "Français",
      "Português",
      "Deutsch"]

# This is for the ortographyc corrector and for the strings language
lang = {"English": "en",
      "Español": "es",
      "Français": "fr",
      "Português": "pt",
      "Deutsch": "de"}

language = "es"

root = Tk()
root.title(obtain_string("THE_HAGNMAN"))
frm = ttk.Frame(root, padding=10)
frm.grid()

language_var = StringVar(root)
language_var.set(languages[0])

language_menu = OptionMenu(frm, language_var, *languages)
language_menu.grid(column=1, row=0)

hangman_print = Label(frm, text="")

labelLang = ttk.Label(frm, text=obtain_string("SELECT_THE_LANGUAGE"))
buttonLang = ttk.Button(frm, text=obtain_string("ACCEPT"), command=button_lang)

labelLang.grid(column=0, row=0)
buttonLang.grid(column=1, row=1)

failures=0
textToPlayGet = ""
labelRules = ttk.Label(frm, text=obtain_string("RULES"))
labelTextToPlay = ttk.Label(frm, text=obtain_string("CHOOSE_WORD"))
textToPlay = Entry(frm)
textToPlay.bind("<Return>", collect_textToPlay)

currentWord = ttk.Label(frm, text="")
labelGessedLetter = ttk.Label(frm, text=obtain_string("CHOOSE_LETTER"))
correctlabelGessedLetter = ttk.Label(frm, text=obtain_string("JUST_LETTER"))
guessedLetter = Entry(frm)
guessedLetter.bind("<Return>", collect_guessedLetter)
error_label = ttk.Label(frm, text="")
error_label.grid(column=1, row=5)

failedLetters = []
labelFailedLetters = ttk.Label(frm, text=obtain_string("FAILED_LETTERS"))
labelFailedLettersText = ttk.Label(frm, text=str(failedLetters))

youLose = ttk.Label(frm, text=obtain_string("YOU_LOSE"))
youWin = ttk.Label(frm, text=obtain_string("YOU_WIN"))

frm.mainloop()