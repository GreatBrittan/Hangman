# hangman.py


# The code snippet is importing necessary modules for the Hangman game. Here's what each import
# statement does:
import PySimpleGUI as sg

from string import ascii_uppercase
from random import choice

# `MAX_WRONG_GUESSES=6` is a constant variable that sets the maximum number of wrong guesses allowed
# in the Hangman game. In this game, the player can make up to 6 incorrect guesses before losing the
# game. This constant is used to determine when the game is over based on the number of wrong guesses
# made by the player.
MAX_WRONG_GUESSES=6

# This class represents a game of Hangman.
class Hangman:
    def __init__(self) -> None:
        """
        The `__init__` function initializes a Hangman game window with different frames for canvas,
        letters, guessed word, and action buttons.
        """
        layout = [
            [
                self._build_canvas_frame(),
                self._build_letters_frame(),
            ],
            [
                self._build_guessed_word_frame(),
            ],
            [
                self._build_action_buttons_frame(),
            ],
        ]

        self._window = sg.Window(
            title="Hangman",
            layout=layout,
            finalize=True,
            margins=(100, 100),
        )

        self._canvas = self._window["-CANVAS-"]
        self.quit = False
        self._played_games = 0
        self._won_games = 0
        self._new_game()

    def _select_word(self):
        """
        The function `_select_word` reads a list of words from a file, selects a random word from the
        list, and returns it in uppercase format.
        :return: The function `_select_word` reads a list of words from a file named "words.txt",
        selects a random word from the list, strips any leading or trailing whitespace, converts it to
        uppercase, and returns the selected word.
        """
        with open("words.txt", mode="r", encoding="utf-8") as words:
            word_list = words.readlines()
        return choice(word_list).strip().upper()


    def _build_guessed_word(self):
        """
        The function `_build_guessed_word` creates a string representation of the target word with
        guessed letters revealed and others hidden as underscores.
        :return: The `_build_guessed_word` method returns a string that represents the current state of
        the guessed word. It replaces any letters in the target word that have been guessed with the
        actual letter, and any letters that have not been guessed with an underscore "_". The letters
        are separated by spaces in the returned string.
        """
        current_letters = []
        for letter in self._target_word:
            if letter in self._guessed_letters:
                current_letters.append(letter)
            else:
                current_letters.append("_")
        return " ".join(current_letters)


    def read_event(self):
        """
        This function reads an event from a window and returns the event ID.
        :return: The `read_event` method returns the event ID of the event read from the window. If
        there is no event, it returns `None`.
        """
        event = self._window.read()
        event_id = event[0] if event is not None else None
        return event_id
    

    def process_event(self, event):
        """
        The `process_event` function checks the type of event and calls corresponding methods to play a
        letter, restart the game, or start a new game.
        
        :param event: The `event` parameter is a string that represents an event that needs to be
        processed. The code snippet provided shows a method `process_event` that takes this `event` as
        input and performs different actions based on the value of the `event` string
        """
        if event[:8] == "-letter-":
            self._play(letter=event[8])
        elif event == "-RESTART-":
            self._restart_game()
        elif event == "-NEW-":
            self._new_game()
    

    def is_over(self):
        """
        The function `is_over` returns True if the number of wrong guesses is equal to the maximum
        allowed wrong guesses or if all letters in the target word have been guessed.
        :return: The `is_over` method is returning a boolean value. It will return `True` if either of
        the conditions inside the `any` function evaluates to `True`, otherwise it will return `False`.
        The conditions being checked are:
        1. If the number of `_wrong_guesses` is equal to `MAX_WRONG_GUESSES`.
        2. If the set of characters in `_target_word`
        """
        return any(
            [
                self._wrong_guesses == MAX_WRONG_GUESSES,
                set(self._target_word) <= self._guessed_letters
            ]
        )
    

    def check_winner(self):
        """
        The `check_winner` function determines if the player has won or lost the game and prompts for a new
        game.
        """
        self._played_games += 1
        if self._wrong_guesses < MAX_WRONG_GUESSES:
            self._won_games += 1
            answer = sg.PopupYesNo(
                "Congratulations! You've won! \n",
                f"You have won {self._won_games} out of {self._played_games}! \n"
                "Play Again?",
                title="Winner!",
            )
        else: 
            answer = sg.PopupYesNo(
                f"You've lost! The word was '{self._target_word}'. \n",
                f"You have won {self._won_games} out of {self._played_games}! \n"
                "Play Again?",
                title="Loser!",
            )
        self.quit = answer == "No"
        if not self.quit:
            self._new_game()

    def close(self):
        """
        The `close` function closes the window associated with the object.
        """
        self._window.close()


    def _new_game(self):
        """
        The `_new_game` function initializes a new game by selecting a target word and restarting the game.
        """
        self._target_word = self._select_word()
        self._restart_game()


    def _restart_game(self):
        """
        The `_restart_game` function resets the game state by clearing guessed letters, resetting wrong
        guesses count, updating the guessed word display, enabling all letter buttons, and redrawing the
        scaffold.
        """
        self._guessed_letters = set()
        self._wrong_guesses = 0
        self._guessed_word = self._build_guessed_word()
        self._canvas.erase()
        self._draw_scaffold()
        for letter in ascii_uppercase:
            self._window[f"-letter-{letter}-"].update(disabled=False)
        self._window["-DISPLAY-WORD-"].update(self._guessed_word)
    

    def _play(self, letter):
        """
        The `_play` function updates the game state based on the player's guessed letter.
        
        :param letter: The `_play` method in the code snippet you provided seems to be a part of a game
        implementation where a player guesses a letter. The method updates the game state based on the
        guessed letter
        """
        if letter not in self._target_word:
            self._wrong_guesses += 1
        self._guessed_letters.add(letter)
        self._guessed_word = self._build_guessed_word()

        self._window[f"-letter-{letter}-"].update(disabled=True)
        self._window["-DISPLAY-WORD-"].update(self._guessed_word)
        self._draw_hanged_man()


    def _build_canvas_frame(self):
        """
        The `_build_canvas_frame` function creates a Frame element with a Graph element inside for a Hangman
        game.
        :return: A `Frame` object is being returned with the title "Hangman" and containing a `Graph`
        element with the specified parameters.
        """
        return sg.Frame(
            "Hangman",
            [
                [
                    sg.Graph(
                        key="-CANVAS-",
                        canvas_size=(200,400),
                        graph_bottom_left=(0, 0),
                        graph_top_right=(200, 400),
                    )
                ]
            ],
            font="Any 20",
        )
    
    def _build_letters_frame(self):
        """
        The function `_build_letters_frame` creates a GUI column with letter buttons arranged in groups
        of four.
        :return: A `sg.Column` object is being returned, which contains a frame titled "Letters" with
        letter buttons arranged in groups of 4. Each button displays a letter from the ASCII uppercase
        alphabet, styled with Courier font size 20 and a border width of 0. The buttons have keys
        assigned based on the letter they represent and are set to enable events.
        """
        letter_groups = [
            ascii_uppercase[i : i + 4]
            for i in range(0, len(ascii_uppercase), 4)
        ]
        letter_buttons = [
            [
                sg.Button(
                    button_text=f"  {letter}  ",
                    font="Courier 20",
                    border_width=0,
                    button_color=(None, sg.theme_background_color()),
                    key=f"-letter-{letter}-",
                    enable_events=True,
                )
                for letter in letter_group
            ]
            for letter_group in letter_groups
        ]
        return sg.Column(
            [
                [
                    sg.Frame(
                        "Letters",
                        letter_buttons,
                        font="Any 20",
                    ),
                    sg.Sizer(),
                ]
            ]
        )


    def _build_guessed_word_frame(self):
        """
        The function `_build_guessed_word_frame` returns a PySimpleGUI Frame containing a Text element
        for displaying a word.
        :return: A `sg.Frame` object is being returned with a `sg.Text` element inside it. The `sg.Text`
        element has the key "-DISPLAY-WORD-" and a font style of "Courier 20". The frame is centered
        using the element_justification parameter.
        """
        return sg.Frame(
            "",
            [
                [
                    sg.Text(
                        key="-DISPLAY-WORD-",
                        font="Courier 20",
                    )
                ]
            ],
            element_justification="center",
        )


    def _build_action_buttons_frame(self):
        """
        The function `_build_action_buttons_frame` creates a frame with buttons for "New", "Restart",
        and "Quit".
        :return: A `sg.Frame` object is being returned with a layout containing three buttons: "New",
        "Restart", and "Quit". Each button has a specific key assigned to it ("-NEW-", "-RESTART-",
        "-QUIT-") and a font size of 20. The buttons are spaced out using `sg.Sizer` elements to provide
        padding between them. The frame itself also has a font size
        """
        return sg.Frame(
            "",
            [
                [
                    sg.Sizer(h_pixels=90),
                    sg.Button(
                        button_text="New",
                        key="-NEW-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=60),
                    sg.Button(
                        button_text="Restart",
                        key="-RESTART-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=60),
                    sg.Button(
                        button_text="Quit",
                        key="-QUIT-",
                        font="Any 20",
                    ),
                    sg.Sizer(h_pixels=90),
                ]
            ],
            font="Any 20",
        )



    def _draw_scaffold(self):
        """
        The `_draw_scaffold` function draws a scaffold using specified lines and widths on a canvas.
        """
        lines = [
            ((40, 55), (180, 55), 10),
            ((165, 60), (165, 365), 10),
            ((160, 360), (100, 360), 10),
            ((100, 365), (100, 330), 10),
            ((100, 330), (100, 310), 1),
        ]
        for *points, width in lines:
            self._canvas.DrawLine(*points, color="black", width=width)


    def _draw_hanged_man(self):
        """
        The function `_draw_hanged_man` defines the body parts of a hanged man to be drawn on a canvas
        based on the number of wrong guesses.
        """
        head = (100, 290)
        torso = [((100, 270), (100, 170))]
        left_arm = [
            ((100, 250), (80, 250)),
            ((80, 250), (60, 210)),
            ((60, 210), (60, 190)),
        ]
        right_arm = [
            ((100, 250), (120, 250)),
            ((120, 250), (140, 210)),
            ((140, 210), (140, 190)),
        ]
        left_leg = [
            ((100, 170), (80, 170)),
            ((80, 170), (70, 140)),
            ((70, 140), (70, 80)),
            ((70, 80), (60, 80)),
        ]
        right_leg = [
            ((100, 170), (120, 170)),
            ((120, 170), (130, 140)),
            ((130, 140), (130, 80)),
            ((130, 80), (140, 80)),
        ]
        body = [
            torso,
            left_arm,
            right_arm,
            left_leg,
            right_leg,
        ]
        if self._wrong_guesses == 1:
            self._canvas.DrawCircle(
                head,
                20,
                line_color="red",
                line_width=2,
            )
        elif self._wrong_guesses > 1:
            for part in body[self._wrong_guesses - 2]:
                self._canvas.DrawLine(*part, color="red", width=2)

    
# The code is a Python script that implements the text-based Hangman game. It
# creates an instance of the Hangman class and enters a loop where it continuously checks for events,
# processes them, and checks if the game is over. The loop continues until the game is either won,
# lost, or the user quits. The game instance is closed at the end.

if __name__ == "__main__":
    game = Hangman()
    while not game.quit:
        while not game.is_over():
            event_id = game.read_event()
            if event_id in {sg.WIN_CLOSED, "-QUIT-"}:
                game.quit = True
                break
            game.process_event(event_id)
        if not game.quit:
            game.check_winner()

    game.close()
