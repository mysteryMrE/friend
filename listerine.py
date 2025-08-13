import speech_recognition as sr
from enum import Enum


class Language(Enum):
    ENGLISH = "en-US"
    SPANISH = "es-ES"
    FRENCH = "fr-FR"
    GERMAN = "de-DE"
    ITALIAN = "it-IT"
    HUNGARIAN = "hu-HU"


class SpeechToText:
    def __init__(self, mic_index: int = 1, adjust_once: bool = True):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1.0
        self.mic_index = mic_index

        # if adjust_once:
        #     with sr.Microphone(device_index=self.mic_index) as source:
        #         print(f"Adjusting ambient sound using microphone {self.mic_index}...")
        #         self.recognizer.adjust_for_ambient_noise(source, duration=1)
        #     print("Ambient noise adjustment complete. Ready for speech.")

    @staticmethod
    def print_mic_device_index():
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone {index}: {name}")

    def speech_to_text(
        self,
        language: Language = Language.ENGLISH,
        save_audio: bool = False,
        audio_filename: str = "microphone_input.wav",
    ):
        try:
            with sr.Microphone(device_index=self.mic_index) as source:
                print(f"Adjusting ambient sound using microphone {self.mic_index}...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print(f"Listening for speech in {language.value}...")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)

                text = None
                try:
                    text = self.recognizer.recognize_google(
                        audio, language=language.value
                    )
                    print(f"Recognized text in {language.value}: {text}")
                except sr.UnknownValueError:
                    print(f"Could not understand audio in {language.value}.")
                except sr.RequestError as e:
                    print(
                        f"Could not request results from Google Speech Recognition service; {e}"
                    )
                finally:
                    return text
        except sr.WaitTimeoutError as e:
            print(f"An error occurred: {e}")
            return "better start talking!"


def check_mic_device_index():
    SpeechToText.print_mic_device_index()


def speech_to_text_english(stt_instance: SpeechToText, save_audio: bool = False):
    print("Starting English speech recognition...")
    return stt_instance.speech_to_text(
        Language.ENGLISH,
        save_audio=save_audio,
        audio_filename="english_test.wav",
    )
