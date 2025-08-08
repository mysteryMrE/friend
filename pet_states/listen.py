import threading
from time import time
from listerine import SpeechToText, speech_to_text_english
from pet_animation import PetAnimation
import os
import sys
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ListenAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="listening_transparent.gif",
            resource_length=5,
            animation_speed=0.5,
            animation_repeat=2,
        )

        self.message = None
        self.speech_thread = None
        self.has_message = False
        self.listening = False
        self.speech_to_text_instance = SpeechToText(mic_index=2)
        self.start_time = None
        self.delay = 0.7
        print("ListenAnimation initialized, ready to start listening")
        self.wait_frame = tk.PhotoImage(
            file="D:\\Dokumentumok\\SCHOOL\\IT_PROJECTS\\pets\\assets\\images\\"
            + "not_listening_yet_transparent.gif",
            format="gif -index 0",
        )

    def start_listening(self):
        """Start speech recognition in a separate thread"""
        print("ListenAnimation: start listening...")
        if not self.listening:
            print("ListenAnimation: Starting speech recognition...")
            self.listening = True
            self.speech_thread = threading.Thread(
                target=self._listen_for_speech,
                daemon=True,
            )
            self.speech_thread.start()

    def _listen_for_speech(self):
        """Private method to handle speech recognition in background"""
        try:
            self.start_time = time()
            result = speech_to_text_english(self.speech_to_text_instance)
            # Only set message if we got actual speech (not the default "test")
            if result:
                self.message = result
            else:
                self.message = None  # Empty string means no speech detected
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            self.message = None
        finally:
            self.listening = False
            self.has_message = True
            print("ListenAnimation: Speech recognition finished")

    def is_finished(self):
        """Animation is finished only when speech recognition is complete"""
        # Finish when speech recognition thread is done (regardless of whether speech was detected)
        return not self.listening

    def update_animation(self):
        if self.is_finished():
            return self.frames[-1], True, self.get_display_message()
        if self.start_time and time() - self.start_time < self.delay:
            return self.wait_frame, False, self.get_display_message()
        frame = self.frames[self.cycle % len(self.frames)]
        self.cycle += 1
        return frame, self.is_finished(), self.get_display_message()

    def cleanup(self):
        """Clean up when animation is done"""
        self.listening = False
        if self.speech_thread and self.speech_thread.is_alive():
            print("ListenAnimation: Cleaning up speech recognition")

    def has_last_message(self):
        """Check if there is a last message available"""
        return self.has_message

    def get_last_message(self):
        last_message = self.message
        self.message = None
        self.has_message = False
        return last_message
