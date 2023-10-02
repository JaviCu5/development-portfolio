import unicodedata
from os import system

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
            guessed_letter = str(input("Escoge una letra: "))
      
            if len(guessed_letter) == 1 and guessed_letter.isalpha():
                  break
            print("¡Una sola letra!")
      return guessed_letter

def quitar_acentos(texto):
    texto_sin_acentos = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
    return texto_sin_acentos

def jugada(word, failed_letters, coded_word, failures):
      posiciones = []
      guess_letter = quitar_acentos(guessed_letter()).upper()
      # Usar un bucle for para buscar todas las ocurrencias de la letra

      if (guess_letter in failed_letters) or (guess_letter+" " in coded_word):
            error = 100
            failures += 1
      else:
            for i in range(len(word)):
                  if quitar_acentos(word[i]) == guess_letter:
                        posiciones.append(i)

      # Comprobar si la letra está en la palabra y mostrar las posiciones
            if posiciones:
                  error = 101
                  for i in posiciones: coded_word[i] = word[i]+" "
            else:
                  failures += 1
                  failed_letters.append(guess_letter)
                  error = 102

      return failed_letters, coded_word, failures, error, guess_letter
system("cls")
print("Tu palabra no puede tener caracteres especiales como ., !, ?, etc")
word = input("Escoge la palabra a adivinar: ").upper()
total_characters = len(word)
system("cls")

coded_word = []
print("El juego empieza: ")
for i in range(total_characters): 
    if word[i] == " ":
        coded_word.append("  ")
    else:
        coded_word.append("_ ")
final_word = ''.join(coded_word)

failed_letters = []
failures=0
hangman(failures)
print("La palabra no contiene las siguientes letras: ", sorted(failed_letters))
print("")
print("La actual palabra: " + final_word)
print("")
while (failures < 6):
    failed_letters, coded_word, failures, error, guess_letter = jugada(word, failed_letters, coded_word, failures)
    final_word = ''.join(coded_word)

    system("cls")
    if error == 100:
        print("La letra " + guess_letter + " ya ha sido usada :/")
    elif error == 101:
        print("¡La letra " + guess_letter + " está en la palabra!")
    elif error == 102:
        print("La letra " + guess_letter + " NO está en la palabra...")
    hangman(failures)
    print("La palabra no contiene las siguientes letras: ", sorted(failed_letters))
    print("")
    print("La actual palabra: " + final_word)
    print("")
    if "_ " not in coded_word:
        break

system("cls")
if failures < 6:
    print("Ganaste!")
    print("La palabra era: "+final_word)
    print("")
else:
    hangman(failures)
    print("")
    print("Perdiste :(")
    coded_word = []
    for i in range(total_characters): coded_word.append(word[i]+" ")
    final_word = ''.join(coded_word)
    print("La palabra era: "+final_word)
    print("")

