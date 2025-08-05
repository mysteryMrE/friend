import threading
from listerine import speech_to_text_english
from pet_animation import PetAnimation


class ListenAnimation(PetAnimation):
    def __init__(self):
        super().__init__(
            speed_x=0,
            speed_y=0,
            resource_name="walking_left_transparent.gif",
            resource_length=8,
            animation_speed=1,
            animation_repeat=100,  # Large number so it keeps looping while listening
        )

        self.message = None
        self.speech_thread = None
        self.listening = False
        self.start_listening()

    def start_listening(self):
        """Start speech recognition in a separate thread"""
        if not self.listening:
            self.listening = True
            self.speech_thread = threading.Thread(
                target=self._listen_for_speech, daemon=True
            )
            self.speech_thread.start()

    def _listen_for_speech(self):
        """Private method to handle speech recognition in background"""
        try:
            result = speech_to_text_english(2)
            # Only set message if we got actual speech (not the default "test")
            if result != "test":
                self.message = result
            else:
                self.message = ""  # Empty string means no speech detected
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            self.message = ""
        finally:
            self.listening = False

    def is_finished(self):
        """Animation is finished only when speech recognition is complete"""
        # Only finish when speech recognition thread is done
        return not self.listening and self.message is not None

    def cleanup(self):
        """Clean up when animation is done"""
        self.listening = False
        if self.speech_thread and self.speech_thread.is_alive():
            print("ListenAnimation: Cleaning up speech recognition")
