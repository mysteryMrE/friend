from enum import Enum
import os
import pvporcupine
from pvrecorder import PvRecorder
import time
import threading
from typing import Callable
from dotenv import load_dotenv


class Language(Enum):
    ENGLISH = "en-US"


class Hot:

    def __init__(
        self,
        mic_index: int = None,
        access_key: str = None,
        language: Language = Language.ENGLISH,
        custom_keyword_paths: list = None,
        builtin_keywords: list = None,
        wake_word_callback: Callable = None,
        flag: threading.Event = None,
    ):
        # Auto-detect microphone if not specified
        self.mic_index = 0

        print(f"Using microphone index: {self.mic_index}")
        self.access_key = access_key
        self.custom_keyword_paths = custom_keyword_paths or []
        self.builtin_keywords = builtin_keywords or []
        self.language = language
        # Threading control
        self._listening_thread = None
        self._stop_listening = threading.Event()
        self._wait_for_callback = flag
        self._is_listening = False

        # Callback for when wake word is detected
        self._wake_word_callback = wake_word_callback
        self._find_working_microphone()

    def start_listening(self):
        """Start listening for wake words in a background thread"""
        if self._is_listening:
            print("Already listening. Stop first before starting again.")
            return False

        self._stop_listening.clear()
        self._wait_for_callback.clear()

        # Start listening thread
        self._listening_thread = threading.Thread(
            target=self._listen_worker,
            daemon=True,
        )
        self._listening_thread.start()
        self._is_listening = True
        print("Started listening in background thread")
        return True

    def _find_working_microphone(self):
        """Find a working microphone device index and print device names."""
        print("Auto-detecting microphone devices...")

        try:
            devices = PvRecorder.get_available_devices()
            print("Found the following audio devices:")
            for i, device in enumerate(devices):
                print(f"Device index {i}: {device}")

            # Now, try to use each device by its index
            for i in range(len(devices)):
                try:
                    print(f"Testing PvRecorder device {i} ({devices[i]})...")
                    test_recorder = PvRecorder(device_index=i, frame_length=512)
                    test_recorder.start()
                    test_recorder.stop()
                    test_recorder.delete()
                    print(f"Successfully tested PvRecorder device {i}")
                    return i  # Return the index of the first working device
                except Exception as e:
                    print(f"Device {i} failed: {e}")
                    continue
        except Exception as e:
            print(f"Failed to get audio devices from PvRecorder: {e}")
            # Fallback to the original method if device listing fails
            print("Falling back to testing common hardcoded indices...")
            test_indices = [0, 1, 2, -1]
            for i in test_indices:
                try:
                    print(f"Testing PvRecorder device {i}...")
                    test_recorder = PvRecorder(device_index=i, frame_length=512)
                    test_recorder.start()
                    test_recorder.stop()
                    test_recorder.delete()
                    print(f"Successfully tested PvRecorder device {i}")
                    return i
                except Exception as e:
                    print(f"Device {i} failed: {e}")
                    continue

        # If nothing works, return default
        print("No working device found, using default (-1)")
        return -1

    def stop_listening(self):
        """Stop the background listening thread"""
        if not self._is_listening:
            print("Not currently listening")
            return

        print("Stopping background listener...")
        self._stop_listening.set()

        if self._listening_thread:
            self._listening_thread.join(timeout=2.0)

        self._is_listening = False
        print("Background listener stopped")

    def is_listening(self):
        """Check if currently listening"""
        return self._is_listening

    def wake_thread(self):
        """Wake the background thread to process any pending callbacks"""
        self._wait_for_callback.clear()

    def _listen_worker(self):
        """Worker method that runs in background thread"""
        porcupine = None
        recorder = None

        try:
            # Create Porcupine instance with either custom or built-in keywords
            if self.custom_keyword_paths:
                print(f"Using custom keywords: {self.custom_keyword_paths}")
                porcupine = pvporcupine.create(
                    access_key=self.access_key, keyword_paths=self.custom_keyword_paths
                )
                keyword_names = [
                    os.path.basename(path).replace(".ppn", "")
                    for path in self.custom_keyword_paths
                ]
            elif self.builtin_keywords:
                print(f"Using built-in keywords: {self.builtin_keywords}")
                porcupine = pvporcupine.create(
                    access_key=self.access_key, keywords=self.builtin_keywords
                )
                keyword_names = self.builtin_keywords
            else:
                # Default to built-in "porcupine"
                print("Using default built-in keyword: porcupine")
                porcupine = pvporcupine.create(
                    access_key=self.access_key, keywords=["porcupine"]
                )
                keyword_names = ["porcupine"]

            print(f"Porcupine initialized with frame length: {porcupine.frame_length}")
            print(f"Listening for keywords: {keyword_names}")

            # Create PvRecorder with error handling
            try:
                recorder = PvRecorder(
                    device_index=self.mic_index, frame_length=porcupine.frame_length
                )
                print(f"PvRecorder created successfully with device {self.mic_index}")
            except Exception as e:
                print(f"Failed to create PvRecorder with device {self.mic_index}: {e}")
                # Try with default device
                print("Trying with default device (-1)...")
                self.mic_index = -1
                recorder = PvRecorder(
                    device_index=-1, frame_length=porcupine.frame_length
                )
                print("PvRecorder created with default device")

            recorder.start()
            print(
                f"Background thread listening for hotwords: {', '.join(keyword_names)}..."
            )

            while not self._stop_listening.is_set():
                try:
                    pcm = (
                        recorder.read()
                    )  # This blocks, but only blocks this background thread
                    result = porcupine.process(pcm)

                    if result >= 0:
                        detected_keyword = keyword_names[result]
                        print(
                            f"Hotword '{detected_keyword}' detected! Processing command..."
                        )

                        # Pause wake word detection temporarily
                        recorder.stop()

                        # Process speech to text
                        self._wait_for_callback.set()
                        if self._wake_word_callback:
                            self._wake_word_callback()
                        else:
                            print(
                                "No wake word callback provided, skipping...AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                            )
                        while self._wait_for_callback.is_set():
                            time.sleep(0.1)
                        # Resume listening after callback
                        if not self._stop_listening.is_set():
                            recorder.start()
                            print(f"Resumed listening for hotwords...")

                except Exception as e:
                    print(f"Error during recording: {e}")
                    break

        except pvporcupine.PorcupineError as e:
            print(f"Porcupine error: {e}")
            print("Please check your access key and ensure it's valid.")
        except Exception as e:
            print(f"Unexpected error in listen worker: {e}")
        finally:
            # Clean up resources
            if recorder is not None:
                try:
                    if hasattr(recorder, "is_recording") and recorder.is_recording:
                        recorder.stop()
                    recorder.delete()
                    print("PvRecorder cleaned up")
                except:
                    pass
            if porcupine is not None:
                try:
                    porcupine.delete()
                    print("Porcupine cleaned up")
                except:
                    pass
