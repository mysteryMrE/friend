import random
from pet_animation import PetAnimation
import time


# TODO: so many flags
class TalkAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="talking.gif",
            resource_length=2,
            animation_speed=0.2,
            animation_repeat=1,
        )
        self.messages = [
            "Woof! Woof!",
            "Bark! Bark!",
            "Hello there!",
            "How are you?",
            "Let's play!",
            "I love you!",
            "Feed me!",
            "I'm happy!",
            "Where's my toy?",
            "Let's go for a walk!",
        ]
        self.current_message = None
        self.current_message_index = 0
        self.last_message_time = time.time()
        self.last_message = None
        self.message_interval = 0.3
        self.separators = [" ", "!", "?", ".", ",", ";", ":", "'"]
        self.message_sent = False
        self.full_message_display_time = 2

    def update_animation(self):
        if self.is_finished():
            return self.frames[-1], True, self.get_display_message()
        frame = self.frames[self.cycle % len(self.frames)]
        self.cycle += 1
        return frame, self.is_finished(), self.get_display_message()

    def is_finished(self):
        return (
            self.message_sent
            and time.time() - self.last_message_time > self.full_message_display_time
        )

    def get_display_message(self):
        if (
            time.time() - self.last_message_time > self.message_interval
            and not self.message_sent
        ):
            if self.current_message is None:
                print("Choosing a new message")
                self.current_message = random.choice(
                    self.messages
                )  # if random.random() < 0.5 else None
                self.current_message_index = 0
                self.last_message = None
            if self.current_message is not None:
                print(f"Current message: {self.current_message}")
                if self.current_message_index < len(self.current_message) - 1:
                    self.last_message = self.current_message[
                        : self.current_message_index + 1
                    ]
                    if (
                        self.last_message is not None
                        and self.last_message[-1] not in self.separators
                    ):
                        self.last_message_time = time.time()
                    self.current_message_index += 1
                    return self.last_message
                else:
                    self.last_message = self.current_message
                    self.last_message_time = time.time()
                    self.message_sent = True
                    self.current_message = None
                    return self.last_message

        return "" if self.last_message is None else self.last_message
