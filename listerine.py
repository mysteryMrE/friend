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
    @staticmethod
    def print_mic_device_index():
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone {index}: {name}")

    @staticmethod
    def speech_to_text(language: Language = Language.ENGLISH, mic_index: int = 1):
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 2.0
        text = "test"
        with sr.Microphone(device_index=mic_index) as source:
            print(f"Listening for speech in {language.value}...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language=language.value)
                print(f"Recognized text in {language.value}: {text}")
            except sr.UnknownValueError:
                print(f"Could not understand audio in {language.value}.")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )
            finally:
                print(f"Final recognized text: {text}")
                return text


def check_mic_device_index():
    SpeechToText.print_mic_device_index()


def speech_to_text_english(mic_index: int = 2):
    return SpeechToText().speech_to_text(Language.ENGLISH, mic_index)


def speech_to_text_hungarian(mic_index: int = 2):
    return SpeechToText().speech_to_text(Language.HUNGARIAN, mic_index)


if __name__ == "__main__":
    check_mic_device_index()
    speech_to_text_english()
    # speech_to_text_hungarian()
