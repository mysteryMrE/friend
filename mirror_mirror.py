from fuzzywuzzy import fuzz

from pet_states.hide import HideAnimation
from pet_states.lie_down import LieDownAnimation
from pet_states.die import DieAnimation


class MirrorMirror:
    _q_and_a = {
        "what is your name": [
            "I am Mirror Mirror on the wall, I can tell you if you are the fairest of them all.",
            False,
            False,
        ],
        "who are you": [
            "I am Mirror Mirror on the wall, I can tell you if you are the fairest of them all.",
            False,
            False,
        ],
        "what's the weather like": [
            "Wouldn't you like to know, weatherboy?",
            False,
            False,
        ],
        "tell me a joke": [
            "Why did the mirror break? Because it couldn't handle the reflection of its own beauty!",
            False,
            False,
        ],
        "tell me a story": [
            "Once upon a time, there was a mirror that could talk. It told stories to everyone who looked into it, but it never revealed its own secrets.",
            False,
            False,
        ],
        "stop": ["Stopping now. See you later!", False, True],
        "goodbye": ["Goodbye! Have a great day!", False, False],
        "hi": ["Hello! How can I assist you today?", True, False],
        "hello": ["Hi there stranger! What can I do for you?", True, False],
        "help": ["I'm here to help! What do you need assistance with?", True, False],
        "go hide": [HideAnimation, False, True],
        "go sleep": [LieDownAnimation, False, True],
        "go to sleep": [LieDownAnimation, False, True],
        "go to bed": [LieDownAnimation, False, True],
        "go die": [DieAnimation, False, True],
    }

    def __init__(
        self,
        threshold=70,
        default_answer="Sorry, I didn't understand that. Can you rephrase?",
    ):
        self.q_and_a = {q.lower(): a for q, a in self._q_and_a.items()}
        self.threshold = threshold
        self.default_answer = default_answer
        self.listen_again = False
        self.force_state = None

    def is_rebound(self):
        """Check if we should rebound to listening again (and reset the flag)"""
        temp = self.listen_again
        self.listen_again = False
        print(f"DEBUG: is_rebound() returning {temp}")
        return temp

    def is_directed_to_state(self):
        return self.force_state is not None

    def get_directed_state(self):
        temp = self.force_state
        self.force_state = None
        return temp

    def get_answer(self, query: str) -> str:
        best_match = None
        if query is None:
            self.listen_again = True
            return self.default_answer
        highest_score = 0
        normalized_query = query.lower().strip()

        for question in self.q_and_a.keys():
            score = fuzz.ratio(normalized_query, question)

            if score > highest_score:
                highest_score = score
                best_match = question

        if highest_score >= self.threshold:
            print(
                f"DEBUG: Found best match with score {highest_score}% for question: '{best_match}'"
            )
            self.listen_again = self.q_and_a[best_match][1]
            self.force_state = (
                self.q_and_a[best_match][0] if self.q_and_a[best_match][2] else None
            )
            return self.q_and_a[best_match][0]
        else:
            print(
                f"DEBUG: No match found above threshold of {self.threshold}%. Highest score was {highest_score}%."
            )
            self.listen_again = True
            return self.default_answer
