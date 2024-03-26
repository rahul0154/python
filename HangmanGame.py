import json
import random

file = open("words.json", "r")
json_data = json.load(file)


def user_option_selection(options, need_value=False):
    user_message = ''
    for option, description in options.items():
        user_message += f"{option}. {description}\n"

    try:
        user_response = int(input(user_message))

        if options.get(user_response):
            if need_value:
                return options[user_response]
            else:
                return user_response
    except ValueError:
        pass

    print("Please provide a valid option.")
    return user_option_selection(options, need_value)


def get_random_word(difficulty=1):
    if difficulty == 1:
        new_words = [word for word in json_data["words"] if len(word) < 7]
        return random.choice(new_words)
    elif difficulty == 2:
        new_words = [word for word in json_data["words"] if 5 < len(word) < 7]
        return random.choice(new_words)
    elif difficulty == 3:
        new_words = [word for word in json_data["words"] if 5 < len(word) < 15]
        return random.choice(new_words)


def add_spaces_in_word(random_word, difficulty=1):
    spaces = {2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 3, 9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 6}

    if difficulty == 1:
        spaces = {2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2}
    elif difficulty == 2:
        spaces = {2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 6}
    elif difficulty == 3:
        spaces = {5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 6}

    word_length = len(random_word)
    required_spaces = spaces[word_length]
    space_index = random.sample(range(0, len(random_word)), required_spaces)

    new_word_list = list(random_word)
    for i in space_index:
        new_word_list[i] = '_'

    new_word = ''.join(new_word_list)
    return new_word


def start_game(difficulty=5):
    if difficulty == 5:
        print("Choose a difficulty level.")
        difficulty = user_option_selection({1: 'Easy', 2: 'Medium', 3: 'Hard'})

    global allowed_guess
    user_guess = 1
    original_word = get_random_word(difficulty)
    hidden_word = add_spaces_in_word(original_word, difficulty)

    try:
        while user_guess <= allowed_guess:
            user_word = input("Guess a letter: " + hidden_word + ': ')

            if user_word.lower() == original_word.lower():
                print("Congratulations! You guessed the correct word " + original_word)
                print("Press Enter to play again.")
                input()
                start_game(difficulty)
                continue
            if user_word.lower() == 'restart':
                print("Restarting game with new word.")
                start_game()
                continue

            print("Ahhh! Wrong. You have " + str(allowed_guess - user_guess) + " guesses left.")
            user_guess += 1
    except:
        print("Press Enter to play again.")
        input()
        start_game(difficulty)

    print("Original word: " + original_word)
    print("Better luck next time!.")
    print("Press Enter to play again.")
    input()
    start_game(difficulty)


allowed_guess = 5
print("************ Welcome to Hangman! ************")
print("* Try to guess the secret word.")
print("* You have " + str(allowed_guess) + " attempts to guess correctly.")
print("* Type 'restart' to get new word in between game.")
print("* Let's begin!")
print("*" * 45)

start_game()
