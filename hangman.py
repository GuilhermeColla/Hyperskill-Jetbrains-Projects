import random
import string


#  Início do jogo
class Hangman:
    def game_start(self):
        number_of_tries = 8
        print("H A N G M A N")
        word_list = ('python', 'java', 'kotlin', 'javascript')
        correct_word = random.choice(word_list)
        printed_word = "-" * len(correct_word) # coloca traços no lugar das letras, para ser mostrado ao jogador
        correct_word_set = set(correct_word) # apenas para pesquisa rápida
        previous_guesses = []

        while number_of_tries > 0:
            print()
            print(printed_word)
            user_guess = input("Input a letter: ")

            if len(user_guess) != 1:    # Erro caso a entrada possua mais que 1 caractere
                print("You should print a single letter")
            elif user_guess not in string.ascii_lowercase:  # Erro caso a entrada não seja letra minúscula
                print("It is not an ASCII lowercase letter")
            elif user_guess in previous_guesses:  # Testa se a entrada já foi utilizada
                print("You already typed this letter")
            elif user_guess in correct_word_set:    # Testa se a entrada está correta
                i = 0
                while i < len(correct_word):    # Troca o traço pela entrada do jogador
                    if correct_word[i] == user_guess:
                        printed_word = printed_word[:i] + user_guess + printed_word[i+1:]
                    i += 1
            else:   # Se a entrada estiver errada.
                print("No such letter in the word")
                number_of_tries -= 1
            previous_guesses.append(user_guess)
            if printed_word == correct_word:    # Testa se o jogador venceu ou não.
                print("You guessed the word!\nYou survived!")
                break
        if printed_word != correct_word:
            print("You are hanged!\n")


game = Hangman()
while True:
    play_or_exit = input('Type "play" to play the game, "exit" to quit:')
    if play_or_exit == "play":
        game.game_start()
    elif play_or_exit == "exit":
        break
