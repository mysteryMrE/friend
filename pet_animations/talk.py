import random
from pet_animation import PetAnimation
import tkinter as tk
import time
import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pep_talk import PepTalk


# TODO: so many flags
class TalkAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="talk_transparent.gif",
            resource_length=2,
            animation_speed=0.2,
            animation_repeat=1,
        )

        # Add unique ID for debugging
        self.animation_id = str(uuid.uuid4())[:8]
        print(f"TalkAnimation {self.animation_id}: Creating new instance")
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
        self.ending_image = tk.PhotoImage(
            file="D:\\Dokumentumok\\SCHOOL\\pets\\assets\\images\\"
            + "talk_stopped_transparent.gif",
            format="gif -index 0",
        )

        self.current_message = None
        self.current_message_index = 0
        self.last_message_time = time.time()
        self.last_message = None
        self.message_interval = 0.1
        self.separators = [" ", "!", "?", ".", ",", ";", ":", "'"]
        self.message_sent = False
        self.full_message_display_time = 2

        # Initialize TTS (singleton)
        self.tts = PepTalk()
        self.tts_started = False
        self.message_chosen = False

        # Ensure TTS is ready for new instance
        print(
            f"TalkAnimation {self.animation_id}: New instance created, TTS singleton ready"
        )

    def update_animation(self):
        if self.message_sent:
            return self.ending_image, self.is_finished(), self.get_display_message()
        frame = self.frames[self.cycle % len(self.frames)]
        self.cycle += 1
        return frame, self.is_finished(), self.get_display_message()

    def is_finished(self):
        # Wait for both the message display time AND TTS to finish for THIS animation
        message_display_finished = (
            self.message_sent
            and time.time() - self.last_message_time > self.full_message_display_time
        )
        tts_finished = (
            self.tts.is_finished(self.animation_id) if self.tts_started else True
        )

        return message_display_finished and tts_finished

    def get_display_message(self):
        if (
            time.time() - self.last_message_time > self.message_interval
            and not self.message_sent
        ):
            if self.current_message is None:
                print(f"TalkAnimation {self.animation_id}: Choosing a new message")
                self.current_message = random.choice(
                    self.messages
                )  # if random.random() < 0.5 else None
                self.current_message_index = 0
                self.last_message = None
                self.message_chosen = True

                # Start TTS immediately when message is chosen
                print(
                    f"TalkAnimation {self.animation_id}: Message chosen, attempting TTS for: {self.current_message}"
                )
                print(
                    f"TalkAnimation {self.animation_id}: Starting TTS for: {self.current_message}"
                )

                # Add a prefix to make it more obvious when testing
                tts_message = f"{self.current_message}"
                print(
                    f"TalkAnimation {self.animation_id}: TTS message will be: {tts_message}"
                )
                self.tts.speech(tts_message, speaker_id=self.animation_id)
                self.tts_started = True
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

    def cleanup(self):
        """Clean up TTS when animation is finished"""
        print(
            f"TalkAnimation {self.animation_id}: Cleaning up (no TTS stop needed for singleton)"
        )
        # Don't stop the singleton TTS - let it manage its own state
