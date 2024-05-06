import threading
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text
from questionary import select, text, confirm

def get_language_code(language_name):
    language_codes = {
        "English": "en",
        "Hindi": "hi",
        "Bengali": "bn",
        "Spanish": "es",
        "Chinese (Simplified)": "zh-CN",
        "Russian": "ru",
        "Japanese": "ja",
        "Korean": "ko",
        "German": "de",
        "French": "fr",
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn",
        "Gujarati": "gu",
        "Punjabi": "pa"
    }
    return language_codes.get(language_name)

def translate_text(input_lang_code, output_lang_code):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Now!\n")
        audio = r.listen(source)

        try:
            speech_text = r.recognize_google(audio)
            speech_text_transliteration = (
                transliterate_text(speech_text, lang_code=input_lang_code)
                if input_lang_code not in ("auto", "en")
                else speech_text
            )
            print(f"Recognized Text: {speech_text_transliteration}")

            if speech_text.lower() in {"exit", "stop"}:
                return

            translated_text = GoogleTranslator(
                source=input_lang_code, target=output_lang_code
            ).translate(text=speech_text_transliteration)

            print(f"Translated Text: {translated_text}")

            voice = gTTS(translated_text, lang=output_lang_code)
            voice.save("voice.mp3")
            playsound("voice.mp3")

        except sr.UnknownValueError:
            print("Could not understand!\n")
        except sr.RequestError:
            print("Could not request from Google!\n")

def run_translator():
    input_lang_name = select("Select Input Language:", choices=[
        "English", "Hindi", "Bengali", "Spanish", "Chinese (Simplified)",
        "Russian", "Japanese", "Korean", "German", "French",
        "Tamil", "Telugu", "Kannada", "Gujarati", " Indonesian"
    ]).ask()

    output_lang_name = select("Select Output Language:", choices=[
        "English", "Hindi", "Bengali", "Spanish", "Chinese (Simplified)",
        "Russian", "Japanese", "Korean", "German", "French",
        "Tamil", "Telugu", "Kannada", "Gujarati", "Indonesian"
    ]).ask()

    input_lang_code = get_language_code(input_lang_name)
    output_lang_code = get_language_code(output_lang_name)

    translate_thread = threading.Thread(target=translate_text, args=(input_lang_code, output_lang_code))
    translate_thread.start()

    confirm("Press Enter to stop the translation...").ask()

run_translator()
