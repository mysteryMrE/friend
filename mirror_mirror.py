from fuzzywuzzy import fuzz


class MirrorMirror:
    _q_and_a = {
        "what is your name": "I am Mirror Mirror on the wall, your virtual assistant.",
        "who are you": "I am Mirror Mirror on the wall, your virtual assistant.",
        "how can you help me": "I can assist you with a variety of tasks, including answering questions and providing information.",
        "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "what's the weather like": "Wouldn't you like to know, weatherboy?",
        "stop": "Stopping now. If you need anything else, just ask!",
        "goodbye": "Goodbye! Have a great day!",
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there stranger! What can I do for you?",
        "help": "I'm here to help! What do you need assistance with?",
    }

    def __init__(
        self,
        threshold=70,
        default_answer="Sorry, I didn't understand that. Can you rephrase?",
    ):
        self.q_and_a = {q.lower(): a for q, a in self._q_and_a.items()}
        self.threshold = threshold
        self.default_answer = default_answer
        self.repeat_question = False

    def is_rebound(self):
        """Check if we should rebound to listening again (and reset the flag)"""
        temp = self.repeat_question
        self.repeat_question = False
        print(f"DEBUG: is_rebound() returning {temp}")
        return temp

    def get_answer(self, query: str) -> str:
        best_match = None
        if query is None:
            self.repeat_question = True
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
            return self.q_and_a[best_match]
        else:
            print(
                f"DEBUG: No match found above threshold of {self.threshold}%. Highest score was {highest_score}%."
            )
            self.repeat_question = True
            return self.default_answer
