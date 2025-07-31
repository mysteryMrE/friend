import threading
import time
import subprocess
import tempfile
import os


class MyTextToSpeech:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MyTextToSpeech, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not hasattr(self, "initialized"):
            print("TTS: Initializing singleton TTS engine using Windows SAPI")
            self.is_speaking = False
            self.speech_thread = None
            self.current_speaker_id = None
            self.speech_start_time = None
            self.initialized = True
        else:
            print("TTS: Using existing singleton TTS engine instance")

    def speech(self, message, speaker_id=None):
        """Start speaking the given message using Windows SAPI TTS."""
        print(f"TTS: Speaker {speaker_id} attempting to speak: '{message}'")

        if self.is_speaking:
            print(
                f"TTS: Currently speaking for {self.current_speaker_id}, stopping previous speech"
            )
            self.stop()

        self.is_speaking = True
        self.current_speaker_id = speaker_id
        self.speech_start_time = time.time()
        self.speech_thread = threading.Thread(
            target=self._speak_async, args=(message, speaker_id)
        )
        self.speech_thread.daemon = True
        self.speech_thread.start()
        print(f"TTS: Speech thread started for speaker {speaker_id}")

    def _speak_async(self, message, speaker_id):
        """Internal method to handle speech using Windows SAPI."""
        try:
            print(f"TTS: Starting to speak for {speaker_id}: '{message}'")
            start_time = time.time()

            # Use Windows PowerShell to call SAPI TTS
            # This is much more reliable than pyttsx3
            powershell_command = f"""
            Add-Type -AssemblyName System.Speech
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $synth.Rate = -2
            $synth.Volume = 100
            $synth.Speak("{message}")
            $synth.Dispose()
            """

            # Execute the PowerShell command
            result = subprocess.run(
                ["powershell", "-Command", powershell_command],
                capture_output=True,
                text=True,
                timeout=30,
            )

            end_time = time.time()
            duration = end_time - start_time
            print(
                f"TTS: Finished speaking for {speaker_id} (duration: {duration:.2f}s)"
            )

            if result.returncode != 0:
                print(f"TTS: PowerShell error: {result.stderr}")

        except Exception as e:
            print(f"TTS: Error during speech for {speaker_id}: {e}")
        finally:
            self.is_speaking = False
            self.current_speaker_id = None
            self.speech_start_time = None
            print(f"TTS: Speech finished for {speaker_id}, is_speaking set to False")
            self.speech_start_time = None
            print(f"TTS: Speech finished for {speaker_id}, is_speaking set to False")

    def is_finished(self, speaker_id=None):
        """Check if TTS is currently speaking."""
        if speaker_id and self.current_speaker_id != speaker_id:
            # If asking about a specific speaker and it's not the current one, they're finished
            return True
        return not self.is_speaking

    def stop(self):
        """Stop current speech."""
        if self.is_speaking and self.speech_thread:
            try:
                print(f"TTS: Stopping speech for {self.current_speaker_id}")
                # Kill any running PowerShell processes (rough but effective)
                subprocess.run(
                    ["taskkill", "/f", "/im", "powershell.exe"],
                    capture_output=True,
                    check=False,
                )
                self.is_speaking = False
                self.current_speaker_id = None
                if self.speech_thread.is_alive():
                    self.speech_thread.join(timeout=1)
                print("TTS: Speech stopped")
            except Exception as e:
                print(f"TTS: Error stopping speech: {e}")
                self.is_speaking = False
                self.current_speaker_id = None
