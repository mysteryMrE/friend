import os
import sys
import threading
import time
from RealtimeTTS import TextToAudioStream, CoquiEngine


class XTTSVoicePet:
    def __init__(self, voice_sample_paths: list = None):
        """
        Initializes the XTTS-v2 model via the RealtimeTTS CoquiEngine.

        Args:
            voice_sample_paths (list): List of paths to voice samples for cloning.
        """
        # If no specific sample paths provided, use bundled defaults
        if voice_sample_paths is None:
            voice_sample_paths = [
                os.path.join(os.path.dirname(__file__), "first.wav"),
                os.path.join(os.path.dirname(__file__), "second.wav"),
                os.path.join(os.path.dirname(__file__), "third.wav"),
                os.path.join(os.path.dirname(__file__), "fourth.wav"),
            ]

        # Resolve relative paths (allow passing just filenames) and validate existence
        resolved_paths = []
        base_dir = os.path.dirname(__file__)
        for p in voice_sample_paths:
            if not os.path.isabs(p):
                candidate = os.path.join(base_dir, p)
            else:
                candidate = p
            resolved_paths.append(candidate)

        if not resolved_paths or not all(os.path.exists(p) for p in resolved_paths):
            raise FileNotFoundError("One or more voice sample files not found.")

        voice_sample_paths = resolved_paths

        print(f"Using {len(voice_sample_paths)} voice sample(s) for cloning.")

        # Define explicit paths for models and voices
        # The library will download the model files to this directory.
        models_dir = os.path.join(os.getcwd(), "xtts_models")

        # Create the directory if it doesn't exist
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        # Initialize the CoquiEngine with explicit paths
        self.engine = CoquiEngine(
            # Coqui will automatically download model files to `models_dir`
            local_models_path=models_dir,
            voices_path=os.getcwd(),
            voice=voice_sample_paths,
            language="en",  # en
            # The 'model_name' is not strictly necessary here since XTTS-v2 is the default.
            # But you can keep it for clarity if you wish.
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
        )
        print("✅ XTTS-v2 CoquiEngine initialized successfully!")

        # Streaming manager
        self.stream = TextToAudioStream(self.engine)
        print("-" * 50)
        self.speaking = False

    def is_finished(self):
        return not self.speaking

    def speak(self, text):
        if not self.speaking:
            self.speaking = True
            thread = threading.Thread(target=self._speak_async, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            print("🔊 Already speaking, please wait.")

    def _speak_async(self, text):
        """
        Feeds text into the streaming system for real-time playback.

        Args:
            text (str): The text to be spoken.
        """

        if not text.strip():
            return

        print(f"\n📢 Generating and streaming: '{text}'")
        start_time = time.time()

        # Feed text to stream
        self.stream.feed(text)

        # Play stream (blocks until finished)
        self.stream.play()

        print("✅ Streaming completed.")
        print("✅ Streaming completed.")
        # Explicitly close the stream here.
        # self.stream.close()
        self.speaking = False


if __name__ == "__main__":
    voice_samples = [
        "first.wav",
        "second.wav",
        "third.wav",
        "fourth.wav",
    ]
    # voice_samples = ["egyke.wav", "ketke.wav", "haromka.wav"]

    try:
        pet = XTTSVoicePet(voice_sample_paths=voice_samples)

        # while True:
        #     # user_input = input("\nAsk your pet a question (or 'quit' to exit): ")

        #     # if user_input.lower() == "quit":
        #     #     break

        #     # pet.speak(user_input)
        for i in range(200):
            print(f"Hello, this is message number {i + 1}")
            time.sleep(1)
            pet.speak(
                f"This is another message, with the number {i + 1}. Before this finishes no new messages shall be played! After this the speaking flag should be false."
            )

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure your voice sample files are in the correct directory.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    print("\nGoodbye!")
    sys.exit()
