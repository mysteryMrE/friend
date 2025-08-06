import speech_recognition as sr
from enum import Enum
import os


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

        if adjust_once:
            with sr.Microphone(device_index=self.mic_index) as source:
                print(f"Adjusting ambient sound using microphone {self.mic_index}...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ambient noise adjustment complete. Ready for speech.")

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
        with sr.Microphone(device_index=self.mic_index) as source:
            # print(f"Adjusting ambient sound using microphone {self.mic_index}...")
            # self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"Listening for speech in {language.value}...")
            audio = self.recognizer.listen(source)

            # if save_audio:
            #     # Create a directory for saved audio if it doesn't exist
            #     save_directory = "recorded_audio"
            #     if not os.path.exists(save_directory):
            #         os.makedirs(save_directory)

            #     file_path = os.path.join(save_directory, audio_filename)

            #     # Write the audio data to a WAV file
            #     try:
            #         with open(file_path, "wb") as f:
            #             f.write(audio.get_wav_data())
            #         print(f"Audio saved to {file_path}")
            #     except Exception as e:
            #         print(f"Failed to save audio file: {e}")
            text = "test"
            try:
                text = self.recognizer.recognize_google(audio, language=language.value)
                print(f"Recognized text in {language.value}: {text}")
            except sr.UnknownValueError:
                print(f"Could not understand audio in {language.value}.")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )
            finally:
                return text


def check_mic_device_index():
    SpeechToText.print_mic_device_index()


def speech_to_text_english(stt_instance: SpeechToText, save_audio: bool = False):
    print("Starting English speech recognition...")
    return stt_instance.speech_to_text(
        Language.ENGLISH,
        save_audio=save_audio,
        audio_filename="english_test.wav",
    )


def speech_to_text_hungarian(stt_instance: SpeechToText, save_audio: bool = False):
    stt_instance.speech_to_text(
        Language.HUNGARIAN,
        save_audio=save_audio,
        audio_filename="hungarian_test.wav",
    )


if __name__ == "__main__":
    check_mic_device_index()

    # Create an instance of the class once. The ambient noise adjustment runs here.
    speech_to_text_instance = SpeechToText(mic_index=2)

    # Now, call the functions on this instance.
    # The ambient noise adjustment will NOT run again.
    speech_to_text_english(stt_instance=speech_to_text_instance, save_audio=True)
    # speech_to_text_hungarian(stt_instance=speech_to_text_instance)
