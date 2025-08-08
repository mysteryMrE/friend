import time
from hot import Hot
from dotenv import load_dotenv
import os
import threading

from listerine import SpeechToText, speech_to_text_english

load_dotenv()

if __name__ == "__main__":
    # Initialize Hot with default parameters
    access_key = os.getenv("PORCUPINE_ACCESS_KEY")
    custom_path = [os.getenv("KEYWORD_PATH")]

    watcher = threading.Event()

    # def wake_word_callback(flag: threading.Event):
    #     flag.set()

    def something():
        speech_instance = SpeechToText(mic_index=1, adjust_once=False)
        text = speech_to_text_english(speech_instance)
        if text:
            print(f"Recognized text: {text}")
        else:
            print("No text recognized.")
        watcher.clear()

    hot_instance = Hot(
        mic_index=1,
        access_key=access_key,
        custom_keyword_paths=custom_path,
        # wake_word_callback=wake_word_callback,
        flag=watcher,
    )
    # hot_instance._find_working_microphone()
    hot_instance.start_listening()

    for i in range(100):
        if not watcher.is_set():
            print("Main running. " + str(i))
            time.sleep(0.5)
        else:
            something()
